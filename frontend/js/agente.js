const TOKEN_KEY = "mercado_viva_token";
const USUARIO_KEY = "mercado_viva_usuario";

const seccionLogin = document.getElementById("seccion-login");
const seccionPanel = document.getElementById("seccion-panel");
const formLogin = document.getElementById("form-login");
const mensajeLogin = document.getElementById("mensaje-login");
const formBuscar = document.getElementById("form-buscar");
const listaCasos = document.getElementById("lista-casos");
const btnSalir = document.getElementById("btn-salir");

function mostrarPanel() {
  seccionLogin.classList.add("oculto");
  seccionPanel.classList.remove("oculto");
}

function mostrarLogin() {
  seccionPanel.classList.add("oculto");
  seccionLogin.classList.remove("oculto");
}

if (localStorage.getItem(TOKEN_KEY)) {
  mostrarPanel();
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
      mensajeLogin.textContent = cuerpo.detail || "Usuario o contrasena incorrectos.";
      return;
    }

    localStorage.setItem(TOKEN_KEY, cuerpo.access_token);
    localStorage.setItem(USUARIO_KEY, username);
    mensajeLogin.textContent = "";
    formLogin.reset();
    mostrarPanel();
  } catch (error) {
    mensajeLogin.textContent = "No se pudo conectar con el servidor.";
  }
});

btnSalir.addEventListener("click", () => {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(USUARIO_KEY);
  listaCasos.innerHTML = "";
  mostrarLogin();
});

formBuscar.addEventListener("submit", async (evento) => {
  evento.preventDefault();
  listaCasos.innerHTML = "Buscando...";

  const identificacion = formBuscar.identificacion.value.trim();

  try {
    const resp = await fetch(`/historial/${encodeURIComponent(identificacion)}`);
    const cuerpo = await resp.json();

    if (!resp.ok) {
      listaCasos.innerHTML = `<p>${cuerpo.detail || "No se encontro historial para esa identificacion."}</p>`;
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
          <h3>${caso.numero_caso} — ${caso.tipo}</h3>
          <p><strong>Estado actual:</strong> <span class="estado">${caso.estado}</span></p>
          <p>${caso.descripcion}</p>
          <p class="canal">Canal de origen: ${caso.canal_origen}</p>

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
        estado: form.estado.value.trim(),
        responsable: usuario,
        canal: "tienda_fisica",
      }),
    });
    const cuerpo = await resp.json();

    if (!resp.ok) {
      const validos = (cuerpo.estados_validos_siguientes || []).join(", ");
      mensaje.textContent = `${cuerpo.detail || "No se pudo actualizar el estado."}${
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
