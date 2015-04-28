/**
 * Created by kaosterra on 15/04/15.
 */

showAlarms = function () {
    $('#alarms').show();
    $('#events').hide();

    $('#alarms_tab').addClass('active');
    $('#events_tab').removeClass('active');
};

showEvents = function () {
    $('#alarms').hide();
    $('#events').show();

    $('#events_tab').addClass('active');
    $('#alarms_tab').removeClass('active');
};

sensorStatus = function (sensor) {
    if (window.time && sensor.events) {
        var event;
        for (var n in sensor.events) {
            if (sensor.events.hasOwnProperty(n)) {
                event = sensor.events[n];
                if (event.timestamp < time) {
                    sensor.url = event.url;
                    sensor.status = event.status;
                    sensor.posX = event.posX;
                    sensor.posY = event.posY;
                    break;
                }
            }
        }
    }
};

isValid = function (sensor) {
    var floor = window.floor, time = window.time;
    return ((!floor || sensor.floor === floor.number) && (!time || sensor.creationDate < time));
};

function showIcons() {
    var c = document.getElementById("place_canvas");
    var ctx = c.getContext("2d");

    function drawSensor(sensor) {
        var image = new Image();
        image.src = sensor.url;
        ctx.drawImage(image, sensor.posX, sensor.posY);
    }

    var sensors = window.sensors, sensor;
    ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
    for (var i in sensors) {
        if (sensors.hasOwnProperty(i)) {
            sensor = $.extend({}, sensors[i]);
            if (isValid(sensor)) {
                sensorStatus(sensor);
                drawSensor(sensor);
            }
        }
    }
}
$(showIcons);
$(window).load(showIcons);
$(function () {
    $("#popup-panel").hide();
});

$("#place_canvas").on("click", function (event) {
    var sensors = window.sensors, sensor;
    var area = 34; //tamaño de las imágenes de los sensores
    var modal = $("#popup-panel");
    var body = $("#popup-sensor");

    if (typeof event.offsetX === "undefined" || typeof event.offsetY === "undefined") {
        var targetOffset = $(event.target).offset();
        event.offsetX = event.pageX - targetOffset.left;
        event.offsetY = event.pageY - targetOffset.top;
    }

    for (var i in sensors) {
        if (sensors.hasOwnProperty(i)) {
            sensor = $.extend({}, sensors[i]);
            if (isValid(sensor)) {
                sensorStatus(sensor);
                if ((sensor.posX <= event.offsetX && event.offsetX <= sensor.posX + area) &&
                    (sensor.posY <= event.offsetY && event.offsetY <= sensor.posY + area)) {
                    body.html("Sensor on " + (sensor.description || "Private Asset") + "<br/>Status: " + sensor.status);
                    modal.show();
                    return;
                }
            }
        }
    }
    modal.hide();
});