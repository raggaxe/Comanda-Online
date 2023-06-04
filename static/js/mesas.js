function createMesaInPanel(numero_maximo_mesas ){
        var lista = []
        document.querySelectorAll('.nr_mesa').forEach(i=> {
			lista.push(parseInt($(i).html()))
		})
    $('.panel-mesas').html('')
    for (let i = 1; i <= numero_maximo_mesas ; i++) {
        if ( lista.includes(i) === true ){
             html = '<div data-numero="'+i+'" class="mesa-item disabled" onclick="preSelecionarMesa('+i+', this)">'+i+'</div>';
        }
        else{
            html = '<div data-numero="'+i+'" class="mesa-item" onclick="preSelecionarMesa('+i+', this)">'+i+'</div>';
        }
         $('.panel-mesas').append(html)
    };

    $.ajax({
      url: '/max_mesas/' + numero_maximo_mesas, // Adicionamos o ID à URL da API
      method: 'POST',
      dataType: 'json',
      success: function(data) {
        // O código a seguir é executado se a requisição for bem-sucedida
        console.log('Dados recebidos:');
        console.log(data);
      },
      error: function(xhr, status, error) {
        // O código a seguir é executado se a requisição falhar
        console.log('Erro ao fazer a requisição:');
        console.log(error);
      }
    });


};

function preSelecionarMesa(numero_mesa_selecionada,_this){
     lista_mesas = []
    if (_this.classList.contains('active')) {
        _this.classList.remove('active');
    } else {
        _this.classList.add('active');
    }
     document.querySelectorAll('.mesa-item.active').forEach(i=> {
			lista_mesas.push(numero_mesa_selecionada)
		})
    $("#numero_mesa").val(lista_mesas);
    $('#add_mesa').prop("disabled", false);
}

$(document).ready(function() {
    createMesaInPanel($("#max_mesas").val())
});



const exampleModal = document.getElementById('exampleModal');
exampleModal.addEventListener('show.bs.modal', event => {
  const button = event.relatedTarget;
  const mesa = button.getAttribute('data-bs-mesa');
  const _status = button.getAttribute('data-bs-status');
  const _id = button.getAttribute('data-bs-id');
  const modalTitle = exampleModal.querySelector('.modal-title');

  if (_status === 'True') {
    $('#edit_mesa').hide();
    $('.remover').hide();
    $('#comanda').show();
    $.ajax({
      url: '/comanda_info',
      method: 'GET',
      data: {_idMesa:_id},
      success: function(response) {
        console.log(response);
        if (!response.erro) {
          $('#nome_cliente').html(response.nome_cliente);
          $('#numero_comanda').html(response._idComanda);
          $('#date_comanda').html(response.hora_abertura);
          $('#CPF_cliente').html(response.CPF);
          $('#total-subtotal').html(response.total);

          response.pedidos.forEach(function(pedido) {
            var html = '<tr>' +
                '<td class="px-0">' + pedido.nome_produto + '</td>' +
                '<td class="text-end px-0">' + pedido.quantidade + '</td>' +
                '<td class="valor text-end px-0">' + pedido.valor + '</td>' +
                '</tr>';
            $('#tabela-pedidos').append(html);
          });

          if(response.is_admin_comanda){
            $('#comanda_admin').show();
            $('#_idComanda_view').val(response._idComanda);
            $('#_idMesa_view').val(response._idMesa);
          }
          else{
           $('#comanda_admin').hide();
           }

        }
        else {
          actionModalComComanda();
        }
      },
      error: function(error) {
        // adicione aqui o código para lidar com o erro da requisição AJAX
      }
    });
  } else {
    actionModalComComanda();
  }

  function actionModalComComanda() {
    $('#edit_mesa').show();
    $('.remover').show();
    $('#comanda').hide();

    const status = exampleModal.querySelector('#status_mesa');
    modalTitle.textContent = `Gerenciar mesa ${mesa}`;
    $("#mesa_delete").val(mesa);
    $("#mesa_delete_status").val(mesa);
    $("#mesa_delete_id").val(_id);
    $("#_idMesa").val(_id);

    if (_status === "True") {
      status.checked = true;
      $("#ativo").val(true);
    } else {
      status.checked = false;
      $("#ativo").val(false);
    }
  }
});
