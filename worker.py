# consumer_kafka.py
from confluent_kafka import Consumer, KafkaException
import json
import sys

# Configuración mejorada
conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'flask-consumer-group',
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': False,  # Control manual de offsets
    'isolation.level': 'read_committed'  # Solo mensajes confirmados
}

consumer = Consumer(conf)
topics = ['flask-topic']

def msg_process(msg):
    """Procesamiento de mensajes recibidos"""
    try:
        value = json.loads(msg.value().decode('utf-8'))
        print(f"""
        [Nuevo mensaje]
          Topic: {msg.topic()}
          Partición: {msg.partition()}
          Offset: {msg.offset()}
          Clave: {msg.key().decode('utf-8')}
          Valor: {value}
        """)
        
        # Procesamiento del mensaje aquí...
        
        # Confirmar offset después de procesar
        consumer.commit(msg)
        return True
        
    except Exception as e:
        print(f"Error procesando mensaje: {str(e)}")
        return False

try:
    consumer.subscribe(topics)
    
    while True:
        msg = consumer.poll(timeout=1.0)
        
        if msg is None:
            continue
            
        if msg.error():
            if msg.error().code() == KafkaException._PARTITION_EOF:
                # Fin de partición
                continue
            else:
                print(f"Error: {msg.error()}")
                break
                
        # Procesar mensaje
        if not msg_process(msg):
            # Manejar errores de procesamiento
            pass

except KeyboardInterrupt:
    print("Cancelado por usuario")
    
finally:
    # Cerrar limpiamente
    consumer.close()