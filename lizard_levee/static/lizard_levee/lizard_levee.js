(function() {
  var ANIMATION_DURATION, changeDisplay, fixCrossSectionImages;

  ANIMATION_DURATION = 150;

  fixCrossSectionImages = function() {
    var newHeight;
    newHeight = $(".cross-section-image:visible").innerHeight();
    return $(".cross-section-image img").height(newHeight);
  };

  changeDisplay = function(display_option) {
    var toHide1, toHide2, toShow;
    toShow = $(display_option.data('show'));
    toHide1 = $(display_option.data('hide1'));
    toHide2 = $(display_option.data('hide2'));
    if (toHide1.is(':visible')) {
      toHide1.slideUp(ANIMATION_DURATION, function() {
        return toShow.slideDown(ANIMATION_DURATION);
      });
    }
    if (toHide2.is(':visible')) {
      toHide2.slideUp(ANIMATION_DURATION, function() {
        return toShow.slideDown(ANIMATION_DURATION);
      });
    }
    return fixCrossSectionImages();
  };

  $(".display-option-link").live('click', function(e) {
    e.preventDefault();
    return changeDisplay($(this));
  });

}).call(this);
