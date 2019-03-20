"use strict";
/*
 * By Osvaldas Valutis, www.osvaldas.info Available for use under the MIT
 * License
 */
(function ($, window, document, undefined) {
  $.fn.doubleTapToGo = function (params) {
    if (!('ontouchstart' in window) && !navigator.msMaxTouchPoints
      && !navigator.userAgent.toLowerCase().match(/windows phone os 7/i))
      return false;

    this.each(function () {
      var curItem = false;

      $(this).on('click', function (e) {
        var item = $(this);
        if (item[0] != curItem[0]) {
          e.stopPropagation();
          e.preventDefault();
          curItem = item;
        }
      });

      $(document).on('click touchstart MSPointerDown', function (e) {
        var resetItem = true, parents = $(e.target).parents();

        for (var i = 0; i < parents.length; i++)
          if (parents[i] == curItem[0]) {
            resetItem = false;
            break;
          }

        if (resetItem)
          curItem = false;
      });
    });
    return this;
  };
})(jQuery, window, document);

var reflow = function () {

  var $window = $(window);
  var $body = $('body');

  var initTocTop = function() {
    var tocTop = $('#toc-bar');
    if (!tocTop.length) {
      return;
    }

    tocTop.affix({
      offset: {
        top: tocTop.offset().top,
        bottom: ($('footer').outerHeight(true) + $('.subfooter').outerHeight(true) - 70)
        // padding of footer.
      }
    });

    $body.scrollspy({
      target: '#toc-scroll-target'
    });
  }

  var initTocSlidebar = function () {
    // toc aside bar
    // calculate the offset when DOM has finished loading.
    $(function () {
      if ($('#toc-sidebar[data-spy=affix]').length) {
        $('#toc-sidebar').affix({
          offset: {
            top: $('#toc-sidebar').offset().top + $('#m-top-navbar').height(),
            bottom: ($('footer').outerHeight(true) + $('.subfooter').outerHeight(true) - 40)
            // padding of footer.
          }
        });
      }
    });
    $body.scrollspy({ target: '#toc-scroll-target' })
  };

  var initCarousel = function () {
    // Start carousel
    var el = $('.carousel');
    el.carousel();
  };

  var initHighlighting = function () {
    // activate syntax higlighting with highlight.js
    // Note: only run if `hljs` exists
    if (typeof hljs !== 'undefined') {
      // classic encoding with <div class="source"><pre></pre></div>
      // and HTML5 version with <pre><code></code></pre>
      $('div.source pre, pre code').each(function (i, e) {
        hljs.highlightBlock(e);
      });
    }
  };

  var resizeTopNavBar = function () {
    var navbar = $('#m-top-navbar');
    var size = 0;
    if (navbar.length) {
      size = navbar.height() + 20; // normally 70
    }
    $('body').css('padding-top', size);
  };

  var initTopNavBar = function () {
    $(window).resize(resizeTopNavBar);
    // initialize size on start up
    resizeTopNavBar();

    // prevents the browser from opening a URL but allows that if tapped once
    // again in succession
    $('.dropdown-submenu').doubleTapToGo();

    // auto adjust placement of sub dropdown menu when out of window.
    $('.dropdown-submenu').on('mouseenter', function (event) {
      var ww = $(window).width();
      var menu = $(this);
      var $menuItem = menu.find('.dropdown-menu');
      var width = $menuItem.width();
      var mw = width + (menu.offset().left + menu.width());
      if (ww < mw) {
        $menuItem.css('left', -1 * (width), 'important');
      } else {
        $menuItem.css('left', '100%');
      }
    });
  };


  return {
    init: function () {
      initCarousel();
      initTocTop();
      initTocSlidebar();
      initHighlighting();
      initTopNavBar();
    }
  };
}();

// Additional skin Javascript
// ++++++++++++++++++++++++++++++++++++++++++
$(document).ready(function () {

  reflow.init();

});
