-- ============================================================
--  Mercado VIVA - MVP Gestion de PQR
--  Esquema de base de datos para Supabase (PostgreSQL)
--  Ejecutar este script en:  Supabase -> SQL Editor -> New query
-- ============================================================

create extension if not exists pgcrypto;

create table if not exists clientes (
  id uuid primary key default gen_random_uuid(),
  identificacion text unique not null,
  nombre text not null,
  creado_en timestamptz not null default now()
);

create table if not exists agentes (
  id uuid primary key default gen_random_uuid(),
  username text unique not null,
  password_hash text not null,
  nombre text not null,
  creado_en timestamptz not null default now()
);

create table if not exists casos (
  id uuid primary key default gen_random_uuid(),
  cliente_id uuid not null references clientes(id),
  tipo text not null check (tipo in ('peticion','queja','reclamo','sugerencia')),
  descripcion text not null,
  estado text not null default 'abierta' check (estado in (
    'abierta','en_proceso','pendiente_info','escalada','reabierta',
    'resuelta_cerrada','cerrada_sin_respuesta','cerrada_sin_acuerdo'
  )),
  canal_origen text not null check (canal_origen in ('web','tienda')),
  creado_en timestamptz not null default now(),
  actualizado_en timestamptz not null default now()
);

create table if not exists historial_casos (
  id uuid primary key default gen_random_uuid(),
  caso_id uuid not null references casos(id),
  estado_anterior text,
  estado_nuevo text not null,
  responsable text not null,
  canal text not null,
  fecha timestamptz not null default now()
);

-- ------------------------------------------------------------
-- Tabla: evidencias
-- Notas de texto y/o archivos (fotos, PDF) que el cliente adjunta
-- a un caso como respaldo de la PQR.
-- ------------------------------------------------------------
create table if not exists evidencias (
  id uuid primary key default gen_random_uuid(),
  caso_id uuid not null references casos(id),
  tipo text not null check (tipo in ('texto','archivo')),
  contenido_texto text,
  archivo_path text,
  archivo_nombre text,
  creado_en timestamptz not null default now()
);

create index if not exists idx_casos_cliente on casos(cliente_id);
create index if not exists idx_historial_caso on historial_casos(caso_id);
create index if not exists idx_evidencias_caso on evidencias(caso_id);

-- ------------------------------------------------------------
-- Bucket de Storage para los archivos de evidencia (privado).
-- El backend tambien lo crea solo la primera vez que se necesita
-- (ver app/models/evidencia_model.py), asi que este INSERT es
-- opcional/redundante -- lo dejamos aqui para que quede documentado
-- como parte de la infraestructura del proyecto.
-- ------------------------------------------------------------
insert into storage.buckets (id, name, public)
values ('evidencias', 'evidencias', false)
on conflict (id) do nothing;
