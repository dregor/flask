window.onload = function () {
	jQuery("#user-city").text(ymaps.geolocation.city);
	jQuery("#user-region").text(ymaps.geolocation.region);
	jQuery("#user-country").text(ymaps.geolocation.country);
}

$( document ).ready( function() 
{

	$('.lang-option').click(
		function(event)
				{
					$.cookie("locale",$(this).find('.lang-id').html(),  { path: '/' });
		});

	$('.navbar').each(function(){
		var highestBox = 0;
		columns = $.merge($(this).find('.navbar-nav').children('li').children('a'), $(this).find(".navbar-brand, .navbar-form"));
		columns.each(function(){
			highestBox = Math.max($(this).height(),highestBox);
		});
		columns.each(function(){
			if ($(this).height() <= highestBox)
				{$(this).css('line-height',highestBox + 'px');}
		})
	});
});

