app.factory("PanelVersionFactory", function PanelVersionFactory() {
  var obj = {};
  obj.panel_visible = false;

  function alternar_panel_version() {
    obj.panel_visible = !obj.panel_visible;
  }

  function consultar_panel_visible() {
    return obj.panel_visible;
  }

  obj.consultar_panel_visible = consultar_panel_visible;
  obj.alternar_panel_version = alternar_panel_version;

  return obj;
});
