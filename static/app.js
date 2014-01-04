/* Initialize */
/* ---------------------------------------------------- */

//Load Components
var modalContent;
$.ajax({
  type : "GET",
  url : 'static/components/component_modal_new.html',
  success: function(data){
    modalContent = data;
  }
});

var registerPanelContent;
$.ajax({
  type : "GET",
  url : 'static/components/component_registeredPanel.html',
  success: function(data){
    registerPanelContent = data;
  }
});

var userPanelContent;
$.ajax({
  type : "GET",
  url : 'static/components/component_user.html',
  success: function(data){
    userPanelContent = data;
  }
});

//Globals
var feed;
var typeaheadItems = []
var rawCategories = new Array();

//Allow Direct Linking but Prevent Back Button Behavior
if(window.location.hash.substr(1) != ' ') {
  value = window.location.hash.substr(1)
  if(value!='')showLinkedEvent(value)
  window.location.replace("#");
}

//Initialize Typeahead Search
$('.typeahead').on('typeahead:selected', function($e, datum){
  showLinkedEvent(datum["id"]);
});


/* HELPER FUNCTIONS */
/* ---------------------------------------------------- */
function unique(array) {
    return $.grep(array, function(el, index) {
        return index == $.inArray(el, array);
    });
}

/* APP FUNCTIONS */
/* ---------------------------------------------------- */

//Register For an Event
function registerEvent(e_id) {
  $('#myModal').modal('hide');
  $.ajax({
      type : "GET",
      dataType : "json",
      url : '/registerFRC/'+e_id,
      success: function(data){

        //Parse returned data and alert user if necessary
        if(data.result == "error") {

          msg = Messenger({
            extraClasses: 'messenger-fixed messenger-on-bottom messenger-on-left'
          });

          msg.post({
            message: "Registration Error <br/> You can only signup for 3 events a week",
            type: "error"
          })

        } else {
          msg = Messenger({
            extraClasses: 'messenger-fixed messenger-on-bottom messenger-on-left'
          });

          msg.post({
            message: "Successfuly Registered",
            type: "success"
          })
          var theEvent = $('#calendar').fullCalendar( 'clientEvents', parseInt(e_id));
          theEvent[0].isRegistered = true;
          $('#calendar').fullCalendar('updateEvent', theEvent);
          console.log($('#calendar').fullCalendar( 'clientEvents', parseInt(e_id)))
          loadEvents();
        }
        
      }
    });
}

//Cancel Registration for Event
function cancelEvent(e_id) {
    $('#myModal').modal('hide');
    bootbox.dialog({
    message: "<h4>Are you sure you want to cancel your signup?</h5>",
    title: "Confirm Cancellation",
    buttons: {
      main: {
        label: "No",
        className: "btn-primary"
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
              msg = Messenger({
                extraClasses: 'messenger-fixed messenger-on-bottom messenger-on-left'
              });

              msg.post({
                message: "Registration Cancelled",
                type: "info"
              })
              var theEvent = $('#calendar').fullCalendar( 'clientEvents', parseInt(e_id));
              theEvent[0].isRegistered = false;
              $('#calendar').fullCalendar('updateEvent', theEvent);
              console.log($('#calendar').fullCalendar( 'clientEvents', parseInt(e_id)))
              loadEvents();
            }
          });
        }
      }
    }
  });
}


//Show the Event Modal - Internal Use Only
function showEventModal(calEvent) {

  calEvent.spotsLeft = calEvent.maxRegistrations - calEvent.numberOfRegistrations;
  // alert("isOpen: " + calEvent.open + " - isRegistered: " + calEvent.isRegistered)
  if(calEvent.isRegistered && calEvent.open) {
    calEvent.button_html = '<button type="button" onclick="cancelEvent('+calEvent.id+')" class="btn btn-danger btn-block">Deregister</button>';
  }
  else if(calEvent.isRegistered && !calEvent.open) {
    calEvent.button_html = '<button type="button" onclick="cancelEvent('+calEvent.id+')" class="btn btn-danger btn-block">Deregister</button>';
  }
  else if(!calEvent.isRegistered && calEvent.open) {
    calEvent.button_html = '<button type="button" onclick="registerEvent('+calEvent.id+')" class="btn btn-primary btn-block">Signup</button>';
  }
  else if(!calEvent.isRegistered && !calEvent.open) {
    calEvent.button_html = '<button type="button" disabled="disabled" class="btn btn-default btn-block">Signups Full</button>';
  }
  else {
    calEvent.button_html = "ERROR";
  }


  template = Mustache.render(modalContent, calEvent);
  $(".component_modal").html("");
  $(".component_modal").append(template);
  $('#myModal').modal('show');
  $("#loader"+calEvent.id).hide();
  $("#chevron"+calEvent.id).show();
  

    
}

