import chatbot_service

chatbot_service = chatbot_service.ChatBotService()

print("Enter in a prompt:")

while True:
    user_input = input()
    print(chatbot_service.get_bot_response_with_conversation_buffer_memory(user_input))
    #print(chatbot_service.get_bot_response_with_conversation_summary_memory(user_input))
    #print(chatbot_service.get_bot_response_with_conversation_buffer_window_memory(user_input))

