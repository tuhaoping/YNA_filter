$(document).ready(function(){
	$("#feature_accordion input.feature-checkbox").change(function(){
		$(this).closest('div.row').find('select').attr('disabled',!$(this).prop("checked"));
		$(this).closest('div.row').find('input.value').attr('disabled',!$(this).prop("checked"));
	});
});