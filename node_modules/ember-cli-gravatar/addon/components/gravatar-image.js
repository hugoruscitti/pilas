import Ember from 'ember';

export default Ember.Component.extend({
  tagName: 'img',
  attributeBindings: ['src', 'alt', 'title'],
  classNames: ['gravatar-image'],
  size: 250,
  email: '',
  title: '',
  default: '',

  src: Ember.computed('email', 'size', 'default', function() {
    var email = this.get('email'),
        size = this.get('size'),
        def = this.get('default');

    return '//www.gravatar.com/avatar/' + md5(email) + '?s=' + size + '&d=' + def;
  }),

  alt: Ember.computed.alias('email')
});
