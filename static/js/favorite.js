$(document).ready(function () {
    $(".favorite_form").submit(function (event) {
        event.preventDefault();
        data = $(this).serialize();
        form = $(this);

        $.post("/favorite", data, function (response) {
            if (response.status === 'ok') {
                x = "<div><button class='btn btn-success active save_button' disabled><i class='fas fa-check'></i> Sauvegardé</button></div>";
                form.after(x);
                form.remove();
            }
        });
    })
});
