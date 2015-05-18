'use strict';

module.exports = {
  name: 'ember-cli-gravatar',

  included: function included(app) {
    this.app = app;
    this._super.included(app);

    app.import(app.bowerDirectory + '/JavaScript-MD5/js/md5.js');
  }
};
