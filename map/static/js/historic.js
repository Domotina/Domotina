/**
 * Created by kaosterra on 17/04/15.
 */
function secondsFormatter(value) {
    var seconds = ("00" + Math.floor(value % 60)).slice(-2);
    var minutes = ("00" + Math.floor(value / 60 % 60)).slice(-2);
    var hours = ("00" + (Math.floor((value / 60 / 60 + 23) % 12) + 1)).slice(-2);
    var am_pm;
    if (value / 60 / 60 > 12) {
        am_pm = " p.m.";
    } else {
        am_pm = " a.m.";
    }
    return hours + ":" + minutes + ":" + seconds + am_pm;
};

$(function () {
    for (idx in floors) {
        $("#floors").append("<option value=" + idx + ">Floor " + floors[idx].number + "</option>");
    }
    $("#floors").change(function(){
        var idx = $("#floors").find(":selected").val();
        floor = floors[idx];
        $('#map').css("background-image", "url(" + floor.url + ")");
        showIcons();
    });

    $('#map').css("background-image", "url(" + floor.url + ")");

    var slider = $('#slider').slider({formater: secondsFormatter})
    slider.on('slide', function (value) {
        var seconds = value.value;
        time.setHours(seconds / 60 / 60);
        time.setMinutes(seconds / 60 % 60);
        time.setSeconds(seconds % 60);
        showIcons()
    });
});