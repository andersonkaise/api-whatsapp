FROM python:3.8

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Instalar dependências do Yowsup
RUN apt-get update && apt-get install -y libssl-dev libevent-dev libffi-dev
RUN git clone https://github.com/tgalal/yowsup.git && cd yowsup && pip install .

COPY . .

CMD ["python", "main.py"]

