class ChatbotWidget {
  private container: HTMLElement;
  private chatArea: HTMLElement;
  private inputField: HTMLInputElement;
  private chatEndpointApi: string;
  private chatBotType: string;

  constructor(containerId: string, chatEndPointApi: string, chatBotType: string) {
    this.container = document.getElementById(containerId) as HTMLElement;
    this.chatBotType = chatBotType;
    this.chatEndpointApi = chatEndPointApi;
    if (!this.container) {
      throw new Error('Container element not found');
    }
    this.render();
  }

  private render() {
    this.container.innerHTML = `
      <div class="chatbot-widget">
        <div class="chatbot-chat-area"></div>
        <input class="chatbot-input-field" type="text" placeholder="Type your message...">
      </div>
    `;

    this.chatArea = this.container.querySelector('.chatbot-chat-area') as HTMLElement;
    this.inputField = this.container.querySelector('.chatbot-input-field') as HTMLInputElement;
    this.chatEndpointApi = this.chatEndpointApi;
    
    this.inputField.addEventListener('keydown', (event) => {
      if (event.key === 'Enter') {
        this.handleUserMessageChat(this.inputField.value);
        this.inputField.value = '';
      }
    });
  }

  private handleUserMessageChat(message: string) {
    this.addMessageToChat('User', message);
    let chatBotType =  this.chatBotType;
    // Send the message to the Flask endpoint and get the response
    fetch(this.chatEndpointApi, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: message, chatBotType: chatBotType})
    })
    .then(response => response.json())
    .then(data => {

      if (data.error) {
        this.addMessageToChat('Bot', 'Sorry, I am unable to respond at the moment.');
      } else {
        this.addMessageToChat('Bot', data.response);
      }
    })
    .catch(error => {
      console.error(error);
      this.addMessageToChat('Bot', 'Sorry, I am unable to respond at the moment.');
    });
  }

  private handleUserMessage(message: string) {
    this.addMessageToChat('User', message);
    const response = this.getBotResponse(message);
    this.addMessageToChat('Bot', response);
  }

  private addMessageToChat(sender: string, message: string) {
    const messageElement = document.createElement('div');
    messageElement.className = 'chatbot-message';
    messageElement.innerHTML = `<strong>${sender}:</strong> ${message}`;
    this.chatArea.appendChild(messageElement);
  }

  private getBotResponse(message: string): string {
    // Define simple predefined responses based on user input
    type ResponseKeys = 'hello' | 'how are you' | 'goodbye';

    // Define simple predefined responses based on user input
    const responses: Record<ResponseKeys, string> = {
      'hello': 'Hi there! How can I help you?',
      'how are you': 'I am doing well, thank you!',
      'goodbye': 'Goodbye! Have a great day!'
    };

    // Convert the message to lowercase and find a matching response
    const response = responses[message.toLowerCase() as ResponseKeys];

    // If there is no matching response, provide a default response
    return response || 'I am not sure how to respond to that.';
  }
}

(window as any).ChatbotWidget = ChatbotWidget;
