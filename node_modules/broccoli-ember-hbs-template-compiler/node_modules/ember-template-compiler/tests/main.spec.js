var sut = require('../lib/main');
var fs = require('fs');
var path = require('path');

describe("ember-template-compiler tests", function() {
  var result,
      template = fs.readFileSync(path.join(path.dirname(fs.realpathSync(__filename)),'file-system', 'app', 'templates', 'foo.handlebars')).toString();

  it("compiles down a handlebars template", function() {
    result = sut.precompile(template).toString();
    expect(result).toContain("outlet");
  });

});
