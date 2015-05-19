'use strict';

var transpiler = require('6to5-core');
var Filter     = require('broccoli-filter');
var clone      = require('clone');

function SixToFive(inputTree, options) {
  if (!(this instanceof SixToFive)) {
    return new SixToFive(inputTree, options);
  }

  this.inputTree = inputTree;
  this.options = options || {};
}

SixToFive.prototype = Object.create(Filter.prototype);
SixToFive.prototype.constructor = SixToFive;

SixToFive.prototype.extensions = ['js'];
SixToFive.prototype.targetExtension = 'js';

SixToFive.prototype.transform = function(string, options) {
  return transpiler.transform(string, options);
};

SixToFive.prototype.processString = function (string, relativePath) {
  var options = this.copyOptions();

  options.filename = options.sourceMapName = options.sourceFileName = relativePath;

  return this.transform(string, options).code;
};

SixToFive.prototype.copyOptions = function() {
  return clone(this.options);
};

module.exports = SixToFive;
