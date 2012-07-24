ANIMATION_DURATION = 150


fixCrossSectionImages = ->
    newHeight = $(".cross-section-image:visible").innerHeight()
    $(".cross-section-image img").height(newHeight)


changeDisplay = (display_option) ->
    toShow = $(display_option.data('show'))
    toHide1 = $(display_option.data('hide1'))
    toHide2 = $(display_option.data('hide2'))
    if toHide1.is(':visible')
        toHide1.slideUp ANIMATION_DURATION, () ->
            toShow.slideDown(ANIMATION_DURATION)
    if toHide2.is(':visible')
        toHide2.slideUp ANIMATION_DURATION, () ->
            toShow.slideDown(ANIMATION_DURATION)
    fixCrossSectionImages()


$(".display-option-link").live 'click', (e) ->
    e.preventDefault()
    changeDisplay $(@)


divideVerticalSpaceEqually = () ->
    """ For #evenly-spaced-vertical, divide the vertical space evenly between
    the .vertical-item elements.  Take note of the 4px border between
    them.
    Note that a "not-evenly-spaced" element will be given half the
    space.
    Handy for forms underneath the graphs.
    """
    mainContentHeight = $("#evenly-spaced-vertical").innerHeight();
    #var numberOfItems, numberOfDoubleItems;
    numberOfItems = $('#evenly-spaced-vertical > .vertical-item').length;
    numberOfDoubleItems = $('#evenly-spaced-vertical > .double-vertical-item').length;
    verticalItemHeight = Math.floor(
        (mainContentHeight / (numberOfItems + 2 * numberOfDoubleItems))) - 1;
    console.log(verticalItemHeight);
    $('#evenly-spaced-vertical > .vertical-item').height(verticalItemHeight);
    $('#evenly-spaced-vertical > .double-vertical-item').height(2 * verticalItemHeight);

$ ->
    console.log('hallo');
    $("#evenly-spaced-vertical").height($(window).height() - $("header").height() - $("#footer").height())
    divideVerticalSpaceEqually()
