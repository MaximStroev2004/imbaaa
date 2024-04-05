document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('messageForm');
    const input = document.getElementById('messageInput');
    const messagesDiv = document.getElementById('messages');

    form.addEventListener('submit', function(event) {
        event.preventDefault();
        const message = input.value;
        input.value = '';
        sendMessage(message);
    });
const audio = document.getElementById('background-music');

audio.play();

audio.addEventListener('ended', function() {
  audio.play();
});

    function sendMessage(message) {
        fetch('/send', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {

            messagesDiv.innerHTML += `<div>${data.message}</div>`;
        })
        .catch(error => console.error('Ошибка:', error));
    }
});
