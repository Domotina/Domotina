var login = document.getElementById('login');

login.onclick = function(evt){
    var modal = document.getElementById('modal');
	modal.style.display = "block";

	modal.onclick = function(evt){
        if(evt.target.id == "modal"){
            var modal = document.getElementById('modal');
            modal.style.display = "none";
        }
	};
};