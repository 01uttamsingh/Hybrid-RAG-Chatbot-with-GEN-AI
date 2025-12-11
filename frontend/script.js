// Function to handle sending the question
async function askQuestion() {
    const input = document.getElementById("questionInput");
    const button = document.querySelector("button");
    const chatBox = document.getElementById("chat-box");
    const question = input.value.trim();

    if (!question) return;

    // 1. Add User Message to Chat
    addMessage("You", question, "user");
    input.value = "";

    // 2. Disable Input/Button & Show Loading State
    input.disabled = true;
    button.disabled = true;
    button.innerText = "...";

    try {
        // 3. Fetch Answer from Backend
        const response = await fetch(`http://127.0.0.1:8000/ask?question=${encodeURIComponent(question)}`);
        
        if (!response.ok) {
            throw new Error("Server Error");
        }

        const data = await response.json();

        // Determine Source Text
        const sourceText = data.source === "document"
            ? `Source: PDF (${data.document})`
            : "Source: Gen AI";

        // 4. Parse Markdown -> HTML & Sanitize
        // We use marked.parse() to turn **bold** into <b>bold</b>
        // We use DOMPurify to make sure the HTML is safe
        const rawHtml = marked.parse(data.answer);
        const safeHtml = DOMPurify.sanitize(rawHtml);

        // 5. Add Bot Message
        addMessage("Bot", safeHtml, "bot", sourceText);

    } catch (error) {
        console.error(error);
        addMessage("Bot", "Error connecting to the server.", "bot");
    } finally {
        // 6. Reset UI
        input.disabled = false;
        button.disabled = false;
        button.innerText = "Send";
        input.focus();
    }
}

// Function to Render Messages
function addMessage(sender, text, type, source = "") {
    const chatBox = document.getElementById("chat-box");
    
    // Create the main message wrapper (.message)
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message");

    // Create the content div (.user or .bot)
    const contentDiv = document.createElement("div");
    contentDiv.classList.add(type);

    if (type === "bot") {
        // Render HTML for Bot (to show Markdown formatting)
        // We add the sender name in bold manually since we are using innerHTML
        contentDiv.innerHTML = `<strong>${sender}:</strong> ${text}`;
    } else {
        // Render Plain Text for User (Security best practice)
        contentDiv.innerText = `${sender}: ${text}`;
    }
    
    messageDiv.appendChild(contentDiv);

    // If there is a source, add it (.source)
    if (source) {
        const sourceDiv = document.createElement("div");
        sourceDiv.classList.add("source");
        sourceDiv.innerText = source;
        messageDiv.appendChild(sourceDiv);
    }

    // Append to Chat Box and Scroll to Bottom
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Allow sending with "Enter" key
document.getElementById("questionInput").addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        askQuestion();
    }
});