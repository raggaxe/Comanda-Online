
var mousePosition;
var isDown;
var componente;
var positionDRAG = { x: 0, y: 0 }

var componentesCount = 0

$(document).ready(function() {
    $('.layer--').each(function(i,x){
        componentesCount++;
    })
});

//SHAPE

//var height = $('#height')
//var background = $('#background')
////MARGIN
//var margin_top = $('#margin-top')
//var margin_bottom = $('#margin-bottom')
//var margin_left = $('#margin-left')
//var margin_right = $('#margin-right')
////PADDING
//var padding_top = $('#padding-top')
//var padding_bottom = $('#padding-bottom')
//var padding_left = $('#padding-left')
//var padding_right = $('#padding-right')




//
//
//
// //COLOCA A FUNCAO DE CLICAR E ARRASTAR
//$('.compontente--custom').on('mousedown', function(e) {
//            isDown = true;
//            componente = $(this);
//              settingNav(this);
//              settingConfig(this)
//            var offsetDiv = $( this ).offset();
//            offset = [
//                    offsetDiv.left - e.clientX,
//                    offsetDiv.top - e.clientY
//            ];
//        });
//
//////COLOCA A FUNCAO DE CLICAR E ARRASTAR
//document.addEventListener('mouseup', function() {
//    isDown = false;
//}, true);
////
////COLOCA A FUNCAO DE CLICAR E ARRASTAR
//document.addEventListener('mousemove', function(event) {
//var frame = $('#frame').offset()
//var widthFrame = $('#frame').width()
//var heightrame = $('#frame').height()
//    event.preventDefault();
//    if (isDown) {
//        mousePosition = {
//            x : event.clientX,
//            y : event.clientY
//        };
//
//        if(  (mousePosition.x + offset[0]) >= (frame.left )
//         &&  (mousePosition.x - offset[0])   <=   ( widthFrame + frame.left   )
//         &&
//         (mousePosition.y + offset[1]) >= (frame.top )
//         &&  (mousePosition.y - offset[1])   <=   ( heightrame + frame.top   )
//
//         )   {
//         console.log((mousePosition.y + offset[1]) ,
//            (mousePosition.x + offset[0]))
//         $("#offset"+ componente.attr('data-componente')+componente.attr('data-camada')).val( parseInt(mousePosition.y + offset[1]) +","+ parseInt(mousePosition.x + offset[0] ) )
//            componente.offset({
//            top: (mousePosition.y + offset[1]) ,
//            left: (mousePosition.x + offset[0])
//            });
//        }
//    }
//}, true);






function openCanvas(_this){
    const bsOffcanvas = new bootstrap.Offcanvas('#staticBackdrop');
    bsOffcanvas.show();
   // console.log($(_this))
     settingNav($(_this))
    settingConfig($(_this))
    $("#settings").show();
    $("#bodyCriar").hide();
    $("#bodyEditar").show();
    $("#staticBackdropLabel").html("Editar");
}






//CONSTROE A CAMADA E INCLUI NA LISTA DE CAMADAS
function buildLayer( _idComponente,categoria,name,html,_idCena){

     $('#listaCamadas').append(`<div data-cena="${_idCena}" data-camada="${componentesCount}" data-categoria="${categoria}" data-name="${name}" data-componente="${_idComponente}" data-html='${html}' class="layer-- mb-1"   > <div><i class="bi bi-layers me-2"></i> ${name} </div><div><i class="bi bi-trash2"></i></div>  </div>`);
       $('.layer--').bind('click', function() {
       settingNav(this);
       settingConfig(this)
        openCanvas($(this))
            $('.layer--').each(function(i,el){
                $(el).removeClass('active--')
            })
            $(this).addClass('active--')
            openCanvas($(event.currentTarget))
        });

}


function clickLayer(_this){
       settingNav(_this);
       settingConfig(_this)
        openCanvas($(_this))
            $('.layer--').each(function(i,el){
                $(el).removeClass('active--')
            })
            $(_this).addClass('active--')
            openCanvas($(event.currentTarget))

}


