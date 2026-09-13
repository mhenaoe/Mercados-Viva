# Mercado Viva — Gestion de PQR

MVP de gestion de peticiones, quejas, reclamos y sugerencias (PQR) con
historial unificado del cliente, sin importar si radica desde la web
(rol cliente) o es atendido en tienda fisica (rol agente).

## Proceso seleccionado

El proceso cubierto es el ciclo completo de una PQR: un cliente o un
agente radica el caso (`POST /pqr`), el caso avanza por un ciclo de
estados controlado (`abierta -> en_proceso -> ... -> resuelta_cerrada`,
con posibilidad de reapertura), y cada cambio de estado queda registrado
en una bitacora de trazabilidad (`historial_casos`) con fecha, canal y
responsable. Tanto el cliente como el agente pueden consultar el
historial completo de un cliente en un unico lugar (`GET
/historial/{identificacion}`), sin importar por que canal se radico
cada caso.

## Tecnologias

- **Backend:** Python + FastAPI, organizado en capas (`routers` →
  `services` → `models`).
- **Frontend:** HTML + CSS + JavaScript vanilla, sin framework y sin
  paso de compilacion.
- **Persistencia:** Supabase (PostgreSQL gestionado), via el cliente
  oficial `supabase-py`.
- **Autenticacion:** JWT propio (`PyJWT`) + contrasenas cifradas con
  `bcrypt`.
- **Repositorio:** monorepo (`/backend` + `/frontend`).
- **Despliegue:** un unico servicio en Render; FastAPI sirve la API y
  los archivos estaticos del frontend (`StaticFiles`), por lo que no
  hace falta configurar CORS.

## Ejecucion local

1. Clona el repositorio y entra a la carpeta `backend`:
   ```bash
   cd backend
   ```
2. Crea y activa un entorno virtual:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Copia `.env.example` a `.env` y completa las variables con los datos
   reales de tu proyecto de Supabase:
   ```bash
   cp .env.example .env
   ```
5. En el **SQL Editor** de Supabase, ejecuta el script `backend/schema.sql`
   para crear las tablas `agentes`, `clientes`, `casos` e `historial`.
6. Levanta el servidor (desde la carpeta `backend`):
   ```bash
   uvicorn app.main:app --reload
   ```
7. Abre `http://localhost:8000` para la vista de cliente, o
   `http://localhost:8000/agente.html` para la vista de agente.

## Pruebas

Desde la carpeta `backend`, con el entorno virtual activo:

```bash
pytest
```

Las pruebas no requieren conexion a Supabase: sustituyen la capa de
acceso a datos por una version en memoria (ver `backend/tests/conftest.py`).

## Despliegue

URL publicada: [URL_PENDIENTE]

## Integrantes

[INTEGRANTES_PENDIENTE]
