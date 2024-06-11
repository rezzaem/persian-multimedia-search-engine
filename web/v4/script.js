const chatForm = document.getElementById('chat-form');
const chatInput = document.getElementById('chat-input');
const chatMessages = document.getElementById('chat-messages');

chatForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    const userMessage = chatInput.value.trim();
    if (userMessage !== '') {
        appendMessage('user', userMessage);
        chatInput.value = '';

        try {
            const response = await fetchResponse(userMessage);
            appendMessage('assistant', response);
        } catch (error) {
            console.error('Error fetching response:', error);
            appendMessage('assistant', 'Error: Unable to fetch response from the server.');
        }
    }
});

async function fetchResponse(message) {
    const response = await fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message }),
    });

    if (response.ok) {
        const data = await response.json();
        return data.response;
    } else {
        throw new Error(`Error: ${response.status} ${response.statusText}`);
    }
}

function appendMessage(sender, message) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('chat-message', sender);
    messageElement.textContent = message;
    chatMessages.appendChild(messageElement);
}