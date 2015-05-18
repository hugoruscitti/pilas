'use strict';

var fs     = require('fs');
var expect = require('chai').expect;
var broccoli = require('broccoli');
var path = require('path');
var to5 = require('./index');

var builder;
var inputPath = path.join(__dirname, 'fixtures');

function build(path, options) {
  builder = new broccoli.Builder(to5(path, options));

  return builder.build();
}

describe('options', function() {


  var options, toFive;

  before(function() {
    options = {
      foo: 1,
      bar: {
        baz: 1
      }
    };

   toFive = new to5('', options);
  });

  it('are cloned', function() {
    var transpilerOptions;

    toFive.transform = function(string, options) {
      transpilerOptions = options;
      return { code: {} };
    }

    expect(transpilerOptions).to.eql(undefined);
    toFive.processString('path', 'relativePath');

    expect(transpilerOptions.foo).to.eql(1);
    expect(transpilerOptions.bar.baz).to.eql(1);

    options.foo = 2;
    options.bar.baz = 2;

    expect(transpilerOptions.foo).to.eql(1);
    expect(transpilerOptions.bar.baz).to.eql(1);
  });

  it('correct fileName, sourceMapName, sourceFileName', function() {
    var transpilerOptions;

    toFive.transform = function(string, options) {
      transpilerOptions = options;
      return { code: {} };
    }

    expect(transpilerOptions).to.eql(undefined);
    toFive.processString('path', 'relativePath');

    expect(transpilerOptions.filename).to.eql('relativePath');
    expect(transpilerOptions.sourceMapName).to.eql('relativePath');
    expect(transpilerOptions.sourceFileName).to.eql('relativePath');
  });
})

describe('transpile ES6 to ES5', function() {
  afterEach(function () {
    builder.cleanup();
  });

  it('basic', function () {
    return build(inputPath, {}).then(function(results) {
      var outputPath = results.directory;

      var output = fs.readFileSync(path.join(outputPath, 'fixtures.js')).toString();
      var input = fs.readFileSync(path.join(inputPath,  'expected.js')).toString();

      expect(output).to.eql(input);
    });
  });

  it('inline source maps', function () {
    return build(inputPath, {
      sourceMap: 'inline'
    }).then(function(results) {
      var outputPath = results.directory;

      var output = fs.readFileSync(path.join(outputPath, 'fixtures.js')).toString();
      var input = fs.readFileSync(path.join(inputPath,  'expected-inline-source-maps.js')).toString();

      expect(output).to.eql(input);
    });
  });
});
