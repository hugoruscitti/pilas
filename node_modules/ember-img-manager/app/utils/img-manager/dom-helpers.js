/**
 * @module img-manager
 * @type {{attach: Function, detach: Function, attachOnce: Function}}
 */
var helpers = {
  /**
   * Listen for an event on an HTML element
   *
   * @param {HTMLElement} node
   * @param {String} event
   * @param {Function} handler
   * @returns {Boolean}
   */
  attach: function (node, event, handler) {
    if (node.addEventListener) {
      node.addEventListener(event, handler, false);
    }
    else if (node.attachEvent) {
      node.attachEvent('on' + event, handler);
    }
    else {
      return false;
    }
    return true;
  },

  /**
   * Stop listening for an event on an HTML element
   *
   * @param {HTMLElement} node
   * @param {String} event
   * @param {Function} handler
   * @returns {Boolean}
   */
  detach: function (node, event, handler) {
    if (node.removeEventListener) {
      node.removeEventListener(event, handler, true);
    }
    else if (node.detachEvent) {
      node.detachEvent('on' + event, handler);
    }
    else {
      return false;
    }
    return true;
  },

  /**
   * Listen for an HTML event once
   *
   * @param {HTMLElement} node
   * @param {String} event
   * @param {Function} handler
   */
  attachOnce: function (node, event, handler) {
    function wrapper() {
      helpers.detach(node, event, wrapper);
      handler.apply(this, arguments);
    }

    return helpers.attach(node, event, wrapper);
  }
};

export default helpers;
