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
function filterFunction(){
  	var input = document.getElementById("search");
  	var filter = input.value.toUpperCase();
  	var table = document.getElementById("table");
  	var rows = table.getElementsByTagName("tr");
	
	for (var i = 0; i < rows.length; i++) {
   		var cur_col_val = rows[i].getElementsByTagName("td")[0];
  		if (cur_col_val) {
      			if (cur_col_val.innerHTML.toUpperCase().indexOf(filter) > -1) {
        			rows[i].style.display = "";
     			 }
			else {
        			rows[i].style.display = "none";
      			}
    		}
  }
}
