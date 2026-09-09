-- ============================================================
--  Mercado VIVA - MVP Gestion de PQR
--  Esquema de base de datos para Supabase (PostgreSQL)
--  Ejecutar este script en:  Supabase -> SQL Editor -> New query
-- ============================================================

-- ------------------------------------------------------------
-- Tabla: agentes
-- RNF1 (Seguridad): la vista de agente esta protegida por
-- autenticacion (usuario + contrasena). Las contrasenas se
-- guardan SIEMPRE como hash bcrypt, nunca en texto plano.
-- ------------------------------------------------------------
create table if not exists agentes (
    id              bigint generated always as identity primary key,
    username        text unique not null,
    password_hash   text not null,            -- hash bcrypt
    nombre          text not null,
    fecha_registro  timestamptz not null default now()
);

-- ------------------------------------------------------------
-- Tabla: clientes
-- Un unico registro por identificacion (documento o email).
-- Regla de negocio: toda PQR queda asociada a un unico cliente
-- identificado de forma consistente sin importar el canal.
-- ------------------------------------------------------------
create table if not exists clientes (
    id              bigint generated always as identity primary key,
    identificacion  text unique not null,     -- documento o email
    fecha_registro  timestamptz not null default now()
);

-- ------------------------------------------------------------
-- Tabla: casos  (las PQR)
-- tipo: peticion | queja | reclamo | sugerencia
-- canal_origen: web | tienda_fisica
-- estado: ciclo definido en el punto 1.3 del documento
-- ------------------------------------------------------------
create table if not exists casos (
    id                   bigint generated always as identity primary key,
    numero_caso          text unique not null,
    cliente_id           bigint not null references clientes(id),
    tipo                 text not null check (tipo in ('peticion','queja','reclamo','sugerencia')),
    descripcion          text not null,
    estado               text not null default 'Abierta',
    canal_origen         text not null check (canal_origen in ('web','tienda_fisica')),
    fecha_creacion       timestamptz not null default now(),
    fecha_actualizacion  timestamptz not null default now()
);

-- ------------------------------------------------------------
-- Tabla: historial  (bitacora de trazabilidad)
-- Regla de negocio: toda actualizacion de estado o respuesta
-- queda registrada con fecha, canal y responsable.
-- ------------------------------------------------------------
create table if not exists historial (
    id               bigint generated always as identity primary key,
    caso_id          bigint not null references casos(id),
    estado_anterior  text,
    estado_nuevo     text not null,
    canal            text not null,
    responsable      text not null,
    respuesta        text,
    fecha            timestamptz not null default now()
);

-- Indices para acelerar las consultas de historial unificado
create index if not exists idx_casos_cliente   on casos(cliente_id);
create index if not exists idx_historial_caso  on historial(caso_id);
