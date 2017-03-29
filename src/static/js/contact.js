/* global $ */


$(document).ready(function() {


	/*
	 * Check that the user filled in all fields and send an email to the club email
	 */
	$('#send_btn').click(function () {
      var sender = $('#sender_box').val().trim();
      var subject = $('#subject_box').val().trim();
      var body = $('#body_box').val().trim();


      if (sender.length == 0) {
    	  $('#message').text("Please enter a contact name or email.").show().delay(2000).fadeOut();
      }
      else if (subject.length == 0) {
    	  $('#message').text("Please enter a subject.").show().delay(2000).fadeOut();
      }
      else if (body.length == 0) {
    	  $('#message').text("Please enter a message to send.").show().delay(2000).fadeOut();
      }
      else if (sender.length == 0 || subject.length == 0 || body.length == 0) {
    	  $('#message').text("Please make sure all fields are filled in.").show().delay(2000).fadeOut();
      }
      else {
        $('#message').attr('style', 'color:black');
      	$('#message').text('Sending...');;
      	$('#sender_box').hide();
      	$('#subject_box').hide();
      	$('#body_box').hide();
      	$('#send_btn').hide();
        $('#recaptcha').hide();

        $.ajax({
           type: "POST",
           url: "/sendemail/",
           data: $("#email_form").serialize(),
           success: function(data) {

              if (data == "Success") {
                $('#message').attr('style', 'color:green');
        		    $('#message').text('Your message was successfully sent. If you provided your email, we will get back to you as soon as possible.');
              }
              else {
                $('#message').attr('style', 'color:red');
        		    $('#message').text("Error: " + data + ". Please try again later or use an email application.");
              }
           },
           error: function() {
              $('#message').attr('style', 'color:red');
        		  $('#message').text('Failed to send your message. Please try again later or use an email application.');
           }
         });

      }

    });
});