//Show an Event by eventID
function showLinkedEvent(eventId) {
  $("#chevron"+eventId).hide();
  $("#loader"+eventId).show();
  $.ajax({
      type : "GET",
      dataType : "json",
      url : '/event/'+eventId,
      success: function(data){
        showEventModal(data);
      }
    });

}

//Load Registered Events List
function loadEvents() {

  $.ajax({
    type : "GET",
    dataType : "json",
    url : '/mySignupsFeed',
    success: function(data){

      feed = data;
      template = Mustache.render(registerPanelContent, data);
      $(".component_registeredPanel").html("");
      $(".component_registeredPanel").append(template);

    }
  });
}

//Filter Categories
function filter(category) {
  if(category=="all") {
    $('.fc-event').show(100);

    //Render Categories Selector
    var categoryArr = unique(rawCategories);
    var data = { "categories": categoryArr, "currentCat" : "All" };
    var template = Mustache.render('<div class="btn-group"> <button type="button" class="btn btn-primary btn-sm dropdown-toggle" data-toggle="dropdown"> Category: {{currentCat}} <span class="caret"></span> </button> <ul class="dropdown-menu" role="menu"> <li><a href="javascript:filter(\'all\')">View All</a></li><li class="divider"></li>{{#categories}}<li><a href="javascript:filter(\'{{.}}\')">{{.}}</a></li>{{/categories}}</ul></div>', data);
    $('.fc-header-left').html(template);

  }
  else {
    $('.fc-event').hide(100);
    $('div[category="'+category+'"]').show(100);

    //Render Categories Selector
    var categoryArr = unique(rawCategories);
    var data = { "categories": categoryArr, "currentCat" : category };
    var template = Mustache.render('<div class="btn-group"> <button type="button" class="btn btn-primary btn-sm dropdown-toggle" data-toggle="dropdown"> Category: {{currentCat}} <span class="caret"></span> </button> <ul class="dropdown-menu" role="menu"> <li><a href="javascript:filter(\'all\')">View All</a></li><li class="divider"></li>{{#categories}}<li><a href="javascript:filter(\'{{.}}\')">{{.}}</a></li>{{/categories}}</ul></div>', data);
    $('.fc-header-left').html(template);
  }
 
}


$(document).ready(function() {
  
  //Load Registered Event List
  loadEvents();

  //Load User Panel
  $.ajax({
    type : "GET",
    dataType : "json",
    url : '/user',
    success: function(user_data){
      template = Mustache.render(userPanelContent, user_data);
      $(".component_user").html("");
      $(".component_user").append(template);
    }
  });
  

  //Start Moving Progress Bar
  $('#progressBar').addClass('progress-striped');
  $('#progressBar').addClass('active');

  //Load Fullcalendar
  $('#calendar').fullCalendar({

    header: {
      left: '',
      center: 'title',
      right: ''
    },

    weekMode: 'liquid',
    lazyFetching: true,
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

    //Modal Listener
    eventClick: function(calEvent, jsEvent, view) {
      showLinkedEvent(calEvent.id);
    },

    //Add Category
    eventRender: function(event, element) {
        element.attr("category",event.category)
        rawCategories.push(event.category);
        typeaheadItems.push({"value":event.title, "id":event.id});
    },

    //Apply Custom Modifications when done loading
    loading: function(bool) {
      if (!bool){

        //Put pointers on all the events
        $('.fc-event').css( 'cursor', 'pointer' );

        //Render Categories Selector
        var categoryArr = unique(rawCategories);
        var data = { "categories": categoryArr, "currentCat" : "All" };
        var template = Mustache.render('<div class="btn-group"> <button type="button" class="btn btn-primary btn-sm dropdown-toggle" data-toggle="dropdown"> Category: {{currentCat}} <span class="caret"></span> </button> <ul class="dropdown-menu" role="menu"> <li><a href="javascript:filter(\'all\')">View All</a></li><li class="divider"></li>{{#categories}}<li><a href="javascript:filter(\'{{.}}\')">{{.}}</a></li>{{/categories}}</ul></div>', data);
        $('.fc-header-left').html(template);

        //Modify buttons
        var prev = "$('#calendar').fullCalendar('prev');"
        var next = "$('#calendar').fullCalendar('next');"
        $('.fc-header-right').html('<div class="btn-group btn-group-sm"> <button type="button" onclick="'+prev+'" class="btn btn-primary"><i class="fa fa-chevron-left"></i></button> <button type="button" onclick="'+next+'" class="btn btn-primary"><i class="fa fa-chevron-right"></i></button> </div>');
      }
    }
  
  });

  var template = Mustache.compile('<p><strong>{{value}}</strong></p><p> – {{start_date_pretty}}</p>');
  //Initialize Search
  $('.typeahead').typeahead({
      name: '',
      remote: '/search/%QUERY',
      template: template
  });

  // ​$(window).on('resize', function(){
  //     var win = $(".typeahead"); //this = window
  //     $()
  // });​​​​
  

  
});