//CLICK DA ESCOLHA DE UM ELEMENTO e INCLUI NA TELA.
function createComponente(_this){

    //FECHAR O OFFCANVAS DE CRIACAO
   $("#closeComponentes").click();
    //CONSTROE A CAMADA E INCLUI NA LISTA DE CAMADAS
   buildLayer(
   $(_this).attr('data-componente'),
   $(_this).attr('data-categoria'),
   $(_this).attr('data-name'),
   $(_this).attr('data-html'),
   $('#idCenaValue').val(),
   )

    //CONSTROE O ELEMENTO E INCLUI NO FRAME
   var _idCompnente =$(_this).attr('data-componente')
   var _categoria = $(_this).attr('data-categoria')
   var _name = $(_this).attr('data-name')
   var _cena = $('#idCenaValue').val()
   var _html = $(_this).attr('data-html')

    $('#frame').append('<div data-x=0 data-y=0  id="'+$(_this).attr('data-componente') + componentesCount +'"data-camada="'+componentesCount+'" data-categoria="'+$(_this).attr('data-categoria')+'" data-name="'+ $(_this).attr('data-name')+'" data-componente="'+$(_this).attr('data-componente')+'" data-cena="'+$('#idCenaValue').val()+'" class="compontente--custom auto--focus draggable resizable">'+$(_this).attr('data-html')+'</div>');
    //$('#frame').append(`<div id="${$(this).attr('data-componente') + componentesCount}"data-camada="${componentesCount}" data-categoria="${$(this).attr('data-categoria')}" data-name="${$(this).attr('data-name')}" data-componente="${$(this).attr('data-componente')}" class="compontente--custom auto--focus ">${$(this).attr('data-html')}</div>`);

    //CONSTROE UMA CONFIGURACAO PARA ESSE ELEMENTO
    buildConfig(_idCompnente,_categoria,_name,_html,_cena,componentesCount)

        var token = '#'+_idCompnente+componentesCount
        $(_this).attr('data-camada',componentesCount)
            settingNav($(_this))
            settingConfig($(_this))


    //SOMA DO CONTADOR DE COMPONENTES
    componentesCount ++;
};
////CONSTROE UMA CONFIGURACAO PARA ESSE ELEMENTO
function buildConfig(_idCompnente,_categoria,_name,_html,_cena,componentesCount){
//console.log(_idCompnente,_categoria,_name,_html,_cena,componentesCount)
    $.ajax({
        type: "GET",
        url: '/config',
        async:false,
        contentType: 'application/json;charset=UTF-8',
        data: {'id':_idCompnente,'categoria':_categoria,'name':_name,'html':_html,'camada':componentesCount,'cena':_cena }, // serializes the form's elements.
        success: function(data)
        {
        $('#bodyEditar').append(data.data)

        }
    });
}
//CONSTROE UMA NAV-BAR PARA ESSE ELEMENTO
function settingNav(_this){
    $('.myConfigsPanel').hide();
    $("#config"+ $(_this).attr('data-componente')+$(_this).attr('data-camada')).parent('.myConfigsPanel').show()
    $("#nomeDaCamadaNav").html($(_this).attr('data-name'))
    $("#categoria"+ +$(_this).attr('data-camada')).val(  $(_this).attr('data-categoria') )

    $("#settings").show()
}



////RESTABELECE A CONFIGURACAO PARA ESSE ELEMENTO
function settingConfig(_this){

    //SHAPE
    var overlay =  $("#"+ $(_this).attr('data-componente')+$(_this).attr('data-camada'))
    var tokenOverlay = $(_this).attr('data-componente')+$(_this).attr('data-camada')


    setWidth(tokenOverlay)
    setHeight(tokenOverlay)
//    setBackground(tokenOverlay)
    setHTML(tokenOverlay)

//
//    //MARGIN
//    var atual_margin_top = $('#margin-top').val()
//    var atual_margin_bottom = $('#margin-bottom').val()
//    var atual_margin_left = $('#margin-left').val()
//    var atual_margin_right = $('#margin-right').val()
//    //PADDING
//    var atual_padding_top = $('#padding-top').val()
//    var atual_padding_bottom = $('#padding-bottom').val()
//    var atual_padding_left = $('#padding-left').val()
//    var atual_padding_right = $('#padding-right').val()
}
//LARGURA  DESSE ELEMENTO NA TELA
function setWidth(tokenOverlay){
    var _width = $('#width'+tokenOverlay)
    var atual_width = $('#'+  tokenOverlay ).width()
    _width.attr({
       "max" : parseInt($('#frame').width()),
       "min" : 0,
       "val" : parseInt(atual_width),

    });

    document.getElementById('width'+tokenOverlay).value = parseInt(atual_width);
    $('#atualWidth'+tokenOverlay).html( atual_width );
    $('#width'+tokenOverlay).on('change', function(e) {
            $('#atualWidth'+tokenOverlay).html( this.value);
             $('#'+  tokenOverlay ).width($(this).val());
    });
}
//ALTURA  DESSE ELEMENTO NA TELA
function setHeight(tokenOverlay){
    var _height = $('#height'+tokenOverlay)
    var atual_height = $('#'+  tokenOverlay ).height()
    _height.attr({
       "max" : parseInt($('#frame').height()),
       "min" : 0,
       "val" : parseInt(atual_height),

    });
    document.getElementById('height'+tokenOverlay).value = parseInt(atual_height);
    $('#atualHeight'+tokenOverlay).html( atual_height );
    $('#height'+tokenOverlay).on('change', function(e) {
           $('#atualHeight'+tokenOverlay).html( this.value);
             $('#'+  tokenOverlay ).height($(this).val())

    });
}






