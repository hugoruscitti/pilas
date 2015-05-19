'use strict';

var path = require('path');
var fs   = require('fs');

module.exports = {
  name: 'Ember CLI QUnit',

  blueprintsPath: function() {
    return path.join(__dirname, 'blueprints');
  },

  included: function included(app) {
    this._super.included(app);

    if (app.tests) {
      var fileAssets = [
        app.bowerDirectory + '/qunit/qunit/qunit.js',
        app.bowerDirectory + '/qunit/qunit/qunit.css',
        app.bowerDirectory + '/qunit-notifications/index.js',
      ];

      var imgAssets = [
        app.bowerDirectory + '/ember-qunit-notifications/passed.png',
        app.bowerDirectory + '/ember-qunit-notifications/failed.png',
      ];

      app.import(app.bowerDirectory + '/ember-qunit/dist/named-amd/main.js', {
        type: 'test',
        exports: {
          'ember-qunit': [
            'globalize',
            'moduleFor',
            'moduleForComponent',
            'moduleForModel',
            'test',
            'setResolver'
          ]
        }
      });

      app.import(app.bowerDirectory + '/ember-cli-shims/test-shims.js', {
        type: 'test',
        exports: {
          'qunit': ['default']
        }
      });

      fileAssets.forEach(function(file){
        app.import(file, {
          type: 'test'
        });
      });

      imgAssets.forEach(function(img){
        app.import(img, {
          type: 'test',
          destDir: 'assets'
        });
      });
    }
  },

  contentFor: function(type) {
    if (type === 'test-body') {
      return this._readTemplate('test-body');
    }
  },

  _readTemplate: function(name) {
    return fs.readFileSync(path.join(__dirname, 'templates', name + '.html'));
  }
};
