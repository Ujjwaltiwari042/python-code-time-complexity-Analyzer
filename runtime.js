document.getElementById("analyze-btn").addEventListener("click", function() {
    const code = document.getElementById("code-editor").value;

    fetch('http://127.0.0.1:5000/analyze', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ code: code })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert('Error: ' + data.error);
        } else {
            document.getElementById("big-o").textContent = data.complexity;
            document.getElementById("reasoning").textContent = data.reasoning;
        }
    })
    .catch(error => console.error('Error:', error));
});

