
$(document).ready(function () {
  $('#m-scroll-top').on('click', function(e) {

    function scrollTo(el, offset, clbck) {
      var pos = (el && el.length > 0) ? el.offset().top : 0;
      pos = pos + (offset ? offset : 0);

      $('html,body').animate({
          scrollTop: pos
      }, 300, clbck);
    };

     // prevent default anchor click behavior
     e.preventDefault();
    scrollTo();

  });
});
