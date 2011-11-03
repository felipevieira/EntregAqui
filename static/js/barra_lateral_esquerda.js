$(document).ready(function() {
    $(".categoria > ul").hide();
    $(".categoria").click(function(e) {
        $(this).find("li").slideToggle("fast");
        $(this).find("ul").show("fast");
    })
})