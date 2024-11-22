
        async function sendMessage() {
            const inputField = document.getElementById("messageInput");
            const responseField = document.getElementById("responseField");
            const userMessage = inputField.value.trim();
    
            if (!userMessage) {
                alert("Please enter a message.");
                return;
            }
    
            // Display the user's message in the response field
            responseField.innerHTML += `<p><strong>You:</strong> ${userMessage}</p>`;
    
            // Send the message to the Flask backend
            try {
                const response = await fetch("http://127.0.0.1:5000/chat", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ message: userMessage })
                });
    
                const data = await response.json();
                if (response.ok) {
                    responseField.innerHTML += `<p><strong>AlexGPT:</strong> ${data.response}</p>`;
                } else {
                    responseField.innerHTML += `<p><strong>Error:</strong> ${data.error}</p>`;
                }
            } catch (error) {
                responseField.innerHTML += `<p><strong>Error:</strong> Could not send the message.</p>`;
            }
    
            // Clear the input field
            inputField.value = "";
            responseField.scrollTop = responseField.scrollHeight;
        }
