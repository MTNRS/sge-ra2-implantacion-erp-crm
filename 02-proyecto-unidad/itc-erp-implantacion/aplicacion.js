const $ = selector => document.querySelector(selector);
const textoSeguro = texto => String(texto ?? '').replace(/[&<>'"]/g, caracter => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[caracter]));

async function cargarEstado() {
  const estado = await (await fetch('/api/estado')).json();
  const botones = [...document.querySelectorAll('[data-perfil]')];
  botones.forEach(boton => boton.disabled = estado.instalado);
  if (!estado.instalado) {
    $('#mensaje').textContent = estado.mensaje;
    return;
  }
  const configuracion = estado.configuracion;
  $('#estadoGeneral').textContent = 'Instalación operativa';
  $('#estadoGeneral').className = 'insignia verde';
  $('#contadorModulos').textContent = estado.modulos.length;
  $('#estadoBase').textContent = 'Activa';
  $('#contadorOperaciones').textContent = estado.operaciones.length;
  $('#perfilActual').textContent = `Perfil ${configuracion.perfil}`;
  $('#mensaje').textContent = `Instalado para ${configuracion.empresa}. Para cambiar de supuesto se prepara una instalación nueva.`;
  $('#listaModulos').innerHTML = estado.modulos.map(modulo => `<article class="modulo"><b>${textoSeguro(modulo.codigo)}</b><span>${textoSeguro(modulo.nombre)}</span></article>`).join('');
  $('#operaciones').innerHTML = estado.operaciones.map(operacion => `<tr><td>${textoSeguro(operacion.accion)}</td><td>${textoSeguro(operacion.detalle)}</td><td>${textoSeguro(operacion.momento)}</td></tr>`).join('');
}

async function instalar(perfil) {
  $('#mensaje').textContent = 'Instalando perfil…';
  const respuesta = await fetch('/api/instalar', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({perfil})});
  const resultado = await respuesta.json();
  if (!respuesta.ok) { $('#mensaje').textContent = resultado.error; return; }
  await cargarEstado();
}

async function verificar() {
  const pruebas = await (await fetch('/api/verificar')).json();
  $('#contadorPruebas').textContent = `${pruebas.filter(prueba => prueba.ok).length}/${pruebas.length}`;
  $('#pruebas').innerHTML = pruebas.map(prueba => `<li class="${prueba.ok ? 'ok' : 'fallo'}"><strong>${prueba.ok ? 'OK' : 'FALLO'}</strong> · ${textoSeguro(prueba.nombre)} — ${textoSeguro(prueba.detalle)}</li>`).join('');
}

document.querySelectorAll('[data-perfil]').forEach(boton => boton.addEventListener('click', () => instalar(boton.dataset.perfil)));
$('#botonVerificar').addEventListener('click', verificar);
cargarEstado().catch(error => { $('#mensaje').textContent = `Error de conexión: ${error.message}`; });
