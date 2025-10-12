from nicegui import ui
from xai_sdk import Client
import os

client = Client(api_key=os.getenv("XAI_API_KEY"))
chat_history = []

def askGrok():
    prompt = prompt_input.value.strip()
    if not prompt:
        output_label.value = 'Todo: Prompt'
        return

    # Verwende ROLE_USER für die Eingabe
    chat_history.append({"role": "ROLE_USER", "content": prompt})

    try:
        response = client.chat.create(
            model="grok-3-mini",
            messages=chat_history
        )

        # Debugging: Antwortstruktur ausgeben
        print("API-Antwort:", response)
        print("Antwort-Attribute:", dir(response))

        # Zugriff auf message/content
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
        print("Ausgabe:", output_text)
        chat_history.append({"role": "ROLE_ASSISTANT", "content": output_text})

    except Exception as e:
        output_label.value = f'Fehler: {str(e)}'
        print(f'Fehler bei API-Aufruf: {str(e)}')

prompt_input = ui.textarea(label='API Prompt', placeholder='Frag Grok3 mini')
ui.button('Frage Grok', on_click=askGrok)
output_label = ui.textarea()

ui.run(port=8081)

