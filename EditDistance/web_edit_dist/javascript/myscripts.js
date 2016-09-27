/*
function showFiles(){
	htmlstr = ""
	files = {1,2,3,4}
	htmlstr += "<table>";
	for f in files{
		htmlstr += "<tr><td>"+f+"</td></tr>";
	}
	htmlstr += "</table>";
	//return htmlstr;
	
	document.getElementById("files").src=htmlstr;
		
}
*/
function defaultName(){
	now = new Date;
	timestamp = "";
	timestamp += (now.getHours() < 10) ? "0"+now.getHours() : now.getHours();
	timestamp += (now.getMinutes() > 9) ? now.getMinutes() : "0" + now.getMinutes();
	timestamp += (now.getSeconds() > 9) ? now.getSeconds() : "0" + now.getSeconds();
	timestamp += "_"+(now.getMonth()+1)+"_"+now.getDate()+"_"+now.getFullYear();
    
    name = "edit_distance_"+timestamp;
    resfile = "result_"+timestamp+".tar";

	document.getElementById("procname").value = name;
	document.getElementById("procname").select();
	document.getElementById("outputname").value = resfile;
	document.getElementById("inputfile").value = "";
}
