var currentPage = window.location.pathname;
console.log(currentPage)
$('.menu-item').each(function(){
    if("/"+$(this).attr('id') == currentPage){
        $(this).addClass('dKktdX');
    }
});


$('.menu-item').bind('click', function() {
    $('.menu-item').each(function(i,el){
        $(el).removeClass('dKktdX')
    })
    $(this).addClass('dKktdX')

      if($(this).attr('id') != currentPage){
        window.location.href = "/"+$(this).attr('id')
    }



});