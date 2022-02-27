/*---------------------------------------------
Template name:  BizBlog
Version:        1.0
Author:         ThemeLooks
Author url:     http://themelooks.com

NOTE:
------
Please DO NOT EDIT THIS JS, you may need to use "custom.js" file for writing your custom js.
We may release future updates so it will overwrite this file. it's better and safer to use "custom.js".

[Table of Content]

01: Background Image
02: Image To SVG
03: Searh Box
04: Navbar
05: Banner
06: Post Video Thumbnail
07: Owl Carousel Defaults
08: Preloader
09: Back To Top
10: Ajex Contact Form
----------------------------------------------*/

(function ($) {
  "use strict";

  /* 01: Background Image
  ==============================================*/
  var $bgImg = $('[data-bg-img]');
  $bgImg.css('background-image', function () {
    return 'url("' + $(this).data('bg-img') + '")';
  }).removeAttr('data-bg-img').addClass('bg-img');


  /* 02: Image To SVG
  ==============================================*/

  jQuery('img.svg').each(function () {
    var $img = jQuery(this);
    var imgID = $img.attr('id');
    var imgClass = $img.attr('class');
    var imgURL = $img.attr('src');
    jQuery.get(imgURL, function (data) {
      // Get the SVG tag, ignore the rest
      var $svg = jQuery(data).find('svg'); // Add replaced image's ID to the new SVG

      if (typeof imgID !== 'undefined') {
        $svg = $svg.attr('id', imgID);
      } // Add replaced image's classes to the new SVG


      if (typeof imgClass !== 'undefined') {
        $svg = $svg.attr('class', imgClass + ' replaced-svg');
      } // Remove any invalid XML tags as per http://validator.w3.org


      $svg = $svg.removeAttr('xmlns:a'); // Check if the viewport is set, if the viewport is not set the SVG wont't scale.

      if (!$svg.attr('viewBox') && $svg.attr('height') && $svg.attr('width')) {
        $svg.attr('viewBox', '0 0 ' + $svg.attr('height') + ' ' + $svg.attr('width'));
      } // Replace image with new SVG


      $img.replaceWith($svg);
    }, 'xml');
  });


  /* 03: Searh Box
  ==============================================*/
  var searchOpen = $('.mobile-nav-menu .search-toggle-open');
  var searchClose = $('.mobile-nav-menu .search-toggle-close');
  var searchBox = $('.nav-search-box');
  
  searchOpen.on('click', function () {
    searchBox.addClass('show');
    $(this).addClass('hide');
    searchClose.removeClass('hide');
  });
  searchClose.on('click', function () {
    searchBox.removeClass('show');
    $(this).addClass('hide');
    searchOpen.removeClass('hide');
  });


  /* 04: Navbar
  ==============================================*/
  $(window).on('scroll', function () {
    navOnScroll();
  });

  function navOnScroll() {
    if ($(window).scrollTop() > 0) {
      $('.header-fixed').addClass('is-sticky fadeInDown animated');
    } else {
      $('.header-fixed').removeClass('is-sticky fadeInDown animated');
    }
  }

  navOnScroll();
  $('.mobile-nav-menu .nav-menu-toggle').on('click', function () {
    $('.nav-menu').toggleClass('show');
  });
  $('.nav-menu .menu-item-has-children a').on('click', function (e) {
    if ($(window).width() <= 991) {
      $(this).siblings('.sub-menu').addClass('show');
    }
  });

  var subToggle = function subToggle() {
    $('.nav-menu .menu-item-has-children a').each(function () {
      $(this).siblings('.sub-menu').prepend('<li class="sub-menu-close"> <i class="fa fa-long-arrow-left"></i> ' + $(this).siblings('.sub-menu').parent().children('a').text() + '</li>');
    });
  };

  subToggle();
  $('.nav-menu .menu-item-has-children .sub-menu .sub-menu-close').on('click', function () {
    $(this).parent('.sub-menu').removeClass('show');
  });

  function subMenu() {
    $('.nav-menu .menu-item-has-children .sub-menu').each(function () {
      if ($(window).width() > 991) {
        if ($(this).offset().left + $(this).width() > $(window).width()) {
          $(this).css({
            'left': 'auto',
            'right': '100%'
          });
        }
      }
    });
  }

  subMenu();
  $(window).resize(subMenu);


  /* 05: Banner
  ==============================================*/
  var bannerText = [];
  $('.banner-slide .banner-slide-text h1').each(function () {
    bannerText.push($(this).text());
    $('.banner-slider-dots').prepend('<div class="dots-count"></div>');
  });
  $('.banner-slider-dots .dots-count').each(function (i) {
    $(this).html(bannerText[i]);
  });
  $('.banner-slider-dots .dots-count').append('<span class="process-bar"></span> <span class="process-bar-active"></span>');
  var sync1 = $(".banner-slider");
  var sync2 = $(".banner-slider-dots");
  var slidesPerPage = 3;
  var syncedSecondary = true;
  sync1.owlCarousel({
    items: 1,
    slideSpeed: 2000,
    autoplay: true,
    loop: true,
    responsiveRefreshRate: 200,
    animateIn: "fadeIn",
    animateOut: "fadeOut",
    margin: 50
  }).on('changed.owl.carousel', syncPosition);
  sync2.on('initialized.owl.carousel', function () {
    setTimeout(function () {
      sync2.find(".owl-item").eq(0).addClass("current");
    }, 100);
  }).owlCarousel({
    items: slidesPerPage,
    dots: true,
    nav: true,
    smartSpeed: 200,
    slideSpeed: 500,
    slideBy: slidesPerPage,
    responsiveRefreshRate: 100,
    margin: 110
  }).on('changed.owl.carousel', syncPosition2);

  function syncPosition(el) {
    //if you set loop to false, you have to restore this next line
    //var current = el.item.index;
    //if you disable loop you have to comment this block
    var count = el.item.count - 1;
    var current = Math.round(el.item.index - el.item.count / 2 - .5);

    if (current < 0) {
      current = count;
    }

    if (current > count) {
      current = 0;
    } //end block


    sync2.find(".owl-item").removeClass("current").eq(current).addClass("current");
    var onscreen = sync2.find('.owl-item.active').length - 1;
    var start = sync2.find('.owl-item.active').first().index();
    var end = sync2.find('.owl-item.active').last().index();

    if (current > end) {
      sync2.data('owl.carousel').to(current, 100, true);
    }

    if (current < start) {
      sync2.data('owl.carousel').to(current - onscreen, 100, true);
    }
  }

  function syncPosition2(el) {
    if (syncedSecondary) {
      var number = el.item.index;
      sync1.data('owl.carousel').to(number, 100, true);
    }
  }

  sync2.on("click", ".owl-item", function (e) {
    e.preventDefault();
    var number = $(this).index();
    sync1.data('owl.carousel').to(number, 300, true);
  });


  /* 06: Post Video Thumbnail
  ==============================================*/
  $('.vid-play-btn').magnificPopup({
    type: 'iframe',
    iframe: {
      markup: '<div class="mfp-iframe-scaler">' + '<div class="mfp-close"></div>' + '<iframe class="mfp-iframe" frameborder="0" allowfullscreen></iframe>' + '</div>',
      patterns: {
        youtube: {
          index: 'youtube.com/',
          id: 'v=',
          src: 'https://www.youtube.com/embed/%id%?autoplay=1'
        },
        vimeo: {
          index: 'vimeo.com/',
          id: '/',
          src: 'https://player.vimeo.com/video/%id%?autoplay=1'
        },
        gmaps: {
          index: 'https://maps.google.',
          src: '%id%&output=embed'
        }
      },
      srcAction: 'iframe_src'
    }
  });


  /* 07: Owl Carousel Defaults
  ==============================================*/
  var checkData = function checkData(data, value) {
    return typeof data === 'undefined' ? value : data;
  };

  var $owlCarousel = $('.owl-carousel');
  $owlCarousel.each(function () {
    var $t = $(this);
    $t.owlCarousel({
      items: checkData($t.data('owl-items'), 1),
      margin: checkData($t.data('owl-margin'), 0),
      loop: checkData($t.data('owl-loop'), true),
      smartSpeed: 1000,
      autoplay: checkData($t.data('owl-autoplay'), false),
      autoplayTimeout: checkData($t.data('owl-speed'), 8000),
      center: checkData($t.data('owl-center'), false),
      animateIn: checkData($t.data('owl-animate-in'), false),
      animateOut: checkData($t.data('owl-animate-out'), false),
      nav: checkData($t.data('owl-nav'), false),
      navText: ['<i class="fa fa-angle-left"></i>', '<i class="fa fa-angle-right"></i>'],
      dots: checkData($t.data('owl-dots'), false),
      responsive: checkData($t.data('owl-responsive'), {}),
      mouseDrag: checkData($t.data('owl-mouse-drag'), false)
    });
  });


  /* 08: Preloader
  ==============================================*/
  $(window).on('load', function () {
    $('.preloader').fadeOut(2000);
  });

  /* 09: Back to Top
  ==============================================*/
  var $backToTopBtn = $('.back-to-top');

  if ($backToTopBtn.length) {
    var scrollTrigger = 400,
        // px
    backToTop = function backToTop() {
      var scrollTop = $(window).scrollTop();

      if (scrollTop > scrollTrigger) {
        $backToTopBtn.addClass('show');
      } else {
        $backToTopBtn.removeClass('show');
      }
    };

    backToTop();
    $(window).on('scroll', function () {
      backToTop();
    });
    $backToTopBtn.on('click', function (e) {
      e.preventDefault();
      $('html,body').animate({
        scrollTop: 0
      }, 700);
    });
  }

  /* 10: Ajax Contact Form
    ==============================================*/
    $('.my-contact-form-cover').on('submit', 'form', function(e) {
      e.preventDefault();

      var $el = $(this);

      $.post($el.attr('action'), $el.serialize(), function(res){
          res = $.parseJSON( res );
          $el.parent('.my-contact-form-cover').find('.form-response').html('<span>' + res[1] + '</span>');
      });
    });
  
})(jQuery);