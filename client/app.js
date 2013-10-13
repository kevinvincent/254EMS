var feed;

function cancelEvent(e_id) {
  var event_str;
  for (i in feed) {
    theEvent = feed[i]
    if(theEvent.id == e_id) event_str = " for " + theEvent.title + " on " + theEvent.start;
  }
  bootbox.dialog({
  message: "Are you sure you want to cancel your signup" + event_str + "?",
  title: "Confirm Cancellation",
  buttons: {
    main: {
      label: "No",
      className: "btn-primary pull-left",
    },
    success: {
      label: "Yes",
      className: "btn-danger",
      callback: function() {
        $.ajax({
          type : "GET",
          dataType : "jsonp",
          url : 'http://www.team254.com:5000/cancel/'+e_id,
          success: function(data){
            alert("Event Cancelled!");
            location.reload(true);
          }
        });
      }
    }
  }
});
}


$(document).ready(function() {


    $.ajax({
      type : "GET",
      dataType : "jsonp",
      url : 'http://www.team254.com:5000/mySignupsFeed',
      success: function(data){
        feed = data;
        var feedHTML = "";
        if(feed.length == 0) {
        	feedHTML += ['<a href="#" class="list-group-item">',
	                      '<h4 class="list-group-item-heading">No Events Found</h4>',
	                      '<p class="list-group-item-text">Events you have signed up for will appear here </p>',
	                      '</a>'
	                      ].join('\n');
        } else {
	        for (i in feed) {
	          var theEvent = feed[i]
	          feedHTML += ['<a href="#" class="list-group-item">',
	                      '<button type="button" onclick="cancelEvent('+theEvent.id+')" class="btn btn-danger btn-xs pull-right">Cancel</button>',
	                      '<h4 class="list-group-item-heading">'+theEvent.title+'</h4>',
	                      '<p class="list-group-item-text">Date: '+theEvent.start+'</p>',
	                      '</a>'
	                      ].join('\n');
	        }
    	}
        $("#feed-wrapper").html(feedHTML);
      }
    });

    $('#calendar').fullCalendar({

      header: {
        left: 'prev,next',
        center: 'title',
        right: 'today'
      },

      weekMode: 'liquid',
      handleWindowResize: true,
      editable: false,
      buttonIcons: true,
      height: 700,

      events: {
        url: 'http://team254.com:5000/loadView',
        type: 'GET',
        dataType: "jsonp",
        error: function() {
            alert('there was an error while fetching events!');
          }
       },

      eventClick: function(calEvent, jsEvent, view) {

        var start_time = new Date(calEvent.start);
        var end_time = new Date(calEvent.end || calEvent.start);

        var start_time_string = start_time.getHours()+":"+start_time.getMinutes()
        var end_time_string = end_time.getHours()+":"+end_time.getMinutes()

        $('#event-title').html(calEvent.title);
        $('#event-category').html(calEvent.category);
        $('#event-start').html(start_time_string);
        $('#event-end').html(end_time_string);

        if(calEvent.registrations.length > 0) {
	        var attendees_string = "";

	        for (var i = 0; i < calEvent.registrations.length; i++) {
	        	var element = calEvent.registrations[i];
				attendees_string += '<li class="list-group-item">'+element+'</li>'

			}
	        $('#attendees-wrapper').html(attendees_string);
    	} else {
    		$('#attendees-wrapper').html('<li class="list-group-item">No Attendees</li>');
    	}

        $('#myModal').modal('show');

      }

    
    });
    

});

