$(document).ready(function() {
    $('#playlist-selector').change(function() {
        $('#searchform').submit();
    });
    $('.queueAdd').on("click", function() {
        var token = $("#csrf").val();
        var sid = $(this).data("sid");
        $.ajax({
            type: 'POST',
            url: '/api/queueAdd',
            data: { "csrf_token" : token, "songid" : sid },
            success: function() {
                alert("Song added successfully");
            }
        });
    });
});
