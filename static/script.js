$( "#submit" ).click(function() {
    console.log('hi')
    $.post( "/start", { hostname: $('#hostname').val() }).done(function( r ) {
    if (r['msg'] == 'Y') {
        console.log('Started');
    }});
});
