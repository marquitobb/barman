# Barman

Bot as a service to make drinks

## Posible arquitecture

```
barman/
├── raspberry-pi/            # Código para el control de hardware
│   ├── main.py              # Punto de entrada principal
│   ├── controllers/         # Controladores de hardware
│   │   ├── relay_controller.py
│   │   └── motor_controller.py
│   ├── api/                 # Cliente API para comunicación
│   │   ├── client.py
│   │   └── models.py
│   └── config.py            # Configuración
│
├── brain-ia/                # Servicio de IA
│   ├── main.py              # Aplicación FastAPI
│   ├── api/                 # Endpoints de la API
│   │   ├── routes.py
│   │   └── models.py
│   ├── agents/              # Agentes de IA
│   │   ├── ollama_agent.py
│   │   └── llama3_agent.py
│   ├── services/            # Servicios de negocio
│   │   └── drink_service.py
│   └── config.py            # Configuración
│
└── shared/                  # Código compartido
    ├── models/              # Modelos de datos comunes
    └── utils/               # Utilidades comunes
```