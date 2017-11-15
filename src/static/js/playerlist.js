function SearchFunction(){
	var input = document.getElementById("search").value.toUpperCase().trim();
	var table = document.getElementById("table");
  	var rows = table.getElementsByTagName("tr");

  	for (var i = 0; i < (rows.length); i++){
  		rows[i].style.display = "";
  	}

  	for (var i = 0; i < (rows.length); i++){
  		var cur_row_name = rows[i].getElementsByTagName("a")[0];
  		// alert(cur_row_name.innerHTML);

  		if (cur_row_name){
  			if(cur_row_name.innerHTML.toUpperCase().indexOf(input) > -1){
  				rows[i].style.display = "";
  			}
  			else{
  				rows[i].style.display = "none";
  			}
  		}
  	}
}