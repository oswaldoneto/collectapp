/**
 * Extract labels from value label pair.
 * 
 * For:
 * [{"value": 1, 
 * 	 "label": "Cliente"}, 
 *  {"value": 2, 
 *   "label": "Proposta"}]
 * 
 * Return:
 * ["Cliente",Proposta]
 * 
 * @param JSON availableTags
 */
function fnListTagLabel(availableTags){
	var tag_labels = [];
	$.each(availableTags,function(){
		tag_labels.push(this.label);					
	});
	return tag_labels;
}


function fnListTagLabelAndValue(availableTags){
	var tags = [];
	$.each(availableTags,function(){
		tags.push([this.value,this.label]);
	});
	return tags;
}


function fnGetTagId(label, availableTags){
	var id = null;
	$.each(availableTags,function(){
		if (this.label == label) {
			id = this.value;
		} 
	});
	return id;
}

function fnGetTagLabel(value, availableTags) {
	var label = null;
	$.each(availableTags,function(){
		if (this.value == value) {
			label = this.label; 
		}
	});
	return label;
}
	