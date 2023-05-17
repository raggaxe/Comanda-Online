  function previewImagem() {
      var preview = document.querySelector('#preview');
      var file    = document.querySelector('#imagem').files[0];
      var reader  = new FileReader();

      reader.onloadend = function () {
        preview.src = reader.result;
        $('#preview').show()
      }

      if (file) {
        reader.readAsDataURL(file);
      } else {
        preview.src = "";
      }
    }

$('.cnpj').inputmask("99.999.999/9999-99", {
    placeholder: "*",
    clearIncomplete: true,
    removeMaskOnSubmit: true,
    keepStatic: true
});
// Seleciona o input do telefone
var telefoneInput = $('#telefone_comercial');

// Adiciona a máscara de telefone
telefoneInput.inputmask("+55 (99) 9999-9999[9]", {
  placeholder: "_",
  clearIncomplete: true,
  removeMaskOnSubmit: true
});
// Adiciona evento de input no input do telefone
telefoneInput.on('input', function() {
   var telefone = $(this).val().replace('_',"");
  var telefoneCompleto = telefone.length > 17;  // Telefone completo tem 11 dígitos
  // Adiciona ou remove a classe 'is-valid' ou 'is-invalid' baseado na validação do telefone
  if (telefoneCompleto) {
    telefoneInput.removeClass('is-invalid').addClass('is-valid');
ValidadorStep1();
  } else {
    telefoneInput.removeClass('is-valid').addClass('is-invalid');
  }
  ValidadorStep1()
});


$('.cep').inputmask("99999-999");

$(document).ready(function() {

  $('.card-plan').on('click', function() {
        $('.selected-card').removeClass('selected-card');
        $(this).addClass('selected-card');
  });


  var maxLength = 200;
  $('textarea#detalhes_comercial').attr('maxlength', maxLength);
  $('textarea#detalhes_comercial').after('<p class="form-text" id="caracteres_restantes" style="text-align: right;">' + maxLength + '/200</p>');
  $('textarea#detalhes_comercial').on('input', function() {
    var length = $(this).val().length;
    var remaining = maxLength - length;
    $('#caracteres_restantes').text(remaining + '/200');

  });
});



function ValidadorStep1(){
    var is_valid = document.querySelectorAll('.step-2 .is-valid')
    if( is_valid.length === 6 ){
        $('#btn-step-2').prop('disabled', false);
    }
    else{
        $('#btn-step-2').prop('disabled', true);
    }

}

var map;

function initMap() {
  var geocoder = new google.maps.Geocoder();
  map = new google.maps.Map(document.getElementById('map'), {
    zoom: 15,
    center: { lat: -23.5505, lng: -46.6333 } // São Paulo, Brasil
  });

  // You can add a marker to the map with a generic location
  var marker = new google.maps.Marker({
    position: { lat: -23.5505, lng: -46.6333 },
    map: map,
    title: 'São Paulo, Brasil'
  });
}

function updateGeolocation() {
  var geocoder = new google.maps.Geocoder();
  var address = $('input#endereco').val() + ', ' + $('input#bairro').val() + ', ' + $('input#cidade').val() + ', ' + $('input#estado').val();

  geocoder.geocode({ 'address': address }, function(results, status) {

    if (status === 'OK') {
      map.setCenter(results[0].geometry.location);
      var marker = new google.maps.Marker({
        map: map,
        position: results[0].geometry.location
      });
    } else {
      alert('Erro ao geocodificar o endereço: ' + status);
    }
  });
}

