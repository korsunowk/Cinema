/**
 * Created by 1 on 16.05.2016.
 */
$(document).ready(function(){
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    $('#button').click(otziv);
    function otziv() {

        $.ajax({
            type: "POST",
            url: "/otziv/"+$("#hid1").val()+'/',
            data:{
                csrfmiddlewaretoken : csrftoken,
                name : $("#name").val(),
                email : $("#email").val(),
                comment: $("#comment").val(),

            },
            dataType: "html",
            cache: false,
            success: function(data){
                if (data == 'ok'){

                }
            }
        });
    }
});