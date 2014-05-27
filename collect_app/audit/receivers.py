from django.dispatch.dispatcher import receiver
from audit.models import AuditLog, AuditLogDetail
from django.contrib.contenttypes.models import ContentType
from audit import events
from document.models import DocumentAttribute, AbstractValue
from ext.db.models.query import InheritanceQuerySet
from document.templatetags.kilobytefy import kilobytefy
from audit import signals


DOCUMENT_CONTENT_TYPE = ContentType.objects.get(app_label="document", model="document")


@receiver(signals.post_add_tag_document)
def tag_add_to_document(sender,**kwargs):
    doc = kwargs.get("document")
    tag = kwargs.get("tag")
    user = kwargs.get("user")
    
    log = AuditLog( content_type=DOCUMENT_CONTENT_TYPE, object_id=doc.id, user=user, event=events.ADD_TAG_TO_DOCUMENT  )
    log.save()
    
    log_detail = AuditLogDetail(audit_log=log,description=tag.name)
    log_detail.save()
    
    

@receiver(signals.post_remove_tag_document)
def tag_remove_to_document(sender,**kwargs):
    doc = kwargs.get("document")
    tag = kwargs.get("tag")
    user = kwargs.get("user")
    
    log = AuditLog( content_type=DOCUMENT_CONTENT_TYPE, object_id=doc.id, user=user, event=events.REMOVE_TAG_TO_DOCUMENT  )
    log.save()
    
    log_detail = AuditLogDetail(audit_log=log,description=tag.name)
    log_detail.save()
    

    
@receiver(signals.post_attach_file)
def attach_file_log(sender,**kwargs):
    doc = kwargs.get("document")
    file = kwargs.get("file")
    user = kwargs.get("user")
    
    log = AuditLog( content_type=DOCUMENT_CONTENT_TYPE, object_id=doc.id, user=user, event=events.FILE_ATTACHED )
    log.save()
    
    log_detail = AuditLogDetail(audit_log=log,description="%s (%s)" % (file.filename, kilobytefy(file.filesize)))
    log_detail.save()
    

@receiver(signals.post_detach_file)    
def post_detach_file(sender,**kwargs):
    doc = kwargs.get("document")
    file = kwargs.get("file")
    user = kwargs.get("user")    

    log = AuditLog( content_type=DOCUMENT_CONTENT_TYPE, object_id=doc.id, user=user, event=events.FILE_DETACHED)
    log.save()
    
    log_detail = AuditLogDetail(audit_log=log,description="%s (%s)" % (file.filename, kilobytefy(file.filesize)))
    log_detail.save()
    
    
@receiver(signals.post_classify_document)
def classify_log(sender,**kwargs):
    doc = kwargs.get("document")
    user = kwargs.get("user")

    log = AuditLog( content_type=DOCUMENT_CONTENT_TYPE, object_id=doc.id, user=user, event=events.CLASSIFY_DOCUMENT )
    log.save()

    log_detail = AuditLogDetail(audit_log=log,description="Categoria: %s" % (doc.category.title))
    log_detail.save()

    for doc_attr in DocumentAttribute.objects.filter(document=doc):
        value = InheritanceQuerySet(model=AbstractValue).select_subclasses().get(id=doc_attr.value.id)
        log_detail = AuditLogDetail(audit_log=log,description="%s: %s" % (doc_attr.attribute.name, value.value))
        log_detail.save()
        

@receiver(signals.post_remove_classify_document)
def remove_classify_log(sender,**kwargs):
    doc = kwargs.get("document")
    user = kwargs.get("user")
    
    log = AuditLog( content_type=DOCUMENT_CONTENT_TYPE, object_id=doc.id, user=user, event=events.REMOVE_CLASSIFY_DOCUMENT )
    log.save()    
    
    
@receiver(signals.post_document_shared_to_user)
def document_shared_to_user_log(sender,**kwargs):
    shared_from = kwargs.get("shared_from")
    shared_to = kwargs.get("shared_to")
    doc = kwargs.get("document")
    permission = kwargs.get("permission")
        
    log = AuditLog( content_type=DOCUMENT_CONTENT_TYPE, object_id=doc.id, user=shared_from, event=events.DOCUMENT_SHARED )
    log.save()
    
    log_detail = AuditLogDetail(audit_log=log,description="%s pode %s" % (shared_to, _translate_permission(permission)))
    log_detail.save()


