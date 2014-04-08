<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>{{ title }}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <meta name="author" content="Katherine A. Scott -- kscottz">
    
    <!-- styles -->
    <link href="/css/bootstrap.css" rel="stylesheet">
    <style>
      body {
        padding-top: 60px; /* 60px to make the container go all the way to the bottom of the topbar */
      }
    </style>
    <link href="/css/bootstrap-responsive.css" rel="stylesheet">
  </head>

  <body>

    <div class="navbar navbar-fixed-top">
      <div class="navbar-inner">
        <div class="container">
          <a class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </a>
          <a class="brand" href="#">Rat Status Page</a>
          <div class="nav-collapse">
            <ul class="nav">
              <li class="active"><a href="#">Give Food</a></li>
              <li><a href="/activity">Activity</a></li>
              <li><a href="/experiments">Experiments</a></li>
              <li><a href="/live">Camera</a></li>
              <li><a href="/about">About</a></li>
            </ul>
          </div><!--/.nav-collapse -->
        </div>
      </div>
    </div>

    <div class="container">
      <div class="btn-group">
	<button type="button" class="btn btn-primary" id="BUZZ">buzz</button>
	<button type="button" class="btn btn-warning" id="FEED">feed</button>
	<button type="button" class="btn btn-danger" id="PICS">pics</button>
      </div>
      <div class="container">
	<div class="btn-group">
	  <button type="button" class="btn btn-primary" id="activity">activity</button>
	  <button type="button" class="btn btn-warning" id="presses">food requests</button>
	</div>
	<div class="btn-group">
	  <span class="input-group-addon">
            <input type="checkbox" id="experiment"> Experiments Enbabled
	  </span>
	</div>



	<h2>Live Event Feed</h2>
	<div class="container">
          <!-- Table -->
          <div class="table-responsive"> 
          <table class="table table-bordered table-hover" id="messages" width=500>  
	    <thead>
	      <tr>
		<th>Time</th>
		<th>Event</th>
		<th>Value</th>
	    </thead>
            <tbody>  
	    </tbody>
	</table>
	</div>
	</div>
     
      {{ content }}

    </div> <!-- /container -->

    <!-- javascript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <!-- But really should be async loaded -->
    <script src="/js/jquery-1.7.1.min.js"></script>
    <script src="/js/bootstrap-transition.js"></script>
    <script src="/js/bootstrap-alert.js"></script>
    <script src="/js/bootstrap-modaljs"></script>
    <script src="/js/bootstrap-dropdown.js"></script>
    <script src="/js/bootstrap-scrollspy.js"></script>
    <script src="/js/bootstrap-tab.js"></script>
    <script src="/js/bootstrap-tooltip.js"></script>
    <script src="/js/bootstrap-popover.js"></script>
    <script src="/js/bootstrap-button.js"></script>
    <script src="/js/bootstrap-collapse.js"></script>
    <script src="/js/bootstrap-carousel.js"></script>
    <script type="text/javascript">
      $('#BUZZ').on('click', function (e) {
      $.ajax({
      type: "POST",
      url: "/buzz",
      });
      });

      $('#FEED').on('click', function (e) {
      $.ajax({
      type: "POST",
      url: "/feed",
      });
      });

      $('#PICS').on('click', function (e) 
      {
      window.location.href = '/pics';
      return false;
      });

      $('#activity').on('click', function (e) 
      {
      window.location.href = '/activity';
      return false;
      });
      
      $('#presses').on('click', function (e) 
      {
      window.location.href = '/presses';
      return false;
      });
      

      $(document).ready(function() {
      if (!window.WebSocket) {
      if (window.MozWebSocket) {
      window.WebSocket = window.MozWebSocket;
      } else {
      $('#messages').append("<li>Your browser doesn't support WebSockets.</li>");
      }
      }
      wshost = 'ws://'+document.location.host+'/websocket'
      ws = new WebSocket(wshost);
      //ws = new WebSocket('ws://192.168.1.42:5000/websocket');
      ws.onopen = function(evt) {
      $('#messages').append('<tr class="warning"><td>Connected to Skinner Box.</td><td></td><td></td></tr>');
      }
      ws.onmessage = function(evt) {
      //$('#messages').empty();
        result = $.parseJSON( evt.data );
        if( result.color === 'warning' ){
          var color = 'bgcolor="FFADAD"';
          $('#messages').prepend('<tr '+color+'><td>' + result.time+ '</td><td>' +result.data+ '</td><td>'+ result.value + '</td></tr>');
        }
        else if( result.color === 'success' ){
          var color = 'bgcolor="ADFFC3"';
          $('#messages').prepend('<tr '+color+'><td>' + result.time+ '</td><td>' +result.data+ '</td><td>'+ result.value + '</td></tr>');
        } 
        else{
          $('#messages').prepend('<tr class="'+result.color+'"><td>' + result.time+ '</td><td>' +result.data+ '</td><td>'+ result.value + '</td></tr>');
        }
      }
      $('#send-message').submit(function() {
      ws.send($('#name').val() + ": " + $('#message').val());
      $('#message').val('').focus();
      return false;
      });
      });
    </script>


    </script>
    <script src="/js/bootstrap-typeahead.js"></script>

  </body>
</html>
