const TOKEN_KEY = "mercado_viva_token";
const USUARIO_KEY = "mercado_viva_usuario";

const seccionLogin = document.getElementById("seccion-login");
const seccionPanel = document.getElementById("seccion-panel");
const seccionRadicar = document.getElementById("seccion-radicar");
const formLogin = document.getElementById("form-login");
const mensajeLogin = document.getElementById("mensaje-login");
const formBuscar = document.getElementById("form-buscar");
const listaCasos = document.getElementById("lista-casos");
const btnSalir = document.getElementById("btn-salir");
const formPqrAgente = document.getElementById("form-pqr-agente");
const resultadoPqrAgente = document.getElementById("resultado-pqr-agente");
const barraSesion = document.getElementById("barra-sesion");
const horaInicioSesion = document.getElementById("hora-inicio-sesion");
const tiempoRestanteSesion = document.getElementById("tiempo-restante-sesion");

let intervaloSesion = null;

// Decodifica el payload de un JWT (sin verificar la firma: eso ya lo hizo
// el backend). Se usa solo para mostrar "iat"/"exp" en la interfaz.
function decodificarJWT(token) {
  let base64 = token.split(".")[1].replace(/-/g, "+").replace(/_/g, "/");
  base64 += "=".repeat((4 - (base64.length % 4)) % 4);
  return JSON.parse(atob(base64));
}

// Muestra la hora de inicio de sesion y arranca un cronometro que cuenta
// hacia atras hasta que expire el JWT (2 horas, ver JWT_EXP_MINUTES en el
// backend). Al llegar a cero, cierra la sesion automaticamente.
function iniciarCronometroSesion(token) {
  let payload;
  try {
    payload = decodificarJWT(token);
  } catch (error) {
    return;
  }
  if (!payload.iat || !payload.exp) return;

  const expiraEn = payload.exp * 1000;
  horaInicioSesion.textContent = new Date(payload.iat * 1000).toLocaleTimeString();
  barraSesion.classList.remove("oculto");

  function actualizar() {
    const restanteMs = expiraEn - Date.now();
    if (restanteMs <= 0) {
      tiempoRestanteSesion.textContent = "expirada";
      cerrarSesion();
      return;
    }
    const totalSeg = Math.floor(restanteMs / 1000);
    const horas = Math.floor(totalSeg / 3600);
    const minutos = Math.floor((totalSeg % 3600) / 60);
    const segundos = totalSeg % 60;
    tiempoRestanteSesion.textContent = `${horas}:${String(minutos).padStart(2, "0")}:${String(segundos).padStart(2, "0")}`;
  }

  if (intervaloSesion) clearInterval(intervaloSesion);
  actualizar();
  intervaloSesion = setInterval(actualizar, 1000);
}

function cerrarSesion() {
  if (intervaloSesion) clearInterval(intervaloSesion);
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(USUARIO_KEY);
  listaCasos.innerHTML = "";
  barraSesion.classList.add("oculto");
  mostrarLogin();
}

// FastAPI/Pydantic devuelve los errores 422 como una lista en "detail",
// cada uno con "loc" (el campo que fallo) y "msg". Esta funcion arma un
// mensaje legible campo por campo en vez de mostrar la lista cruda.
function mensajeDeError(cuerpo) {
  if (Array.isArray(cuerpo?.detail)) {
    return cuerpo.detail
      .map((err) => {
        const campo = Array.isArray(err.loc) ? err.loc[err.loc.length - 1] : "campo";
        return `${campo}: ${err.msg}`;
      })
      .join(" | ");
  }
  return cuerpo?.detail || "Ocurrio un error inesperado.";
}

function mostrarPanel() {
  seccionLogin.classList.add("oculto");
  seccionRadicar.classList.remove("oculto");
  seccionPanel.classList.remove("oculto");
}

function mostrarLogin() {
  seccionRadicar.classList.add("oculto");
  seccionPanel.classList.add("oculto");
  seccionLogin.classList.remove("oculto");
}

if (localStorage.getItem(TOKEN_KEY)) {
  mostrarPanel();
  iniciarCronometroSesion(localStorage.getItem(TOKEN_KEY));
}

formLogin.addEventListener("submit", async (evento) => {
  evento.preventDefault();
  mensajeLogin.textContent = "Ingresando...";

  const username = formLogin.username.value.trim();

  try {
    const resp = await fetch("/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password: formLogin.password.value }),
    });
    const cuerpo = await resp.json();

    if (!resp.ok) {
      mensajeLogin.textContent = cuerpo.detail ? mensajeDeError(cuerpo) : "Usuario o contrasena incorrectos.";
      return;
    }

    localStorage.setItem(TOKEN_KEY, cuerpo.access_token);
    localStorage.setItem(USUARIO_KEY, username);
    mensajeLogin.textContent = "";
    formLogin.reset();
    mostrarPanel();
    iniciarCronometroSesion(cuerpo.access_token);
  } catch (error) {
    mensajeLogin.textContent = "No se pudo conectar con el servidor.";
  }
});

