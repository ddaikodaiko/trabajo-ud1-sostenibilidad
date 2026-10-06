// Menú en pantallas pequeñas
(function () {
  var rail = document.querySelector(".rail");
  var boton = document.querySelector(".menu-boton");
  if (!rail || !boton) return;
  boton.addEventListener("click", function () {
    var abierto = rail.getAttribute("data-abierto") === "true";
    rail.setAttribute("data-abierto", abierto ? "false" : "true");
    boton.setAttribute("aria-expanded", abierto ? "false" : "true");
  });
})();

// Simulador del proceso de selección del IBEX ESG (Parte 2)
(function () {
  var form = document.getElementById("simulador");
  if (!form) return;
  var salida = form.querySelector("output");
  var niveles = ["A+", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-"];

  function valor(nombre) {
    var marcado = form.querySelector('input[name="' + nombre + '"]:checked');
    return marcado ? marcado.value : null;
  }

  function evaluar() {
    var universo = valor("universo");
    var nota = form.querySelector("select[name='nota']").value;
    var pacto = valor("pacto");
    var actividad = valor("actividad");
    var titulo, detalle, estado;

    if (universo === "no") {
      estado = "no";
      titulo = "No entra: se queda en el paso 1.";
      detalle = "Solo son candidatas las empresas del IBEX 35 o del IBEX Medium Cap.";
    } else if (niveles.indexOf(nota) > niveles.indexOf("C+")) {
      estado = "no";
      titulo = "No entra: se queda en el paso 2.";
      detalle = "Su calificación de Inrate (" + nota + ") está por debajo del mínimo exigido, que es C+.";
    } else if (pacto === "no") {
      estado = "no";
      titulo = "No entra: se queda en el paso 3.";
      detalle = "No supera la evaluación del Pacto Mundial de las Naciones Unidas.";
    } else if (actividad === "si") {
      estado = "no";
      titulo = "No entra: se queda en el paso 4.";
      detalle = "Supera el umbral de negocio en una actividad excluida, aunque su calificación sea buena.";
    } else {
      estado = "si";
      titulo = "Entra en el IBEX ESG.";
      detalle = "Cumple los cuatro filtros. Su peso dependerá de su capitalización ajustada por capital flotante, no de su nota (" + nota + ").";
    }
    salida.setAttribute("data-estado", estado);
    salida.innerHTML = titulo + "<span>" + detalle + "</span>";
  }

  form.addEventListener("change", evaluar);
  form.addEventListener("submit", function (e) { e.preventDefault(); });
  evaluar();
})();
