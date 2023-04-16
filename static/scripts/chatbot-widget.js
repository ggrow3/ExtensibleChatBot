var ChatbotWidget = /** @class */ (function () {
    function ChatbotWidget(containerId, chatEndPointApi, chatBotType) {
        if (chatEndPointApi === void 0) { chatEndPointApi = ""; }
        this.container = document.getElementById(containerId);
        this.chatBotType = chatBotType;
        this.chatEndpointApi = chatEndPointApi;
        if (this.chatEndpointApi == "") {
            this.chatEndpointApi = window.location.href + "chat";
        }
        if (!this.container) {
            throw new Error('Container element not found');
        }
        this.render();
    }
    ChatbotWidget.prototype.render = function () {
        var _this = this;
        this.container.innerHTML = "\n      <div class=\"chatbot-widget\">\n        <div class=\"chatbot-chat-area\"></div>\n        <input class=\"chatbot-input-field\" type=\"text\" placeholder=\"Type your message...\">\n      </div>\n    ";
        this.chatArea = this.container.querySelector('.chatbot-chat-area');
        this.inputField = this.container.querySelector('.chatbot-input-field');
        this.chatEndpointApi = this.chatEndpointApi;
        this.inputField.addEventListener('keydown', function (event) {
            if (event.key === 'Enter') {
                _this.handleUserMessageChat(_this.inputField.value);
                _this.inputField.value = '';
            }
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
        messageElement.innerHTML = "<strong>".concat(sender, ":</strong> ").concat(message);
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
