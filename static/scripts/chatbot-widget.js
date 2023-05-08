var ChatbotWidget = /** @class */ (function () {
    function ChatbotWidget(containerId, chatBotType, chatEndPointApi) {
        if (chatEndPointApi === void 0) { chatEndPointApi = ""; }
        this.container = document.getElementById(containerId);
        this.chatBotType = chatBotType;
        if (this.chatEndpointApi == "" || this.chatEndpointApi == null) {
            this.chatEndpointApi = window.location.href + "chat";
        }
        if (!this.container) {
            throw new Error('Container element not found');
        }
        this.render();
    }
    ChatbotWidget.prototype.render = function () {
        var _this = this;
        this.container.innerHTML = "\n      <div class=\"chatbot-widget\">\n        <div class=\"chatbot-chat-area\"></div>\n        <input class=\"chatbot-input-field\" type=\"text\" placeholder=\"Type your message...\">\n        <button class=\"chatbot-button\" onclick=\"sendMessage()\">Send</button>\n      </div>\n    ";
        this.chatArea = this.container.querySelector('.chatbot-chat-area');
        this.inputField = this.container.querySelector('.chatbot-input-field');
        this.button = this.container.querySelector('.chatbot-button');
        this.inputField.addEventListener('keydown', function (event) {
            if (event.key === 'Enter') {
                _this.handleUserMessageChat(_this.inputField.value);
                _this.inputField.value = '';
            }
        });
        this.button.addEventListener('click', function (event) {
            _this.handleUserMessageChat(_this.inputField.value);
            _this.inputField.value = '';
        });
    };
    ChatbotWidget.prototype.handleUserMessageChat = function (message) {
        var _this = this;
        this.addMessageToChat('User', message);
        var chatBotType = this.chatBotType;
        // Send the message to the Flask endpoint and get the response
        fetch(this.chatEndpointApi, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: message, chatBotType: chatBotType })
        })
            .then(function (response) { return response.json(); })
            .then(function (data) {
            if (data.error) {
                _this.addMessageToChat('Bot', 'Sorry, I am unable to respond at the moment.');
            }
            else {
                _this.addMessageToChat('Bot', data.response);
            }
        })["catch"](function (error) {
            console.error(error);
            _this.addMessageToChat('Bot', 'Sorry, I am unable to respond at the moment.');
        });
    };
    ChatbotWidget.prototype.handleUserMessage = function (message) {
        this.addMessageToChat('User', message);
        var response = this.getBotResponse(message);
        this.addMessageToChat('Bot', response);
    };
    ChatbotWidget.prototype.addMessageToChat = function (sender, message) {
        var messageElement = document.createElement('div');
        messageElement.className = 'chatbot-message';
        // Get the current date and time
        var timestamp = new Date();
        // Format the timestamp as desired (e.g., "HH:mm:ss")
        var formattedTimestamp = timestamp.toLocaleTimeString();
        // Include the bot name in the message element for bot responses
        if (sender === 'Bot') {
            messageElement.classList.add('bot-message'); // Add a CSS class for bot messages
        }
        else {
            messageElement.classList.add('user-message'); // Add a CSS class for user messages
        }
        // Include the timestamp in the message element
        messageElement.innerHTML = "<div class=\"message-bubble\"><strong>".concat(sender, " (").concat(formattedTimestamp, "):</strong> ").concat(message, "</div>");
        this.chatArea.appendChild(messageElement);
    };
    ChatbotWidget.prototype.getBotResponse = function (message) {
        // Define simple predefined responses based on user input
        var responses = {
            'hello': 'Hi there! How can I help you?',
            'how are you': 'I am doing well, thank you!',
            'goodbye': 'Goodbye! Have a great day!'
        };
        // Convert the message to lowercase and find a matching response
        var response = responses[message.toLowerCase()];
        // If there is no matching response, provide a default response
        return response || 'I am not sure how to respond to that.';
    };
    return ChatbotWidget;
}());
window.ChatbotWidget = ChatbotWidget;
