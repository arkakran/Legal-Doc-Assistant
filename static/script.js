// const chatBox = document.getElementById("chat-box");
// const input = document.getElementById("question");
// const sendBtn = document.getElementById("send");
// const charCounter = document.querySelector(".char-counter");
// const loadingOverlay = document.getElementById("loading-overlay");

// let messageCount = 0;

// // Auto-resize textarea
// function autoResize() {
//     input.style.height = 'auto';
//     input.style.height = Math.min(input.scrollHeight, 120) + 'px';
// }

// // Update character counter and button state
// function updateInputState() {
//     const length = input.value.length;
//     const maxLength = parseInt(input.getAttribute('maxlength'));
    
//     charCounter.textContent = `${length}/${maxLength}`;
    
//     if (length > maxLength * 0.9) {
//         charCounter.style.color = 'var(--warning-color)';
//     } else if (length === maxLength) {
//         charCounter.style.color = 'var(--error-color)';
//     } else {
//         charCounter.style.color = 'var(--text-light)';
//     }
    
//     sendBtn.disabled = !input.value.trim() || length > maxLength;
// }

// // Add message with enhanced styling
// function addMessage(text, role, isError = false) {
//     // Remove welcome message on first user message
//     if (role === 'user' && messageCount === 0) {
//         const welcomeMsg = chatBox.querySelector('.welcome-message');
//         if (welcomeMsg) {
//             welcomeMsg.style.animation = 'fadeOut 0.3s ease-out forwards';
//             setTimeout(() => welcomeMsg.remove(), 300);
//         }
//     }
    
//     messageCount++;
    
//     const messageDiv = document.createElement("div");
//     messageDiv.className = `message ${role}${isError ? ' error-message' : ''}`;
    
//     const avatar = document.createElement("div");
//     avatar.className = "message-avatar";
//     avatar.innerHTML = role === 'user' ? '<i class="fas fa-user"></i>' : '<i class="fas fa-robot"></i>';
    
//     const contentDiv = document.createElement("div");
//     contentDiv.className = "message-content";
    
//     const bubbleDiv = document.createElement("div");
//     bubbleDiv.className = "message-bubble";
//     bubbleDiv.textContent = text;
    
//     contentDiv.appendChild(bubbleDiv);
//     messageDiv.appendChild(avatar);
//     messageDiv.appendChild(contentDiv);
    
//     chatBox.appendChild(messageDiv);
//     scrollToBottom();
    
//     return contentDiv; // Return for adding sources later
// }

// // Add thinking indicator
// function addThinkingIndicator() {
//     const messageDiv = document.createElement("div");
//     messageDiv.className = "message assistant thinking-message";
    
//     const avatar = document.createElement("div");
//     avatar.className = "message-avatar";
//     avatar.innerHTML = '<i class="fas fa-robot"></i>';
    
//     const contentDiv = document.createElement("div");
//     contentDiv.className = "message-content";
    
//     const bubbleDiv = document.createElement("div");
//     bubbleDiv.className = "message-bubble thinking";
//     bubbleDiv.innerHTML = `
//         <span>Assistant is thinking</span>
//         <div class="thinking-dots">
//             <span></span>
//             <span></span>
//             <span></span>
//         </div>
//     `;
    
//     contentDiv.appendChild(bubbleDiv);
//     messageDiv.appendChild(avatar);
//     messageDiv.appendChild(contentDiv);
    
//     chatBox.appendChild(messageDiv);
//     scrollToBottom();
    
//     return messageDiv;
// }

// // Add sources with enhanced styling
// function addSources(sources, contentDiv) {
//     if (!sources || !Array.isArray(sources) || sources.length === 0) return;
    
//     const sourcesDiv = document.createElement("div");
//     sourcesDiv.className = "sources";
    
//     const titleDiv = document.createElement("div");
//     titleDiv.className = "sources-title";
//     titleDiv.innerHTML = '<i class="fas fa-book"></i> Sources';
    
//     const listDiv = document.createElement("div");
//     listDiv.className = "sources-list";
    
//     sources.forEach(source => {
//         const page = source.meta && typeof source.meta.page === "number" ? source.meta.page + 1 : "?";
//         const srcName = source.meta && source.meta.source ? source.meta.source : "unknown";
        
//         const tagDiv = document.createElement("div");
//         tagDiv.className = "source-tag";
//         tagDiv.textContent = `${srcName}#p${page}`;
        
//         listDiv.appendChild(tagDiv);
//     });
    
//     sourcesDiv.appendChild(titleDiv);
//     sourcesDiv.appendChild(listDiv);
//     contentDiv.appendChild(sourcesDiv);
// }

// // Smooth scroll to bottom
// function scrollToBottom() {
//     chatBox.scrollTo({
//         top: chatBox.scrollHeight,
//         behavior: 'smooth'
//     });
// }

// // API call with better error handling
// async function askServer(question) {
//     const response = await fetch("/ask", {
//         method: "POST",
//         headers: {"Content-Type": "application/json"},
//         body: JSON.stringify({question})
//     });
    
