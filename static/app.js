//alertify.js
//offline.js

//Code to make allow direct linking but prevent back button linking
if(window.location.hash.substr(1) != '') {
	value = window.location.hash.substr(1)
	window.location.replace("#");
	showLinkedEvent(value)
}
$(window).on('hashchange', function() {
	value = window.location.hash.substr(1)
	$(window).unbind( 'hashchange', hashChanged);
	window.location.replace(window.location+"#");
	 setTimeout(function(){
        $(window).bind( 'hashchange', hashChanged);
    }, 100);
	if(value!='') showLinkedEvent(value)
});

//
var feed;

//Cancel user registration for event id
function cancelEvent(e_id) {
  var event_str;
  for (i in feed) {
    theEvent = feed[i]
    if(theEvent.id == e_id) event_str = " for </h4></br><h5>" + theEvent.title + " on " + theEvent.start;
  }
  	bootbox.dialog({
	  message: "<h4>Are you sure you want to cancel your signup" + event_str + "?</h5>",
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

//Converts ratio of signups/maxsignups to a color value
function ratioToColor(numberAttending, maxAttending) {
	ratio = maxAttending/numberAttending;
	if(ratio < 1.33) return "danger"
	else if(ratio < 2) return "warning"
	else return "success"
}

function registerEvent() {
	
}

//Used by fullcalendar to launch event modal
function showEventModal(calEvent) {
	var start_time = new Date(calEvent.start);
	var end_time = new Date(calEvent.end || calEvent.start);

	var start_time_string = start_time.getHours()+":"+start_time.getMinutes()
	var end_time_string = end_time.getHours()+":"+end_time.getMinutes()

	$('#event-title').html(calEvent.title);
	$('#event-id').html(calEvent.id);
	$('#event-category').html(calEvent.category);
	$('#event-start').html(start_time_string);
	$('#event-end').html(end_time_string);
	$('#event-number').html(calEvent.maxRegistrations - calEvent.numberOfRegistrations + " Spots Left");
	$('#event-number').addClass(function( index ) {
	  return "label-" + ratioToColor(calEvent.numberOfRegistrations,calEvent.maxRegistrations);
	});

	if(calEvent.numberOfRegistrations > 0) {
		var attendees_string = "";

		for (var i = 0; i < calEvent.numberOfRegistrations; i++) {
			var element = calEvent.registrations[i];
			attendees_string += '<li class="list-group-item">'+element+'</li>'
		}
	    $('#attendees-wrapper').html(attendees_string);

    } else {
    	$('#attendees-wrapper').html('<li class="list-group-item">No Attendees</li>');
    }

    $('#myModal').modal('show');
}

//An event that wasn't loaded by fullcalendar
function showLinkedEvent(eventId) {
	$.ajax({
      type : "GET",
      dataType : "jsonp",
      url : 'http://www.team254.com:5000/getEvent/'+eventId,
      success: function(data){
      	showEventModal(data);
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
	          feedHTML += ['<li class="list-group-item">',
	                      '<a onclick="cancelEvent('+theEvent.id+')" class="btn btn-danger btn-md pull-right" role="button"><i class="fa fa-times"></i></a>',
	                      '<a href="/signup#'+theEvent.id+'" class="btn btn-success btn-md pull-right" role="button"> <i class="fa fa-info"></i> </a>',
	                      '<h4 class="list-group-item-heading">'+theEvent.title+'</h4>',
	                      '<p class="list-group-item-text">Date: '+theEvent.start+'</p>',
	                      '</li>'
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
      aspectRatio: 1.75,

      events: {
        url: 'http://www.team254.com:5000/loadView',
        type: 'GET',
        dataType: "jsonp",
        error: function() {
            alert('there was an error while fetching events!');
          }
       },

      eventClick: function(calEvent, jsEvent, view) {
      	showEventModal(calEvent);
      }

    
    });

    

});

