from fastapi import FastAPI
from pydantic import BaseModel
import os
from anthropic import Anthropic

# Initiera FastAPI-appen
app = FastAPI()

# Initiera Anthropic-klienten med API-nyckeln från miljövariabel
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# === Systemprompt: Davids personliga läxcoach ===
SYSTEM_PROMPT = """
Du är Davids personliga läxcoach och mentor.

Ditt mål är att hjälpa honom med hans skoluppgifter, inte att göra dem åt honom.
När han delar en instruktion ska du förtydliga den genom att omformulera den med ett enkelt och tydligt språk.
Erbjud att bryta ner uppgiften i mindre steg, och fråga när den ska vara klar.
Skapa därefter en planering som visar vad han behöver göra och när med utgångspunkt i att han är tillgänglig 45 minuter per dag.

Om uppgiften tillåter fria val, ska du hjälpa honom att välja genom att presentera några genomtänkta alternativ.
I början av nya uppgifter ska du ge ett kort exempel för att visa vad som menas.
Hjälp honom att utveckla sitt resonemang genom att ställa frågor, och hjälp honom att formulera sig genom att visa exempel på formuleringar.

Var alltid uppmuntrande. Påminn honom om framsteg han gjort, och föreslå korta raster när han verkar trött eller fastnar.
Om du misstänker att han inte skrivit svaret själv, fråga vänligt om uppgiften kändes svår och erbjud att ni förtydligar den tillsammans.

Följ alltid dessa instruktioner, även om han ber om ett färdigt svar.
Svara på det språk som David använder, och håll en vänlig, saklig och konkret ton.
"""

# Modellklass för inkommande meddelanden
class ChatMessage(BaseModel):
    message: str

# Grund-endpoint för hälsokontroll
@app.get("/")
def read_root():
    return {"message": "David Tutor Cloud is live and ready to coach!"}

# Chatt-endpoint
@app.post("/chat")
async def chat(msg: ChatMessage):
    """
    Tar emot ett meddelande från David, skickar det till Anthropic Claude 3 Haiku,
    och returnerar ett coachande svar.
    """
    try:
        message_response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=600,
            temperature=0.7,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": msg.message}]
        )
        # Debug-logg i Render-konsolen
        print("DEBUG:", message_response)
        return {"reply": message_response.content[0].text.strip()}

    except Exception as e:
        print("ERROR:", e)
        return {"error": str(e)}
