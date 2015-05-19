'use strict';

module.exports = function isGitRepo(str) {
  return (/^git(\+(ssh|https?))?:\/\//i).test(str) || (/\.git\/?$/i).test(str) || (/^git@/i).test(str);
};
