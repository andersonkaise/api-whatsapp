# main.py
from flask import Flask, request, jsonify
import subprocess
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

app = Flask(__name__)

# Links das redes sociais
INSTAGRAM_LINK = "https://www.instagram.com/konnect_sc/"
FACEBOOK_LINK = "https://www.facebook.com/Konecti"

# Credenciais do Yowsup
YOWSUP_CREDENTIALS = os.getenv("YOWSUP_CREDENTIALS")  # Exemplo: "SEU_NUMERO:SEU_TOKEN"

# Função para enviar mensagens via Yowsup
def send_whatsapp_message(phone, message):
    if not YOWSUP_CREDENTIALS:
        return "Erro: Credenciais do Yowsup não configuradas."
    
    cmd = ["yowsup-cli", "demos", "-l", YOWSUP_CREDENTIALS, "-s", phone, message]
    process = subprocess.run(cmd, capture_output=True, text=True)
    
    if process.returncode == 0:
        print("Mensagem enviada com sucesso")
    else:
        print("Falha ao enviar mensagem")

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    if "messages" in data.get("entry", [{}])[0].get("changes", [{}])[0].get("value", {}):
        messages = data["entry"][0]["changes"][0]["value"]["messages"]
        for message in messages:
            text = message["text"]["body"]
            sender = message["from"]
            
            if text in ["oi", "olá"]:
                send_whatsapp_message(sender, "Olá! Como posso ajudar?")
            elif text == "sim":
                send_whatsapp_message(sender, "Você respondeu SIM.")
            elif text == "não":
                send_whatsapp_message(sender, "Você respondeu NÃO.")
            else:
                send_whatsapp_message(sender, "Desculpe, não entendi. Responda apenas SIM ou NÃO.")
    
    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

# Dockerfile

#"FROM python:3.8;"

#"WORKDIR /app;"

#"COPY requirements.txt requirements.txt"
#"RUN pip install -r requirements.txt"

# Instalar dependências do Yowsup
#RUN apt-get update && apt-get install -y libssl-dev libevent-dev libffi-dev
#RUN git clone https://github.com/tgalal/yowsup.git && cd yowsup && pip install .

#COPY . .

#CMD ["python", "main.py"]