//     if (!response.ok) {
//         const data = await response.json().catch(() => ({}));
//         throw new Error(data.error || `Server error (${response.status})`);
//     }
    
//     return response.json();
// }

// // Handle suggestion chip clicks
// function askSuggestion(question) {
//     input.value = question;
//     updateInputState();
//     sendMessage();
// }

// // Main send function
// async function sendMessage() {
//     const question = input.value.trim();
//     if (!question || sendBtn.disabled) return;
    
//     // Add user message
//     addMessage(question, "user");
    
//     // Clear input and reset state
//     input.value = "";
//     updateInputState();
//     autoResize();
    
//     // Add thinking indicator
//     const thinkingDiv = addThinkingIndicator();
    
//     // Show loading overlay
//     loadingOverlay.classList.add('show');
    
//     try {
//         const data = await askServer(question);
        
//         // Remove thinking indicator
//         thinkingDiv.remove();
        
//         // Add assistant response
//         const contentDiv = addMessage(data.answer, "assistant");
        
//         // Add sources if available
//         if (data.sources && Array.isArray(data.sources)) {
//             addSources(data.sources, contentDiv);
//         }
        
//     } catch (error) {
//         // Remove thinking indicator
//         thinkingDiv.remove();
        
//         // Add error message
//         addMessage(`Sorry, I encountered an error: ${error.message}`, "assistant", true);
//     } finally {
//         // Hide loading overlay
//         loadingOverlay.classList.remove('show');
//     }
// }

// // Event listeners
// sendBtn.addEventListener('click', sendMessage);

// input.addEventListener('input', () => {
//     updateInputState();
//     autoResize();
// });

// input.addEventListener('keydown', (e) => {
//     if (e.key === 'Enter' && !e.shiftKey) {
//         e.preventDefault();
//         sendMessage();
//     }
// });

// // Initialize
// updateInputState();
// autoResize();

// // Add fadeOut animation for welcome message
// const style = document.createElement('style');
// style.textContent = `
//     @keyframes fadeOut {
//         from { opacity: 1; transform: translateY(0); }
//         to { opacity: 0; transform: translateY(-10px); }
//     }
// `;
// document.head.appendChild(style);

// // Expose askSuggestion globally for onclick handlers
// window.askSuggestion = askSuggestion;
























































const chatBox = document.getElementById("chat-box");
const input = document.getElementById("question");
const sendBtn = document.getElementById("send");
const charCounter = document.querySelector(".char-counter");
const loadingOverlay = document.getElementById("loading-overlay");

let messageCount = 0;

