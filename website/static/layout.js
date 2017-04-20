$(document).ready(function () {
    $('#logout-btn').click(function(e) {
        e.preventDefault();
        var token = $('#csrf').val();
        $.ajax({
            type: 'POST',
            url: '/api/logout', 
            data: {"csrf_token" : token},
            success: function() {
                window.location.href = $('#logout-btn').attr('href');
            }
        });
    });
});
