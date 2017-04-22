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
            data: {"csrf_token": token, "songid": sid},
            success: function(data) {
                data = JSON.parse(data);
                if(data['type'] == 'success')
                    window.location.href="/queue";
                else
                    alert('Error: ' + data['error']);
            }
        });
    });
    $('.playlistAdd').on('change', function() {
        var token = $("#csrf").val();
        var sid = $(this).data("sid");
        var pid = $(this).val();
        $.ajax({
            type: "POST",
            url: 'api/playlistAdd',
            data: {"csrf_token": token, "songid": sid, "playlistid": pid},
            success: function() {
                alert('Added to playlist successfully');
            }
        });
    });
    $('.playlistRemove').on('click', function() {
        var token = $("#csrf").val();
        var sid = $(this).data("sid");
        var pid = $(this).data("pid");
        $.ajax({
            type: "POST",
            url: 'api/playlistRemove',
            data: {"csrf_token": token, "songid": sid, "playlistid": pid},
            success: function() {
                location.reload();
            }
        });
    });
    $('.order-header').on("click", function() {
        var val = "sort=" + $(this).html().toLowerCase();

        var sort = new RegExp("[?&]" + val)
        var reverse = new RegExp("[?&]reversed=true");
        var anysort = new RegExp("[?&]sort=[a-zA-Z]*")
        var endurl = '';

        if(window.location.href.match(sort)) {
            if(window.location.href.match(reverse))
                var newurl = window.location.href.replace(reverse, ''); 
            else
            {
                var newurl = window.location.href;
                endurl = '&reversed=true'; 
            }
        }
        else {
            var newurl = window.location.href.replace(reverse, '');
        }

        newurl = newurl.replace(anysort, '');
        var separator = newurl.indexOf('?') !== -1 ? "&" : "?";
        window.location.href = newurl + separator + val + endurl;
    });
});
