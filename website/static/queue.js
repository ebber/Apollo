$(document).ready(function() {
    $('#songtable tbody').sortable({
        helper: myHelper,
        stop: updateQueue
    }).disableSelection();

    function myHelper(e, tr) {
        var orig = tr.children();
        var helper = tr.clone();
        helper.children().each(function(index) {
            $(this).width(orig.eq(index).width())
        });
        return helper;
    }

    function updateQueue(e, ui) {
        var items = $("#songtable tr");
        var ids = [];
        var token = $("#csrf").val();

        items.each(function(intIndex) {
            ids.push($(this).data("sid"));
        });

        //Remove blank info from title row
        ids = ids.slice(1);

        $.ajax({
            type: "POST",
            url: "/api/queueUpdate",
            data: {"csrf_token": token, "queue[]": ids}
        });

        $('td.songindex', ui.item.parent()).each(function(i) {
            $(this).html(i+1);
        });
    }
});
