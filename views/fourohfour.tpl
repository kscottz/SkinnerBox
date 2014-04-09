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

    <div class="row-fluid">
      
      <div class="span12 pagination-centered"><img src="/img/fourohfour.gif" alt="header" class="img-polaroid"/></div>
      <h1><p class="text-center">Ooops, our tubes are clogged!</p></h1>
      <h3><p class="text-center">{{error}}</p></h3>
      <h3><p class="text-center"><a class="brand" href="/">Take me home!</a></p></h3>
    </div>


      


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
      $('#PICS').on('click', function (e) 
      {
      window.location.href = '/pics';
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
