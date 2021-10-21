wait = ''
$( "#submit" ).click(function() {
    console.log('hi')
    $.post( "/start", { hostname: $('#hostname').val() }).done(function( r ) {
    if (r['msg'] == 'Y') {
        console.log('Started');
        wait = setInterval(function(){
            socket.send({"type":"wait"})
        },2000);
    }});
});

const socket = io('http://127.0.0.1:6001')

socket.on('connect', function() {
    socket.send('user connected')
});

socket.on("message", function(msg) {
    if (msg['type'] == 'data') {
        clearInterval(wait)
        console.log(msg['content'])
        if (msg['content'].length == 0) {
            $("#ports").html($("#ports").html() + "<h4>No ports are open</h4>")
        } else {
            for (p in msg['data']) {
                $("ports").html($("#ports").html() + "<h6>Port " + String(p) + "</h6>")
            }
        }
    }
});

