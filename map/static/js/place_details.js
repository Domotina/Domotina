/**
 * Created by kaosterra on 15/04/15.
 */
document.getElementById("popup-panel").style.display = 'none';

function showIcons() {
    var c = document.getElementById("place_canvas");
    var ctx = c.getContext("2d");
    var currentSensor;
    for (var i in sensors) {
        currentSensor = new Image();
        currentSensor.src = sensors[i].url;
        ctx.drawImage(currentSensor, sensors[i].pos_x, sensors[i].pos_y);
    }
}
$(document).ready(showIcons);
$(window).load(showIcons);

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

$("#place_canvas").on("click", function (event) {
    var modal = document.getElementById('popup-panel');
    modal.style.display = "block";

    modal.onclick = function (evt) {
        if (evt.target.id == "popup-panel") {
            var modal = document.getElementById('popup-panel');
            modal.style.display = "none";
        }
    };

    if (sensors != null) {
        var totalOffsetX = 0;
        var totalOffsetY = 0;
        var canvasX = 0;
        var canvasY = 0;
        var currentElement = this;

        do {
            totalOffsetX += currentElement.offsetLeft - currentElement.scrollLeft;
            totalOffsetY += currentElement.offsetTop - currentElement.scrollTop;
        } while (currentElement = currentElement.offsetParent)

        canvasX = event.pageX - totalOffsetX;
        canvasY = event.pageY - totalOffsetY;

        var is_any_sensor = false;
        for (var i in sensors) {
            if ((canvasX >= sensors[i].pos_x + 1 && canvasX <= sensors[i].pos_x + 30) &&
                (canvasY >= sensors[i].pos_y - 2 && canvasY <= sensors[i].pos_y + 28)) {
                //alert("canvasX:"+canvasX+"  "+"canvasY:"+canvasY);
                if (sensors[i].description == "") {
                    document.getElementById("popup-sensor").innerHTML =
                        "Sensor on a hidden asset.<br/>Status: " + sensors[i].status;
                    document.getElementById("popup-panel").style.display = 'block';
                } else {
                    document.getElementById("popup-sensor").innerHTML =
                        "Sensor on " + sensors[i].description + "<br />Status: " + sensors[i].status;
                    document.getElementById("popup-panel").style.display = 'block';
                }
                is_any_sensor = true;
            } else {
                if (!is_any_sensor) {
                    document.getElementById("popup-panel").style.display = 'none';
                }
            }
        }
    }
});