// Inspired from:
// https://github.com/twokul/ember-lazy-image
// https://medium.com/delightful-ui-for-ember-apps/ember-js-detecting-if-a-dom-element-is-in-the-viewport-eafcc77a6f86

import Ember from 'ember';

var on = Ember.on;
var get = Ember.get;
var debounce = Ember.run.debounce;
var scheduleOnce = Ember.run.scheduleOnce;
var computed = Ember.computed;
var bind = Ember.run.bind;
var next = Ember.run.next;

/**
 * @mixin ImgManagerInViewportMixin
 * @extension ImgManagerInViewportMixin
 * @uses Ember.Evented
 */
export default Ember.Mixin.create(Ember.Evented, {
  /**
   * The timeout to observe scrolling
   * @property scrollTimeout
   * @type {number}
   */
  scrollTimeout: 100,

  /**
   * Set to true when it entered viewport
   * @property enteredViewport
   * @type {boolean}
   */
  enteredViewport: computed(function (key, value, oldValue) {
    if (arguments.length > 1) {
      if (value) {
        this._unbindScroll();
        if (!oldValue) {
          //Ember.debug('[img-manager] Element entered viewport: ' + this + '.');
          next(this, 'trigger', 'didEnterViewport');
        }
      }
    }
    else {
      value = false;
    }
    return value;
  }),

  /**
   * Updates the `enteredViewport` property
   *
   * @method _setViewport
   * @private
   */
  _setViewport: function () {
    var rect;
    if (this.isDestroying || this.isDestroyed || this._state !== 'inDOM' || this.get('enteredViewport')) {
      return;
    }
    rect = this.$()[0].getBoundingClientRect();
    this.set('enteredViewport',
      rect.top >= 0 &&
      rect.left >= 0 &&
      rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
      rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
  },

  /**
   * Set the initial value of `enteredViewport`
   *
   * @method _setInitialViewport
   * @private
   */
  _setInitialViewport: on('didInsertElement', function () {
    scheduleOnce('afterRender', this, '_setViewport');
  }),

  /**
   * Handles the scroll event
   *
   * @method _scrollHandler
   * @private
   */
  _scrollHandler: function () {
    debounce(this, '_setViewport', get(this, 'scrollTimeout'));
  },

  /**
   * Starts listening for the scroll event
   *
   * @method _bindScroll
   * @private
   */
  _bindScroll: on('didInsertElement', function () {
    this._unbindScroll();
    if (!this.get('enteredViewport')) {
      this._boundScrollHandler = bind(this, '_scrollHandler');
      Ember.$(document).on('touchmove', this._boundScrollHandler);
      Ember.$(window).on('scroll', this._boundScrollHandler);
    }
  }),

  /**
   * Stops listening for the scroll event
   *
   * @method _bindScroll
   * @private
   */
  _unbindScroll: on('willDestroyElement', function () {
    if (this._boundScrollHandler) {
      Ember.$(window).off('scroll', this._boundScrollHandler);
      Ember.$(document).off('touchmove', this._boundScrollHandler);
      this._boundScrollHandler = null;
    }
  })
});
