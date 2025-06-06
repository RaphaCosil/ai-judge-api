document.addEventListener('DOMContentLoaded', function() {
    const chatContainer = document.getElementById('chatContainer');
    const userInput = document.getElementById('userInput');
    const sendButton = document.getElementById('sendButton');
    const topic = new URLSearchParams(window.location.search).get('topic') || 'pluto';
    
    function addMessage(sender, message, isEvaluation = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `mb-2 p-2 rounded ${isEvaluation ? 'evaluation-message' : sender === 'user' ? 'user-message' : 'ai-message'}`;
        
        const senderSpan = document.createElement('span');
        senderSpan.className = 'fw-bold';
        senderSpan.textContent = sender === 'user' ? 'Você: ' : isEvaluation ? 'Juiz de IA: ' : 'IA Enviesada: ';
        
        messageDiv.appendChild(senderSpan);
        messageDiv.appendChild(document.createTextNode(message));
        chatContainer.appendChild(messageDiv);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
    
    async function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;
        
        addMessage('user', message);
        userInput.value = '';
        
        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    question: message,
                    topic: topic
                })
            });
            
            const data = await response.json();
            
            if (data.error) {
                addMessage('system', `Erro: ${data.error}`);
                return;
            }
            
            addMessage('ai', data.response);
            addMessage('judge', data.evaluation, true);
        } catch (error) {
            addMessage('system', 'Erro ao conectar com o servidor');
            console.error(error);
        }
    }
    
    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') sendMessage();
    });
    
    addMessage('system', `Tópico atual: ${topic}. Faça uma pergunta sobre este assunto.`);
});