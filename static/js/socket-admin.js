var socket = io.connect(document.protocol + '//' + document.domain + ':' + location.port);

socket.on('connect-admin', function() {
  console.log('Conectado ao servidor!');
});

socket.on('update-mesas-ocupadas', function(data) {
  var atual = $('#total_mesas_abertas').html();
  if (parseInt(atual) !== parseInt(data.num_mesas)) {
    $('#total_mesas_abertas').html(data.num_mesas);
  }

  const mesasCadastradas = document.querySelectorAll('.mesa');
  if (mesasCadastradas.length > 0) {
    const idMesa = data._idMesa;
    mesasCadastradas.forEach(mesa => {
      const aElement = mesa.querySelector('a[data-bs-id]');
      const statusElement = mesa.querySelector('.status_mesa');
      if (aElement && aElement.getAttribute('data-bs-id') === idMesa) {
        mesa.classList.remove('completed');
        mesa.classList.add('not-completed');
        statusElement.innerHTML = 'Ocupada';
        statusElement.setAttribute('style', 'color: var(--orange)');
      } else {
        mesa.classList.add('completed');
        mesa.classList.remove('not-completed');
        statusElement.innerHTML = 'Livre';
        statusElement.setAttribute('style', 'color: var(--dark-grey)');
      }
    });
  }
});




socket.on('pedido-cliente-solicitado', function(pedido) {

 var pedidoComponente = '<div class="d-flex justify-content-between align-items-center pedidoCard">'+
            '<div class="d-flex flex-column justify-content-start align-items-start profile w-100">'+
                '<div>'+pedido.nome_produto+'</div>'+
                '<small class="text-body-secondary" id="tempo-decorrido'+pedido._idPedido+'">00:00:00</small>'+
                '<input type="hidden" id="tempo'+pedido._idPedido+'" value="'+pedido.created_at+'">'+
                '<input type="hidden" class="order-id" value="'+pedido._idPedido+'">'+
            '</div>'+
            '<div class="text-center">'+pedido.quantidade+'</div>'+
            '<div>'+
             '<div class="d-flex flex-column justify-content-center align-items-start">'+
              '<form action="/aceitar_pedidos" method="post">'+
               '<input type="hidden" name="_idPedido" value="'+pedido._idPedido+'">'+
                `<button type="button" onclick="aceitarPedido('`+pedido._idPedido+`')"` +
                 ' class="optionAceitar text-success  d-flex justify-content-center align-items-center">'+
                  ' <div style=" font-size: .8rem;">Aceitar</div>'+
                            '<div><i style=" font-size: 1.5rem;" class="bi bi-check my-icon"></i></div>'+
                        '</button>'+
                    '</form>'+
                    '<a href="#" class="optionAceitar text-danger d-flex justify-content-center align-items-center">'+
                        '<div style=" font-size: .8rem;">Recusar</div>'+
                        '<i style=" font-size: 1.5rem;" class="bi bi-x my-icon"></i>'+
                    '</a>'+
               '</div>'+
            '</div>'+
        '</div>';

// Use o método append() do jQuery para adicionar o novo elemento filho à #listaPedidos
    $('#listaPedidos').append(pedidoComponente);
     setTimmer(pedido.created_at,pedido._idPedido)
    });

 $(document).ready(function() {
    socket.emit('join-room-admin', {});
  });



socket.on('pedido-admin-pagamento', function(comanda) {
   var numeroMesa = '';
    $.ajax({
        url: '/get_mesa/' + comanda._idMesa,
        type: 'GET',
        success: function(response) {
        console.log(response)
            numeroMesa = response.numero_mesa;
            var pagamentoComponente = `
  <div class="d-flex justify-content-between align-items-center pedidoCard">
    <div class="d-flex flex-column justify-content-start align-items-start profile w-100">
      <div>Mesa: <strong>${numeroMesa}</strong></div>
      <div>Tipo: <strong>${comanda.tipo_pagamento}</strong></div>
      <div>Esperando: <strong class="text-danger "  id="tempo-decorrido-pagamente${comanda.id_comanda}">00:00:00</strong></div>
      <input type="hidden" id="tempoUp${comanda.id_comanda}" data-id="${comanda.id_comanda}" class="pagComanda" value="${comanda.updated_at}">
      <input type="hidden" class="order-id-pagamento" value="${comanda.id_comanda}">
    </div>
    <div>
      <div class="d-flex flex-column justify-content-center align-items-start">
        <form id="form-finalizar-pagamento${comanda.id_comanda}" action="/finalizar_pagamento" method="post">
          <input type="hidden" name="_idComanda" value="${comanda.id_comanda}">
          <button type="button" data-comanda="${comanda.id_comanda}" class="optionAceitar text-success aceitarPagamentos d-flex justify-content-center align-items-center">
            <div style="font-size: .8rem;">Finalizar</div>
            <div><i style="font-size: 1.5rem;" class="bi bi-check my-icon"></i></div>
          </button>
        </form>
      </div>
    </div>
  </div>
`;
    $('#listaPagamentos').append(pagamentoComponente);
    $('.aceitarPagamentos').click(function(event) {
      event.preventDefault(); // impedir o comportamento padrão de enviar o formulário
     var _idComanda=$(this).attr('data-comanda')
      // Obter os dados do formulário
      var formData = $('#form-finalizar-pagamento'+_idComanda).serialize();

      // Enviar os dados do formulário via AJAX
      $.ajax({
        url: $('#form-finalizar-pagamento'+_idComanda).attr('action'),
        type: 'POST',
        data: formData,
        success: function(response) {
            socket.emit('pagamento-realizado',{_idComanda: _idComanda});
            window.location.href = response.redirect_url;
        },
        error: function(error) {
          console.log(error);
        }
      });
    });

    // Encontra todos os elementos com a classe "tempo-decorrido"
var elementosTempoDecorrido = document.querySelectorAll('.pagComanda');

// Para cada elemento encontrado
elementosTempoDecorrido.forEach(function(elemento) {
  // Cria um timer que atualiza o tempo decorrido a cada segundo
  setInterval(function() {
    // Calcula o tempo decorrido em segundos
    var tempoDecorrido = Math.floor((Date.now() - new Date($(elemento).val())) / 1000);
      console.log(tempoDecorrido)
    // Formata o tempo decorrido como HH:MM:SS
    var horas = Math.floor(tempoDecorrido / 3600);
    var minutos = Math.floor((tempoDecorrido % 3600) / 60);
    var segundos = tempoDecorrido % 60;
    var tempoDecorridoFormatado = horas.toString().padStart(2, '0') + ':' + minutos.toString().padStart(2, '0') + ':' + segundos.toString().padStart(2, '0');
    // Atualiza o texto do elemento com o tempo decorrido formatado
    $('#tempo-decorrido-pagamente'+$(elemento).attr('data-id')).html(tempoDecorridoFormatado)
  }, 1000); // Intervalo de atualização: 1 segundo
});


        },
        error: function(error) {
            console.log(error);
        }
    });


});

