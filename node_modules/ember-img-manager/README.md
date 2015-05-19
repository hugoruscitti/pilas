# ember-img-manager [![Build Status](https://travis-ci.org/huafu/ember-img-manager.svg?branch=master)](https://travis-ci.org/huafu/ember-img-manager)

This Ember addon lets you control how images are loaded (batch size, delay, ...),
setup events for success or error, re-use DOM `img` nodes by cloning them so that
external images with no cache are cached, and use different image sources while an
image is loading or becomes error.

The `batchSize` is particularly helpful when dealing with Google contacts library for
example, where Google limits each client to 10 requests per second for contact images.

You can also use this addon to avoid loading any external images on `dev` environment
for example if you are used to work disconnected from internet.

By default images are lazy loaded, which means that if they have not yet been loaded,
the load will trigger only when the image will appear in the viewport.


## Example configuration

```js
// config/environment.js

// all settings are optionals
ENV.imgManager = {
  // how many times to try to load an image (default: 1)
  maxTries: 3,
  // wait 10 milliseconds before trying to load more images (default: 1)
  delay: 10,
  // how many images to try to load in a raw (if 0 then it'll load all at once) (default: 0)
  batchSize: 0,
  // should we start loading a source image only when it appear in the viewport (default: true)
  lazyLoad: false,
  // the image to use while loading the real image (default: null)
  loadingSrc: 'assets/loading-img.png',
  // the image to use when an image has failed to load (default: null)
  errorSrc: 'assets/error-img.png',
  // in the `rules`, you can define specific settings for each image depending on its `src` (default: null)
  rules: [
    // for use with google contacts photos for example:
    {match: 'www.google.com/m8/feeds/photos', delay: 1000, batchSize: 10},
    // do not try to load any external image (for dev env for example):
    {match: /^https?:\/\//, maxTries: 0}
  ],
  // ------ global only settings (show with their default values) -----
  // css class to use when loading an image
  loadingClass: 'loading',
  // css class to use when the load was successful
  successClass: 'success',
  // css class to use when the load has failed
  errorClass: 'error'
};
```

## Installation

* `npm install --save-dev ember-img-manager`
* or, with the latest `ember-cli`, `ember install:addon ember-img-manager`


## Usage:

* Simply replace any `<img ...>` tag that you want to be handled by the manager with the equivalent
`{{img-wrap ...}}` handlebars tag. All HTML attributes are supported.

    ```handlebars
    {{!-- old tag was <img {{bind-attr src=photoUrl}} alt="Landscape"> --}}
    {{img-wrap src=photoUrl alt="Landscape"}}
    ```

    There are a few properties you can use:
    - `loadingClass`, `successClass`, `errorClass`: the css classes to use for each status (using
    the default ones from config if they are not set)
    - `isLoading`, `isSuccess`, `isError`: whether the image is in one of those status
    - `progress`: the value representing the percentage of the image which has been loaded already
    - `load-error`: name of an Ember action to trigger when the image fails to load
    - `load-success`: name of an Ember action to trigger when the image loads successfully
    - `lazyLoad`: whether to directly load the image or wait until it appears in the viewport (will override anything set in the rules)

* One thing to note is that the `<img>` is then wrapped inside a `<span>` which has `display: inline-block`.
It should not break your design in most of the cases.
* This `<span>` tag has then a `img-wrap` class, plus a `loading`, `error` or `success` class depending
on the state of the load.
* Any other `class` defined in the hash of the handlebars tag is defined on the `<span>` element
instead of the `<img>` itself.


## Author

Huafu Gandon [@huafu_g](https://twitter.com/huafu_g) - [my website](http://huafu.github.io)

---

For more information on using ember-cli, visit [http://www.ember-cli.com/](http://www.ember-cli.com/).
