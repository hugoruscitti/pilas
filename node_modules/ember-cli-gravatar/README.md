# Gravatar Image Tag

[![Build Status](https://travis-ci.org/johnotander/ember-cli-gravatar.svg?branch=master)](https://travis-ci.org/johnotander/ember-cli-gravatar)

An [ember-cli](http://ember-cli.com) addon for a gravatar image component.

See it in action: <http://ember-cli-gravatar.divshot.io/>.

## Installation

```
ember install:addon ember-cli-gravatar
```

For older versions of Ember CLI:

```
npm i --save ember-cli-gravatar
ember g ember-cli-gravatar
```

## Usage

```hbs
{{gravatar-image email='johnotander@gmail.com'}}
```

__An example with multiple options:__

```hbs
{{gravatar-image email='johnotander@gmail.com' alt='John Otander gravatar' size=250 default='identicon' class='img-circle'}}
```

The default property is optional as well as the size. You can use a encoded url or a default icon name.
[Gravatar documentation](https://en.gravatar.com/site/implement/images/#default-image).

### Required

  * `email`

### Optional

  * `class`
  * `alt`
  * `size`
  * `default`
  * `title`

### Content Security Policy

With the latest versions of the Ember CLI, you will have to whitelist gravatar.com with the following
in your `config/environment.js`:

```javascript
module.exports = function(environment) {
  // ...
  var ENV = {
    // ...
    contentSecurityPolicy: {
      'default-src': "'none'",
      'script-src': "'self'",
      'font-src': "'self'",
      'connect-src': "'self'",
      'img-src': "'self' www.gravatar.com",
      'style-src': "'self'",
      'media-src': "'self'"
    },
    // ...
  }
  // ...
};
```

## License

MIT

## Contributing

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create new Pull Request

Crafted with <3 by [John Otander](http://johnotander.com).
