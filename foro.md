---
layout: base
title: Comunidad
css: foro.css
---


<script>
  anterior_alto = -100;
  anterior_url = "...";

  /*
   * Cambia el tamaño del contenedor de iframe.
   */
  function redimensionar_iframe_desde_respuesta(elementos, url) {
    var tamano = elementos.split(',');
    var contenedor = document.getElementById('contenedor-iframe');
    

    if (tamano[0] != anterior_alto) {
        anterior_alto = tamano[0];
        //console.log("Cambió el tamaño del iframe, redimensionando contenedor ...");
        contenedor.style.width = tamano[1] + 'px';
        contenedor.style.height = tamano[0] + 'px';
        iframe.style.height = "100%";
    }

    if (anterior_url != url) {
        //console.log("Cambio la URL, se solicita redimensionar...");
        iframe.style.height = "600px"; // tamano minimo...
        anterior_url = url;
        anterior_alto = 1;
        iframe.contentWindow.postMessage('sizing?', 'http://foro-pilasengine.com.ar');
    }
    window.contenedor = contenedor;
  }

  /* 
   * Procesa el cambio de tamaño del iframe.
   */
  handleSizingResponse = function(e) {

    if (e.origin == 'http://foro-pilasengine.com.ar') {
      var action = e.data.split(':')[0];
      var url = 'http:' + e.data.split(':')[3];

      if (action == 'sizing') {
        redimensionar_iframe_desde_respuesta(e.data.split(':')[1], url);
      }
    }
}


function sincronizar_tamano_iframe() {
  /* console.log("sincronizando..."); */
    iframe = document.getElementById('ifrm');
    iframe.contentWindow.postMessage('sizing?', 'http://foro-pilasengine.com.ar');
    return true;
}

window.onload = function() {
    window.addEventListener('message', handleSizingResponse, false);
    sincronizar_tamano_iframe();
    setInterval(sincronizar_tamano_iframe, 1000);
}
</script>


<a href='http://foro-pilasengine.com.ar/' target="_blank">Abrir el foro en una ventana nueva</a>

<div id='contenedor-iframe' style="width: 886px;">
    <iframe id="ifrm" src="http://foro-pilasengine.com.ar" width='110%' height="900px" frameborder="0">&nbsp;</iframe>
</div>
