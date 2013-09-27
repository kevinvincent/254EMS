$(document).ready(function() {
  
    var date = new Date();
    var d = date.getDate();
    var m = date.getMonth();
    var y = date.getFullYear();
    
    $('#calendar').fullCalendar({
      header: {
        left: 'prev,next',
        center: 'title',
        right: 'today'
      },

      weekMode: 'liquid',
      height: 600,
      editable: true,

      events: {
        url: 'http://team254.com:5000/loadView',
        type: 'GET',
        dataType: "jsonp",
        error: function() {
            alert('there was an error while fetching events!');
        }
       }
    
    });
    
  });
