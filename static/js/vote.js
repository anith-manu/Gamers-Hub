var isIgnore = false;
$(document).ready(function() {
	$('div.vote-buttons i.fa-arrow-circle-o-up, div.vote-buttons i.fa-arrow-circle-up, div.vote-buttons i.fa-arrow-circle-o-down, div.vote-buttons i.fa-arrow-circle-down').click(function() {
		var review_id = $(this).data('review');
		var elem = $(this);
		if (isIgnore)return;
		isIgnore = true;
		var csrf = $(this).data('csrf');
		if ($(this).hasClass('fa-arrow-circle-o-up')){
			var vote_type = 'up';
			var vote_action = 'vote';
			$.post('/gamer_hub/vote/', {review_id:review_id, action:vote_action, type:vote_type, csrfmiddlewaretoken:csrf}, function(response){
					elem.toggleClass('fa-arrow-circle-o-up fa-arrow-circle-up');
					$('div#' + review_id + ' div.vote-buttons span').text(response);
					if ($(elem).siblings(".fa-arrow-circle-down")){
						$(elem).siblings(".fa-arrow-circle-down").toggleClass('fa-arrow-circle-o-down fa-arrow-circle-down');
					}
					isIgnore = false;

			});
			
		}
		else if ($(this).hasClass('fa-arrow-circle-up')){
			var vote_type = 'up';
			var vote_action = 'recall-vote';
			$.post('/gamer_hub/vote/', {review_id:review_id, action:vote_action, type:vote_type, csrfmiddlewaretoken:csrf}, function(response){
					$('div#' + review_id + ' div.vote-buttons span').text(response);
					elem.toggleClass('fa-arrow-circle-o-up fa-arrow-circle-up');
					isIgnore = false;
			});
		}
		else if ($(this).hasClass('fa-arrow-circle-o-down')){
			var vote_type = 'down';
			var vote_action = 'vote';
			$.post('/gamer_hub/vote/', {review_id:review_id, action:vote_action, type:vote_type, csrfmiddlewaretoken:csrf}, function(response){
					$('div#' + review_id + ' div.vote-buttons span').text(response);
					elem.toggleClass('fa-arrow-circle-o-down fa-arrow-circle-down');
					if ($(elem).siblings(".fa-arrow-circle-up")){
						$(elem).siblings(".fa-arrow-circle-up").toggleClass('fa-arrow-circle-o-up fa-arrow-circle-up');
					}
					isIgnore = false;
			});
		}
		else if ($(this).hasClass('fa-arrow-circle-down')){
			
			var vote_type = 'down';
			var vote_action = 'recall-vote';
			$.post('/gamer_hub/vote/', {review_id:review_id, action:vote_action, type:vote_type, csrfmiddlewaretoken:csrf}, function(response){
					$('div#' + review_id + ' div.vote-buttons span').text(response);
					elem.toggleClass('fa-arrow-circle-o-down fa-arrow-circle-down');
					isIgnore = false;
			});
		}
	});
});