$(document).ready(function(){
$('a.poplight[href^=#]').click(function() {                 
        var popID = $(this).attr('rel'); //Get Popup Name
        var popURL = $(this).attr('href'); //Get Popup href to define size
        var source = $(this).attr('source');
        
        //Pull Query & Variables from href URL
        var query= popURL.split('?');
        var dim= query[1].split('&');                   

        var popWidth = dim[0].split('=')[1];                    
        var popHeight = dim[1].split('=')[1];   
                            
        //Fade in the Popup and add close button
        console.log("chegou aqui");
        $('#' + popID).fadeIn();
        $('#' + popID).css({ 'width': Number( popWidth ), 'height' : Number( popHeight ) });
        $('#' + popID).load(source, function() {
            $('#' + popID).prepend('<a href="#" class="close"><img src="/static/images/close_pop.png" class="btn_close" title="Close Window" alt="Close" /></a>');
        });
        console.log("passou");
        //Define margin for center alignment (vertical   horizontal) - we add 80px to the height/width to accomodate for the padding  and border width defined in the css
        var popMargTop = ($('#' + popID).height() + 80) / 2;
        var popMargLeft = ($('#' + popID).width() + 80) / 2;
    
        //Apply Margin to Popup
        $('#' + popID).css({
            'margin-top' : -popMargTop,
            'margin-left' : -popMargLeft
        });
    
        //Fade in Background
        $('body').append('<div id="fade"></div>'); //Add the fade layer to bottom of the body tag.
        $('#fade').css({'filter' : 'alpha(opacity=80)'}).fadeIn(); //Fade in the fade layer - .css({'filter' : 'alpha(opacity=80)'}) is used to fix the IE Bug on fading transparencies 
    
        return false;
    });
    
    //Close Popups and Fade Layer
    $('a.close, #fade').live('click', function() { //When clicking on the close or fade layer...
        $('#fade , .popup_block').fadeOut(function() {
            $('#fade, a.close').remove();  //fade them both out
        });
        return false;
    });
});