//alertify.js
//offline.js

var feed;

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
	          dataType : "json",
	          url : '/cancel/'+e_id,
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

function ratioToColor(numberAttending, maxAttending) {
	ratio = maxAttending/numberAttending;
	if(ratio < 1.33) return "danger"
	else if(ratio < 2) return "warning"
	else return "success"
}

function registerEvent() {
	
}
function showEvent(calEvent) {
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


$(document).ready(function() {


    $.ajax({
      type : "GET",
      dataType : "json",
      url : '/mySignupsFeed',
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
        url: '/loadView',
        type: 'GET',
        dataType: "json",
        error: function() {
            alert('there was an error while fetching events!');
          }
       },

      eventClick: function(calEvent, jsEvent, view) {
      	showEvent(calEvent);
      }

    
    });

    

});