$(document).ready(function() {
  var cepInput = $('.cep');
  cepInput.inputmask("99999-999");
  var cnpjInput = $('#cnpj')
  var nomeComercialInput = $('#nome_comercial');

    var nomeComercial = $('#nome_comercial');

nomeComercial.on('keypress', function(e) {
  if (nomeComercial.val().length >= 30 && e.keyCode !== 8 && e.keyCode !== 46) {
    e.preventDefault();
  }
});
nomeComercialInput.on('input', function() {
  var nomeComercial = $(this).val();

  if (nomeComercial.length >= 1 && nomeComercial.length <= 30) {
    $(this).addClass('is-valid').removeClass('is-invalid');
    ValidadorStep1()
  } else {
    $(this).removeClass('is-valid').addClass('is-invalid');
  }
  ValidadorStep1()
});

  // Initialize map on page load
  initMap();
  cepInput.on('input', function() {
    var cep = $(this).val().replace('-', '');
    var url = 'https://viacep.com.br/ws/' + cep + '/json/';
    if (cep.replace('_', '').length == 8){
    $.getJSON(url, function(data) {
      if (!("erro" in data)) {
        $('input#endereco').val(data.logradouro);
        $('input#bairro').val(data.bairro);
        $('input#cidade').val(data.localidade);
        $('input#estado').val(data.uf);
        $('#btn-step-3').prop('disabled', false);
        cepIsValid()
        // Update geolocation after searching for the CEP
        updateGeolocation();
      } else {

        cepIsInValid()
      }
    });
    }
    else{
    $('#btn-step-3').prop('disabled', true);
        $('input#CEP').removeClass('is-invalid').removeClass('is-valid');

        $('input#endereco').removeClass('is-invalid').removeClass('is-valid');
        $('input#endereco').val('');
        $('input#bairro').removeClass('is-invalid').removeClass('is-valid');
        $('input#bairro').val('');
        $('input#cidade').removeClass('is-invalid').removeClass('is-valid');
        $('input#cidade').val('');
        $('input#estado').removeClass('is-invalid').removeClass('is-valid');
        $('input#estado').val('');
    }

  });

  cnpjInput.on('input', function() {
  var cnpj = $(this).val().replace(/[^\d]/g, '');

  if (cnpj.length == 14) {
    $.ajax({
      url: 'https://www.receitaws.com.br/v1/cnpj/' + cnpj,
      type: 'GET',
      dataType: 'jsonp',
      success: function(data) {
        if (data.situacao == "ATIVA"){
          $('input#razao_social').val(data.nome);
          $('input#tipo_empresa').val(data.natureza_juridica);
          cnpjInput.removeClass('is-invalid').addClass('is-valid');
          $('input#razao_social').removeClass('is-invalid').addClass('is-valid');
          $('input#tipo_empresa').removeClass('is-invalid').addClass('is-valid');

            $('#cnpj_banco').val(cnpj)
            $('#cnpj_banco').removeClass('is-invalid').addClass('is-valid');
            $('#razao_social_banco').val(data.nome)
            $('#razao_social_banco').removeClass('is-invalid').addClass('is-valid');
            ValidadorStep1()
        } else {
          cnpjInput.removeClass('is-valid').addClass('is-invalid');
          $('input#razao_social').removeClass('is-valid').addClass('is-invalid');
        }
      },
      error: function() {
        cnpjInput.removeClass('is-valid').addClass('is-invalid');
        $('input#razao_social').removeClass('is-valid').addClass('is-invalid');
        $('input#tipo_empresa').removeClass('is-valid').addClass('is-invalid');
      }
    });
  } else {
    $('input#razao_social').val('');
    $('input#tipo_empresa').val('');
    cnpjInput.removeClass('is-valid is-invalid');
    $('input#razao_social').removeClass('is-valid is-invalid');
    $('input#tipo_empresa').removeClass('is-valid is-invalid');
//    $('#btn-step-2').prop('disabled', true);
  }

});


});


function cepIsValid(){
        $('input#CEP').addClass('is-valid').removeClass('is-invalid');
        $('input#endereco').addClass('is-valid').removeClass('is-invalid');
        $('input#bairro').addClass('is-valid').removeClass('is-invalid');
        $('input#cidade').addClass('is-valid').removeClass('is-invalid');
        $('input#estado').addClass('is-valid').removeClass('is-invalid');
}
function cepIsInValid(){
        $('input#CEP').addClass('is-invalid').removeClass('is-valid');

        $('input#endereco').addClass('is-invalid').removeClass('is-valid');
        $('input#endereco').val('');
        $('input#bairro').addClass('is-invalid').removeClass('is-valid');
        $('input#bairro').val('');
        $('input#cidade').addClass('is-invalid').removeClass('is-valid');
        $('input#cidade').val('');
        $('input#estado').addClass('is-invalid').removeClass('is-valid');
        $('input#estado').val('');
}
function validateCNPJAndRazaoSocial(cnpj, razaoSocial) {
  var isValid = true;

  // Verifica se o CNPJ e a Razão Social estão preenchidos
  if (!cnpj) {
    $('input#cnpj').addClass('is-invalid');
    isValid = false;
  } else {
    $('input#cnpj').removeClass('is-invalid').addClass('is-valid');
  }

  if (!razaoSocial) {
    $('input#razao_social').addClass('is-invalid');
    isValid = false;
  } else {
    $('input#razao_social').removeClass('is-invalid').addClass('is-valid');
  }

  return isValid;
}



var cpf_responsavel = $('#cpf_responsavel')

cpf_responsavel.inputmask("999.999.999-99", {
    placeholder: "*",
    clearIncomplete: true,
    removeMaskOnSubmit: true,
    keepStatic: true
});


cpf_responsavel.on('input', function() {
  var _cpf_responsavel = $(this).val().replace(/[^\d]/g, '');;
  if (_cpf_responsavel.length >= 11 ) {
    $(this).addClass('is-valid').removeClass('is-invalid');
                $('#cpf_banco').val(this.value)
            $('#cpf_banco').removeClass('is-invalid').addClass('is-valid');
    ValidadorStep4()
  } else {
    $(this).removeClass('is-valid').addClass('is-invalid');
  }

});