@receiver(signals.post_document_unshared_to_user)
def document_unshared_to_user_log(sender,**kwargs):
    shared_from = kwargs.get("shared_from")
    shared_to = kwargs.get("shared_to")
    doc = kwargs.get("document")
    permission = kwargs.get("permission")
        
    log = AuditLog( content_type=DOCUMENT_CONTENT_TYPE, object_id=doc.id, user=shared_from, event=events.DOCUMENT_UNSHARED )
    log.save()
    
    log_detail = AuditLogDetail(audit_log=log,description="%s nao pode %s" % (shared_to, _translate_permission(permission)))
    log_detail.save()


@receiver(signals.post_document_shared_to_group)
def document_shared_to_group_log(sender,**kwargs):
    shared_from = kwargs.get("shared_from")
    shared_to = kwargs.get("shared_to")
    doc = kwargs.get("document")
    permission = kwargs.get("permission")
        
    log = AuditLog( content_type=DOCUMENT_CONTENT_TYPE, object_id=doc.id, user=shared_from, event=events.DOCUMENT_SHARED )
    log.save()
    
    log_detail = AuditLogDetail(audit_log=log,description="Grupo %s pode %s" % (shared_to, _translate_permission(permission)))
    log_detail.save()


@receiver(signals.post_document_unshared_to_group)
def document_unshared_to_group_log(sender,**kwargs):
    shared_from = kwargs.get("shared_from")
    shared_to = kwargs.get("shared_to")
    doc = kwargs.get("document")
    permission = kwargs.get("permission")
        
    log = AuditLog( content_type=DOCUMENT_CONTENT_TYPE, object_id=doc.id, user=shared_from, event=events.DOCUMENT_UNSHARED )
    log.save()
    
    log_detail = AuditLogDetail(audit_log=log,description="Grupo %s nao pode %s" % (shared_to, _translate_permission(permission)))
    log_detail.save()


@receiver(signals.post_document_shared_to_all)
def document_shared_to_all_log(sender,**kwargs):
    shared_from = kwargs.get("shared_from")
    doc = kwargs.get("document")
    permission = kwargs.get("permission")
        
    log = AuditLog( content_type=DOCUMENT_CONTENT_TYPE, object_id=doc.id, user=shared_from, event=events.DOCUMENT_SHARED )
    log.save()
    
    log_detail = AuditLogDetail(audit_log=log,description="Todos Usuarios podem %s" % (_translate_permission(permission)))
    log_detail.save()


@receiver(signals.post_document_unshared_to_all)
def document_unshared_to_all_log(sender,**kwargs):
    shared_from = kwargs.get("shared_from")
    doc = kwargs.get("document")
    permission = kwargs.get("permission")
        
    log = AuditLog( content_type=DOCUMENT_CONTENT_TYPE, object_id=doc.id, user=shared_from, event=events.DOCUMENT_UNSHARED )
    log.save()
    
    log_detail = AuditLogDetail(audit_log=log,description="Todos Usuarios nao podem %s" % (_translate_permission(permission)))
    log_detail.save()
    

@receiver(signals.post_download_attachment)    
def download_attachment_log(sender,**kwargs):
    user = kwargs.get("user")
    doc = kwargs.get("document")
    file = kwargs.get("file")

    log = AuditLog( content_type=DOCUMENT_CONTENT_TYPE, object_id=doc.id, user=user, event=events.DOWNLOAD_ATTACHMENT )
    log.save()
    
    log_detail = AuditLogDetail(audit_log=log,description="%s (%s)" % (file.filename, kilobytefy(file.filesize)))
    log_detail.save()

   
def _translate_permission(permission):
    if permission == 'read_document':
        return "Visualizar"
    elif permission == 'change_document':
        return "Alterar"
    elif permission == 'delete_document':
        return "Excluir"
        
    
    
    
    
    
    
    
    
    
    
    
    
    

    
    
    
    
    
    