//HTML  DESSE ELEMENTO NA TELA
function setHTML(tokenOverlay){
    var _html = $('#html'+tokenOverlay)

    var atual_html = $('#'+  tokenOverlay ).html();

    _html.val(atual_html);
    _html.on('input', function(e) {
             $('#'+  tokenOverlay ).html($( this ).val() );
    });
}

function saveConfig(_idCena){

    $('.myConfigsPanel .config').each(function(i,e){
        var form = $(e);
        var actionUrl = form.attr('action');
    $.ajax({
        type: "POST",
        url: actionUrl,
        data: form.serialize(), // serializes the form's elements.
        success: function(data)
        {
          alert(data); // show response from the php script.
         }
      });
    })


}




interact('.resizable')
  .resizable({
  modifiers: [
        interact.modifiers.restrictSize({ max: 'parent' }),
      ],
    edges: { top: true, left: true, bottom: true, right: true },
    listeners: {
      move: function (event) {
        let { x, y } = event.target.dataset

        x = (parseFloat(x) || 0) + event.deltaRect.left
        y = (parseFloat(y) || 0) + event.deltaRect.top

        Object.assign(event.target.style, {
          width: `${event.rect.width}px`,
          height: `${event.rect.height}px`,
          transform: `translate(${x}px, ${y}px)`
        })

        Object.assign(event.target.dataset, { x, y })
      }
    }
  })
  .on(['resizestart', 'resizemove', 'resizeend','tap'], function (event) {
        $("#offsetX"+ $(event.currentTarget).attr('data-componente')+$(event.currentTarget).attr('data-camada')).val(positionDRAG.x)
        $("#offsetY"+ $(event.currentTarget).attr('data-componente')+$(event.currentTarget).attr('data-camada')).val(positionDRAG.y)

            openCanvas($(event.currentTarget))
            settingNav($(event.currentTarget))
            settingConfig($(event.currentTarget))
})





interact('.draggable').draggable({
  modifiers: [
     interact.modifiers.restrictRect({
      restriction: 'parent',
        endOnly: true,
      elementRect: { top: 0, left: 0, bottom: 1, right: 1 }

        })
    ],
  listeners: {

    start (event) {
     // console.log(event.type, event.target)
    },
    move (event) {
    positionDRAGIni.x = parseInt($(event.currentTarget).attr('data-x'))
    positionDRAGIni.y = parseInt($(event.currentTarget).attr('data-y'))
      positionDRAG.x += event.dx
      positionDRAG.y += event.dy

      event.target.style.transform =
        `translate(${positionDRAG.x}px, ${positionDRAG.y}px)`
    },
  }
}).on('dragend', function (event) {
        $("#offsetX"+ $(event.currentTarget).attr('data-componente')+$(event.currentTarget).attr('data-camada')).val(positionDRAG.x)
        $("#offsetY"+ $(event.currentTarget).attr('data-componente')+$(event.currentTarget).attr('data-camada')).val(positionDRAG.y)
}).on('tap', function (event) {
            openCanvas($(event.currentTarget))
            settingNav($(event.currentTarget))
            settingConfig($(event.currentTarget))
})


// Step 1
const slider = interact('.slider')    // target elements with the "slider" class

slider
  // Step 2
  .draggable({                        // make the element fire drag events
    origin: 'self',                   // (0, 0) will be the element's top-left
    inertia: true,                    // start inertial movement if thrown
    modifiers: [
      interact.modifiers.restrict({
        restriction: 'self'           // keep the drag coords within the element
      })
    ],
    // Step 3
    listeners: {
      move (event) {                  // call this listener on every dragmove
        const sliderWidth = interact.getElementRect(event.target).width
        const value = event.pageX / sliderWidth

        event.target.style.paddingLeft = (value * 100) + '%'
        event.target.setAttribute('data-value', value.toFixed(2))
      }
    }
  })
