// this class is in purpose not Ember, for faster processing
import Ember from 'ember';
import imgFactory from './img-node-factory';


var EnumerableUtils = Ember.EnumerableUtils;
var assert = Ember.assert;
var forEach = EnumerableUtils.forEach;
var filter = EnumerableUtils.filter;
var hasOwn = {}.hasOwnProperty;
var run = Ember.run;
var next = run.next;

export var TRANSPARENT_PIXEL = 'data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7';

/**
 * Set an attribute of a node
 *
 * @function setAttr
 * @param {HTMLElement} node
 * @param {string} name
 * @param {*} value
 */
var setAttr = (function (hasSetAttr) {
  if (hasSetAttr) {
    return function (node, name, value) {
      node.setAttribute(name, value);
    };
  }
  else {
    return function (node, name, value) {
      node[name] = value;
    };
  }
})(typeof document.createElement('img').setAttribute === 'function');


/**
 * @class ImgCloneHolder
 * @constructor
 */
function ImgCloneHolder() {
  this.handler = Ember.K;
  this.attributeNames = [];
  this.src = null;
  this.node = null;
  this.hooksHandled = [];
}


(function (proto) {

  /**
   * Release the clone
   *
   * @method release
   * @chainable
   */
  proto.release = function () {
    var i, len, attrNames = this.attributeNames;
    if (this.node) {
      for (i = 0, len = attrNames.length; i < len; i++) {
        this.node.removeAttribute(attrNames[i]);
      }
      this.attributeNames = [];
      imgFactory.free(this.src, this.node);
      this.node = this.src = null;
      this.handler = Ember.K;
    }
    return this;
  };

  /**
   * Switch the src for this node and call the handler so that it can insert the new node into the DOM
   *
   * @method switchSrc
   * @param {string} newSrc
   * @param {HTMLImageElement} [original]
   * @param {boolean} [force=false]
   * @chainable
   */
  proto.switchSrc = function (newSrc, original) {
    var oldImg, newImg, attrNames, hasChanged;
    assert('[img-manager] Trying to switch the source of a clone holder with no node.', this.node);
    if (!newSrc) {
      newSrc = TRANSPARENT_PIXEL;
    }
    if (this.src !== newSrc) {
      oldImg = this.node;
      this.node = newImg = imgFactory.forSrc(newSrc, original);
      hasChanged = false;
      attrNames = [];
      forEach(this.attributeNames, function (name) {
        var attr = oldImg.getAttributeNode(name);
        if (attr) {
          attr = oldImg.removeAttributeNode(attr);
          newImg.setAttributeNode(attr);
          attrNames.push(name);
        }
        else {
          hasChanged = true;
        }
      });
      if (hasChanged) {
        this.attributeNames = attrNames;
      }
      imgFactory.free(this.src, oldImg);
    }
    return this;
  };

  /**
   * Use this clone with the given src, attributes and handler
   *
   * @method useWith
   * @param {string} src
   * @param {ImgCloneHolder|Object} [attributes=null]
   * @param {HTMLImageElement} [original]
   * @param {Function} [handler=Ember.K]
   * @chainable
   */
  proto.useWith = function (src, attributes, original, handler) {
    assert('[img-manager] Clone already used for src `' + this.src + '`.', !this.src);
    this.src = src || TRANSPARENT_PIXEL;
    this.node = imgFactory.forSrc(this.src, original);
    this.handler = handler || Ember.K;
    this._defineAttributes(attributes);
    return this;
  };

  /**
   * Call the handler only if it has not yet been triggered
   *
   * @method triggerOnce
   * @param {string} event
   * @param {string} realEvent
   */
  proto.triggerOnce = function (event, realEvent) {
    if (this.hooksHandled.indexOf(event) === -1) {
      this.hooksHandled.push(event);
      next(null, this.handler, realEvent || event, this.node);
    }
  };

  /**
   * Set one attribute of this clone
   *
   * @method setAttribute
   * @param {string} name
   * @param {*} value
   */
  proto.setAttribute = function (name, value) {
    var attrNames, index;
    attrNames = this.attributeNames;
    index = attrNames.indexOf(name);
    if (name === 'src') {
      this.switchToSrc(value);
    }
    if (value == null) {
      if (index !== -1) {
        attrNames.splice(index, 1);
        this.node.removeAttribute(name);
      }
    }
    else {
      if (index === -1) {
        attrNames.push(name);
      }
      setAttr(this.node, name, value);
    }
  };

  /**
   * Set the attributes with given attributes array or from another clone
   *
   * @method _defineAttributes
   * @param {ImgCloneHolder|Object} cloneOrAttrs
   * @private
   */
  proto._defineAttributes = function (cloneOrAttrs) {
    if (cloneOrAttrs) {
      if (cloneOrAttrs instanceof ImgCloneHolder) {
        // move attributes from the given node to the clone
        this._importAttributes(cloneOrAttrs);
      }
      else {
        // set attributes
        this._setAttributes(cloneOrAttrs);
      }
    }
  };

  /**
   * Import and move attributes from the given clone
   *
   * @method _importAttributes
   * @param {ImgCloneHolder} clone
   * @private
   */
  proto._importAttributes = function (clone) {
    var node, attrNames;
    node = this.node;
    attrNames = this.attributeNames;
    forEach(clone.node.attributes, function (attr) {
      if (clone.attributeNames.indexOf(attr.localName) !== -1) {
        attr = clone.node.removeAttributeNode(attr);
        node.setAttributeNode(attr);
        attrNames.push(attr.localName);
      }
    });
    // remove the names from the index
    clone.attributeNames = filter(clone.attributeNames, function (name) {
      return attrNames.indexOf(name) !== -1;
    });
  };

  /**
   * Sets the attributes from a hash
   *
   * @method _setAttributes
   * @param {Object} attributes
   * @private
   */
  proto._setAttributes = function (attributes) {
    var name, value, node, attrNames;
    node = this.node;
    attrNames = this.attributeNames;
    for (name in attributes) {
      if (hasOwn.call(attributes, name)) {
        value = attributes[name];
        if (name !== 'src' && value != null) {
          attrNames.push(name);
          setAttr(node, name, value);
        }
      }
    }
  };

})(ImgCloneHolder.prototype);

export default ImgCloneHolder;
