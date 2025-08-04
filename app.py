# app_kafka.py
from confluent_kafka import Producer
from flask import Flask, jsonify, request
import json
import socket

app = Flask(__name__)

# Configuración para Kafka 3.9
conf = {
    'bootstrap.servers': 'localhost:9092',
    'client.id': socket.gethostname(),
    'acks': 'all',  # Mayor confiabilidad
    'retries': 3,    # Reintentos automáticos
    'compression.type': 'lz4'  # Compresión eficiente
}

producer = Producer(conf)

def delivery_report(err, msg):
    """Callback para manejar confirmaciones de entrega"""
    if err:
        print(f'Entrega fallida: {err}')
    else:
        print(f'Mensaje entregado a {msg.topic()} [{msg.partition()}]')

@app.route('/send', methods=['POST'])
def send_message():
    data = request.json
    topic = data.get('topic', 'flask-topic')
    message = data.get('message', '')
    
    # Enviar mensaje de forma asíncrona
    producer.produce(
        topic=topic,
        value=json.dumps(message).encode('utf-8'),
        key=str(hash(message)).encode('utf-8'),
        callback=delivery_report  # Callback para confirmación
    )
    
    # No flush inmediato - mejor rendimiento
    return jsonify({
        'status': 'Mensaje en cola',
        'topic': topic,
        'message': message
    })

@app.route('/flush', methods=['POST'])
def flush_messages():
    """Endpoint para forzar envío de mensajes pendientes"""
    producer.flush()
    return jsonify({'status': 'Mensajes enviados'})

if __name__ == '__main__':
    app.run(port=5000, debug=True)