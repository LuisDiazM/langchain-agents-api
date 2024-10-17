# Información

Este repositorio contiene un ejemplo de como exponer un agente de langchain usando fastapi,
El agente tiene memoria conectada a una caché de redis para aplicaciones que requieren más de una 
instancia, debido a que las API son sin estado, la caché ayudará a los agentes a mantener la memoria
de sus conversaciones con una duración de 1h (TTL de redis definido para el ejemplo)

Para ello se requiere tener un API_KEY de openIA


Para correr el proyecto puede hacerlo con docker compose

```
docker compose up -d --build
```


y Puede ejecutar la API

```
curl --location 'http://localhost:8000/invoke' \
--header 'Content-Type: application/json' \
--data '{"session_id":"287292", "content":"Quien es James Rodriguez"}'
```