// check if files is in the list
function file_exists(filename){
	var files = $(".file").map(function(){
		return $(this).text();
		}).get();		
	return (files.indexOf(filename) != -1);		
}

$(document).ready(function(){
	$("#files").hide();
	
	$("#browse").hover(function(){
  		$(this).css('cursor','pointer');
  	});
	$("#browse").click(function(){
		$(this).hide();
		//$("#files").show();
		$("#files").slideDown( "fast");
	});
  
   	$(".file").hover(function(){
  		$(this).css('cursor','pointer');
  		$(this).css({"font-size":"105%"});
  	});
  	
  	   	$(".file").mouseout(function(){
  			$(this).css({"font-size":"100%"});
  	});
  	
	
	$(".file").click(function(){
		$("#inputfile").val($(this).text());
		$("#files").slideUp( "fast");
		$("#browse").show();
		
		//var files_url = $("input#file_url").attr("value");
		//alert(file_exists($(this).text()));
	});
  
  	$("#submit_button").click(function(){
		if($("#inputfile").val()==""){
			alert("Please choose an input file");
			return false;
		}
		if($("#procname").val()==""){
			alert("Please choose name for the procedure");
			return false;
		}
		var filename = $("#inputfile").val();
		if (!file_exists(filename)){
			alert("File not found");
			return false;
		}
	    });
		
	$("img#delete").hover(function(){
		$(this).css('cursor','pointer');
		$(this).width($(this).width()*1.2);
		},function(){
		$(this).width($(this).width()/1.2);
		});
	    
	    
	    $("img#delete").click(function(){
	    	if(confirm("Delete entry including output files : "+$(this).attr("name"))){
			var url = "delete_process.py?filename="+$(this).attr("filename")+"&format=json";
			$.getJSON(url,
				function(jsonRes, text){
					alert(jsonRes.message);
					if(jsonRes.status){
						// remove the file we just deleted from the list
						var selstr = "a:contains('"+jsonRes.name+"')";
						$(selstr).parent().parent().hide(); // select the row
					}
				});
 		}
		});
		
});