var nome_completo = $('#nome_completo');
nome_completo.on('keypress', function(e) {
  if (nome_completo.val().length >= 30 && e.keyCode !== 8 && e.keyCode !== 46) {
    e.preventDefault();
  }
});
nome_completo.on('input', function() {
  var _nome_completo = $(this).val();
  if (_nome_completo.length >= 1 && _nome_completo.length <= 30) {
    $(this).addClass('is-valid').removeClass('is-invalid');
    $('#nome_banco').val(this.value)
            $('#nome_banco').removeClass('is-invalid').addClass('is-valid');
             ValidadorStep4()
  } else {
    $(this).removeClass('is-valid').addClass('is-invalid');
  }

});
function ValidadorStep4(){
    var is_valid = document.querySelectorAll('.step-4 .is-valid')
    if( is_valid.length === 2 ){
        $('#btn-step-4').prop('disabled', false);
    }
    else{
        $('#btn-step-4').prop('disabled', true);
    }
}


 // Máscara para o campo de Banco
  $('#banco').inputmask('999[9]', { placeholder: '' });

  // Máscara para o campo de Agência
  $('#agencia').inputmask('9999-9', { placeholder: '' });

  // Define uma máscara genérica para o campo de Conta
  $('#conta').inputmask('9999999', { placeholder: '' });

      // Função para verificar o tipo de conta e ajustar a máscara
      function ajustarMascaraConta(tipoConta) {
        switch (tipoConta) {
          case 'poupanca':
            $('#conta').inputmask('99999999-9', { placeholder: '' });
            break;
          case 'investimento':
            $('#conta').inputmask('99.999-9', { placeholder: '' });
            break;
          case 'corrente':
             // Se o tipo de conta não for reconhecido, utiliza a máscara genérica
            $('#conta').inputmask('9999999', { placeholder: '' });
            break;
          default:

            break;
        }
        $('#conta').val('')
        $('#conta').prop('disabled', false);
        $('#conta').removeClass('is-valid').removeClass('is-invalid');

        $('#digito').val('')
        $('#digito').prop('disabled', false);
        $('#digito').removeClass('is-valid').removeClass('is-invalid');

        $('#conta').on('input', function() {
          var _conta = $(this).val();

          switch (tipoConta) {
            case 'poupanca':
              if (_conta.length === 10) {
                $(this).addClass('is-valid').removeClass('is-invalid');
                ValidadorTerminar()
              } else {
                $(this).removeClass('is-valid').addClass('is-invalid');
              }
              break;
            case 'investimento':
              if (_conta.length === 8) {
                $(this).addClass('is-valid').removeClass('is-invalid');
              ValidadorTerminar()
                } else {
                $(this).removeClass('is-valid').addClass('is-invalid');
              }
              break;
            case 'corrente':
              if (_conta.length === 7) {
                $(this).addClass('is-valid').removeClass('is-invalid');
             ValidadorTerminar()
              } else {
                $(this).removeClass('is-valid').addClass('is-invalid');
              }
              break;
            default:

              break;
          }
        });




      }

      // Exemplo de uso da função ajustarMascaraConta
      $('select[name="tipo_conta"]').change(function() {
        var tipoConta = $(this).val();
        ajustarMascaraConta(tipoConta);
        $(this).addClass('is-valid').removeClass('is-invalid');
        ValidadorTerminar()
      });



  // Máscara para o campo de Dígito
  $('#digito').inputmask('9', { placeholder: 'X' });


$('#agencia').on('input', function() {
  var _agencia = $(this).val();
  var regex = /^\d{4}-\d{1}$/; // Expressão regular que representa o formato 9999-9
  if (regex.test(_agencia)) {
    $(this).addClass('is-valid').removeClass('is-invalid');
    ValidadorTerminar()

  } else {
    $(this).removeClass('is-valid').addClass('is-invalid');
  }
});

$('#digito').on('input', function() {
  var _digito = $(this).val();
  if (_digito.length > 0) {
    $(this).addClass('is-valid').removeClass('is-invalid');
    ValidadorTerminar()
  } else {
    $(this).removeClass('is-valid').addClass('is-invalid');
  }
});
$(document).ready(function() {
  var listaDeBancos = [];

  // Carrega a lista de bancos do arquivo JSON
  $.getJSON('/static/data/listaDeBancos.json', function(data) {
    listaDeBancos = data;

    // Cria as opções do select a partir da lista de bancos
    var options = '';
    $.each(listaDeBancos, function(index, banco) {
      options += '<option value="' + banco.COMPE + '">' + banco.COMPE + ' - ' + banco.LongName + '</option>';
    });
    var x= '<option disabled selected>Selecione um banco...</option>'+options
    $('#banco').html(x);
  });
  // Adiciona a classe .is-valid na select quando o valor for alterado
  $('#banco').on('change', function() {
    $(this).addClass('is-valid');
    ValidadorTerminar()
  });
});


function ValidadorTerminar(){
    var is_valid = document.querySelectorAll('.step-6 .is-valid')

    if( is_valid.length === 9 ){
        $('#btn-terminar').prop('disabled', false);
    }
    else{
        $('#btn-terminar').prop('disabled', true);
    }
}





