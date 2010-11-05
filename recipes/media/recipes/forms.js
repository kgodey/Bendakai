function cloneMore(selector, type) {
	var newElement = $(selector).clone(false);
	var total = $('#id_' + type + '-TOTAL_FORMS').val();
	newElement.find(':input').each(function() {
		var name = $(this).attr('name').replace('-' + (total-1) + '-','-' + total + '-');
		var id = 'id_' + name;

		if ($(this).attr('type') != 'hidden') {
			$(this).val('');
		}
		$(this).attr({'name': name, 'id': id}).removeAttr('checked');
	});
	newElement.find('label').each(function() {
		var newFor = $(this).attr('for').replace('-' + (total-1) + '-','-' + total + '-');
		$(this).attr('for', newFor);
	});
	total++;
	$('#id_' + type + '-TOTAL_FORMS').val(total);
	$(selector).after(newElement);
	return newElement;
}