$( "#submit" ).click(function() {
    console.log('hi')
    $.post( "/start", { hostname: $('#hostname').val() }).done(function( r ) {
    if (r['msg'] == 'Y') {
        console.log('Started');
    }});
});

const socket = io('ws://127.0.0.1:6001')

socket.on('connect', () => {
  console.log("socket connected");
});

socket.onAny(data => {
  console.log(data);
});

socket.on("message", data => {
  console.log(data);
});
