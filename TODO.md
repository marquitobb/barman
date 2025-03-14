# TODO List

## General

- [ ] Mejorar la documentación del proyecto.
- [ ] Refactorizar el código para mejorar la legibilidad y el mantenimiento.

## raspberry-pi/

- [ ] agregar detectar comando de voz
- [ ] Implementar la lógica para el control de los motores.
- [ ] Agregar manejo de errores robusto.
- [ ] Implementar la comunicación con la API de `server-ia`.

## server-ia/

- [ ] Implementar la lógica para la selección de ingredientes basada en el tamaño de la bebida.
- [ ] Mejorar la precisión de la interpretación de comandos en lenguaje natural.
- [ ] Agregar soporte para múltiples idiomas.
- [ ] **agents/ollama_agent.py**:
    - [ ] Mejorar la extracción de JSON de las respuestas de Ollama.
    - [ ] Implementar un mecanismo de reintento en caso de error al contactar a Ollama.
- [ ] **api/routes.py**:
    - [ ] Agregar validación de datos de entrada para los endpoints de la API.
    - [ ] Implementar manejo de errores más específico para cada ruta.

## shared/

- [ ] Definir modelos de datos comunes para la comunicación entre `raspberry-pi` y `server-ia`.
- [ ] Implementar utilidades para el manejo de errores y logs.