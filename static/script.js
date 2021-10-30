wait = ''
$( "#submit" ).click(function() {
    console.log('hi')
    $.post( "/start", { hostname: $('#hostname').val() }).done(function( r ) {
    if (r['msg'] == 'Y') {
        console.log('Started');
        $('#message').text('Scan started');
        wait = setInterval(function(){
            socket.send({"type":"wait"})
        },2000);
    }});
});


$( "#genpdf" ).click(function() {
    $.post( "/generate-pdf" ).done(function( r ) {
    if (r['msg'] == 'Y') {
      console.log('Report generated')  
    }});
});


url = 'http://127.0.0.1:6001'
/*url = 'http://vsc.gabrielseet.com:6001'*/ /*for hosted*/
const socket = io(url)

socket.on('connect', function() {
    socket.send('user connected')
});

socket.on("message", function(msg) {
    console.log(msg)
    if (msg['type'] == 'data') {
        clearInterval(wait)
        console.log(msg['content'])
        /*
        if (msg['content'].length == 0) {
            $("#ports").html($("#ports").html() + "<h4>No ports are open</h4>")
        } else {
            for (p in msg['data']) {
                $("#ports").html($("#ports").html() + "<h6>Port " + String(p) + "</h6>")
            }
        }
        */
        if (msg['content-type'] !== undefined) {
            if (msg['content-type'] == 'nmap,searchsploit') {
                ports = msg['content'][0]
                searchsploitdata = msg['content'][1]
                
                for (p in ports) {
                    $("#ports").html($("#ports").html() + "<h4>Port " + String(ports[p]) + " open</h4>")
                }
                
                $("#searchsploit").html($("#searchsploit").html() + searchsploitdata.replace(/(?:\r\n|\r|\n)/g, '<br>'));
            }
            
        }   
    }
});

