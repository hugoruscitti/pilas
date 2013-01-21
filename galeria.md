---
layout: base 
title: Imágenes
---


<!-- These files are needed for FancyBox -->
<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js"></script>
<link href="./js/jquery.fancybox/jquery.fancybox.css" rel="stylesheet" type="text/css"/>
<script src="./js/jquery.fancybox/jquery.fancybox.pack.js" type="text/javascript"></script>

<link href="./js/jquery.fancybox/helpers/jquery.fancybox-buttons.css?v=2.0.5"  rel="stylesheet" type="text/css"/>
<script type="text/javascript" src="./js/jquery.fancybox/helpers/jquery.fancybox-buttons.js?v=2.0.5"></script>

<link href="./css/pwi.css" rel="stylesheet" type="text/css"/>
<script src="./js/jquery.pwi-min.js" type="text/javascript"></script>


<script type="text/javascript">

      $(document).ready(function() {
        var $viewerJs, $viewerName;

        $viewerName = "FancyBox";
        $viewerCss  = "js/jquery.fancybox/jquery.fancybox.css";
        $viewerJs   = "js/jquery.fancybox/jquery.fancybox.pack.js";

        $("#jqueryVersion").text($().jquery);
        $("#viewername").text($viewerName);
        $("#viewernameCss").text($viewerCss);
        $("#viewernameJs").text($viewerJs);
        $("a#inline").fancybox({closeClick: false});

        var settings = {
          username: 'hugoruscitti',
          maxresults: 50,
          mode: 'album',
          popupPlugin: "fancybox",
          showAlbumDescription: false,
          showAlbumThumbs: false,
          showAlbumdate: false,
          thumbSize:128,

          fancybox_config: {
                config_photos: {
                    closeClick : false,
                    nextEffect : 'none',
			        closeEffect: 'none',
                    loop       : false,
                    beforeLoad : formatPhotoTitleFancyBox,
                    helpers	   : {
                        buttons	: {}
                    }
                },
            },
        };

        settings.album = 'PilasEngineEventos';
        $("#container-eventos").pwi(settings);

        settings.album = 'PilasEngineSistema';
        $("#container-sistema").pwi(settings);

        settings.album = 'PilasEngineEquipos';
        $("#container-equipos").pwi(settings);

        settings.album = 'PilasEngineEjemplos';
        $("#container-ejemplos").pwi(settings);

      });
</script>

# Galería de imágenes

## Ejemplos

<div id="container-ejemplos"> </div>

## Equipos

<div id="container-equipos"> </div>

## Sistemas

<div id="container-sistema"> </div>


## Eventos

<div id="container-eventos"> </div>

