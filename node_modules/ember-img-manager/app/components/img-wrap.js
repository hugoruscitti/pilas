import Ember from 'ember';
import ImgManagerInViewportMixin from '../mixins/img-manager/in-viewport';

var IMG_ATTRIBUTES = [
  'id', 'title', 'align', 'alt', 'border', 'height',
  'hspace', 'ismap', 'longdesc', 'name', 'width',
  'usemap', 'vspace'
];

var computed = Ember.computed;
var readOnly = computed.readOnly;
var oneWay = computed.oneWay;
var run = Ember.run;
var bind = run.bind;
var once = run.once;
var on = Ember.on;


/**
 * @module img-manager/img-source
 * @class Current
 * @property {ImgSource} source
 * @property {ImgCloneHolder} cloneHolder
 */

/**
 * @class ImgWrapComponent
 * @extends Ember.Component
 *
 * @property {ImgManagerService} manager
 */
var ImgWrapComponent;
ImgWrapComponent = Ember.Component.extend(ImgManagerInViewportMixin, {
  /**
   * @inheritDoc
   */
  attributeBindings: ['style'],

  /**
   * @inheritDoc
   */
  tagName: 'span',

  /**
   * @inheritDoc
   */
  classNames: ['img-wrap'],

  /**
   * @inheritDoc
   */
  classNameBindings: ['statusClass'],

  /**
   * The css styles of our span
   * @property style
   * @type {string}
   */
  style: 'display: inline-block;',


  /**
   * The src attribute of the image
   * @property src
   * @type {string}
   */
  src: computed(function (key, value, oldValue) {
    if (arguments.length > 1 && value !== oldValue) {
      once(this, '_updateSrc', value);
    }
    return value;
  }),

  /**
   * Update the src property and its dependencies
   *
   * @method _updateSrc
   * @param {string} src
   * @private
   */
  _updateSrc: function (src) {
    var imgSource, cloneHolder;
    this.releaseCloneHolder();
    if (src) {
      imgSource = this.manager.imgSourceForSrc(src);
      cloneHolder = imgSource.createClone(
        this.getProperties(IMG_ATTRIBUTES), this.get('_cloneHolderActionHandler')
      );
      this.setProperties({
        imgSource:   imgSource,
        cloneHolder: cloneHolder
      });
      this._insertImgNode();
    }
  },


  /**
   * Releases the clone holder
   *
   * @method releaseCloneHolder
   */
  releaseCloneHolder: on('destroy', function () {
    var cloneHolder = this.get('cloneHolder');
    if (cloneHolder) {
      this.get('imgSource').releaseClone(cloneHolder);
    }
    this.setProperties({
      cloneHolder: null,
      imgSource:   null
    });
  }),

  /**
   * Our image source
   * @property imgSource
   * @type {ImgSource}
   */
  imgSource: null,

  /**
   * Our clone holder
   * @property cloneHolder
   * @type {ImgCloneHolder}
   */
  cloneHolder: null,

  /**
   * Is it loading the source image?
   * @property isLoading
   * @type {boolean}
   */
  isLoading: readOnly('imgSource.isLoading'),

  /**
   * Did the source image fail to load?
   * @property isError
   * @type {boolean}
   */
  isError: readOnly('imgSource.isError'),

  /**
   * Did the source image succeed to load?
   * @property isSuccess
   * @type {boolean}
   */
  isSuccess: readOnly('imgSource.isSuccess'),

  /**
   * How many percent have been loaded so far?
   * @property progress
   * @type {number}
   */
  progress: readOnly('imgSource.progress'),

  /**
   * Lazy load
   * @property lazyLoad
   * @type {boolean}
   */
  lazyLoad: oneWay('imgSource.lazyLoad'),

  /**
   * Loading class
   * @property loadingClass
   * @type {string}
   */
  loadingClass: oneWay('manager.defaultLoadingClass'),

  /**
   * Error class
   * @property errorClass
   * @type {string}
   */
  errorClass: oneWay('manager.defaultErrorClass'),

  /**
   * Success class
   * @property successClass
   * @type {string}
   */
  successClass: oneWay('manager.defaultSuccessClass'),

  /**
   * The css class related to the current status
   * @property statusClass
   * @type {string}
   */
  statusClass: computed(
    'imgSource.isLoading', 'imgSource.isError', 'imgSource.isSuccess',
    'loadingClass', 'errorClass', 'successClass',
    function () {
      var imgSource, opt;
      imgSource = this.get('imgSource');
      if (!imgSource) {
        return this.get('loadingClass');
      }
      opt = imgSource.getProperties('isLoading', 'isError', 'isSuccess');
      if (opt.isLoading) {
        return this.get('loadingClass');
      }
      else if (opt.isError) {
        return this.get('errorClass');
      }
      else if (opt.isSuccess) {
        return this.get('successClass');
      }
    }).readOnly(),

  /**
   * Inserts the clone in the element if this one is in the DOM
   *
   * @method _insertImgNode
   */
  _insertImgNode: on('didInsertElement', function () {
    var cloneHolder;
    if (this._state === 'inDOM' && (cloneHolder = this.get('cloneHolder'))) {
      this.get('element').appendChild(cloneHolder.node);
      this._scheduleSourceLoad();
    }
  }),

  /**
   * Initialize our component
   *
   * @method _setupImgWrap
   * @private
   */
  _setupImgWrap: on('init', function () {
    if (!this.get('lazyLoad')) {
      this.set('enteredViewport', true);
    }
  }),

  /**
   * Starts loading the source when the element enter the viewport
   *
   * @method _scheduleSourceLoad
   */
  _scheduleSourceLoad: on('didEnterViewport', function () {
    var imgSource = this.get('imgSource');
    if (imgSource && this._state === 'inDOM' && this.get('enteredViewport')) {
      //Ember.debug('[img-manager] Scheduling load for `' + imgSource.get('src') + '`.');
      imgSource.scheduleLoad();
    }
  }),

  /**
   * The handler called when the source is changed
   * @property _cloneHolderActionHandler
   * @type {Function}
   */
  _cloneHolderActionHandler: computed(function () {
    return bind(this, function (action, imgNode) {
      var imgSource, event;
      if (action === 'change') {
        imgSource = this.get('imgSource');
        if (imgSource) {
          this._insertImgNode();
          if (imgSource.get('isSuccess')) {
            event = 'load-success';
          }
          else if (imgSource.get('isError')) {
            event = 'load-error';
          }
          if (event) {
            this.sendAction(event, imgNode);
          }
        }
      }
    });
  })
});

// now create the setters for each image attribute so that we can update them on each clone
var extra = {};
Ember.EnumerableUtils.forEach(IMG_ATTRIBUTES, function (name) {
  extra[name] = computed(function (key, value) {
    var current;
    if (arguments.length > 1 && !this.isDestroying && !this.isDestroyed && this._state === 'inDOM') {
      current = this.get('cloneHolder');
      if (current && current.cloneHolder.clone) {
        current.cloneHolder.setAttribute(name, value);
      }
    }
    return value;
  });
});
ImgWrapComponent.reopen(extra);

export default ImgWrapComponent;
