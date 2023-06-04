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

function submitLogin() {
  const alertaArea = document.querySelector('.alerta-area'); // Seleciona a área do alerta
  const form = $('form'); // Seleciona o formulário
  $.ajax({
    url: '/login-cliente',
    type: 'POST',
    data: form.serialize(), // Envia os dados do formulário
    success: function(response) {
      if(response.resp){
        // Lida com a resposta do servidor em caso de sucesso
       window.location.href = '/home'; // Recarrega a página atual
      } else if(response.erro){
        // Lida com erros durante a requisição
        alertaArea.innerHTML = `<div class="alert alert-danger" role="alert">${response.erro}</div>`; // Insere o alerta com o erro na área especificada
        setTimeout(() => {
          alertaArea.innerHTML = ''; // Remove o alerta após 5 segundos
        }, 5000);
      }
    },
    error: function(jqXHR, textStatus, errorThrown) {
      // Lida com erros durante a requisição
      alertaArea.innerHTML = `<div class="alert alert-danger" role="alert">Ocorreu um erro durante a requisição, tente novamente mais tarde.</div>`; // Insere o alerta com o erro na área especificada
      setTimeout(() => {
        alertaArea.innerHTML = ''; // Remove o alerta após 5 segundos
      }, 5000);
    }
  });
}


function submitRegister() {
const alertaAreaErro = document.querySelector('.alerta-area-register'); // Seleciona a área do alerta
  const formRegister = $('#register_form'); // Seleciona o formulário
  $.ajax({
    url: '/register',
    type: 'POST',
    data: formRegister.serialize(), // Envia os dados do formulário
    success: function(response) {
      if(response.resp){
        // Lida com a resposta do servidor em caso de sucesso
       window.location.reload(); // Recarrega a página atual
      } else if(response.erro){
        // Lida com erros durante a requisição
        alertaAreaErro.innerHTML = `<div class="alert alert-danger" role="alert">${response.erro}</div>`; // Insere o alerta com o erro na área especificada
        setTimeout(() => {
          alertaAreaErro.innerHTML = ''; // Remove o alerta após 5 segundos
        }, 5000);
      }
    },
    error: function(jqXHR, textStatus, errorThrown) {
      // Lida com erros durante a requisição
      alertaAreaErro.innerHTML = `<div class="alert alert-danger" role="alert">Ocorreu um erro durante a requisição, tente novamente mais tarde.</div>`; // Insere o alerta com o erro na área especificada
      setTimeout(() => {
        alertaAreaErro.innerHTML = ''; // Remove o alerta após 5 segundos
      }, 5000);
    }
  });
}








const menuOff = document.getElementById('logadoOff')
menuOff.addEventListener('show.bs.offcanvas', event => {
    $.ajax({
        url: "/status_pedidos",
        type: "GET",
        success: function(response) {
            // handle successful response here
            console.log(response)
            if( response.pedidos != 0){
                $('#pedido_tag').html(response.pedidos)
            }
        },
        error: function(xhr, status, error) {
            // handle error response here
            console.log(xhr.responseText);
        }
    });


})





const myOffcanvas = document.getElementById('cart')
myOffcanvas.addEventListener('show.bs.offcanvas', event => {

var page = window.location.pathname.split('/').pop()

$.ajax({
    url: "/carrinho/"+page,
    type: "GET",
    success: function(response) {
        // handle successful response here

        $('#cart').html(response)


    },
    error: function(xhr, status, error) {
        // handle error response here
        console.log(xhr.responseText);
    }
});


})



function countCart(_idComanda) {
 var totalCart = $('#totalCart'+_idComanda);
 console.log(totalCart)
  let total = 0;
  // Percorre cada elemento com a classe "subtotal"
  $(".subtotal"+_idComanda).each(function() {

    // Obtém o valor numérico do elemento usando a função MoneyParser()
    let valor = MoneyParser($(this).text());

    // Soma o valor no contador total
    total += valor;
  });
  // Formata o valor total como dinheiro usando a função MoneyFormatter()

  let valor_formatado = MoneyFormatter(total);
    console.log(valor_formatado)
  // Atualiza o elemento HTML com o valor total formatado
  totalCart.html(valor_formatado);
}
function MoneyFormatter(valor) {
  return valor.toLocaleString('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  });
}
function MoneyParser(valor) {
  return parseFloat(valor.replace(/[^0-9,-]/g, '').replace(',', '.'));
}



function atualizarPedido(pedido_id, nova_quantidade,_idComanda) {
  $.ajax({
    type: "POST",
    url: "/atualizar_pedido",
    data: {
      pedido_id: pedido_id,
      nova_quantidade: nova_quantidade,
      valor: $('#valor_pedido'+pedido_id).val()
    },
    success: function(response) {
       $('#pedido_item_valor'+pedido_id).html(response.valor);
       countCart(_idComanda)

    },
    error: function(xhr, status, error) {
      console.log(error);
    }
  });
}