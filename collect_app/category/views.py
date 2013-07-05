import json

from django.shortcuts import render_to_response, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from category.models import Category
from category.forms import CategoryForm
from category.models import Attribute
from category.forms import AttributeForm
from tag.models import Tag
from django.contrib import messages
from document.models import Document, DocumentAttribute
from django.views.generic.list import ListView
from document.search_indexes import DocumentIndex


class AttributeOrderView(ListView):
	model=Attribute
	template_name="app/category/attribute_order_dialog.xhtml"	
	def get_context_data(self,**kwargs):
		context = super(AttributeOrderView,self).get_context_data(**kwargs)
		context.update({'params': self.kwargs})
		return context
	def get_queryset(self):
		cat = get_object_or_404(Category,pk=self.kwargs['category'])
		self.queryset = Attribute.objects.filter(category=cat).order_by('order')
		return super(AttributeOrderView,self).get_queryset()
		



@csrf_protect
@login_required
def list(request):
	categories = Category.objects.all()
	return render_to_response('app/category/category_list.xhtml',
							  {'categories':categories},
							  context_instance=RequestContext(request))

@csrf_protect
def search(request):
	categories = []
	searchField = ''
	if 'searchField' in request.GET:
		searchField = request.GET['searchField']
		if not searchField:
			categories = Category.objects.all()
		else:
			categories = Category.objects.filter(title__icontains=searchField)
	return render_to_response('app/category/category_list.xhtml',
							  {'categories':categories,'searchField':searchField},
							  context_instance=RequestContext(request))
							  
def json_search(request):
	result = []	
	if 'cat_search_str' in request.GET:
		cat_search_str = request.GET['cat_search_str']
		cats = Category.objects.filter(title__icontains=cat_search_str)
		result = [ ({'id':cat.id, 'title':cat.title}) for cat in cats]
	json_result = json.dumps(result)
	return HttpResponse(json_result,mimetype="application/json")
	
@csrf_protect
def add(request):
	if request.method == 'POST':
		form = CategoryForm(request.POST)
		if form.is_valid():
			new_category = form.save(commit=False)
			new_category.user = request.user
			new_category.save()
			return HttpResponseRedirect('/category/%s/edit' % new_category.id)				
	else:
		form = CategoryForm()
	return render_to_response('app/category/category_form.xhtml',
							  {'form':form},
							   context_instance=RequestContext(request))
							   
@csrf_protect
def edit(request, category):
	cat = Category.objects.get(id=category)
	if request.method == 'POST':
		form = CategoryForm(request.POST,instance=cat)
		if form.is_valid():
			form.save()			
			#TODO: Refactor #124 and #125
			DocumentIndex().update()
			return HttpResponseRedirect('/category/%s/edit' % cat.id)							
	else:
		form = CategoryForm(instance=cat)
	return render_to_response('app/category/category_form.xhtml',
							  {'form':form,'category':cat,'edit_mode':True},
							  context_instance=RequestContext(request))
	
@csrf_protect
def delete(request, category):
	cat = Category.objects.get(id=category)
	doc_amount = Document.objects.filter(category=cat).count()
	if doc_amount == 0:
		cat.delete()
	else:
		#TODO externalize message
		messages.error(request,'A categoria nao pode ser deletada, existem %s documentos associados a categoria.' % doc_amount)
	return HttpResponseRedirect('/category/list')		
	
@csrf_protect
def edit_attribute(request, category, attribute):
	cat = Category.objects.get(id=category)
	att = Attribute.objects.get(id=attribute)
	if request.method == 'POST':
		attForm = AttributeForm(request.POST,instance=att)
		if attForm.is_valid():
			attForm.save()
			return HttpResponseRedirect("/category/%s/attribute/list" % cat.id)			
	else:
		attForm = AttributeForm(instance=att)
	return render_to_response('app/category/attribute_form.xhtml',
							  {'form':attForm,'category':cat,'attribute':att,'edit_mode':True},
							  context_instance=RequestContext(request))
							  
@csrf_protect
def delete_attribute(request, category, attribute):
	att =  Attribute.objects.get(id=attribute)
	for doc_attr in DocumentAttribute.objects.filter(attribute=att):
		doc_attr.delete()
	att.delete()
	return HttpResponseRedirect('/category/%s/attribute/list' % category)				

@csrf_protect
def inactivate_attribute(request, category, attribute):
	Attribute.objects.get(id=attribute).inactivate()
	return HttpResponseRedirect('/category/%s/attribute/list' % category)				
	
@csrf_protect
def add_attribute(request, category):
	cat = Category.objects.get(id=category)
	if request.method == 'POST':
		form = AttributeForm(request.POST)
		if form.is_valid():
			att = form.save(commit=False)
			att.category=cat
			att.order=0
			att.save()
			return HttpResponseRedirect("/category/%s/attribute/list" % cat.id)
	else:
		form = AttributeForm()
	return render_to_response('app/category/attribute_form.xhtml',
							  {'form':form,'category':cat},
							  context_instance=RequestContext(request))
	
@csrf_protect
def list_attribute(request, category):
	cat = Category.objects.get(id=category)
	attributeByCategory = Attribute.objects.filter(category=cat).exclude(active=False)
	return render_to_response('app/category/attribute_list.xhtml',
							  {'attributes':attributeByCategory,'category':cat},
							  context_instance=RequestContext(request))
	
def list_tag(request, category):
	cat = Category.objects.get(id=category);
	return render_to_response('app/category/tag_list.xhtml',
							  {'category':cat,'tag_list':cat.tags.all()},
							  context_instance=RequestContext(request))
	
def add_tag(request, category):
	cat = Category.objects.get(id=category)
	if 'tag_id' in request.GET:
		tag_id = request.GET['tag_id']
		tag = Tag.objects.get(id=tag_id)
		for t in tag.get_descendants(include_self=True):
			cat.tags.add(t)
	return HttpResponse("OK")

def delete_tag(request, category):
	cat = Category.objects.get(id=category)
	if 'tag_id' in request.GET:
		tag_id = request.GET['tag_id']
		tag = Tag.objects.get(id=tag_id)
		for t in tag.get_descendants(include_self=True):
			cat.tags.remove(t)
	return HttpResponse("OK")

	
	
	