// Simple markdown to HTML converter
function markdownToHtml(text) {
    // Convert headers
    text = text.replace(/^### (.*$)/gm, '<h3>$1</h3>');
    text = text.replace(/^## (.*$)/gm, '<h2>$1</h2>');
    text = text.replace(/^# (.*$)/gm, '<h1>$1</h1>');
    
    // Convert bold text
    text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    // Convert italic text
    text = text.replace(/\*(.*?)\*/g, '<em>$1</em>');
    
    // Convert bullet points
    text = text.replace(/^\* (.*$)/gm, '<li>$1</li>');
    text = text.replace(/^- (.*$)/gm, '<li>$1</li>');
    
    // Convert numbered lists
    text = text.replace(/^(\d+)\. (.*$)/gm, '<li>$1. $2</li>');
    
    // Wrap consecutive <li> elements in <ul>
    text = text.replace(/(<li>.*<\/li>)/gs, function(match) {
        const items = match.split('</li>').filter(item => item.trim() !== '').map(item => item + '</li>');
        return '<ul>' + items.join('') + '</ul>';
    });
    
    // Convert line breaks to paragraphs
    text = text.replace(/\n\n/g, '</p><p>');
    text = '<p>' + text + '</p>';
    
    // Clean up empty paragraphs
    text = text.replace(/<p><\/p>/g, '');
    text = text.replace(/<p>\s*<\/p>/g, '');
    
    return text;
}

// Auto-resize textarea
function autoResize() {
    input.style.height = 'auto';
    input.style.height = Math.min(input.scrollHeight, 120) + 'px';
}

// Update character counter and button state
function updateInputState() {
    const length = input.value.length;
    const maxLength = parseInt(input.getAttribute('maxlength'));
    
    charCounter.textContent = `${length}/${maxLength}`;
    
    if (length > maxLength * 0.9) {
        charCounter.style.color = 'var(--warning-color)';
    } else if (length === maxLength) {
        charCounter.style.color = 'var(--error-color)';
    } else {
        charCounter.style.color = 'var(--text-light)';
    }
    
    sendBtn.disabled = !input.value.trim() || length > maxLength;
}

// Add message with enhanced styling and markdown support
function addMessage(text, role, isError = false) {
    // Remove welcome message on first user message
    if (role === 'user' && messageCount === 0) {
        const welcomeMsg = chatBox.querySelector('.welcome-message');
        if (welcomeMsg) {
            welcomeMsg.style.animation = 'fadeOut 0.3s ease-out forwards';
            setTimeout(() => welcomeMsg.remove(), 300);
        }
    }
    
    messageCount++;
    
    const messageDiv = document.createElement("div");
    messageDiv.className = `message ${role}${isError ? ' error-message' : ''}`;
    
    const avatar = document.createElement("div");
    avatar.className = "message-avatar";
    avatar.innerHTML = role === 'user' ? '<i class="fas fa-user"></i>' : '<i class="fas fa-robot"></i>';
    
    const contentDiv = document.createElement("div");
    contentDiv.className = "message-content";
    
    const bubbleDiv = document.createElement("div");
    bubbleDiv.className = "message-bubble";
    
    // For user messages, use plain text. For assistant messages, render markdown
    if (role === 'user') {
        bubbleDiv.textContent = text;
    } else {
        bubbleDiv.innerHTML = markdownToHtml(text);
    }
    
    contentDiv.appendChild(bubbleDiv);
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(contentDiv);
    
    chatBox.appendChild(messageDiv);
    scrollToBottom();
    
    return contentDiv; // Return for adding sources later
}

// Add thinking indicator
function addThinkingIndicator() {
    const messageDiv = document.createElement("div");
    messageDiv.className = "message assistant thinking-message";
    
    const avatar = document.createElement("div");
    avatar.className = "message-avatar";
    avatar.innerHTML = '<i class="fas fa-robot"></i>';
    
    const contentDiv = document.createElement("div");
    contentDiv.className = "message-content";
    
    const bubbleDiv = document.createElement("div");
    bubbleDiv.className = "message-bubble thinking";
    bubbleDiv.innerHTML = `
        <span>Assistant is thinking</span>
        <div class="thinking-dots">
            <span></span>
            <span></span>
            <span></span>
        </div>
    `;
    
    contentDiv.appendChild(bubbleDiv);
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(contentDiv);
    
    chatBox.appendChild(messageDiv);
    scrollToBottom();
    
    return messageDiv;
}

// Add sources with enhanced styling
function addSources(sources, contentDiv) {
    if (!sources || !Array.isArray(sources) || sources.length === 0) return;
    
    const sourcesDiv = document.createElement("div");
    sourcesDiv.className = "sources";
    
    const titleDiv = document.createElement("div");
    titleDiv.className = "sources-title";
    titleDiv.innerHTML = '<i class="fas fa-book"></i> Sources';
    
    const listDiv = document.createElement("div");
    listDiv.className = "sources-list";
    
    sources.forEach(source => {
        const page = source.meta && typeof source.meta.page === "number" ? source.meta.page + 1 : "?";
        const srcName = source.meta && source.meta.source ? source.meta.source : "unknown";
        
        const tagDiv = document.createElement("div");
        tagDiv.className = "source-tag";
        tagDiv.textContent = `${srcName}#p${page}`;
        
        listDiv.appendChild(tagDiv);
    });
    
    sourcesDiv.appendChild(titleDiv);
    sourcesDiv.appendChild(listDiv);
    contentDiv.appendChild(sourcesDiv);
}

// Smooth scroll to bottom
function scrollToBottom() {
    chatBox.scrollTo({
        top: chatBox.scrollHeight,
        behavior: 'smooth'
    });
}

// API call with better error handling
async function askServer(question) {
    const response = await fetch("/ask", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({question})
    });
    
    if (!response.ok) {
        const data = await response.json().catch(() => ({}));
        throw new Error(data.error || `Server error (${response.status})`);
    }
    
    return response.json();
}

// Handle suggestion chip clicks
function askSuggestion(question) {
    input.value = question;
    updateInputState();
    sendMessage();
}

// Main send function
async function sendMessage() {
    const question = input.value.trim();
    if (!question || sendBtn.disabled) return;
    
    // Add user message
    addMessage(question, "user");
    
    // Clear input and reset state
    input.value = "";
    updateInputState();
    autoResize();
    
    // Add thinking indicator
    const thinkingDiv = addThinkingIndicator();
    
    // Show loading overlay
    loadingOverlay.classList.add('show');
    
    try {
        const data = await askServer(question);
        
        // Remove thinking indicator
        thinkingDiv.remove();
        
        // Add assistant response
        const contentDiv = addMessage(data.answer, "assistant");
        
        // Add sources if available
        if (data.sources && Array.isArray(data.sources)) {
            addSources(data.sources, contentDiv);
        }
        
    } catch (error) {
        // Remove thinking indicator
        thinkingDiv.remove();
        
        // Add error message
        addMessage(`Sorry, I encountered an error: ${error.message}`, "assistant", true);
    } finally {
        // Hide loading overlay
        loadingOverlay.classList.remove('show');
    }
}

// Event listeners
sendBtn.addEventListener('click', sendMessage);

input.addEventListener('input', () => {
    updateInputState();
    autoResize();
});

input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

// Initialize
updateInputState();
autoResize();

// Add fadeOut animation for welcome message
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeOut {
        from { opacity: 1; transform: translateY(0); }
        to { opacity: 0; transform: translateY(-10px); }
    }
`;
document.head.appendChild(style);

// Expose askSuggestion globally for onclick handlers
window.askSuggestion = askSuggestion;
