// Change to your URL (Must have Access-Control-Allow-Origin header to allow CORS)
var csvUrl = 'https://raw.githubusercontent.com/keebglo/T4MPPTWebpage/main/test.csv';


function handleCSVResult(csvString) {
  // Get the div element to append the data to
  var dataArea = document.querySelector('#curr_data');
  
  // Split csv to rows
  var rows = csvString.split('\n');
  
  var htmlStr = '';
  var PowerStr = '';
  var CurrentStr = '';
  var VoltageStr = '';
  var Time = '';
  var Temp = '';
  
  // Iterate over each row
  for (var i = 0; i < rows.length; i++) {
    var row = rows[i];
    
    // split row to cells
    var cells = row.split(',');
    
    // Extract data from cell 1 and 2 of current row
    var voltageVal = cells[0];
    var currentVal = cells[1];
	var powerVal = cells[2];
    var timeval = cells[3];
    var tempval = cells[4];
    
    
    // Add extracted CSV data to string
    htmlStr += '<p>'+timeval+': ' + currentVal + ' Amps</p><br>';
  }
  
  // Set the string generated from CSV as HTML of the dedicated div
  dataArea.innerHTML = htmlStr;
}

// Init Ajax Object
var ajax = new XMLHttpRequest();

// Set a GET request to the URL which points to your CSV file
ajax.open('GET', csvUrl);

// Set the action that will take place once the browser receives your CSV
ajax.onreadystatechange = function() {
  if (ajax.readyState === XMLHttpRequest.DONE && ajax.status === 200) {
    // Request was successful
    var csvData2 = ajax.responseText;

    // Do something with that data here
    handleCSVResult(csvData2);
  }
}

// Send request
ajax.send();