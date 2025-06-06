document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/topics')
        .then(response => response.json())
        .then(data => {
            const select = document.getElementById('topicSelect');
            select.innerHTML = '';
            data.topics.forEach(topic => {
                const option = document.createElement('option');
                option.value = topic;
                option.textContent = topic === 'pluto' ? 'Plutão é um planeta' : topic;
                select.appendChild(option);
            });
        });
    
    document.getElementById('startChat').addEventListener('click', function() {
        const topic = document.getElementById('topicSelect').value;
        window.location.href = `/chat?topic=${topic}`;
    });
});