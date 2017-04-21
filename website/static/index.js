$(document).ready(function() {
    $(document).ready(function() {
        var vol = $('#volumeval').html()
        setVolume(Math.floor(parseInt(vol)*360/100));
        var t = $('#timeval').html()
        setTime(Math.floor(parseInt(t)*360/100));
    });

    $("body").on("click", "#volume-control", function(e) {
        var token = $("#csrf").val();
        var radius = $('#volume-control').outerHeight()/2;
        var borderdistance = radius - 75;      
        var rect = document.getElementById('volume-control').getBoundingClientRect();
        var y = e.clientY - rect.top - 160;
        var x = e.clientX - rect.left - 160;
        var angle = Math.floor(Math.atan2(y, x) * 180/Math.PI);
        angle += 90;

        console.log(borderdistance);

        while(angle < 0)
            angle += 360;
        while(angle > 360)
            angle -= 360;

        if(Math.sqrt(x*x+y*y) > borderdistance) {
            $.ajax({
                type: 'POST',
                url: '/api/setVolume',
                data: {"csrf_token": token, "volume": Math.floor(angle*100/360)},
                success: function() {
                    setVolume(Math.floor(angle)); 
                }
            });
        }
    });

    $("body").on("click", "#time-control", function(e) {
        var token = $("#csrf").val();
        var radius = $('#time-control').outerHeight()/2;
        var borderdistance = radius - 75;      
        var rect = document.getElementById('time-control').getBoundingClientRect();
        var y = e.clientY - rect.top - 160;
        var x = e.clientX - rect.left - 160;
        var angle = Math.floor(Math.atan2(y, x) * 180/Math.PI);
        angle += 90;

        console.log(borderdistance);

        while(angle < 0)
            angle += 360;
        while(angle > 360)
            angle -= 360;

        if(Math.sqrt(x*x+y*y) > borderdistance) {
            $.ajax({
                type: 'POST',
                url: '/api/setTime',
                data: {"csrf_token": token, "time": Math.floor(angle*100/360)},
                success: function() {
                    setTime(Math.floor(angle)); 
                }
            });
        }
    });

    function setVolume(angle) {
        if(angle == 0)
            angle = 1;

        if(angle > 180) {
            firstangle = 180;
            secondangle = angle-180;
        }
        else {
            firstangle = angle;
            secondangle = 0;
        }

        $("#volume-left").css({'-webkit-transform': 'rotate(' + firstangle +'deg)',
                              '-moz-transform': 'rotate(' + firstangle +'deg)',
                              '-ms-transform': 'rotate(' + firstangle +'deg)',
                              'transform': 'rotate(' + firstangle +'deg)'});
        $("#volume-right").css({'-webkit-transform': 'rotate(' + secondangle +'deg)',
                              '-moz-transform': 'rotate(' + secondangle +'deg)',
                              '-ms-transform': 'rotate(' + secondangle +'deg)',
                              'transform': 'rotate(' + secondangle +'deg)'});

        $('#volumelabel').text('Volume: ' + Math.floor(angle*100/360) + '%')
    }

    function setTime(angle) {
        if(angle == 0)
            angle = 1;

        if(angle > 180) {
            firstangle = 180;
            secondangle = angle-180;
        }
        else {
            firstangle = angle;
            secondangle = 0;
        }

        $("#time-left").css({'-webkit-transform': 'rotate(' + firstangle +'deg)',
                              '-moz-transform': 'rotate(' + firstangle +'deg)',
                              '-ms-transform': 'rotate(' + firstangle +'deg)',
                              'transform': 'rotate(' + firstangle +'deg)'});
        $("#time-right").css({'-webkit-transform': 'rotate(' + secondangle +'deg)',
                              '-moz-transform': 'rotate(' + secondangle +'deg)',
                              '-ms-transform': 'rotate(' + secondangle +'deg)',
                              'transform': 'rotate(' + secondangle +'deg)'});

        $('#timelabel').text('Time: ' + Math.floor(angle*100/360) + '%')
    }
});