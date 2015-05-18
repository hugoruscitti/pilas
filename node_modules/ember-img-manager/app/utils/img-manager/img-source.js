import Ember from 'ember';
import helpers from './dom-helpers';
import ImgCloneHolder from './img-clone-holder';

var assert = Ember.assert;
var observer = Ember.observer;
var computed = Ember.computed;
var oneWay = computed.oneWay;
var or = computed.or;
var on = Ember.on;
var bind = Ember.run.bind;
var next = Ember.run.next;


var uuid = 0;
function appendDummyQP(url) {
  if (typeof url === 'string') {
    url = url.split('#');
    if (url[0].indexOf('?') === -1) {
      url[0] += '?';
    }
    else {
      url[0] += '&';
    }
    url[0] += '__dummy_eim__=' + (++uuid);
    url = url.join('#');
  }
  return url;
}

/**
 * @module img-manager
 * @class ImgSource
 * @extends Ember.Object
 * @uses Ember.Evented
 */
export default Ember.Object.extend(Ember.Evented, {
  /**
   * How many times this source has been duplicated
   * @property hits
   * @type {number}
   */
  hits: 0,

  /**
   * The src of our image
   * @property src
   * @type {string}
   */
  src: null,

  /**
   * Our manager
   * @property manager
   * @type {ImgManagerService}
   */
  manager: null,

  /**
   * Percent loaded
   * @property progress
   * @type {number}
   */
  progress: null,

  /**
   * Our matching rule
   * @property rule
   * @type {ImgRule}
   */
  rule: computed(function () {
    var opt = this.getProperties('manager', 'src');
    return opt.manager.ruleForSrc(opt.src);
  }).readOnly(),

  /**
   * Are we currently loading?
   * @property isLoading
   * @type {boolean}
   */
  isLoading: true,

  /**
   * Whether the load failed or not
   * @property isError
   * @type {boolean}
   */
  isError: false,

  /**
   * Is the real load initiated?
   * @property isInitiated
   * @type {boolean}
   */
  isInitiated: false,

  /**
   * Are we ready? either loaded or error
   * @property isReady
   * @type {boolean}
   */
  isReady: or('isError', 'isSuccess'),

  /**
   * Whether we are loaded successfully or not
   * @property isSuccess
   * @type {boolean}
   */
  isSuccess: computed('isLoading', 'isError', function () {
    return !this.get('isLoading') && !this.get('isError');
  }),

  /**
   * Our source node
   * @property node
   * @type {HTMLImageElement}
   */
  node: computed(function () {
    return document.createElement('img');
  }).readOnly(),

  /**
   * Loads the image
   *
   * @method load
   */
  load: function () {
    var node, opt, src;
    if (!this.get('isInitiated')) {
      this.set('isInitiated', true);
      opt = this.getProperties(
        'src', '_onLoadHandler', '_onErrorHandler', '_onProgressHandler', 'maxTries'
      );
      node = this.get('node');
      this.trigger('willLoad');
      if (opt.maxTries) {
        this.set('isLoading', true);
        this.set('progress', undefined);
        helpers.attachOnce(node, 'load', opt._onLoadHandler);
        helpers.attachOnce(node, 'error', opt._onErrorHandler);
        helpers.attachOnce(node, 'progress', opt._onProgressHandler);
        if (this.get('errorCount')) {
          src = appendDummyQP(opt.src);
        }
        else {
          src = opt.src;
        }
        this.set('modifiedSrc', src);
        node.src = src;
      }
      else {
        // do not even try to load the image, and directly fires the ready event
        next(this, function () {
          this.setProperties({isError: true, isLoading: false});
          this.trigger('ready');
        });
      }
    }
  },

  /**
   * Maximum number of load tries
   * @property maxTries
   * @type {number}
   */
  maxTries: oneWay('rule.maxTries'),

  /**
   * Should we lazy load the image?
   * @property lazyLoad
   * @type {number}
   */
  lazyLoad: oneWay('rule.lazyLoad'),

  /**
   * Number of errors when trying to load the image
   * @property errorCount
   * @type {number}
   */
  errorCount: 0,

  /**
   * Our virtual src depending on our state
   * @property virtualSrc
   * @type {string}
   */
  virtualSrc: computed('isLoading', 'isError', 'rule.errorSrc', 'rule.loadingSrc', function () {
    var opt = this.getProperties('isLoading', 'isError');
    if (opt.isLoading) {
      return this.get('rule.loadingSrc');
    }
    else if (opt.isError) {
      return this.get('rule.errorSrc');
    }
    else {
      // use the node.src since we might have added some parameters for another try
      return this.get('modifiedSrc');
    }
  }).readOnly(),


  /**
   * All the existing clones for this image
   * @property cloneHolders
   * @type {Array.<ImgCloneHolder>}
   */
  cloneHolders: computed(function () {
    return [];
  }).readOnly(),

  /**
   * All the existing free clones for this image
   * @property freeCloneHolders
   * @type {Array.<ImgCloneHolder>}
   */
  freeCloneHolders: computed(function () {
    return [];
  }).readOnly(),


  /**
   * Creates a new clone with given attributes
   *
   * @method createClone
   * @param {Object} attributes
   * @param {Function} [handler]
   * @return {ImgCloneHolder}
   */
  createClone: function (attributes, handler) {
    var cloneHolder, original;
    cloneHolder = this.get('freeCloneHolders').pop();
    original = this.get('isSuccess') ? this.get('node') : null;
    if (!cloneHolder) {
      cloneHolder = new ImgCloneHolder();
    }
    this.get('cloneHolders').push(cloneHolder);
    this.incrementProperty('hits');
    cloneHolder.useWith(this.get('virtualSrc'), attributes, original, handler);
    cloneHolder.triggerOnce(this.get('cloneHolderEvent'), 'change');
    return cloneHolder;
  },

  /**
   * The event reference when calling triggerOnce
   * @property cloneHolderEvent
   * @type {string}
   */
  cloneHolderEvent: computed('isSuccess', 'isError', function () {
    if (this.get('isSuccess')) {
      return 'success';
    }
    else if (this.get('isError')) {
      return 'error';
    }
    return 'loading';
  }),


  /**
   * Release a clone
   *
   * @method releaseClone
   * @param {ImgCloneHolder} cloneHolder
   */
  releaseClone: function (cloneHolder) {
    var cloneHolders = this.get('cloneHolders'), index = cloneHolders.indexOf(cloneHolder);
    assert('[img-manager] Clone holder asked to be released does not belong to this source', index !== -1);
    cloneHolder.release();
    cloneHolders.splice(index, 1);
    this.get('freeCloneHolders').push(cloneHolder);
  },

  /**
   * Schedule a switch of src for all the clones when the ready event is fired
   *
   * @method switchClonesSrc
   */
  switchClonesSrc: on('ready', observer('virtualSrc', function () {
    next(this, '_switchClonesSrc');
  })),

  /**
   * Switch the clones' src
   *
   * @method _switchClonesSrc
   * @private
   */
  _switchClonesSrc: function () {
    var opt, original, i, len, event;
    opt = this.getProperties('cloneHolders', 'virtualSrc', 'manager', 'isSuccess', 'node', 'isError');
    if (opt.isSuccess) {
      original = opt.node;
    }
    event = this.get('cloneHolderEvent');
    for (i = 0, len = opt.cloneHolders.length; i < len; i++) {
      opt.cloneHolders[i].switchSrc(opt.virtualSrc, original);
      opt.cloneHolders[i].triggerOnce(event, 'change');
    }
  },


  /**
   * The progress event handler
   * @property _onProgressHandler
   * @type Function
   * @private
   */
  _onProgressHandler: computed(function () {
    return bind(this, function (event) {
      if (event.lengthComputable) {
        this.set('progress', event.loaded / event.total * 100);
      }
    });
  }).readOnly(),


  /**
   * The load event handler
   * @property _onLoadHandler
   * @type Function
   * @private
   */
  _onLoadHandler: computed(function () {
    return bind(this, function (event) {
      var opt = this.getProperties('node', '_onErrorHandler', '_onProgressHandler');
      helpers.detach(opt.node, 'error', opt._onErrorHandler);
      helpers.detach(opt.node, 'progress', opt._onProgressHandler);
      this.setProperties({
        isError:   false,
        isLoading: false,
        progress:  100
      });
      this.trigger('didLoad', event);
      this.trigger('ready', event);
    });
  }).readOnly(),

  /**
   * The error event handler
   * @property _onErrorHandler
   * @type Function
   * @private
   */
  _onErrorHandler: computed(function () {
    return bind(this, function (event) {
      var opt = this.getProperties('node', '_onLoadHandler', '_onProgressHandler', 'maxTries', 'rule');
      helpers.detach(opt.node, 'load', opt._onLoadHandler);
      helpers.detach(opt.node, 'progress', opt._onProgressHandler);
      if (this.incrementProperty('errorCount') < opt.maxTries) {
        this._continueRuleProcessingQueue();
        this.scheduleLoad(true);
      }
      else {
        // we're done trying, trigger the `didError` event
        this.setProperties({
          isError:   true,
          isLoading: false
        });
        this.trigger('didError', event);
        this.trigger('ready', event);
      }
    });
  }).readOnly(),

  /**
   * Schedule the image load
   *
   * @method scheduleLoad
   * @param {boolean} [forceReload=false]
   * @private
   */
  scheduleLoad: function (forceReload) {
    var initiated = this.get('isInitiated');
    if (initiated && forceReload) {
      this.set('isInitiated', initiated = false);
    }
    if (!initiated) {
      this.get('rule').scheduleForLoad(this, 'load');
    }
  },

  /**
   * Pauses the load processing queue
   *
   * @method _pauseRuleProcessingQueue
   * @private
   */
  _pauseRuleProcessingQueue: on('willLoad', function () {
    this.get('rule').pauseLoadQueue();
  }),

  /**
   * Continues the load processing queue
   *
   * @method _continueRuleProcessingQueue
   * @private
   */
  _continueRuleProcessingQueue: on('ready', function () {
    this.get('rule').continueLoadQueue();
  })
});
