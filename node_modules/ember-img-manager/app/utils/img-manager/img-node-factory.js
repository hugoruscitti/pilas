import Ember from 'ember';
import SimpleMap from './simple-map';

var assert = Ember.assert;


export default {
  /**
   * Our nodes collection
   * @property index
   * @type {SimpleMap.<{src: string, node: HTMLDivElement.<HTMLImageElement>, original: HTMLImageElement}>}
   */
  index: new SimpleMap(),

  /**
   * Our container
   * @property container
   * @type {HTMLDivElement}
   */
  container: null,

  /**
   * The index for the given src
   *
   * @method indexFor
   * @param {string} src
   * @param {boolean} [createIfNotExists=false]
   * @return {{src: string, node: HTMLDivElement.<HTMLImageElement>, original: HTMLImageElement}|undefined}
   */
  indexFor: function (src, createIfNotExists) {
    var idx;
    if (!this.container) {
      if (!createIfNotExists) {
        return;
      }
      this.container = document.createElement('div');
    }
    idx = this.index.get(src);
    if (!idx) {
      if (!createIfNotExists) {
        return;
      }
      idx = Object.create(null);
      idx.src = src;
      idx.node = document.createElement('div');
      idx.original = null;
      this.index.set(src, idx);
      this.container.appendChild(idx.node);
    }
    return idx;
  },

  /**
   * Get one free node for the given src
   *
   * @method forSrc
   * @param {string} src
   * @param {HTMLImageElement} [original]
   * @return {HTMLImageElement}
   */
  forSrc: function (src, original) {
    var img, idx;
    assert('[img-manager] Can\'t get a clone with no `src`.', src);
    idx = this.indexFor(src, true);
    if (idx && (img = idx.node.lastChild)) {
      idx.node.removeChild(img);
      return img;
    }
    if (original) {
      img = original.cloneNode(true);
    }
    else {
      if (!idx.original) {
        idx.original = document.createElement('img');
        idx.original.src = src;
      }
      img = idx.original.cloneNode(true);
    }
    return img;
  },

  /**
   * Free the given img node
   *
   * @method free
   * @param {string} src
   * @param {HTMLImageElement} img
   */
  free: function (src, img) {
    assert('[img-manager] Can\'t free a clone with no `src`.', src);
    assert('[img-manager] Can\'t free a clone with undefined node for src `' + src + '`.', img);
    this.indexFor(src, true).node.appendChild(img);
  }
};
