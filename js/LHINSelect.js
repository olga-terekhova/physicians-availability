function selectLHIN(current)  {
	var val = current
	var t = document.getElementById("LHINresult");
	//var current = document.getElementById("currentLHIN");
	var mymap = document.getElementById("LHINmap");
	
	t.innerHTML = ''
	mymap.src = "../pic/ontario-lhins-map-gtranked" +val+".png"
	


}