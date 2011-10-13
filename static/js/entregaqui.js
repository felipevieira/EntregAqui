$(document).ready(function(){
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

});

function go() {
	window.location=document.getElementById("cidades").value;
}

