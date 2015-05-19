import Ember from 'ember';

var slice = [].slice;
var run = Ember.run;
var next = run.next;
var debounce = run.debounce;
var computed = Ember.computed;
var readOnly = computed.readOnly;


function starMatcher() {
  return true;
}
function noneMatcher() {
  return false;
}

function callQueueItem(item) {
  var target = item[0], method = item[1], args = item[2];
  if (!target || (!target.isDestroyed && !target.isDestroying)) {
    try {
      if (typeof method === 'string') {
        method = target[method];
      }
      return method.apply(target, args);
    }
    catch (e) {
      Ember.warn('[img-manager] Error invoking load queue item: ' + e);
    }
  }
}

function anyDefined() {
  var props = Array.prototype.slice.call(arguments);
  return computed.apply(Ember, props.concat([function () {
    var val;
    for (var i = 0; i < props.length; i++) {
      val = this.get(props[i]);
      if (val != null) {
        return val;
      }
    }
  }])).readOnly();
}

/**
 * @module img-manager
 * @class ImgRule
 * @extends Ember.Object
 */
export default Ember.Object.extend({
  /**
   * Our manager
   * @property manager
   * @type {ImgManagerService}
   */
  manager: null,

  /**
   * The rule's config
   * @property config
   * @type {{match: string|RegExp|Function, batchSize: number, delay: number, maxTries: number, loadingSrc: string, errorSrc: string, lazyLoad: boolean}}
   */
  config: null,

  /**
   * The number of images matching which would load at the same time
   * @property batchSize
   * @type {number}
   */
  batchSize: computed('config.batchSize', 'manager.defaultBatchSize', function () {
    var batchSize = this.get('config.batchSize');
    if (batchSize === undefined) {
      batchSize = this.get('manager.defaultBatchSize');
    }
    return batchSize;
  }).readOnly(),

  /**
   * Match used to filter on `src`
   * @property match
   * @type {string|RegExp|Function}
   */
  match: readOnly('config.match'),

  /**
   * How many milliseconds to wait before loading next batch
   * @property delay
   * @type {number}
   */
  delay: anyDefined('config.delay', 'manager.defaultDelay'),

  /**
   * Should we lazy load the image?
   * @property lazyLoad
   * @type {number}
   */
  lazyLoad: anyDefined('config.lazyLoad', 'manager.defaultLazyLoad'),

  /**
   * The maximum number of time to try to load an image
   * @property maxTries
   * @type {number}
   */
  maxTries: anyDefined('config.maxTries', 'manager.defaultMaxTries'),

  /**
   * The src to use when loading the image
   * @property loadingSrc
   * @type {string}
   */
  loadingSrc: anyDefined('config.loadingSrc', 'manager.defaultLoadingSrc'),

  /**
   * The src to use when the image failed loading
   * @property errorSrc
   * @type {string}
   */
  errorSrc: anyDefined('config.errorSrc', 'manager.defaultErrorSrc'),

  /**
   * How many times has it been paused
   * @property loadQueuePausedCount
   * @type {number}
   */
  loadQueuePausedCount: computed(function (key, value) {
    if (arguments.length > 1) {
      // set
      if (value === 0) {
        // time to schedule the queue processing
        next(this, 'processLoadQueue');
      }
      return value;
    }
    else {
      // initial get
      return 0;
    }
  }),

  /**
   * Pauses the load queue processing
   *
   * @method pauseLoadQueue
   */
  pauseLoadQueue: function () {
    this.incrementProperty('loadQueuePausedCount');
  },

  /**
   * Continue the load queue processing
   *
   * @method continueLoadQueue
   */
  continueLoadQueue: function () {
    this.incrementProperty('loadQueuePausedCount', -1);
  },


  /**
   * Matcher used to find out if given src matches the rule
   * @property matcher
   * @type {Function}
   */
  matcher: computed('match', function () {
    var match = this.get('match');
    if (match === undefined || match === '*') {
      return starMatcher;
    }
    switch (typeof match) {
      case 'string':
        return function (src) {
          return src.indexOf(match) !== -1;
        };
      case 'function':
        return match;
      default:
        if (match instanceof RegExp) {
          return function (src) {
            return match.test(src);
          };
        }
        else {
          Ember.warn('[img-manager] Invalid rule `match`: ' + match);
          return noneMatcher;
        }
    }
  }).readOnly(),

  /**
   * Used to test if a given `src` matches our rule
   *
   * @method test
   * @param {string} src
   * @return {boolean}
   */
  test: function (src) {
    return this.get('matcher')(src);
  },

  /**
   * Schedule the given function for load
   *
   * @method scheduleForLoad
   * @param {Object} [target]
   * @param {Function|string} method
   * @param {*} [...args]
   */
  scheduleForLoad: function (target, method/*, args*/) {
    var args;
    if (arguments.length < 2) {
      method = target;
      target = null;
      args = [];
    }
    else {
      args = slice.call(arguments, 2);
    }
    this.get('_loadQueue').pushObject([target, method, args]);
    this.processLoadQueue();
  },

  /**
   * Process our loading queue
   *
   * @method processLoadQueue
   */
  processLoadQueue: function () {
    var opt = this.getProperties('_loadQueue', 'delay', 'loadQueuePausedCount');
    if (!opt._loadQueue.length || opt.loadQueuePausedCount > 0) {
      return;
    }
    this._timer = debounce(this, '_processLoadQueue', opt.delay || 1);
  },

  /**
   * Our load queue
   * @property _loadQueue
   * @type {Array.<Function>}
   * @private
   */
  _loadQueue: computed(function () {
    return Ember.A([]);
  }),

  /**
   * Our load queue processor
   *
   * @method _processLoadQueue
   * @private
   */
  _processLoadQueue: function () {
    var batchSize = this.get('batchSize'),
      queue = this.get('_loadQueue'), items;
    if (this.get('loadQueuePausedCount') === 0) {
      items = queue.splice(0, batchSize || queue.length);
      for (var i = 0; i < items.length; i++) {
        callQueueItem(items[i]);
      }
    }
    next(this, 'processLoadQueue');
  }
});
