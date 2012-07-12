(function() {
  var ANIMATION_DURATION, changeDisplay;

  ANIMATION_DURATION = 150;

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
      return toHide2.slideUp(ANIMATION_DURATION, function() {
        return toShow.slideDown(ANIMATION_DURATION);
      });
    }
  };

  $(".display-option-link").live('click', function(e) {
    e.preventDefault();
    return changeDisplay($(this));
  });

}).call(this);
