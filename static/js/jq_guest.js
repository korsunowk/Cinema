/**
 * Created by 1 on 17.05.2016.
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
    var guest_id;
    $(".admin_but").click(function(){

        $("#hid_but:hidden").show();
        $("#hid_area:hidden").show();
        $("body").scrollTop($(document).height());
        guest_id = $(this).attr("data-target").split(',');

        $("#admin_comment").html("").append(guest_id[1]+', ');
    });

    $('.btn1').click(guest_otziv);
    function guest_otziv() {
        $.ajax({
            type: "POST",
            url: "/guest/",
            data:{
                csrfmiddlewaretoken : csrftoken,
                name : $("#name").val(),
                email : $("#email").val(),
                comment: $("#comment").val(),
                admin: "false",
            },
            dataType: "html",
            cache: false,
            success: function(){

            }
        });
        e.preventDefault();
    }

    $('.btn2').click(admin_otziv);
    function admin_otziv() {
        $.ajax({
            type: "POST",
            url: "/guest/",
            data:{
                csrfmiddlewaretoken : csrftoken,
                comment: $("#admin_comment").val(),
                guest_id : guest_id[0],
                admin: "true",
            },
            dataType: "html",
            cache: false,
            success: function(){

            }
        });
        e.preventDefault();
    }
});