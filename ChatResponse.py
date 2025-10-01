import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.groq import Groq
from gtts import gTTS

# Carrega variáveis do .env
load_dotenv()


class ChatResponse:
    def __init__(self, audio_file="audio/saida/resposta.mp3"):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.audio_file = audio_file

        # inicializa o agente
        self.agent = Agent(
            model=Groq(
                id="llama-3.1-8b-instant",
                api_key=self.api_key
            ),
            name="Agente com Groq",
            instructions="Você é um assistente útil e objetivo."
        )

    def process(self, message: str) -> str:
        resposta = self.agent.run(message)
        texto = resposta.content
        self._gerar_audio(texto)
        return texto

    def _gerar_audio(self, texto: str):
        os.makedirs(os.path.dirname(self.audio_file), exist_ok=True)
        tts = gTTS(text=texto, lang="pt")
        tts.save(self.audio_file)
        print(f"Áudio salvo em: {self.audio_file}")