from flask import Flask, request, jsonify
import threading
import requests  # biblioteca para enviar a resposta HTTP
from PySide6.QtCore import QTimer, QObject, Signal

app = Flask(__name__)
chat_manager = None

DJANGO_CALLBACK_URL = "http://localhost:8000/api/avatar/retorno/"

class UiInvoker(QObject):
    trigger = Signal(str, bool)

ui_invoker = UiInvoker()

@app.route("/falar", methods=["POST"])
def falar():
    data = request.get_json()
    texto = data.get("texto", "")

    if chat_manager:
        confirm_text = f"Você quis dizer: '{texto}'?"
        ui_invoker.trigger.emit(confirm_text, False)
        return jsonify({"status": "ok", "confirmacao": True})
    

@app.route("/falar_final", methods=["POST"])
def falar_final():
    data = request.get_json()
    texto = data.get("texto", "")

    if chat_manager:
        ui_invoker.trigger.emit(texto, True)
        return jsonify({"status": "ok"})


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

    print("[Servidor Flask] Iniciando servidor em http://localhost:5000 ...")
    threading.Thread(target=lambda: app.run(port=5000, debug=False, use_reloader=False), daemon=True).start()