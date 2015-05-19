'use strict';

function Package(name, versionSpecified, versionInstalled) {
  this.name = name;
  this.versionSpecified = versionSpecified;
  this.versionInstalled = versionInstalled;
  this.needsUpdate = this.updateRequired();
}

Package.prototype = Object.create({});
Package.prototype.constructor = Package;

Package.prototype.updateRequired = function() {
  if (!this.versionInstalled) {
    return true;
  }

  var version   = this.versionSpecified;
  var isGitRepo = require('./git-repo');
  var semver    = require('semver');
  if (isGitRepo(version)) {
    var parts = version.split('#');
    if (parts.length === 2) {
      version = semver.valid(parts[1]);
      if (!version) {
        return false;
      }
    }
  }

  if (!semver.validRange(version)) {
    return false;
  }

  return !semver.satisfies(this.versionInstalled, version);
};

module.exports = Package;
