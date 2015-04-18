/**
 * Created by kaosterra on 17/04/15.
 */
function number2Time(value){
    var seconds = ("00"+Math.floor(value % 60)).slice(-2);
    var minutes = ("00"+Math.floor(value/60 % 60)).slice(-2);
    var hours = ("00"+(Math.floor((value/60/60+23) % 12)+1)).slice(-2);
    var am_pm;
    if(value/60/60 > 12){
        am_pm = " p.m.";
    }else{
        am_pm = " a.m.";
    }
    return hours + ":" + minutes + ":" + seconds + am_pm;
};