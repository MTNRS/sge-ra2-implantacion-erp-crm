const $ = selector => document.querySelector(selector);
const textoSeguro = texto => String(texto ?? '').replace(/[&<>'"]/g, caracter => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[caracter]));

const areas = {
  clientes: {codigo: 'crm', titulo: 'Clientes', descripcion: 'Alta y consulta de clientes para el equipo comercial y de soporte.', campos: [['nombre', 'Nombre o empresa', 'text'], ['email', 'Correo de contacto', 'email']]},
  incidencias: {codigo: 'incidencias', titulo: 'Soporte técnico', descripcion: 'Registro inicial de incidencias del servicio ITC.', campos: [['asunto', 'Asunto de la incidencia', 'text'], ['estado', 'Estado', 'select']]},
  equipos: {codigo: 'inventario', titulo: 'Inventario', descripcion: 'Control básico de equipos asociados al servicio.', campos: [['nombre', 'Equipo o activo', 'text'], ['estado', 'Estado', 'select']]}
};

let estadoActual = null;
let vistaActual = 'resumen';

async function pedir(ruta, opciones = {}) {
  const respuesta = await fetch(ruta, opciones);
  const datos = await respuesta.json();
  if (!respuesta.ok) throw new Error(datos.error || 'No se pudo completar la operación.');
  return datos;
}

function pintarEstado(estado) {
  estadoActual = estado;
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
  $('#mensaje').textContent = `Perfil ${configuracion.perfil} activo. Puedes cambiarlo sin perder los registros del entorno local.`;
  $('#listaModulos').innerHTML = estado.modulos.map(modulo => `<article class="modulo"><b>${textoSeguro(modulo.codigo)}</b><span>${textoSeguro(modulo.nombre)}</span></article>`).join('');
  $('#operaciones').innerHTML = estado.operaciones.map(operacion => `<tr><td>${textoSeguro(operacion.accion)}</td><td>${textoSeguro(operacion.detalle)}</td><td>${textoSeguro(operacion.momento)}</td></tr>`).join('');
  document.querySelectorAll('[data-perfil]').forEach(boton => boton.classList.toggle('seleccionado', boton.dataset.perfil === configuracion.perfil));
}

async function cargarEstado() {
  pintarEstado(await pedir('/api/estado'));
}

async function cambiarPerfil(perfil) {
  $('#mensaje').textContent = `Actualizando el perfil ${perfil}…`;
  try {
    pintarEstado(await pedir('/api/perfil', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({perfil})}));
    if (areas[vistaActual]) await mostrarArea(vistaActual);
  } catch (error) {
    $('#mensaje').textContent = error.message;
  }
}

async function verificar() {
  try {
    const pruebas = await pedir('/api/verificar');
    $('#contadorPruebas').textContent = `${pruebas.filter(prueba => prueba.ok).length}/${pruebas.length}`;
    $('#pruebas').innerHTML = pruebas.map(prueba => `<li class="${prueba.ok ? 'ok' : 'fallo'}"><strong>${prueba.ok ? 'OK' : 'FALLO'}</strong> · ${textoSeguro(prueba.nombre)} — ${textoSeguro(prueba.detalle)}</li>`).join('');
  } catch (error) {
    $('#pruebas').innerHTML = `<li class="fallo">${textoSeguro(error.message)}</li>`;
  }
}

function activo(codigo) {
  return estadoActual && estadoActual.modulos.some(modulo => modulo.codigo === codigo);
}

function control(campo) {
  const [nombre, etiqueta, tipo] = campo;
  if (tipo === 'select') return `<label>${etiqueta}<select name="${nombre}" required><option value="abierto">Abierto</option><option value="en revisión">En revisión</option><option value="operativo">Operativo</option></select></label>`;
  return `<label>${etiqueta}<input name="${nombre}" type="${tipo}" required maxlength="100"></label>`;
}

async function mostrarArea(area) {
  const definicion = areas[area];
  vistaActual = area;
  if (!estadoActual || !estadoActual.instalado) {
    $('#zonaOperativa').innerHTML = '<p class="pendiente">Configura un perfil antes de utilizar esta área.</p>';
    return;
  }
  if (!activo(definicion.codigo)) {
    $('#zonaOperativa').innerHTML = `<div class="aviso"><strong>${definicion.titulo} no está activo en este perfil.</strong><p>Cambia al perfil de soporte para habilitar este módulo.</p></div>`;
    return;
  }
  const registros = await pedir(`/api/datos/${area}`);
  const columnas = definicion.campos.map(campo => campo[0]);
  $('#zonaOperativa').innerHTML = `
    <div class="operativa-cabecera"><div><h3>${definicion.titulo}</h3><p class="texto-secundario">${definicion.descripcion}</p></div><span class="insignia azul">${registros.length} registros</span></div>
    <form id="formularioArea" class="formulario" data-area="${area}">${definicion.campos.map(control).join('')}<button class="boton-primario" type="submit">Registrar</button></form>
    <div class="tabla-contenedor"><table><thead><tr>${columnas.map(columna => `<th>${textoSeguro(columna)}</th>`).join('')}<th>Creado</th></tr></thead><tbody>${registros.length ? registros.map(registro => `<tr>${columnas.map(columna => `<td>${textoSeguro(registro[columna])}</td>`).join('')}<td>${textoSeguro(registro.creado)}</td></tr>`).join('') : `<tr><td colspan="${columnas.length + 1}" class="pendiente">Todavía no hay registros. Añade el primero.</td></tr>`}</tbody></table></div>`;
  $('#formularioArea').addEventListener('submit', guardarRegistro);
}

async function guardarRegistro(evento) {
  evento.preventDefault();
  const formulario = evento.currentTarget;
  const area = formulario.dataset.area;
  const datos = Object.fromEntries(new FormData(formulario));
  const boton = formulario.querySelector('button');
  boton.disabled = true;
  try {
    await pedir(`/api/datos/${area}`, {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(datos)});
    await cargarEstado();
    await mostrarArea(area);
  } catch (error) {
    $('#mensaje').textContent = error.message;
  } finally {
    boton.disabled = false;
  }
}

function navegar(evento) {
  evento.preventDefault();
  const vista = evento.currentTarget.dataset.vista;
  document.querySelectorAll('[data-vista]').forEach(enlace => enlace.classList.toggle('activo', enlace.dataset.vista === vista));
  if (areas[vista]) return mostrarArea(vista);
  vistaActual = vista;
  const destino = vista === 'configuracion' ? '#implantacion' : `#${vista}`;
  document.querySelector(destino).scrollIntoView({behavior:'smooth', block:'start'});
}

document.querySelectorAll('[data-perfil]').forEach(boton => boton.addEventListener('click', () => cambiarPerfil(boton.dataset.perfil)));
document.querySelectorAll('[data-vista]').forEach(enlace => enlace.addEventListener('click', navegar));
$('#botonVerificar').addEventListener('click', verificar);
cargarEstado().catch(error => { $('#mensaje').textContent = `Error de conexión: ${error.message}`; });
