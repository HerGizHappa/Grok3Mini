from nicegui import ui
from xai_sdk import Client
from xai_sdk.chat import user, system
import os

client = Client(api_key=os.getenv("XAI_API_KEY"))

def askGrok():
    prompt = prompt_input.value.strip()
    if not prompt:
        output_label.value = 'Todo: Prompt'
        return #Verhinderung unnötiger API Anfrage bei leerem Prompt

    try:
        # Erstellung neues Chat-Objekt (für jeden Call, um History zu resetten; oder global für Multi-Turn)
        chat = client.chat.create(model="grok-3-mini")  

        # Optional: Füge eine System-Prompt hinzu
        chat.append(system("Du bist Grok, ein hilfreicher Assistent von xAI."))

        # User Prompt
        chat.append(user(prompt))

        # Generierung von Response (non-streaming)
        response = chat.sample()

        # Ausgabe: response.content ist der String
        output_text = response.content if hasattr(response, 'content') else str(response)

        output_label.value = output_text
        print("Ausgabe:", output_text)

        # Für Multi-Turn: Append Response zurück (z. B. in globalem Chat)
        # chat.append(response)

    except Exception as e:
        output_label.value = f'Fehler: {str(e)}'
        print(f'Fehler bei API-Aufruf: {str(e)}')

prompt_input = ui.textarea(label='API Prompt', placeholder='Frag Grok3 mini')
ui.button('Frage Grok', on_click=askGrok)
output_label = ui.textarea(placeholder='Grok-Antwort erscheint hier...')

ui.run(port=8081)

