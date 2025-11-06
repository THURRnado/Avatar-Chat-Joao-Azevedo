import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.groq import Groq
import asyncio
import edge_tts
from pydub import AudioSegment
import io

# ESSA CLASSE SERÁ DESCARTADA DPS, POIS SIMULA A IA E SOH SERVE PARA TESTAR

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
            name="Agente João Azevedo",
            instructions="Você é o Governador da Paraíba João Azevedo. Responda com frases de até 2 linhas."
        )

    def process(self, message:str, confirm) -> str:
        #resposta = self.agent.run(message)
        #texto = resposta.content
        if confirm:
            texto = "A resposta poderá ser dada quando minha IA estiver com as capacidades para isso. Porém obrigado por perguntar!"
        else:
            texto = message
        self.gerar_audio(texto)
        return texto

    async def _gerar_audio_async(self, texto: str):
        # Garante que a pasta existe
        os.makedirs(os.path.dirname(self.audio_file), exist_ok=True)

        # Remove arquivo antigo se existir
        try:
            os.remove(self.audio_file)
        except Exception:
            pass

        # Cria o áudio temporário
        temp_file = self.audio_file
        communicate = edge_tts.Communicate(texto, "pt-BR-AntonioNeural")
        await communicate.save(temp_file)

        # Converte para WAV PCM compatível com pygame
        audio = AudioSegment.from_file(temp_file, format="mp3")
        audio = audio.set_frame_rate(44100).set_sample_width(2).set_channels(2)
        audio.export("audio/saida/resposta.wav", format="wav")

        # Remove o arquivo temporário
        os.remove(temp_file)

        print(f"Áudio WAV PCM salvo em: {self.audio_file}")

    def gerar_audio(self, texto: str):
        # Chama o método async do Edge TTS
        asyncio.run(self._gerar_audio_async(texto))