$(document).ready(function() {
	$("button.navbar-toggle").click(function() {
		flag = $('.navbar-toggle').hasClass("collapsed");
		if(flag) {
			$('.glyphicon-menu-hamburger').addClass('glyphicon-remove').removeClass('glyphicon-menu-hamburger')
		} else {
			$('.glyphicon-remove').addClass('glyphicon-menu-hamburger').removeClass('glyphicon-remove')
		}
	});
});