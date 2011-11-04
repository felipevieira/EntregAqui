$(document).ready(function(){
	
	pesquisaTemConteudo = false;
	mensagemFCTemConteudo = false;
	comboCidadeExpandida = false;
	
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
	
	$("#campo_texto_fc").mousedown(function(){
		if (!mensagemFCTemConteudo) {
			$("#campo_texto_fc").val("");
		}
	});
	
	$("#campo_texto_fc").blur(function(){
		if ($("#campo_texto_fc").val() != "") {
			mensagemFCTemConteudo = true;
		}
		
		else {
			mensagemFCTemConteudo = false;
			$("#campo_texto_fc").val("Digite sua mensagem aqui.");
		}
	});
	
	$(".mais_cidades").click(function(){
		$(".table_cidades").hide();
		$(".descricao_sistema").fadeOut();
		$(".table_cidades_expandida").fadeIn();
	});
	
	$(".menos_cidades").click(function(){
		$(".table_cidades_expandida").hide();
		$(".table_cidades").fadeIn();
		$(".descricao_sistema").fadeIn();
	});
	
	$("#demo").click(function(){
		if(!comboCidadeExpandida) {
			comboCidadeExpandida = true;
			$(".options").fadeIn();
		}
		
		else {
			comboCidadeExpandida = false;
			$(".options").fadeOut();
		}
	});
	
	$(".opcao_cidade").click(function(event){
		alert(event.target.id)
		document.getElementById("cidade_selecionada").innerHTML = "peni;";
	});
});

$("document").ready(function(){    

    $("document").ready(function(){             
        $("#demo").jDropDown({selected: 0, callback: callback});
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

function enviar_sugestao() {
	var nome = $("#campo_nome_fc").attr("value");
	var email = $("#campo_email_fc").attr("value");
	var assunto = $("#campo_assunto_fc").attr("value");
	var telefone = $("#campo_telefone_fc").attr("value");
	var texto = $("#campo_texto_fc").val();
	
	console.log('toaqui');
	var html = '';
	html += '<div id="loading_fc_message">'
	html += '<p> Por favor, aguarde... </p> <br> '
	html += '<img id="loading_img_fc" src="/static/images/loading.gif" width=64 height=64/>';
	html += '</div>'
	$("#inner_form_fc").html(html);
	console.log('toaqui2');
	$.ajax({
		url: "/obrigado_fale_conosco/",
		type: "POST",
		data: {'nome' : nome,
				'email' : email,
				'assunto' : assunto,
				'telefone' : telefone,
				'texto' : texto,
				'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()},
		success: function(data) {
			$("#popup_source").html(data);
			$("#popup_source").prepend('<a href="#" class="close"><img src="/static/images/close_pop2.png" class="btn_close" title="Close Window" alt="Close" /></a>');
		},
		error: function(xhr) {
			console.log("status: " + xhr.status);
		}
	});
}

function callback(index, val){
    $("#demo-data p").text("index: " + index + ", value: " + val);
}

