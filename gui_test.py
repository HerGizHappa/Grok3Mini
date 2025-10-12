from nicegui import ui
from xai_sdk import Client
from xai_sdk.chat import user, system
import os

client = Client(api_key=os.getenv("XAI_API_KEY"))
chat_history = []

def askGrok():
    prompt = prompt_input.value.strip() 
    if not prompt:
        output_label.set_value('Todo: Prompt')
        return
        
    chat_history.append({"role": "user", "content": prompt})
    
    try:
        response = client.chat.create(
            model="grok-3-mini",
            messages=chat_history
        )
        
        if hasattr(response, 'choices') and len(response.choices) > 0:
                message = response.choices[0].message
                output_text = message.content
        elif hasattr(response, 'message') and hasattr(response.message, 'content'):
            output_text = response.message.content
        elif hasattr(response, 'content'):
            output_text = response.content
        else:
            output_text = "Fehler: Kein 'choices' oder 'message' in der Antwort gefunden."
      
            output_label.value = output_text
            print(output_text)
            chat_history.append({"role": "assistant", "content": output_text})
    except Exception as e:
        output_label.value = f'Fehler: {str(e)}'


##chat = client.chat.create(model="grok-3-mini")

prompt_input = ui.textarea(label='API Prompt', placeholder='Frag Grok3 mini')

ui.button('Frage Grok', on_click=askGrok)  # Button triggert Verarbeitung

output_label = ui.textarea()

ui.run(port=8081)
