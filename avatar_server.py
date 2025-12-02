from flask import Flask, request, jsonify
import threading
import requests
from PySide6.QtCore import QObject, Signal
import os


app = Flask(__name__)
chat_manager = None

DJANGO_CALLBACK_URL = "http://192.168.0.147:8000/api/avatar/retorno/"

class UiInvoker(QObject):
    trigger = Signal(str, bool, object)

ui_invoker = UiInvoker()

@app.route("/escolha", methods=["POST"])
def escolher():
    data = request.get_json()
    texto = data.get("texto", "")

    if chat_manager:
        done_event = threading.Event()

        def callback():
            done_event.set()

        confirm_text = f"Você quis dizer: '{texto}'\n\nResponda no tablet, por favor."
        ui_invoker.trigger.emit(confirm_text, True, callback)

        waited = done_event.wait(timeout=30)

        if waited:
            return jsonify({"status": "ok", "confirmacao": True})
        else:
            return jsonify({"status": "timeout", "confirmacao": False}), 504

    return jsonify({"status": "no_chat_manager"}), 500
    

@app.route("/responder", methods=["POST"])
def perguntar():
    texto = request.form.get("texto", "")
    audio = request.files.get("audio")

    print("TEXTO RECEBIDO PELA IA:", texto)

    if audio:
        # Salvar para tocar
        audio_path = "audio/saida/resposta.wav"
        os.remove(audio_path)
        audio.save(audio_path)
        print("Áudio recebido e salvo em:", audio_path)

        # Aqui você pode tocar usando alguma lib interna
        # ou enviar para o sistema que faz a reprodução

    if chat_manager:

        done_event = threading.Event()

        def callback():
            done_event.set()

        ui_invoker.trigger.emit(texto, False, callback)
        
        waited = done_event.wait(timeout=30)

        if waited:
            return jsonify({"status": "ok", "confirmacao": True})
        else:
            return jsonify({"status": "timeout", "confirmacao": False}), 504

    return jsonify({"status": "no_chat_manager"}), 500


def enviar_resposta_django(mensagem: str):
    """Envia uma notificação de volta para o Django"""
    try:
        response = requests.post(DJANGO_CALLBACK_URL, json={"mensagem": mensagem})
        print(f"[Servidor Flask] Resposta enviada ao Django: {response.status_code}")
    except Exception as e:
        print(f"[Servidor Flask] Erro ao enviar resposta ao Django: {e}")

def on_processo_finalizado(mensagem: str):
    """Chamado quando o avatar terminar o processo"""
    print("[Servidor Flask] Processo concluído, notificando Django...")
    threading.Thread(target=enviar_resposta_django, args=(mensagem,), daemon=True).start()

def iniciar_servidor(chat_manager_ref):
    global chat_manager
    chat_manager = chat_manager_ref
    ui_invoker.trigger.connect(chat_manager.send_message)

    print("[Servidor Flask] Iniciando servidor...")
    threading.Thread(target=lambda: app.run(host="localhost", port=5000, debug=False, use_reloader=False), daemon=True).start()