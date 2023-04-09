$('.menu-item').bind('click', function() {
    $('.menu-item').each(function(i,el){
        $(el).removeClass('dKktdX')
    })
    $(this).addClass('dKktdX')
});