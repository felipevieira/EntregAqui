$(document).ready(function() {

            $(".signin").click(function(e) {
                e.preventDefault();
                $("fieldset#signin_menu").load("/login/");
                $("fieldset#signin_menu").toggle();
                $(".signin").toggleClass("menu-open");
            });

            $("fieldset#signin_menu").mouseup(function() {
                return false
            });
            $(document).mouseup(function(e) {
                if($(e.target).parent("a.signin").length==0) {
                    $(".signin").removeClass("menu-open");
                    $("fieldset#signin_menu").hide();
                }
            });  
            
            $(".logout").click(function(e) {
                e.preventDefault();
                $("fieldset#logout_menu").load("/menu_usuario/");
                $("fieldset#logout_menu").toggle();
                $(".logout").toggleClass("menu-open");
            });

            $("fieldset#logout_menu").mouseup(function() {
                return false
            });
            $(document).mouseup(function(e) {
                if($(e.target).parent("a.logout").length==0) {
                    $(".logout").removeClass("menu-open");
                    $("fieldset#logout_menu").hide();
                }
            });                 

        });