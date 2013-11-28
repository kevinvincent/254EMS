/* Initialize */
/* ---------------------------------------------------- */

//Load Components
var modalContent;
$.ajax({
  type : "GET",
  url : 'static/components/component_modal.html',
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
  alert(datum["value"]);
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

  var start_time = new Date(calEvent.start);
  var end_time = new Date(calEvent.end || calEvent.start);
  calEvent.start_time = start_time.getHours()+":"+start_time.getMinutes();
  calEvent.end_time = end_time.getHours()+":"+end_time.getMinutes();

  calEvent.spotsLeft = calEvent.maxRegistrations - calEvent.numberOfRegistrations;

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
  
  $('#progressBar').addClass('progress-striped');
  $('#progressBar').addClass('active');
  $('#calendar').fullCalendar('refetchEvents');
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
      showEventModal(calEvent);
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

  //Initialize Search
  $('.typeahead').typeahead({
      name: '',
      local: typeaheadItems
  });
});

