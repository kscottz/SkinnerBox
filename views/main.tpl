<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>{{ title }}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <meta name="author" content="">
    
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
              <li><a href="#about">Activity</a></li>
              <li><a href="#contact">Buzz</a></li>
              <li><a href="#config">Buzz</a></li>
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
    <button type="button" class="btn btn-inverse" id="MERP">Merp</button>
    </div>
    <div class="container">
<div class="btn-group">
    <button type="button" class="btn btn-primary" id="activity">activity</button>
    </div>
    <div class="container">

 <div id="messages"></div>
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
      
      $('#MERP').on('click', function (e) {
      alert( "FUCK IT!!!" );
      $.ajax({
      type: "POST",
      url: "/merp",
      });
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
      $('#messages').append('<li>Connected to Skinner Box.</li>');
      }
      ws.onmessage = function(evt) {
      $('#messages').empty();
      $('#messages').append('<li>' + evt.data + '</li>');
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
