/* global $ */


$(document).ready(function() {

	/*
	 * Check that the user filled in all fields and send an email to the club email
	 */
	$('#send_btn').click(function () {
      var sender = $('#sender_box').val().trim();
      var subject = $('#subject_box').val().trim();
      var body = $('#body_box').val().trim();

      if (sender.length == 0 || subject.length == 0 || body.length == 0) {
    	$('#message').text("Please make sure all fields are filled in.");

		setTimeout(function(){
			$('#message').fadeOut();
		}, 2000);
      }
      else {

      	$('#message').text("");
      	$('#sender_box').text("");
      	$('#subject_box').text("");
      	$('#body_box').text("");

		$.post("/sendemail/", {'sender': sender, 'subject': subject, 'body': body, 'csrftoken': csrftoken}, function(data, status){

    		if (status == "Success") {
				$('#message').attr('style', 'color:green');
        		$('#message').text('Your message was successfully sent. We will get back to you as soon as we can.');
    		}
    		else {
    			$('#message').attr('style', 'color:red');
        		$('#message').text('Failed to send your message. Please try again later or use an email application.');
    		}

    		setTimeout(function(){
				$('#message').fadeOut();
			}, 3000);

		});
      }

    });
});

// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});