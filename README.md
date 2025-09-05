# Sistema de Mensajería con Flask y Kafka

## Descripción del Proyecto

Este proyecto implementa un sistema de mensajería distribuido utilizando Flask como productor de mensajes y un consumidor Kafka para procesamiento de mensajes. El sistema permite enviar mensajes a través de una API REST y procesarlos de manera confiable con Kafka.

## Arquitectura del Sistema

El sistema consta de dos componentes principales:

1. **App (Productor)**: Una aplicación Flask que expone endpoints REST para enviar mensajes a Kafka
2. **Worker (Consumidor)**: Un proceso que consume mensajes de Kafka y los procesa

## Características Principales

### App (Productor)
- API REST con endpoints para enviar mensajes y forzar el envío
- Configuración optimizada de Kafka con confirmaciones de entrega (acks=all)
- Mecanismo de reintentos automáticos para mayor confiabilidad
- Compresión de mensajes para mejor rendimiento
- Callbacks para reporte de entrega de mensajes

### Worker (Consumidor)
- Consumo confiable de mensajes con control manual de offsets
- Procesamiento robusto con manejo de errores
- Configuración optimizada para lectura de mensajes confirmados
- Soporte para múltiples particiones y topics

## Requisitos del Sistema

- Python 3.7+
- Kafka 3.9+ ejecutándose en localhost:9092
- Librerías Python:
  - confluent-kafka
  - flask
  - json

## Instalación y Configuración

1. Instalar las dependencias:
```bash
pip install confluent-kafka flask
```

2. Asegurarse que Kafka esté ejecutándose:
```bash
# Iniciar Zookeeper (si es necesario)
zookeeper-server-start.sh config/zookeeper.properties

# Iniciar Kafka
kafka-server-start.sh config/server.properties
```

3. Crear el topic de Kafka:
```bash
kafka-topics.sh --create --topic flask-topic --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1
```

## Uso del Sistema

### Iniciar la aplicación Flask (Productor)
```bash
python app.py
```

### Iniciar el worker (Consumidor)
```bash
python worker.py
```

### Enviar mensajes a través de la API
```bash
curl -X POST http://localhost:5000/send \
  -H "Content-Type: application/json" \
  -d '{"message": "Hola Kafka", "topic": "flask-topic"}'
```

### Forzar el envío de mensajes pendientes
```bash
curl -X POST http://localhost:5000/flush
```

## Configuración de Kafka

El proyecto está configurado para conectarse a un clúster Kafka local en el puerto 9092. Para conectar a un clúster diferente, modifica la configuración en ambos archivos:

```python
conf = {
    'bootstrap.servers': 'tu-servidor-kafka:9092',
    # ... resto de configuración
}
```

## Manejo de Errores

El sistema incluye mecanismos robustos de manejo de errores:

- Reintentos automáticos en caso de fallos de red
- Confirmación manual de offsets solo después de procesamiento exitoso
- Callbacks para reportar el estado de entrega de mensajes
- Manejo de excepciones en el procesamiento de mensajes

## Monitorización

Para monitorizar el funcionamiento del sistema:

1. Verificar los logs de la aplicación Flask
2. Revisar los logs del consumidor Kafka
3. Usar herramientas de línea de comandos de Kafka:
```bash
# Ver mensajes en el topic
kafka-console-consumer.sh --topic flask-topic --from-beginning --bootstrap-server localhost:9092

# Ver estado de los consumidores
kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group flask-consumer-group --describe
```

## Mejoras Futuras

- Implementar autenticación y SSL para Kafka
- Agregar métricas y monitorización con Prometheus
- Implementar dead letter queue para mensajes problemáticos
- Añadir sistema de retry con backoff exponencial
- Implementar serialización Avro para los mensajes

## Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.
