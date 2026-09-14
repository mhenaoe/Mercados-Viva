const form = document.getElementById("form-pqr");
const resultado = document.getElementById("resultado-pqr");
const formHistorial = document.getElementById("form-historial");
const listaCasos = document.getElementById("lista-casos");

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

form.addEventListener("submit", async (evento) => {
  evento.preventDefault();
  resultado.textContent = "Enviando...";

  const datos = {
    identificacion: form.identificacion.value.trim(),
    nombre: form.nombre.value.trim(),
    tipo: form.tipo.value,
    descripcion: form.descripcion.value.trim(),
    canal_origen: "web",
  };

  try {
    const resp = await fetch("/pqr", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(datos),
    });
    const cuerpo = await resp.json();

    if (!resp.ok) {
      resultado.textContent = `Error: ${mensajeDeError(cuerpo)}`;
      return;
    }

    resultado.textContent = `Caso radicado con exito. Numero de caso: ${cuerpo.id}`;
    await subirEvidencia(cuerpo.id);
    form.reset();
  } catch (error) {
    resultado.textContent = "No se pudo conectar con el servidor.";
  }
});

// Sube (si hay algo que subir) el texto y/o los archivos de evidencia
// para el caso recien creado. Es un segundo POST porque /pqr solo acepta
// JSON y los archivos necesitan multipart/form-data.
async function subirEvidencia(casoId) {
  const texto = form.evidenciaTexto.value.trim();
  const archivos = form.evidenciaArchivos.files;

  if (!texto && archivos.length === 0) {
    return;
  }

  const formData = new FormData();
  if (texto) formData.append("texto", texto);
  for (const archivo of archivos) {
    formData.append("archivos", archivo);
  }

  try {
    const resp = await fetch(`/casos/${casoId}/evidencias`, {
      method: "POST",
      body: formData,
    });
    const cuerpo = await resp.json();

    if (!resp.ok) {
      resultado.textContent += ` (evidencia no guardada: ${mensajeDeError(cuerpo)})`;
      return;
    }

    resultado.textContent += " Evidencia adjuntada.";
  } catch (error) {
    resultado.textContent += " (no se pudo adjuntar la evidencia: sin conexion)";
  }
}

formHistorial.addEventListener("submit", async (evento) => {
  evento.preventDefault();
  listaCasos.innerHTML = "Buscando...";

  const identificacion = formHistorial.identificacion.value.trim();

  try {
    const resp = await fetch(`/historial/${encodeURIComponent(identificacion)}`);
    const cuerpo = await resp.json();

    if (!resp.ok) {
      listaCasos.innerHTML = `<p>${cuerpo.detail ? mensajeDeError(cuerpo) : "No se encontro historial para esa identificacion."}</p>`;
      return;
    }

    if (cuerpo.casos.length === 0) {
      listaCasos.innerHTML = "<p>Este cliente aun no tiene casos registrados.</p>";
      return;
    }

    listaCasos.innerHTML = cuerpo.casos
      .map(
        (caso) => `
          <article class="caso">
            <h3>${caso.id} — ${caso.tipo}</h3>
            <p><strong>Estado actual:</strong> ${caso.estado}</p>
            <p>${caso.descripcion}</p>
            <p class="canal">Canal de origen: ${caso.canal_origen}</p>
            ${renderizarEvidencias(caso.evidencias)}
          </article>
        `
      )
      .join("");
  } catch (error) {
    listaCasos.innerHTML = "<p>No se pudo conectar con el servidor.</p>";
  }
});

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
