
/**
* Simple long polling client based on JQuery
*/

/**
 * Request an update to the server and once it has answered, then update
 * the content and request again.
 * The server is supposed to response when a change has been made on data.
 */

var state;
var stopPoll;

function update() {
    stopPoll = false;    
    $.ajax({
        url: '/api/queries/1',
        success:  function(data) {
            state.push(data);
            $('#result').text(JSON.stringify(state, null, 2));
            stopPoll = true;
        },
        error: function(t, x, m) {
            if (t!=="timeout" && !stopPoll) {
                update();
            }
        },
        timeout: 20000 //If timeout is reached run again
    });
}


function query(event) {
    stopPoll = true;
    // Grab the parameter vlaues from the form
    var form_params = [
        $('input[name="param_1"]').val(),
        $('input[name="param_2"]').val()
    ]

    // Pass them in the params 
    $.ajax({
        url: '/api/queries',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            type: 'semantic_search',
            params: form_params,
        }),
        success: function() {stopPoll=false},
        error: function() {alert("error! :(")}
    });
    event.preventDefault();

}

$(document).ready(function() {
    state = [];
    stopPoll = false;
    document.getElementById('button-0').onclick = update;
    $("form").submit(query)
});    
