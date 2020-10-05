$(document).ready(function(){
	var rel_path = $('.icon.icon-home').attr('href').split('index.html')[0];
	$('.icon.icon-home').html('<img src="' + rel_path + '_static/logo.png" class="logo" alt="Logo">');
});