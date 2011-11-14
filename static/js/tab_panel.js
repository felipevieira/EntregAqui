
// Global vars to hold the object in the panel.
tabPanelArray = new Array(3);
tabMenuArray = new Array(3);
cardsArray = new Array(6);
currentMenuIndex = 0;

/**
 * This MUST be called on page load to fill up the shared global values.
 * Having the panes object accessible by index makes things easier.
 * This is also a good place to display the first page.
 */
function bodyOnLoad()
   {
   tabPanelArray[0] = getItemObj('tabPane0');
   tabPanelArray[1] = getItemObj('tabPane1');
   tabPanelArray[2] = getItemObj('tabPane2');

   tabMenuArray[0] = getItemObj('tabMenu0');
   tabMenuArray[1] = getItemObj('tabMenu1');
   tabMenuArray[2] = getItemObj('tabMenu2');

   cardsArray[0] = 'cash';
   cardsArray[1] = 'visa';
   cardsArray[2] = 'electron';
   cardsArray[3] = 'master';
   cardsArray[4] = 'hiper';
   cardsArray[5] = 'american';
   
   raisePanel ( currentMenuIndex );
   }

/**
 * Utility function just to show an error if I try to get non existent objects
 */
function getItemObj ( itemId )
   {
   obj = document.getElementById(itemId);

   if ( obj == null ) alert('Script Error: id='+itemId+' does not exist');

   return obj;
   }


/**
 * raising a panel means setting all the other panels to a lower level
 * and setting the raided panel to a higher level
 * note that also the size must be set correctly !
 * to activate a menu i switch the class between active and not active.
 */
function raisePanel ( panelIndex )
   {
	var botaoAvancar = getItemObj('botao_avancar');
    if (panelIndex == 2) {
    	botaoAvancar.value = "Finalizar";
    }
    else {
    	botaoAvancar.value = "Prosseguir";
    }
   for (index=0; index<3; index++ )
      {
      // the panel with the index == wantedIndex gets raised.
      if (index == panelIndex )
         {
         raiseObject (tabPanelArray[index], 4);
         tabMenuArray[index].className = 'tabMenuActive';
         tabMenuArray[index].style.background = 'url("/static/images/bt-aba-selected.png")';
         
         }
      else
         {
         raiseObject (tabPanelArray[index], 2);
         tabMenuArray[index].className = 'tabMenu';
         tabMenuArray[index].style.background = 'url("/static/images/bt-aba.png")';
         }
      }

   currentMenuIndex=panelIndex;

   return true;
   }

/**
 * When I raise a panel I may as well check for the correct size and fix it.
 * it is a bit of doubling work, but it does not happens often !
 */
function raiseObject ( target, level )
   {
   /* the number of pixels we shave to the outside filler to fit everything in
    * this value depends on the border set for the filler div and possible padding
    * it is best to experiment a bit with it.
    */
   safeMargin = 6;

   // the size of the panels depends on the size of the tabFiller
   obj = getItemObj('tabFiller');

   newWidth = obj.offsetWidth - safeMargin;
   if ( newWidth < safeMargin ) newWidth = safeMargin;
   target.style.width = newWidth+'px';

   newHeight =obj.offsetHeight - safeMargin;
   if ( newHeight < safeMargin ) newHeight = safeMargin;
   target.style.height = newHeight+'px';

   // setting the z-index last should optimize possible resize.
   target.style.zIndex=level;
   }

function voltar() 
{
	if (currentMenuIndex == 0) {
		alert('voltar pro cardapio!!!');
		return
	}
	currentMenuIndex = (currentMenuIndex - 1) % 3;
	if (currentMenuIndex < 0) {
		currentMenuIndex += 3;
	}
	raisePanel(currentMenuIndex);
}

function avancar()
{
	if (currentMenuIndex == 2) {
		alert('Finalizar Compra!!!');
		return
	}
	currentMenuIndex = (currentMenuIndex + 1) % 3;
	raisePanel(currentMenuIndex);
}

function selecionaCartao(cartao)
{
	var cartaoEscolhido = '#' + cartao + '_button_pagamento';
	$(cartaoEscolhido).attr('escolhido', 'true');
	getItemObj(cartao + '_button_pagamento').style.background = 'url("/static/images/Cards/card-' + cartao+'-selected.png")';
	for (i = 0; i < 6; i++) {
		if (cartao != cardsArray[i]) {
			var cartaoAtual =  '#' + cardsArray[i] + '_button_pagamento';
			$(cartaoAtual).attr('escolhido', 'false');
			getItemObj(cardsArray[i] + '_button_pagamento').style.background = 'url("/static/images/Cards/card-' + cardsArray[i]+'-unselected.png")';
		}
	}
}
