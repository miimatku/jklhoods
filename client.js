window.onload = function(){
var connection = new WebSocket('ws://localhost:9999');
connection.onopen = function () {
  connection.send('Ping'); // Send the message 'Ping' to the server
};

// Log errors
connection.onerror = function (error) {
  console.log('WebSocket Error ' + error);
  alert(e.data);
};

// Log messages from the server
connection.onmessage = function (e) {
//  console.log('Server: ' + e.data);
  alert(e.data);
};
}