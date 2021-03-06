//alertify.js
//offline.js

//Code to make allow direct linking but prevent back button linking
if(window.location.hash.substr(1) != ' ') {
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
var categories;


//Cancel user registration for event id
function cancelEvent(e_id) {
  var event_str;
  for (i in feed) {
    theEvent = feed[i]
    if(theEvent.id == e_id) event_str = " for </h4></br><h5>" + theEvent.title + " on " + theEvent.start;
  }
  	$('#myModal').modal('hide');
  	bootbox.dialog({
	  message: "<h4>Are you sure you want to cancel your signup" + event_str + "?</h5>",
	  title: "Confirm Cancellation",
	  buttons: {
	    main: {
	      label: "No",
	      className: "btn-primary",
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
	            loadEvents();
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

function registerEvent(e_id) {
	$.ajax({
      type : "GET",
      dataType : "json",
      url : '/register/'+e_id,
      success: function(data){
        loadEvents();
        $('#myModal').modal('hide');
      }
    });
    
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

    if(calEvent.isRegistered) {$('.modal-footer').html('<button type="button" onclick="cancelEvent('+calEvent.id+')" class="btn btn-danger btn-block">Cancel</button>');}
    else {$('.modal-footer').html('<button type="button" onclick="registerEvent('+calEvent.id+')" class="btn btn-primary btn-block">Signup</button>');}
    

    $('#myModal').modal('show');
}

//An event that wasn't loaded by fullcalendar
function showLinkedEvent(eventId) {
	$.ajax({
      type : "GET",
      dataType : "json",
      url : '/getEvent/'+eventId,
      success: function(data){
      	showEventModal(data);
      }
    });

}

function loadEvents() {

	$.ajax({
      type : "GET",
      dataType : "json",
      url : '/mySignupsFeed',
      success: function(data){
        feed = data;
        var feedHTML = "";
        if(feed.length == 0) {
	        feedHTML += ['<a href="#" class="list-group-item" >',
              			'<h5 class="list-group-item-heading">No Events Found</h5>',
              			'<p class="list-group-item-text"><span class="label label-danger">Register For Events!</span></p>',
            			'</a>'
            			].join('\n');

        } else {
	        for (i in feed) {
	        var theEvent = feed[i]
	         feedHTML += ['<a href="#" class="list-group-item">',
              				'<button onclick="cancelEvent('+theEvent.id+')" class="btn btn-danger btn-xs pull-right"><i class="fa fa-times"></i></button>',
              				'<button onclick="showLinkedEvent('+theEvent.id+')" class="btn btn-success btn-xs pull-right"><i class="fa fa-chevron-circle-right"></i></button>',
              				'<h5 class="list-group-item-heading">'+theEvent.title+'</h5>',
              				'<p style="font-size: 12px;" class="list-group-item-text">Date: '+theEvent.start+'</p>',
            				'</a>'
            				].join('\n');
	        }
    	}
        $("#feed-wrapper").html(feedHTML);
      }
    });
	
	$('#progressBar').addClass('progress-striped');
	$('#progressBar').addClass('active');
	$('#calendar').fullCalendar('refetchEvents');
}

// function loadCategories() {
// 	var categoriesHTML = "";
// 	for (category in categories) {
// 	     categoriesHTML += ['<a href="#" class="list-group-item">',
// 	      				'<button onclick="cancelEvent('+theEvent.id+')" class="btn btn-danger btn-xs pull-right"><i class="fa fa-times"></i></button>',
// 	      				'<button onclick="showLinkedEvent('+theEvent.id+')" class="btn btn-success btn-xs pull-right"><i class="fa fa-chevron-circle-right"></i></button>',
// 	      				'<h5 class="list-group-item-heading">'+theEvent.title+'</h5>',
// 	      				'<p style="font-size: 12px;" class="list-group-item-text">Date: '+theEvent.start+'</p>',
// 	    				'</a>'
// 	    				].join('\n');
// 	 }
// }

// function showEvents(category) {
// 	$('div[category="'+category+'"').show();
// }

// function hideEvents(category) {
// 	$('div[category="'+category+'"').hide();
// }


$(document).ready(function() {

	$('#myModal').bind('hidden.bs.modal', function () {
	  $("html").css("margin-right", "0px");
	});
	$('#myModal').bind('show.bs.modal', function () {
	  $("html").css("margin-right", "-15px");
	});

	loadEvents();

	$('#progressBar').addClass('progress-striped');
	$('#progressBar').addClass('active');

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
        url: '/loadView',
        type: 'GET',
        dataType: "json",
        success: function () {
        	$('#progressBar').removeClass('progress-striped');
			$('#progressBar').removeClass('active');
        },
        error: function() {
            alert('There was an error while fetching events!');
          }
       },

      eventClick: function(calEvent, jsEvent, view) {
      	showEventModal(calEvent);
      },

      eventRender: function(event, element) {
        	element.attr("category",event.category)
    	}
    
    });

    

});

