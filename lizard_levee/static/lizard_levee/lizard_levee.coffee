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
