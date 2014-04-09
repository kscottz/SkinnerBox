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
          <a class="brand" href="/">Rat Status Page</a>
          <div class="nav-collapse">
            <ul class="nav">
              <li><a href="/">Live Feed</a></li>
              <li  class="active"><a href="/activity">Activity</a></li>
              <li><a href="/passfail">Experiments</a></li>
              <li><a href="/controls">Controls</a></li>
              <li><a href="/pics">Camera</a></li>
              <li><a href="/stats">Today</a></li>
              <li><a href="/about">About</a></li>
            </ul>
          </div><!--/.nav-collapse -->
        </div>
      </div>
    </div>

    <div class="container">
    <button type="button" class="btn btn-primary" id="HOME">Back</button>
    <button type="button" class="btn btn-warning" id="activity">Refresh</button>
    <div class="container">
</div>
    <div class="container">
      <img src="/img/activity.png">
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
      $('#activity').on('click', function (e) 
      {
      window.location.href = '/activity';
      return false;
      });

      $('#HOME').on('click', function (e) 
      {
      window.location.href = '/';
      return false;
      });

    </script>


    </script>
    <script src="/js/bootstrap-typeahead.js"></script>

  </body>
</html>
