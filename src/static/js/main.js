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

        $('#message').attr('style', 'color:black');
      	$('#message').text('Sending...');;
      	$('#sender_box').hide();
      	$('#subject_box').hide();
      	$('#body_box').hide();
      	$('#send_btn').hide();

		$.post("/sendemail/", {'sender': sender, 'subject': subject, 'body': body}, function(data, status){

    		if (data == "Success") {
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
