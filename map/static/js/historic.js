/**
 * Created by kaosterra on 17/04/15.
 */
function secondsFormatter(value) {
    var seconds = ("00" + Math.floor(value % 60)).slice(-2);
    var minutes = ("00" + Math.floor(value / 60 % 60)).slice(-2);
    var hours = ("00" + (Math.floor((value / 60 / 60 + 23) % 12) + 1)).slice(-2);
    var ampm;
    if (value / 60 / 60 > 12) {
        ampm = " p.m.";
    } else {
        ampm = " a.m.";
    }
    return hours + ":" + minutes + ":" + seconds + ampm;
};

$(function () {
    var floorsElement = $("#floors");
    /*
    Se carga el mapa del primer piso por defecto
     */
    $('#map').css("background-image", "url(" + floor.url + ")");

    /*
    Se registran todas las opciones de pisos una vez carga el documento
     */
    for (idx in window.floors) {
        if (window.floors.hasOwnProperty(idx)) {
            floorsElement.append("<option value=" + idx + ">Floor " + window.floors[idx].number + "</option>");
        }
    }

    /*
    Cuando se selecciona un piso, se pinta de nuevo el mapa del piso
    y los respectivos sensores
     */
    floorsElement.change(function(){
        var idx = $("#floors").find(":selected").val();
        window.floor = window.floors[idx];
        $('#map').css("background-image", "url(" + floor.url + ")");
        showIcons();
    });

    /*
    Se crea el slider y se añade comportamiento cuando cambia su valor
     */
    var slider = $('#slider').slider({formater: secondsFormatter});
    slider.on('slide', function (value) {
        var seconds = value.value;
        time.setHours(seconds / 60 / 60);
        time.setMinutes(seconds / 60 % 60);
        time.setSeconds(seconds % 60);
        showIcons();
    });

    /*
    Cuando se selecciona una fecha, se navega hasta el histórico en dicha fecha
     */
    $("#goToDate").submit(function(event){
        var value = $("#calendar").val();
        if(value){
            var url = window.location.pathname.replace(/\d+\/$/, value.replace(/-/g,"")+"/");
            window.location.pathname = url;
        }
        event.preventDefault();
    });
});