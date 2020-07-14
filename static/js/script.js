jQuery(document).ready(function($) {
    var $side_menu_trigger = $('#nav-trigger'),
      $content_wrapper = $('.main-content'),
      $navigation = $('header');
  
    //open-close lateral menu clicking on the menu icon
    $side_menu_trigger.on('click', function(event) {
      event.preventDefault();
  
      $side_menu_trigger.toggleClass('is-clicked');
      $navigation.toggleClass('menu-open');
      $content_wrapper.toggleClass('menu-open').one('webkitTransitionEnd otransitionend oTransitionEnd msTransitionEnd transitionend', function() {
        // firefox transitions break when parent overflow is changed, so we need to wait for the end of the trasition to give the body an overflow hidden
        $('body').toggleClass('overflow-hidden');
      });
      $('#side-nav').toggleClass('menu-open');
  
      //check if transitions are not supported - i.e. in IE9
      if ($('html').hasClass('no-csstransitions')) {
        $('body').toggleClass('overflow-hidden');
      }
    });
  
    //close lateral menu clicking outside the menu itself
    $content_wrapper.on('click', function(event) {
      if (!$(event.target).is('#menu-trigger, #menu-trigger span')) {
        $side_menu_trigger.removeClass('is-clicked');
        $navigation.removeClass('menu-open');
        $content_wrapper.removeClass('menu-open').one('webkitTransitionEnd otransitionend oTransitionEnd msTransitionEnd transitionend', function() {
          $('body').removeClass('overflow-hidden');
        });
        $('#side-nav').removeClass('menu-open');
        //check if transitions are not supported
        if ($('html').hasClass('no-csstransitions')) {
          $('body').removeClass('overflow-hidden');
        }
  
      }
    });
  
    //open (or close) submenu items in the lateral menu. Close all the other open submenu items.
    $('.item-has-children').children('a').on('click', function(event) {
      event.preventDefault();
      $(this).toggleClass('submenu-open').next('.sub-menu').slideToggle(200).end().parent('.item-has-children').siblings('.item-has-children').children('a').removeClass('submenu-open').next('.sub-menu').slideUp(200);
    });
  });