const _email = $('#email')

_email.on('input', function() {
  var email = $(this).val();
  var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (emailRegex.test(email)) {
    // Se o endereço de e-mail é válido, faça a solicitação AJAX
    $.ajax({
      url: '/check_email',
      method: 'POST',
      data: {email: email},
      success: function(data) {
      console.log(data)
        if (data.error) {
          // Adicione uma classe CSS ao elemento de entrada de e-mail
          _email.addClass('is-invalid');
          _email.removeClass('is-valid');
        } else {
          // Remova a classe CSS do elemento de entrada de e-mail se não houver erros
          _email.removeClass('is-invalid');
           _email.addClass('is-valid');
        }
      },
      error: function(xhr, status, error) {
        // lógica de manipulação de resposta de erro
      }
    });
  } else {
    // Se o endereço de e-mail não é válido, exiba uma mensagem de erro ou execute outra lógica de validação
    console.log('Endereço de e-mail inválido');
  }
});


$(document).ready(function() {
  $('#passsword').on('keyup', function() {
    var password = $(this).val();

    // Verifica se a senha atende aos critérios de segurança
    var regex = /^(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,})/;
    if (regex.test(password)) {
      $(this).removeClass('is-invalid').addClass('is-valid');
    } else {
      $(this).removeClass('is-valid').addClass('is-invalid');
    }
  });

  $('#Rpassword').on('keyup', function() {
    var password = $('#passsword').val();
    var confirmPassword = $(this).val();

    // Verifica se as senhas são iguais
    if (password == confirmPassword) {
      $(this).removeClass('is-invalid').addClass('is-valid');
      $('#passsword').removeClass('is-invalid').addClass('is-valid');
      $('#password-feedback').text('');
    } else {
      $(this).removeClass('is-valid').addClass('is-invalid');
      $('#passsword').removeClass('is-valid').addClass('is-invalid');
      $('#password-feedback').text('As senhas não são iguais.');
    }
  });
});


function InserirUser() {
  var form = document.getElementById('cadastrar-user');
  var email = document.getElementById('email');
  var password = document.getElementById('passsword');
  var repeatPassword = document.getElementById('Rpassword');
  var passwordFeedback = document.getElementById('password-feedback');

  if (email.classList.contains('is-valid') &&
      password.classList.contains('is-valid') &&
      repeatPassword.classList.contains('is-valid')) {

    if (password.value !== repeatPassword.value) {
      passwordFeedback.style.display = 'block';
      repeatPassword.classList.remove('is-valid');
      repeatPassword.classList.add('is-invalid');
      return;
    } else {
      passwordFeedback.style.display = 'none';
      repeatPassword.classList.remove('is-invalid');
      repeatPassword.classList.add('is-valid');
    }

    var formData = new FormData(form);

    $.ajax({
      url: form.action,
      type: form.method,
      data: formData,
      success: function(response) {
        console.log(response);
        if(!response.erro){
            window.location.replace('/home');
        }
        else{
            $('#password-feedback').text(response.erro);
        }
      },
      error: function(xhr) {
        console.log(xhr.response);

      }
    });

  }
}
