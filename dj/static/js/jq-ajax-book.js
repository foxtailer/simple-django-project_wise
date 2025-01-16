$(document).ready(function () {
    const csrfToken = $('meta[name="csrf-token"]').attr('content');


    $.ajaxSetup({
        headers: {
            'X-CSRFToken': csrfToken
        }
    });


    $(document).on("click", "#unlike_btn", function (e) {
        e.preventDefault();

        var wisdom_id = $(this).siblings("p").attr("id");
        var button = $(this);
        
        $.ajax({
            type: "PATCH",
            url: "",
            contentType: 'application/json',
            data: JSON.stringify({
                user_id: userId,
                post_id: wisdom_id,
            }),
            success: function (data) {
                button.closest("div").remove();
                console.log(data)
            },

            error: function (data) {
                console.log("Ошибка");
            },
        });
    });

});