$(document).ready(function(){
	$("#feature_accordion input.feature-checkbox").change(function(){
		$(this).closest('div.row').find('select').attr('disabled',!$(this).prop("checked"));
		$(this).closest('div.row').find('input.value').attr('disabled',!$(this).prop("checked"));

		let now_card = $(this).closest('div.card');
		now_card.find('span.track').text(now_card.find('input[type=checkbox]:checked').length);
	});

	$("#collapse1, #collapse2, #collapse3").on('show.bs.collapse', function(){
		$("#genetextarea").removeClass('geneText-close');
	});

	$('#genetextarea').focus(function(){
		$("#genetextarea").removeClass('geneText-close');
		$("#collapse1").collapse('show');
	});

	$("#switch").click(function(){
		if($("#switch").prop("checked")){
			$("#feature-div").removeClass("div-disabled");
			$("#geneText-div").addClass("div-disabled");
		}
		else {
			$("#feature-div").addClass("div-disabled");
			$("#geneText-div").removeClass("div-disabled");
		}
		// console.log($("#switch").prop("checked"));
	});

	// enrichment setting checkbox
	$("#enrich-table input[type=checkbox]").change(function(){
		$(this).parent().siblings('input').prop('disabled', !$(this).prop('checked'));
		console.log($(this).closest('tr').find('td').first().text() + "/" + $(this).closest('td').attr('class') + "/" + $(this).parent().siblings('input').val());
	});
});