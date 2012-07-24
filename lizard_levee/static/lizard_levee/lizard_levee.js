(function() {
  var ANIMATION_DURATION, changeDisplay, divideVerticalSpaceEqually, fixCrossSectionImages;

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

  divideVerticalSpaceEqually = function() {
    " For #evenly-spaced-vertical, divide the vertical space evenly between\nthe .vertical-item elements.  Take note of the 4px border between\nthem.\nNote that a \"not-evenly-spaced\" element will be given half the\nspace.\nHandy for forms underneath the graphs.";
    var mainContentHeight, numberOfDoubleItems, numberOfItems, verticalItemHeight;
    mainContentHeight = $("#evenly-spaced-vertical").innerHeight();
    numberOfItems = $('#evenly-spaced-vertical > .vertical-item').length;
    numberOfDoubleItems = $('#evenly-spaced-vertical > .double-vertical-item').length;
    verticalItemHeight = Math.floor(mainContentHeight / (numberOfItems + 2 * numberOfDoubleItems)) - 1;
    console.log(verticalItemHeight);
    $('#evenly-spaced-vertical > .vertical-item').height(verticalItemHeight);
    return $('#evenly-spaced-vertical > .double-vertical-item').height(2 * verticalItemHeight);
  };

  $(function() {
    console.log('hallo');
    $("#evenly-spaced-vertical").height($(window).height() - $("header").height() - $("#footer").height());
    return divideVerticalSpaceEqually();
  });

}).call(this);
