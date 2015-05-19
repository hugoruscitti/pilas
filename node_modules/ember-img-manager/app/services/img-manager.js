import Ember from 'ember';
import ImgRule from '../utils/img-manager/img-rule';
import ImgSource from '../utils/img-manager/img-source';
import ENV from '../config/environment';
import SimpleMap from '../utils/img-manager/simple-map';


var map = Ember.EnumerableUtils.map;
var computed = Ember.computed;
var readOnly = computed.readOnly;
var bind = Ember.run.bind;

/**
 * @module img-manager
 * @class ImgManagerService
 * @extends Ember.Object
 */
export default Ember.Object.extend({
  /**
   * Our configuration
   * @property config
   * @type {Object}
   */
  config: computed(function () {
    return Ember.merge({
      maxTries:     1,
      loadingClass: 'loading',
      errorClass:   'error',
      successClass: 'success',
      lazyLoad:     true
    }, Ember.get(ENV, 'imgManager'));
  }).readOnly(),

  /**
   * The default delay
   * @property defaultDelay
   * @type {number}
   */
  defaultDelay: readOnly('config.delay'),

  /**
   * The default lazyLoad
   * @property defaultLazyLoad
   * @type {boolean}
   */
  defaultLazyLoad: readOnly('config.lazyLoad'),

  /**
   * The default batch size
   * @property defaultBatchSize
   * @type {number}
   */
  defaultBatchSize: readOnly('config.batchSize'),

  /**
   * The default max tries
   * @property defaultMaxTries
   * @type {number}
   */
  defaultMaxTries: readOnly('config.maxTries', 1),

  /**
   * The default loading src
   * @property defaultLoadingSrc
   * @type {number}
   */
  defaultLoadingSrc: readOnly('config.loadingSrc'),

  /**
   * The default error src
   * @property defaultErrorSrc
   * @type {number}
   */
  defaultErrorSrc: readOnly('config.errorSrc'),

  /**
   * Default css class for the wrapper of a loading image
   * @property defaultLoadingClass
   * @type {string}
   */
  defaultLoadingClass: readOnly('config.loadingClass'),

  /**
   * Default css class for the wrapper of an image which failed to load
   * @property defaultErrorClass
   * @type {string}
   */
  defaultErrorClass: readOnly('config.errorClass'),

  /**
   * Default css class for the wrapper of an image which loaded successfully
   * @property defaultSuccessClass
   * @type {string}
   */
  defaultSuccessClass: readOnly('config.successClass'),


  /**
   * Get the img source object for the given src
   *
   * @method imgSourceForSrc
   * @param {string} src
   * @return {ImgSource}
   */
  imgSourceForSrc: function (src) {
    var dict = this.get('_imgSources'),
      imgSource = dict.get(src);
    if (!imgSource) {
      dict.set(src, imgSource = src ? ImgSource.create({
        src:     src,
        manager: this
      }) : null);
      if (imgSource) {
        this.incrementProperty('totalSources');
        imgSource.one('didError', bind(this, 'incrementProperty', 'totalErrors', 1));
      }
    }
    return imgSource;
  },

  /**
   * Contains all the rules
   * @property rules
   * @type {Ember.Array.<ImgRule>}
   */
  rules: computed(function () {
    var _this = this;
    var rules = Ember.A(map(this.get('config.rules') || [], function (ruleConfig) {
      return ImgRule.create({
        manager: _this,
        config:  ruleConfig
      });
    }));
    // add a default rule matching everything
    rules.pushObject(ImgRule.create({
      manager: this,
      config:  {match: '*'}
    }));
    return rules;
  }).readOnly(),


  /**
   * Get the first rule matching the given src
   *
   * @method ruleForSrc
   * @param {string} src
   * @return {ImgRule}
   */
  ruleForSrc: function (src) {
    return this.get('rules').find(function (rule) {
      return rule.test(src);
    });
  },

  /**
   * Total number of hits
   * @property totalHits
   * @type {number}
   */
  totalHits: 0,

  /**
   * Total number of errors
   * @property totalErrors
   * @type {number}
   */
  totalErrors: 0,

  /**
   * Total number of used clones
   * @property totalUsedClones
   * @type {number}
   */
  totalUsedClones: 0,

  /**
   * Total number of free clones
   * @property totalFreeClones
   * @type {number}
   */
  totalFreeClones: 0,

  /**
   * Total number of sources
   * @property totalSources
   * @type {number}
   */
  totalSources: 0,

  /**
   * All img source objects indexed by src
   * @property _imgSources
   * @type {Object}
   */
  _imgSources: computed(function () {
    return new SimpleMap();
  }).readOnly()
});
