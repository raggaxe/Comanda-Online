

$('.order-id').each(function(i,e){
    var _id = $(e).val()
    var tempo = $('#tempo'+_id).val()
    setTimmer(tempo,_id)
})

$('.order-id-cook').each(function(i,e){
    var _idcook = $(e).val()
    var tempocook = $('#cook'+_idcook).val()
   setCooking(tempocook,_idcook)
})

$('.order-id-pagamento').each(function(i,e){
    var _idcook = $(e).val()
    var tempocook = $('#tempoUp'+_idcook).val()
   setPagamento(tempocook,_idcook)
})

function entregarPedido(_idPedido) {
console.log('etregar')
    $.ajax({
        type: "POST",
        url: "/entregar_pedidos",
        data: { _idPedido: _idPedido },
        success: function(response) {
           if (response.success) {
            // emitir evento de socket
            socket.emit('pedido-entregue',{_idPedido: _idPedido});
            // atualizar a página
            location.reload();
          }
        },
        error: function(xhr, status, error) {
            console.error("Erro ao aceitar pedido: " + error);
        }
    });
}
function aceitarPedido(_idPedido) {
    $.ajax({
        type: "POST",
        url: "/aceitar_pedidos",
        data: { _idPedido: _idPedido },
        success: function(response) {
           if (response.success) {
            // emitir evento de socket
            socket.emit('pedido-aceito',{_idPedido: _idPedido});
            // atualizar a página
            location.reload();
          }
        },
        error: function(xhr, status, error) {
            console.error("Erro ao aceitar pedido: " + error);
        }
    });
}

function setPagamento(tempo,_id){
    var startDate = new Date(tempo);
    // Atualize a cada segundo
    setInterval(function() {

      // Calcule o tempo decorrido em milissegundos
      let elapsed = new Date() - startDate;

      // Converta o tempo decorrido em segundos, minutos e horas
      let seconds = Math.floor(elapsed / 1000);
      let minutes = Math.floor(seconds / 60);
      let hours = Math.floor(minutes / 60);

      // Formate a saída
      let output = hours.toString().padStart(2, '0') + ':' + (minutes % 60).toString().padStart(2, '0') + ':' + (seconds % 60).toString().padStart(2, '0');

      // Atualize a exibição do tempo decorrido
      document.getElementById('tempo-decorrido-pagamente'+_id).innerHTML = output;

    }, 1000); // intervalo em milissegundos


}

function setTimmer(tempo,_id){
    var startDate = new Date(tempo);
    // Atualize a cada segundo
    setInterval(function() {

      // Calcule o tempo decorrido em milissegundos
      let elapsed = new Date() - startDate;

      // Converta o tempo decorrido em segundos, minutos e horas
      let seconds = Math.floor(elapsed / 1000);
      let minutes = Math.floor(seconds / 60);
      let hours = Math.floor(minutes / 60);

      // Formate a saída
      let output = hours.toString().padStart(2, '0') + ':' + (minutes % 60).toString().padStart(2, '0') + ':' + (seconds % 60).toString().padStart(2, '0');

      // Atualize a exibição do tempo decorrido
      document.getElementById('tempo-decorrido'+_id).innerHTML = output;

    }, 1000); // intervalo em milissegundos


}


function setCooking(tempo,_id){
    var startDate = new Date(tempo);
    // Atualize a cada segundo
     setInterval(function() {

      // Calcule o tempo decorrido em milissegundos
      let elapsed = new Date() - startDate;

      // Converta o tempo decorrido em segundos, minutos e horas
      let seconds = Math.floor(elapsed / 1000);
      let minutes = Math.floor(seconds / 60);
      let hours = Math.floor(minutes / 60);

      // Formate a saída
      let output = hours.toString().padStart(2, '0') + ':' + (minutes % 60).toString().padStart(2, '0') + ':' + (seconds % 60).toString().padStart(2, '0');

      // Atualize a exibição do tempo decorrido
      document.getElementById('tempo-cook'+_id).innerHTML = output;

    }, 1000); // intervalo em milissegundos


}


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






