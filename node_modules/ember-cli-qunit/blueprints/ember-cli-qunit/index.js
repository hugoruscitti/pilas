module.exports = {
  normalizeEntityName: function() {
    // this prevents an error when the entityName is
    // not specified (since that doesn't actually matter
    // to us
  },

  afterInstall: function() {
    var addonContext = this;

    return this.addBowerPackageToProject('qunit', '~1.15.0')
      .then(function() {
        return addonContext.addBowerPackageToProject('stefanpenner/ember-cli-shims', '0.0.3');
      })
      .then(function() {
        return addonContext.addBowerPackageToProject('ember-qunit-notifications', '0.0.4');
      })
      .then(function() {
        return addonContext.addBowerPackageToProject('ember-qunit', '0.1.8');
      });
  }
};
