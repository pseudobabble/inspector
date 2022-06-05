
/**
* Simple long polling client based on JQuery
*/

/**
 * Request an update to the server and once it has answered, then update
 * the content and request again.
 * The server is supposed to response when a change has been made on data.
 */
function update() {
    $.ajax({
        url: '/api/queries/1',
        success:  function(data) {
            $('#result').text(JSON.stringify(data));
            update();
        },
        timeout: 20000 //If timeout is reached run again
    });
}


function query(event) {
    var allInputs = $( ":input" );
    $.ajax({
        url: '/api/queries',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            type: 'semantic_search',
            params: allInputs,
        }),
        success: alert("success!"),
        error: alert("error! :(")
    });
    event.preventDefault();

}

$(document).ready(function() {
    document.getElementById('button-0').onclick = update;
    $("form").submit(query)
});    
