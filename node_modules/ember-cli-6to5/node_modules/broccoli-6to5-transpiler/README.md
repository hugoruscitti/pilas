# broccoli-6to5-transpiler

[![Build Status](https://travis-ci.org/6to5/broccoli-6to5-transpiler.svg?branch=master)](https://travis-ci.org/6to5/broccoli-6to5-transpiler)

A [Broccoli](https://github.com/broccolijs/broccoli) plugin which
transpile ES6 to readable ES5 by using
[6to5](https://github.com/sebmck/6to5).

## How to install?

```sh
$ npm install broccoli-6to5-transpiler --save-dev
```

## How to use?

In your `Brocfile.js`:

```js
var esTranspiler = require('broccoli-6to5-transpiler');
var scriptTree = esTranspiler(inputTree, options);
```

You can find [options](https://6to5.github.io/usage.html#options) at 6to5's
github repo.

## About source map

Currently this plugin only support inline source map, if you need
separate source map feature, welcome to submit a pull request.
