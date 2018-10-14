(function($){
  $('.carousel.carousel-slider').carousel({
    fullWidth: true,
    indicators: true
  });

  $(document).ready(function(){
    $('.collapsible').collapsible();
  });

  $(document).ready(function(){
    $('.fixed-action-btn').floatingActionButton();
  });

  $(function(){

    $('.sidenav').sidenav();

  }); // end of document ready
})(jQuery); // end of jQuery name space