btnSalir.addEventListener("click", cerrarSesion);

formPqrAgente.addEventListener("submit", async (evento) => {
  evento.preventDefault();
  resultadoPqrAgente.textContent = "Enviando...";

  const datos = {
    identificacion: formPqrAgente.identificacion.value.trim(),
    nombre: formPqrAgente.nombre.value.trim(),
    tipo: formPqrAgente.tipo.value,
    descripcion: formPqrAgente.descripcion.value.trim(),
    canal_origen: "tienda",
  };

  try {
    const resp = await fetch("/pqr", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(datos),
    });
    const cuerpo = await resp.json();

    if (!resp.ok) {
      resultadoPqrAgente.textContent = `Error: ${mensajeDeError(cuerpo)}`;
      return;
    }

    resultadoPqrAgente.textContent = `Caso radicado con exito. Numero de caso: ${cuerpo.id}`;
    formPqrAgente.reset();
  } catch (error) {
    resultadoPqrAgente.textContent = "No se pudo conectar con el servidor.";
  }
});

formBuscar.addEventListener("submit", async (evento) => {
  evento.preventDefault();
  listaCasos.innerHTML = "Buscando...";

  const identificacion = formBuscar.identificacion.value.trim();

  try {
    const resp = await fetch(`/historial/${encodeURIComponent(identificacion)}`);
    const cuerpo = await resp.json();

    if (!resp.ok) {
      listaCasos.innerHTML = `<p>${cuerpo.detail ? mensajeDeError(cuerpo) : "No se encontro historial para esa identificacion."}</p>`;
      return;
    }

    renderizarCasos(cuerpo.casos);
  } catch (error) {
    listaCasos.innerHTML = "<p>No se pudo conectar con el servidor.</p>";
  }
});

function renderizarCasos(casos) {
  if (casos.length === 0) {
    listaCasos.innerHTML = "<p>Este cliente aun no tiene casos registrados.</p>";
    return;
  }

  listaCasos.innerHTML = casos
    .map(
      (caso) => `
        <article class="caso" data-caso-id="${caso.id}">
          <h3>${caso.id} — ${caso.tipo}</h3>
          <p><strong>Estado actual:</strong> <span class="estado">${caso.estado}</span></p>
          <p>${caso.descripcion}</p>
          <p class="canal">Canal de origen: ${caso.canal_origen}</p>
          ${renderizarEvidencias(caso.evidencias)}

          <form class="form-actualizar-estado">
            <label>Nuevo estado</label>
            <input type="text" name="estado" placeholder="ej: en_proceso" required />
            <button type="submit">Actualizar</button>
          </form>
          <p class="mensaje-estado"></p>
        </article>
      `
    )
    .join("");

  listaCasos.querySelectorAll(".form-actualizar-estado").forEach((form) => {
    form.addEventListener("submit", actualizarEstado);
  });
}

function renderizarEvidencias(evidencias) {
  if (!evidencias || evidencias.length === 0) {
    return "";
  }

  const items = evidencias
    .map((ev) =>
      ev.tipo === "texto"
        ? `<li>${ev.contenido_texto}</li>`
        : `<li><a href="${ev.archivo_url}" target="_blank" rel="noopener">${ev.archivo_nombre}</a></li>`
    )
    .join("");

  return `<div class="evidencias"><strong>Evidencia:</strong><ul>${items}</ul></div>`;
}

async function actualizarEstado(evento) {
  evento.preventDefault();
  const form = evento.target;
  const articulo = form.closest(".caso");
  const casoId = articulo.dataset.casoId;
  const mensaje = articulo.querySelector(".mensaje-estado");
  const token = localStorage.getItem(TOKEN_KEY);
  const usuario = localStorage.getItem(USUARIO_KEY) || "agente";

  mensaje.textContent = "Actualizando...";

  try {
    const resp = await fetch(`/casos/${casoId}`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        estado_nuevo: form.estado.value.trim(),
        responsable: usuario,
      }),
    });
    const cuerpo = await resp.json();

    if (!resp.ok) {
      const validos = (cuerpo.estados_validos_siguientes || []).join(", ");
      mensaje.textContent = `${mensajeDeError(cuerpo)}${
        validos ? ` Estados validos: ${validos}.` : ""
      }`;
      return;
    }

    articulo.querySelector(".estado").textContent = cuerpo.estado;
    mensaje.textContent = "Estado actualizado.";
    form.reset();
  } catch (error) {
    mensaje.textContent = "No se pudo conectar con el servidor.";
  }
}
