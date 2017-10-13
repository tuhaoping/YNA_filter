$(document).ready(function(){
	$("#feature_accordion input.feature-checkbox").change(function(){
		$(this).closest('div.row').find('select').attr('disabled',!$(this).prop("checked"));
		$(this).closest('div.row').find('input.value').attr('disabled',!$(this).prop("checked"));

		let now_card = $(this).closest('div.card');
		now_card.find('span.track').text(now_card.find('input[type=checkbox]:checked').length);
	});
});