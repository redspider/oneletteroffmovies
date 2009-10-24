/*
Dashboard JS
*/

var message_count = [];

function add_entry(destination, message, position) {
    var container = null;
    container = $('twitter');
    
    if (!message_count[destination]) {
        message_count[destination] = 0;
    }
    var message_element = Element('div',{'class': 'message'})
    var user_ref = Element('div', {'class': 'from_user'})
    user_ref.appendChild(Element('a',{'href': 'http://twitter.com/'+message.from_user, 'target': '_blank'}).set('text',message.from_user));
    message_element.appendChild(user_ref);
    message_element.appendChild(Element('img', {'class': 'profile_image'}).set('src',message.profile_image_url));
    var text = Element('div')
    var processed_text = message.text;
    processed_text = processed_text.replace(/(http:\/\/[^ ]+)/g, '<a href="$1" target="_blank">$1</a>');
    processed_text = processed_text.replace(/#([^ ]+)/g, '<a href="http://search.twitter.com/search?q=%23$1" target="_blank">#$1</a>');
    text.innerHTML = processed_text;
    message_element.appendChild(text);
    message_element.inject(container, position);
    message_element.slide('hide');
    message_element.slide('in');
    message_count[destination] ++;
    if (message_count[destination] > 30) {
        container.getLast().destroy();
    }
}

function dashboard_init() {
    stomp = new STOMPClient();
    stomp.onopen = function() {
    };
    stomp.onclose = function(c) { alert('Lost Connection, Code: ' + c);};
    stomp.onerror = function(error) {
        alert("Error: " + error);
    };
    stomp.onerrorframe = function(frame) {
        alert("Error: " + frame.body);
    };
    stomp.onconnectedframe = function() {
        stomp.subscribe("/topic/oneletteroffmovies");
    };
    stomp.onmessageframe = function(frame) {
        var message = JSON.decode(frame.body);
        add_entry(frame.headers.destination, message,'top');
        /* var container = document.getElementById('container');
        container.inject(Element('div').set('text',message.text),'top'); */
    };
    stomp.connect('localhost', 61613);
}
