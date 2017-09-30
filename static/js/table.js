// var searchContent = document.getElementById("search");
// searchContent.addEventListener("input",test);

// function test(){
// 	alert("hi");
// }


// var $rows = $('#table tr');
// var $input = $('#search');
// $input.keyup(filter);

// function filter() {
//     var val = $.trim($input.val()).replace(/ +/g, ' ').toLowerCase();
//     $rows.show().filter().hide(hideFnc);
// }

// function hideFnc() {
//         var text = $input.text().replace(/\s+/g, ' ').toLowerCase();
//         return !~text.indexOf(val);
// }

// var $rows = $('#table tr');
// $('#search').keyup(function() {
//     var val = $.trim($(this).val()).replace(/ +/g, ' ').toLowerCase();
//
//     $rows.show().filter(function() {
//         var text = $(this).text().replace(/\s+/g, ' ').toLowerCase();
//         if (text.indexOf('first') === 1){
//         	return 0;
//         }
//         return !~text.indexOf(val);
//     }).hide();
//
// });

function sortTable(n){
	var table = document.getElementById("table");
	var switching = true;
	var switch_count = 0;
	var dir = "asc";
	while(switching){

		switching = false;
		var rows = table.getElementsByTagName("TR");

		for (var current_row_index = 1; current_row_index < (rows.length - 1); current_row_index ++){
			var shouldSwitch = false;
			var current_row = rows[current_row_index].getElementsByTagName('td')[n];
			var next_row = rows[current_row_index + 1].getElementsByTagName('td')[n];

			if (dir == "asc"){
				if (current_row.innerHTML.toLowerCase() > next_row.innerHTML.toLowerCase()){
					shouldSwitch = true;
					break;
				}
			}
			else if (dir == "desc"){
				if (current_row.innerHTML.toLowerCase() < next_row.innerHTML.toLowerCase()){
					shouldSwitch = true;
					break;
				}
			}
		}
		if (shouldSwitch) {
			rows[current_row_index].parentNode.insertBefore(rows[current_row_index + 1],rows[current_row_index]);
			switching = true;
			switch_count ++;
		}
		else{
			if (switch_count == 0 && dir == "asc"){
				dir = "desc";
				switching = true;
			}
		}
	}
}

function newFilterFunction(name_index, team_index, position_index ){
	var search_filter = document.getElementById("search").value.toUpperCase().trim();
	var team_filter = document.getElementById("team_dropdown").value.toUpperCase()
	var position_filter = document.getElementById("position_dropdown").value.toUpperCase()
	var table = document.getElementById("table");
  	var rows = table.getElementsByTagName("tr");

  	for (var i = 0; i< (rows.length); i++){
  		rows[i].style.display = "";
  	} 
  	for (var i = 1; i< (rows.length); i++){
  		//alert(search_filter+team_filter+position_filter);
  		var cur_row_name = rows[i].getElementsByTagName("td")[name_index];
  		var cur_row_team = rows[i].getElementsByTagName("td")[team_index];
  		var cur_row_pos = rows[i].getElementsByTagName("td")[position_index];
  		if (cur_row_name){
  			if (cur_row_name.innerHTML.toUpperCase().indexOf(search_filter) > -1){
  				var name_bool = true;
  			}
  			else {
  				var name_bool = false;
  			}	
  		}
  		if (search_filter.length == 0){
  			var name_all = true;
  		}
  		else{
  			var name_all = false;
  		}
  		if (cur_row_team){
  			if (cur_row_team.innerHTML.toUpperCase().indexOf(team_filter) > -1){
  				var team_bool = true;
  			}
  			else {
  				var team_bool = false;
  			}
  		}
  		if (team_filter == "ALL"){
  			var team_all = true;
  		}
  		else {
  			var team_all = false;
  		}
  		if (cur_row_pos){
  			if (cur_row_pos.innerHTML.toUpperCase().indexOf(position_filter) > -1){
  				var pos_bool = true;
  			}
  			else {
  				var pos_bool = false;
  			}
  		}
  		if (position_filter == "ALL"){
  			var pos_all = true;
  		}
  		else {
  			var pos_all = false;
  		}
  		if ((name_bool||name_all)&&(team_bool||team_all)&&(pos_bool||pos_all)) {
  			rows[i].style.display = "";
  		}
  		else{
  			rows[i].style.display = "none";
  		}


  	}
}
