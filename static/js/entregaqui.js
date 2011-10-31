$(document).ready(function(){
	
	pesquisaTemConteudo = false;
	
	$(".botao_enviar_parceiro").click(function(){		
		var nomeEmpresa = document.getElementById("campo_empresa").value;
		var emailEmpresa = document.getElementById("campo_email").value;
		var contatoEmpresa = document.getElementById("campo_contato").value;
		
		if(nomeEmpresa == "" || emailEmpresa == "" || contatoEmpresa == "") {
			alert("Por favor, preencha todos os dados para completar sua solicitacao");
			return;
		}
		
		alert("Solicitacao enviada com sucesso!")
		/* TODO Salvar no banco de dados */
		
	});
	
	$(".botao_informar_cidade").click(function(){		
		var nomeUsuario = document.getElementById("campo_nome_usuario").value;
		var emailUsuario = document.getElementById("campo_email_usuario").value;
		var cidade = document.getElementById("campo_cidade").value;
		
		if(nomeUsuario == "" || emailUsuario == "" || cidade == "") {
			alert("Por favor, preencha todos os dados para completar sua solicitacao");
			return;
		}
		
		alert("Solicitacao enviada com sucesso!")
		/* TODO Salvar no banco de dados */
		
	});
	
	$(".link_cadastrar").click(function(){		
		goToUrl("\cadastro")
		
	});
	
	$(".botao_login").click(function(){		
		var nomeUsuario = document.getElementById("campo_username_login").value;
		var senha= document.getElementById("campo_senha_login").value;
		
		if(nomeUsuario == "" || senha == "") {
			alert("Por favor, preencha todos os dados para completar sua solicitacao");
			return;
		}
		
		alert("Login a ser validado");
		/* TODO Checar autenticidade no banco */
		
	});
	
	$(".input_pesquisar").mousedown(function(){
		if (!pesquisaTemConteudo) {
			$(".input_pesquisar").attr('value', "");
		}
	});
	
	$(".input_pesquisar").blur(function(){
		if ($(".input_pesquisar").attr('value') != "") {
			pesquisaTemConteudo = true;
		}
		
		else {
			pesquisaTemConteudo = false;
			$(".input_pesquisar").attr('value',"Pesquisar");
		}
	});
	
	$(".mais_cidades").click(function(){
		$(".table_cidades").fadeOut();
		$(".descricao_sistema").fadeOut();
		sleep(400);
		$(".table_cidades_expandida").fadeIn();
	});
	
	$(".menos_cidades").click(function(){
		$(".table_cidades_expandida").fadeOut();
		sleep(400);
		$(".table_cidades").fadeIn();
		$(".descricao_sistema").fadeIn();
	});

});

function goToUrl(destino) {	
	window.location = destino;
}
function go() {
	goToUrl(document.getElementById("cidades").value);
}

function sleep(milliseconds) {
  var start = new Date().getTime();
  for (var i = 0; i < 1e7; i++) {
    if ((new Date().getTime() - start) > milliseconds){
      break;
    }
  }
}

