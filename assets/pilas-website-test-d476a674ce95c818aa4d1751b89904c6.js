/* jshint ignore:start */

/* jshint ignore:end */

define('pilas-website-test/app', ['exports', 'ember', 'ember/resolver', 'ember/load-initializers', 'pilas-website-test/config/environment'], function (exports, Ember, Resolver, loadInitializers, config) {

  'use strict';

  Ember['default'].MODEL_FACTORY_INJECTIONS = true;

  var App = Ember['default'].Application.extend({
    modulePrefix: config['default'].modulePrefix,
    podModulePrefix: config['default'].podModulePrefix,
    Resolver: Resolver['default']
  });

  loadInitializers['default'](App, config['default'].modulePrefix);

  exports['default'] = App;

});
define('pilas-website-test/components/gravatar-image', ['exports', 'ember-cli-gravatar/components/gravatar-image'], function (exports, gravatarImage) {

	'use strict';

	exports['default'] = gravatarImage['default'];

});
define('pilas-website-test/components/img-wrap', ['exports', 'ember', 'pilas-website-test/mixins/img-manager/in-viewport'], function (exports, Ember, ImgManagerInViewportMixin) {

  'use strict';

  var IMG_ATTRIBUTES = ["id", "title", "align", "alt", "border", "height", "hspace", "ismap", "longdesc", "name", "width", "usemap", "vspace"];

  var computed = Ember['default'].computed;
  var readOnly = computed.readOnly;
  var oneWay = computed.oneWay;
  var run = Ember['default'].run;
  var bind = run.bind;
  var once = run.once;
  var on = Ember['default'].on;


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
  ImgWrapComponent = Ember['default'].Component.extend(ImgManagerInViewportMixin['default'], {
    /**
     * @inheritDoc
     */
    attributeBindings: ["style"],

    /**
     * @inheritDoc
     */
    tagName: "span",

    /**
     * @inheritDoc
     */
    classNames: ["img-wrap"],

    /**
     * @inheritDoc
     */
    classNameBindings: ["statusClass"],

    /**
     * The css styles of our span
     * @property style
     * @type {string}
     */
    style: "display: inline-block;",


    /**
     * The src attribute of the image
     * @property src
     * @type {string}
     */
    src: computed(function (key, value, oldValue) {
      if (arguments.length > 1 && value !== oldValue) {
        once(this, "_updateSrc", value);
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
        cloneHolder = imgSource.createClone(this.getProperties(IMG_ATTRIBUTES), this.get("_cloneHolderActionHandler"));
        this.setProperties({
          imgSource: imgSource,
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
    releaseCloneHolder: on("destroy", function () {
      var cloneHolder = this.get("cloneHolder");
      if (cloneHolder) {
        this.get("imgSource").releaseClone(cloneHolder);
      }
      this.setProperties({
        cloneHolder: null,
        imgSource: null
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
    isLoading: readOnly("imgSource.isLoading"),

    /**
     * Did the source image fail to load?
     * @property isError
     * @type {boolean}
     */
    isError: readOnly("imgSource.isError"),

    /**
     * Did the source image succeed to load?
     * @property isSuccess
     * @type {boolean}
     */
    isSuccess: readOnly("imgSource.isSuccess"),

    /**
     * How many percent have been loaded so far?
     * @property progress
     * @type {number}
     */
    progress: readOnly("imgSource.progress"),

    /**
     * Lazy load
     * @property lazyLoad
     * @type {boolean}
     */
    lazyLoad: oneWay("imgSource.lazyLoad"),

    /**
     * Loading class
     * @property loadingClass
     * @type {string}
     */
    loadingClass: oneWay("manager.defaultLoadingClass"),

    /**
     * Error class
     * @property errorClass
     * @type {string}
     */
    errorClass: oneWay("manager.defaultErrorClass"),

    /**
     * Success class
     * @property successClass
     * @type {string}
     */
    successClass: oneWay("manager.defaultSuccessClass"),

    /**
     * The css class related to the current status
     * @property statusClass
     * @type {string}
     */
    statusClass: computed("imgSource.isLoading", "imgSource.isError", "imgSource.isSuccess", "loadingClass", "errorClass", "successClass", function () {
      var imgSource, opt;
      imgSource = this.get("imgSource");
      if (!imgSource) {
        return this.get("loadingClass");
      }
      opt = imgSource.getProperties("isLoading", "isError", "isSuccess");
      if (opt.isLoading) {
        return this.get("loadingClass");
      } else if (opt.isError) {
        return this.get("errorClass");
      } else if (opt.isSuccess) {
        return this.get("successClass");
      }
    }).readOnly(),

    /**
     * Inserts the clone in the element if this one is in the DOM
     *
     * @method _insertImgNode
     */
    _insertImgNode: on("didInsertElement", function () {
      var cloneHolder;
      if (this._state === "inDOM" && (cloneHolder = this.get("cloneHolder"))) {
        this.get("element").appendChild(cloneHolder.node);
        this._scheduleSourceLoad();
      }
    }),

    /**
     * Initialize our component
     *
     * @method _setupImgWrap
     * @private
     */
    _setupImgWrap: on("init", function () {
      if (!this.get("lazyLoad")) {
        this.set("enteredViewport", true);
      }
    }),

    /**
     * Starts loading the source when the element enter the viewport
     *
     * @method _scheduleSourceLoad
     */
    _scheduleSourceLoad: on("didEnterViewport", function () {
      var imgSource = this.get("imgSource");
      if (imgSource && this._state === "inDOM" && this.get("enteredViewport")) {
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
        if (action === "change") {
          imgSource = this.get("imgSource");
          if (imgSource) {
            this._insertImgNode();
            if (imgSource.get("isSuccess")) {
              event = "load-success";
            } else if (imgSource.get("isError")) {
              event = "load-error";
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
  Ember['default'].EnumerableUtils.forEach(IMG_ATTRIBUTES, function (name) {
    extra[name] = computed(function (key, value) {
      var current;
      if (arguments.length > 1 && !this.isDestroying && !this.isDestroyed && this._state === "inDOM") {
        current = this.get("cloneHolder");
        if (current && current.cloneHolder.clone) {
          current.cloneHolder.setAttribute(name, value);
        }
      }
      return value;
    });
  });
  ImgWrapComponent.reopen(extra);

  exports['default'] = ImgWrapComponent;

});
define('pilas-website-test/components/lf-overlay', ['exports', 'ember'], function (exports, Ember) {

  'use strict';

  exports['default'] = Ember['default'].Component.extend({
    tagName: "span",
    classNames: ["lf-overlay"],
    didInsertElement: function () {
      Ember['default'].$("body").addClass("lf-modal-open");
    },
    willDestroy: function () {
      Ember['default'].$("body").removeClass("lf-modal-open");
    },
    click: function () {
      this.sendAction("clickAway");
    }
  });

});
define('pilas-website-test/components/liquid-bind-c', ['exports', 'ember'], function (exports, Ember) {

  'use strict';

  exports['default'] = Ember['default'].Component.extend({
    tagName: ""
  });

});
define('pilas-website-test/components/liquid-measured', ['exports', 'liquid-fire/mutation-observer', 'ember'], function (exports, MutationObserver, Ember) {

  'use strict';

  exports['default'] = Ember['default'].Component.extend({

    didInsertElement: function () {
      var self = this;

      // This prevents margin collapse
      this.$().css({
        border: "1px solid transparent",
        margin: "-1px"
      });

      this.didMutate();

      this.observer = new MutationObserver['default'](function (mutations) {
        self.didMutate(mutations);
      });
      this.observer.observe(this.get("element"), {
        attributes: true,
        subtree: true,
        childList: true
      });
      this.$().bind("webkitTransitionEnd", function () {
        self.didMutate();
      });
      // Chrome Memory Leak: https://bugs.webkit.org/show_bug.cgi?id=93661
      window.addEventListener("unload", function () {
        self.willDestroyElement();
      });
    },

    willDestroyElement: function () {
      if (this.observer) {
        this.observer.disconnect();
      }
    },

    didMutate: function () {
      Ember['default'].run.next(this, function () {
        this._didMutate();
      });
    },

    _didMutate: function () {
      var elt = this.$();
      if (!elt || !elt[0]) {
        return;
      }

      // if jQuery sees a zero dimension, it will temporarily modify the
      // element's css to try to make its size measurable. But that's bad
      // for us here, because we'll get an infinite recursion of mutation
      // events. So we trap the zero case without hitting jQuery.

      if (elt[0].offsetWidth === 0) {
        this.set("width", 0);
      } else {
        this.set("width", elt.outerWidth());
      }
      if (elt[0].offsetHeight === 0) {
        this.set("height", 0);
      } else {
        this.set("height", elt.outerHeight());
      }
    }

  });

});
define('pilas-website-test/components/liquid-modal', ['exports', 'ember'], function (exports, Ember) {

  'use strict';

  exports['default'] = Ember['default'].Component.extend({
    classNames: ["liquid-modal"],
    currentContext: Ember['default'].computed.oneWay("owner.modalContexts.lastObject"),

    owner: null, // set by injection

    innerView: Ember['default'].computed("currentContext", function () {
      var self = this,
          current = this.get("currentContext"),
          name = current.get("name"),
          container = this.get("container"),
          component = container.lookup("component-lookup:main").lookupFactory(name);
      Ember['default'].assert("Tried to render a modal using component '" + name + "', but couldn't find it.", !!component);

      var args = Ember['default'].copy(current.get("params"));

      args.registerMyself = Ember['default'].on("init", function () {
        self.set("innerViewInstance", this);
      });

      // set source so we can bind other params to it
      args._source = Ember['default'].computed(function () {
        return current.get("source");
      });

      var otherParams = current.get("options.otherParams");
      var from, to;
      for (from in otherParams) {
        to = otherParams[from];
        args[to] = Ember['default'].computed.alias("_source." + from);
      }

      var actions = current.get("options.actions") || {};

      // Override sendAction in the modal component so we can intercept and
      // dynamically dispatch to the controller as expected
      args.sendAction = function (name) {
        var actionName = actions[name];
        if (!actionName) {
          this._super.apply(this, Array.prototype.slice.call(arguments));
          return;
        }

        var controller = current.get("source");
        var args = Array.prototype.slice.call(arguments, 1);
        args.unshift(actionName);
        controller.send.apply(controller, args);
      };

      return component.extend(args);
    }),

    actions: {
      outsideClick: function () {
        if (this.get("currentContext.options.dismissWithOutsideClick")) {
          this.send("dismiss");
        } else {
          proxyToInnerInstance(this, "outsideClick");
        }
      },
      escape: function () {
        if (this.get("currentContext.options.dismissWithEscape")) {
          this.send("dismiss");
        } else {
          proxyToInnerInstance(this, "escape");
        }
      },
      dismiss: function () {
        var source = this.get("currentContext.source"),
            proto = source.constructor.proto(),
            params = this.get("currentContext.options.withParams"),
            clearThem = {};

        for (var key in params) {
          clearThem[key] = proto[key];
        }
        source.setProperties(clearThem);
      }
    }
  });

  function proxyToInnerInstance(self, message) {
    var vi = self.get("innerViewInstance");
    if (vi) {
      vi.send(message);
    }
  }

});
define('pilas-website-test/components/liquid-spacer', ['exports', 'ember', 'liquid-fire/promise'], function (exports, Ember, Promise) {

  'use strict';

  exports['default'] = Ember['default'].Component.extend({
    growDuration: 250,
    growPixelsPerSecond: 200,
    growEasing: "slide",
    enabled: true,

    didInsertElement: function () {
      var child = this.$("> div");
      this.$().css({
        overflow: "hidden",
        width: child.width(),
        height: child.height()
      });
    },

    sizeChange: Ember['default'].observer("width", "height", function () {
      var elt = this.$();
      if (!this.get("enabled")) {
        elt.width(this.get("width"));
        elt.height(this.get("height"));
        return Promise['default'].resolve();
      }
      return Promise['default'].all([this.adaptDimension(elt, "width"), this.adaptDimension(elt, "height")]);
    }),

    adaptDimension: function (elt, dimension) {
      var have = elt[dimension]();
      var want = this.get(dimension);
      var target = {};
      target[dimension] = want;

      return Ember['default'].$.Velocity(elt[0], target, {
        duration: this.durationFor(have, want),
        queue: false,
        easing: this.get("growEasing")
      });
    },

    durationFor: function (before, after) {
      return Math.min(this.get("growDuration"), 1000 * Math.abs(before - after) / this.get("growPixelsPerSecond"));
    } });

});
define('pilas-website-test/components/lm-container', ['exports', 'ember', 'liquid-fire/tabbable'], function (exports, Ember) {

  'use strict';

  /*
     Parts of this file were adapted from ic-modal

     https://github.com/instructure/ic-modal
     Released under The MIT License (MIT)
     Copyright (c) 2014 Instructure, Inc.
  */

  var lastOpenedModal = null;
  Ember['default'].$(document).on("focusin", handleTabIntoBrowser);

  function handleTabIntoBrowser() {
    if (lastOpenedModal) {
      lastOpenedModal.focus();
    }
  }


  exports['default'] = Ember['default'].Component.extend({
    classNames: ["lm-container"],
    attributeBindings: ["tabindex"],
    tabindex: 0,

    keyUp: function (event) {
      // Escape key
      if (event.keyCode === 27) {
        this.sendAction();
      }
    },

    keyDown: function (event) {
      // Tab key
      if (event.keyCode === 9) {
        this.constrainTabNavigation(event);
      }
    },

    didInsertElement: function () {
      this.focus();
      lastOpenedModal = this;
    },

    willDestroy: function () {
      lastOpenedModal = null;
    },

    focus: function () {
      if (this.get("element").contains(document.activeElement)) {
        // just let it be if we already contain the activeElement
        return;
      }
      var target = this.$("[autofocus]");
      if (!target.length) {
        target = this.$(":tabbable");
      }

      if (!target.length) {
        target = this.$();
      }

      target[0].focus();
    },

    constrainTabNavigation: function (event) {
      var tabbable = this.$(":tabbable");
      var finalTabbable = tabbable[event.shiftKey ? "first" : "last"]()[0];
      var leavingFinalTabbable = finalTabbable === document.activeElement ||
      // handle immediate shift+tab after opening with mouse
      this.get("element") === document.activeElement;
      if (!leavingFinalTabbable) {
        return;
      }
      event.preventDefault();
      tabbable[event.shiftKey ? "last" : "first"]()[0].focus();
    }
  });

});
define('pilas-website-test/components/photo-coleccion', ['exports', 'ember'], function (exports, Ember) {

  'use strict';

  exports['default'] = Ember['default'].Component.extend({
    actions: {
      visualizar: function (url) {
        $.magnificPopup.open({
          items: {
            src: url },
          type: "image"
        });
      }

    }
  });

});
define('pilas-website-test/components/pilas-colaborador', ['exports', 'ember'], function (exports, Ember) {

  'use strict';

  exports['default'] = Ember['default'].Component.extend({
    tagName: "div",
    classNames: ["col-lg-2", "miembro-contenedor"],
    href_github: (function () {
      return "https://github.com/" + this.get("github");
    }).property("href_github")
  });

});
define('pilas-website-test/components/pilas-miembro', ['exports', 'ember'], function (exports, Ember) {

  'use strict';

  exports['default'] = Ember['default'].Component.extend({
    tagName: "div",
    classNames: ["col-lg-2", "miembro-contenedor"],
    href_github: (function () {
      return "https://github.com/" + this.get("github");
    }).property("href_github")
  });

});
define('pilas-website-test/components/pilas-noticias', ['exports', 'ember'], function (exports, Ember) {

  'use strict';

  exports['default'] = Ember['default'].Component.extend({
    logs: [],
    didInsertElement: function () {
      this.set("logs", window.pilas_log.posts);
    } });

});
define('pilas-website-test/components/safe-html', ['exports', 'ember'], function (exports, Ember) {

  'use strict';

  exports['default'] = Ember['default'].Component.extend({
    contenido: (function () {
      return new Ember['default'].Handlebars.SafeString(this.get("value"));
    }).property()
  });

});
define('pilas-website-test/controllers/galeria', ['exports', 'ember'], function (exports, Ember) {

  'use strict';

  exports['default'] = Ember['default'].Controller.extend({

    photosEjemplos: (function () {
      return window.photos_ejemplos.feed.entry;
    }).property(),
    photosEquipos: (function () {
      return window.photos_equipos.feed.entry;
    }).property(),
    photosEventos: (function () {
      return window.photos_eventos.feed.entry;
    }).property(),
    photosSistemas: (function () {
      return window.photos_sistemas.feed.entry;
    }).property() });

});
define('pilas-website-test/helpers/liquid-bind', ['exports', 'ember'], function (exports, Ember) {

  'use strict';

  /* liquid-bind is really just liquid-with with a pre-provided block
     that just says {{this}} */
  function liquidBindHelperFunc() {
    var options = arguments[arguments.length - 1];
    var container = options.data.view.container;
    var componentLookup = container.lookup("component-lookup:main");
    var cls = componentLookup.lookupFactory("liquid-bind-c");
    options.hash.value = arguments[0];
    options.hashTypes.value = options.types[0];

    if (options.hash["class"]) {
      options.hash.innerClass = options.hash["class"];
      delete options.hash["class"];
      options.hashTypes.innerClass = options.hashTypes["class"];
      delete options.hashTypes["class"];
    }
    Ember['default'].Handlebars.helpers.view.call(this, cls, options);
  }

  function htmlbarsLiquidBindHelper(params, hash, options, env) {
    var componentLookup = this.container.lookup("component-lookup:main");
    var cls = componentLookup.lookupFactory("liquid-bind-c");
    hash.value = params[0];
    if (hash["class"]) {
      hash.innerClass = hash["class"];
      delete hash["class"];
    }
    env.helpers.view.helperFunction.call(this, [cls], hash, options, env);
  }

  var liquidBindHelper;

  if (Ember['default'].HTMLBars) {
    liquidBindHelper = {
      isHTMLBars: true,
      helperFunction: htmlbarsLiquidBindHelper
    };
  } else {
    liquidBindHelper = liquidBindHelperFunc;
  }

  exports['default'] = liquidBindHelper;

});
define('pilas-website-test/helpers/liquid-if', ['exports', 'ember'], function (exports, Ember) {

  'use strict';

  exports.factory = factory;

  var isHTMLBars = !!Ember['default'].HTMLBars;

  function factory(invert) {
    var helperFunc = function () {
      var property, hash, options, env, container;

      if (isHTMLBars) {
        property = arguments[0][0];
        hash = arguments[1];
        options = arguments[2];
        env = arguments[3];
        container = this.container;
      } else {
        property = arguments[0];
        options = arguments[1];
        hash = options.hash;
        container = options.data.view.container;
      }
      var View = container.lookupFactory("view:liquid-if");

      var templates = [options.fn || options.template, options.inverse];
      if (invert) {
        templates.reverse();
      }
      delete options.fn;
      delete options.template;
      delete options.inverse;

      if (hash.containerless) {
        View = View.extend(Ember['default']._Metamorph);
      }

      hash.templates = templates;

      if (isHTMLBars) {
        hash.showFirst = property;
        env.helpers.view.helperFunction.call(this, [View], hash, options, env);
      } else {
        hash.showFirstBinding = property;
        return Ember['default'].Handlebars.helpers.view.call(this, View, options);
      }
    };

    if (Ember['default'].HTMLBars) {
      return {
        isHTMLBars: true,
        helperFunction: helperFunc,
        preprocessArguments: function () {}
      };
    } else {
      return helperFunc;
    }
  }

  exports['default'] = factory(false);

});
define('pilas-website-test/helpers/liquid-measure', ['exports', 'ember'], function (exports, Ember) {

  'use strict';

  exports['default'] = function () {
    Ember['default'].assert("liquid-measure is deprecated, see CHANGELOG.md", false);
  };

});
define('pilas-website-test/helpers/liquid-outlet', ['exports', 'ember'], function (exports, Ember) {

  'use strict';

  var isHTMLBars = !!Ember['default'].HTMLBars;

  function liquidOutletHelperFunc(property, options) {
    var property, options, container, hash, env;

    if (isHTMLBars) {
      property = arguments[0][0]; // params[0]
      hash = arguments[1];
      options = arguments[2];
      env = arguments[3];
      container = this.container;

      if (!property) {
        property = "main";
        options.paramTypes = ["string"];
      }
    } else {
      property = arguments[0];

      if (property && property.data && property.data.isRenderData) {
        options = property;
        property = "main";
        options.types = ["STRING"];
      }

      container = options.data.view.container;
      hash = options.hash;
    }

    var View = container.lookupFactory("view:liquid-outlet");
    if (hash.containerless) {
      View = View.extend(Ember['default']._Metamorph);
    }
    hash.viewClass = View;

    if (isHTMLBars) {
      env.helpers.outlet.helperFunction.call(this, [property], hash, options, env);
    } else {
      return Ember['default'].Handlebars.helpers.outlet.call(this, property, options);
    }
  }

  var liquidOutletHelper = liquidOutletHelperFunc;
  if (Ember['default'].HTMLBars) {
    liquidOutletHelper = {
      isHTMLBars: true,
      helperFunction: liquidOutletHelperFunc,
      preprocessArguments: function () {}
    };
  }

  exports['default'] = liquidOutletHelper;

});
define('pilas-website-test/helpers/liquid-unless', ['exports', 'pilas-website-test/helpers/liquid-if'], function (exports, liquid_if) {

	'use strict';

	exports['default'] = liquid_if.factory(true);

});
define('pilas-website-test/helpers/liquid-with', ['exports', 'ember'], function (exports, Ember) {

  'use strict';

  var isHTMLBars = !!Ember['default'].HTMLBars;

  function liquidWithHelperFunc() {
    var params, context, options, container, innerOptions, data, hash, env;

    var innerOptions = {
      hashTypes: {}
    };

    var innerHash = {};

    if (isHTMLBars) {
      params = arguments[0];
      hash = arguments[1];
      options = arguments[2];
      env = arguments[3];
      context = params[0];
      container = this.container;
      data = arguments[3].data;
      innerOptions.morph = options.morph;

      if (params.length === 3) {
        hash.keywordName = params[2]._label;
        params = [context];
      }
      innerHash.boundContext = context;
    } else {
      params = Array.prototype.slice.apply(arguments, [0, -1]);
      context = arguments[0];
      options = arguments[arguments.length - 1];
      data = options.data;
      hash = options.hash;
      container = data.view.container;
      innerOptions.data = data;
      innerOptions.hash = innerHash;
      innerHash.boundContextBinding = context;
    }

    var View = container.lookupFactory("view:liquid-with");

    View = View.extend({
      originalArgs: params,
      originalHash: hash,
      originalHashTypes: options.hashTypes,
      innerTemplate: options.fn || options.template
    });

    var containerless = isHTMLBars && hash.containerless && (!hash.containerless.isStream || hash.containerless.value()) || !isHTMLBars && (options.hashTypes.containerless === "BOOLEAN" && hash.containerless || options.hashTypes.containerless === "ID" && this.containerless);

    if (containerless) {
      View = View.extend(Ember['default']._Metamorph);
    }


    ["class", "classNames", "classNameBindings", "use", "id", "growDuration", "growPixelsPerSecond", "growEasing", "enableGrowth", "containerless"].forEach(function (field) {
      if (hash.hasOwnProperty(field)) {
        innerHash[field] = hash[field];
        innerOptions.hashTypes[field] = options.hashTypes ? options.hashTypes[field] : undefined;
      }
    });

    if (isHTMLBars) {
      env.helpers.view.helperFunction.call(this, [View], innerHash, innerOptions, env);
    } else {
      if (containerless) {
        delete innerOptions.hash["class"];
        delete innerOptions.hash.classNames;
        delete innerOptions.hash.classNameBindings;
      }
      return Ember['default'].Handlebars.helpers.view.call(this, View, innerOptions);
    }
  }

  var liquidWithHelper = liquidWithHelperFunc;
  if (isHTMLBars) {
    liquidWithHelper = {
      isHTMLBars: true,
      helperFunction: liquidWithHelperFunc,
      preprocessArguments: function () {}
    };
  }

  exports['default'] = liquidWithHelper;

});
define('pilas-website-test/helpers/with-apply', ['exports', 'ember'], function (exports, Ember) {

  'use strict';

  var isHTMLBars = !!Ember['default'].HTMLBars;

  // This helper is internal to liquid-with.
  function withApplyHelperFunc() {
    var hash, options, env, view;

    if (isHTMLBars) {
      hash = arguments[1];
      options = arguments[2];
      env = arguments[3];
      view = this;
    } else {
      options = arguments[0];
      hash = options.hash;
      view = options.data.view;
    }

    var parent = view.get("liquidWithParent");
    var withArgs = parent.get("originalArgs").slice();

    withArgs[0] = "lwith-view.boundContext";
    options = Ember['default'].copy(options);

    // This works to inject our keyword in Ember >= 1.9
    if (!view._keywords) {
      view._keywords = {};
    }
    view._keywords["lwith-view"] = view;

    // This works to inject our keyword in Ember < 1.9
    if (!isHTMLBars) {
      if (!options.data.keywords) {
        options.data.keywords = {};
      }
      options.data.keywords["lwith-view"] = view;
    }

    if (isHTMLBars) {
      options.template = parent.get("innerTemplate");
    } else {
      options.fn = parent.get("innerTemplate");
    }

    hash = parent.get("originalHash");
    options.hashTypes = parent.get("originalHashTypes");

    if (isHTMLBars) {
      env.helpers["with"].helperFunction.call(this, [view.getStream(withArgs[0])], hash, options, env);
    } else {
      options.hash = hash;
      withArgs.push(options);
      return Ember['default'].Handlebars.helpers["with"].apply(this, withArgs);
    }
  }

  var withApplyHelper = withApplyHelperFunc;
  if (Ember['default'].HTMLBars) {
    withApplyHelper = {
      isHTMLBars: true,
      helperFunction: withApplyHelperFunc,
      preprocessArguments: function () {}
    };
  }

  exports['default'] = withApplyHelper;

});
define('pilas-website-test/initializers/ember-moment', ['exports', 'ember-moment/helpers/moment', 'ember-moment/helpers/ago', 'ember-moment/helpers/duration', 'ember'], function (exports, moment, ago, duration, Ember) {

  'use strict';

  var initialize = function () {
    var registerHelper;

    if (Ember['default'].HTMLBars) {
      registerHelper = function (helperName, fn) {
        Ember['default'].HTMLBars._registerHelper(helperName, Ember['default'].HTMLBars.makeBoundHelper(fn));
      };
    } else {
      registerHelper = Ember['default'].Handlebars.helper;
    };

    registerHelper("moment", moment['default']);
    registerHelper("ago", ago['default']);
    registerHelper("duration", duration['default']);
  };

  exports['default'] = {
    name: "ember-moment",

    initialize: initialize
  };
  /* container, app */

  exports.initialize = initialize;

});
define('pilas-website-test/initializers/export-application-global', ['exports', 'ember', 'pilas-website-test/config/environment'], function (exports, Ember, config) {

  'use strict';

  exports.initialize = initialize;

  function initialize(container, application) {
    var classifiedName = Ember['default'].String.classify(config['default'].modulePrefix);

    if (config['default'].exportApplicationGlobal && !window[classifiedName]) {
      window[classifiedName] = application;
    }
  };

  exports['default'] = {
    name: "export-application-global",

    initialize: initialize
  };

});
define('pilas-website-test/initializers/img-manager-service', ['exports'], function (exports) {

  'use strict';

  exports.initialize = initialize;

  function initialize(container, application) {
    application.inject("component:img-wrap", "manager", "service:img-manager");
    application.inject("view", "imgManagerService", "service:img-manager");
  }

  exports['default'] = {
    name: "img-manager-service",
    initialize: initialize
  };

});
define('pilas-website-test/initializers/liquid-fire', ['exports', 'liquid-fire', 'ember'], function (exports, liquid_fire, Ember) {

  'use strict';

  exports['default'] = {
    name: "liquid-fire",

    initialize: function (container) {
      if (!Ember['default'].$.Velocity) {
        Ember['default'].warn("Velocity.js is missing");
      } else {
        var version = Ember['default'].$.Velocity.version;
        var recommended = [0, 11, 8];
        if (Ember['default'].compare(recommended, [version.major, version.minor, version.patch]) === 1) {
          Ember['default'].warn("You should probably upgrade Velocity.js, recommended minimum is " + recommended.join("."));
        }
      }

      liquid_fire.initialize(container);
    }
  };

});
define('pilas-website-test/initializers/videos-service', ['exports'], function (exports) {

  'use strict';

  exports.initialize = initialize;

  function initialize(container, application) {
    application.inject("route", "videosService", "service:videos");
  }

  exports['default'] = {
    name: "videos-service",
    initialize: initialize
  };

});
define('pilas-website-test/mixins/img-manager/in-viewport', ['exports', 'ember'], function (exports, Ember) {

  'use strict';

  // Inspired from:
  // https://github.com/twokul/ember-lazy-image
  // https://medium.com/delightful-ui-for-ember-apps/ember-js-detecting-if-a-dom-element-is-in-the-viewport-eafcc77a6f86

  var on = Ember['default'].on;
  var get = Ember['default'].get;
  var debounce = Ember['default'].run.debounce;
  var scheduleOnce = Ember['default'].run.scheduleOnce;
  var computed = Ember['default'].computed;
  var bind = Ember['default'].run.bind;
  var next = Ember['default'].run.next;

  /**
   * @mixin ImgManagerInViewportMixin
   * @extension ImgManagerInViewportMixin
   * @uses Ember.Evented
   */
  exports['default'] = Ember['default'].Mixin.create(Ember['default'].Evented, {
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
            next(this, "trigger", "didEnterViewport");
          }
        }
      } else {
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
      if (this.isDestroying || this.isDestroyed || this._state !== "inDOM" || this.get("enteredViewport")) {
        return;
      }
      rect = this.$()[0].getBoundingClientRect();
      this.set("enteredViewport", rect.top >= 0 && rect.left >= 0 && rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) && rect.right <= (window.innerWidth || document.documentElement.clientWidth));
    },

    /**
     * Set the initial value of `enteredViewport`
     *
     * @method _setInitialViewport
     * @private
     */
    _setInitialViewport: on("didInsertElement", function () {
      scheduleOnce("afterRender", this, "_setViewport");
    }),

    /**
     * Handles the scroll event
     *
     * @method _scrollHandler
     * @private
     */
    _scrollHandler: function () {
      debounce(this, "_setViewport", get(this, "scrollTimeout"));
    },

    /**
     * Starts listening for the scroll event
     *
     * @method _bindScroll
     * @private
     */
    _bindScroll: on("didInsertElement", function () {
      this._unbindScroll();
      if (!this.get("enteredViewport")) {
        this._boundScrollHandler = bind(this, "_scrollHandler");
        Ember['default'].$(document).on("touchmove", this._boundScrollHandler);
        Ember['default'].$(window).on("scroll", this._boundScrollHandler);
      }
    }),

    /**
     * Stops listening for the scroll event
     *
     * @method _bindScroll
     * @private
     */
    _unbindScroll: on("willDestroyElement", function () {
      if (this._boundScrollHandler) {
        Ember['default'].$(window).off("scroll", this._boundScrollHandler);
        Ember['default'].$(document).off("touchmove", this._boundScrollHandler);
        this._boundScrollHandler = null;
      }
    })
  });

});
define('pilas-website-test/router', ['exports', 'ember', 'pilas-website-test/config/environment'], function (exports, Ember, config) {

  'use strict';

  var Router = Ember['default'].Router.extend({
    location: config['default'].locationType
  });

  Router.map(function () {
    this.route("blog");
    this.route("foro");
    this.route("galeria");

    this.resource("videos", { path: "/videos" }, function () {
      this.route("play", { path: "/:video_id" });
    });

    this.route("docs");
    this.route("descargas");
    this.route("acercade");
    this.route("photo-modal");
  });

  exports['default'] = Router;

});
define('pilas-website-test/routes/acercade', ['exports', 'ember'], function (exports, Ember) {

	'use strict';

	exports['default'] = Ember['default'].Route.extend({});

});
define('pilas-website-test/routes/blog', ['exports', 'ember'], function (exports, Ember) {

  'use strict';

  exports['default'] = Ember['default'].Route.extend({
    model: function () {
      return [];
    }
  });

});
define('pilas-website-test/routes/descargas', ['exports', 'ember'], function (exports, Ember) {

  'use strict';

  exports['default'] = Ember['default'].Route.extend({
    model: function () {
      return {
        version: "0.90.37",
        fecha: "2015-06-16",
        link_mac: "https://dl.dropboxusercontent.com/u/1335422/releases/pilas-engine/0.90.37/pilas-engine-0.90.37.dmg",
        link_windows: "https://dl.dropboxusercontent.com/u/1335422/releases/pilas-engine/0.90.37/pilas-engine_0.90.37.exe",
        link_deb: "http://repo.huayra.conectarigualdad.gob.ar/huayra/pool/main/p/python-pilas/" };
    }
  });

});
define('pilas-website-test/routes/descargas_template', ['exports', 'ember'], function (exports, Ember) {

  'use strict';

  exports['default'] = Ember['default'].Route.extend({
    model: function () {
      return {
        version: "VERSION",
        fecha: "FECHA",
        link_mac: "https://dl.dropboxusercontent.com/u/1335422/releases/pilas-engine/VERSION/pilas-engine-VERSION.dmg",
        link_windows: "https://dl.dropboxusercontent.com/u/1335422/releases/pilas-engine/VERSION/pilas-engine_VERSION.exe",
        link_deb: "http://repo.huayra.conectarigualdad.gob.ar/huayra/pool/main/p/python-pilas/" };
    }
  });

});
define('pilas-website-test/routes/docs', ['exports', 'ember'], function (exports, Ember) {

	'use strict';

	exports['default'] = Ember['default'].Route.extend({});

});
define('pilas-website-test/routes/foro', ['exports', 'ember'], function (exports, Ember) {

	'use strict';

	exports['default'] = Ember['default'].Route.extend({});

});
define('pilas-website-test/routes/galeria', ['exports', 'ember'], function (exports, Ember) {

	'use strict';

	exports['default'] = Ember['default'].Route.extend({});

});
define('pilas-website-test/routes/index', ['exports', 'ember'], function (exports, Ember) {

	'use strict';

	exports['default'] = Ember['default'].Route.extend({});

});
define('pilas-website-test/routes/photo-modal', ['exports', 'ember'], function (exports, Ember) {

	'use strict';

	exports['default'] = Ember['default'].Route.extend({});

});
define('pilas-website-test/routes/videos', ['exports', 'ember'], function (exports, Ember) {

  'use strict';

  exports['default'] = Ember['default'].Route.extend({
    model: function () {
      return this.get("videosService").getVideos();
    }
  });

});
define('pilas-website-test/routes/videos/play', ['exports', 'ember'], function (exports, Ember) {

  'use strict';

  exports['default'] = Ember['default'].Route.extend({
    needs: ["video"],
    model: function (params) {
      return this.get("videosService").getVideobyIndex(params.video_id);
    }
  });

});
define('pilas-website-test/services/img-manager', ['exports', 'ember', 'pilas-website-test/utils/img-manager/img-rule', 'pilas-website-test/utils/img-manager/img-source', 'pilas-website-test/config/environment', 'pilas-website-test/utils/img-manager/simple-map'], function (exports, Ember, ImgRule, ImgSource, ENV, SimpleMap) {

  'use strict';

  var map = Ember['default'].EnumerableUtils.map;
  var computed = Ember['default'].computed;
  var readOnly = computed.readOnly;
  var bind = Ember['default'].run.bind;

  /**
   * @module img-manager
   * @class ImgManagerService
   * @extends Ember.Object
   */
  exports['default'] = Ember['default'].Object.extend({
    /**
     * Our configuration
     * @property config
     * @type {Object}
     */
    config: computed(function () {
      return Ember['default'].merge({
        maxTries: 1,
        loadingClass: "loading",
        errorClass: "error",
        successClass: "success",
        lazyLoad: true
      }, Ember['default'].get(ENV['default'], "imgManager"));
    }).readOnly(),

    /**
     * The default delay
     * @property defaultDelay
     * @type {number}
     */
    defaultDelay: readOnly("config.delay"),

    /**
     * The default lazyLoad
     * @property defaultLazyLoad
     * @type {boolean}
     */
    defaultLazyLoad: readOnly("config.lazyLoad"),

    /**
     * The default batch size
     * @property defaultBatchSize
     * @type {number}
     */
    defaultBatchSize: readOnly("config.batchSize"),

    /**
     * The default max tries
     * @property defaultMaxTries
     * @type {number}
     */
    defaultMaxTries: readOnly("config.maxTries", 1),

    /**
     * The default loading src
     * @property defaultLoadingSrc
     * @type {number}
     */
    defaultLoadingSrc: readOnly("config.loadingSrc"),

    /**
     * The default error src
     * @property defaultErrorSrc
     * @type {number}
     */
    defaultErrorSrc: readOnly("config.errorSrc"),

    /**
     * Default css class for the wrapper of a loading image
     * @property defaultLoadingClass
     * @type {string}
     */
    defaultLoadingClass: readOnly("config.loadingClass"),

    /**
     * Default css class for the wrapper of an image which failed to load
     * @property defaultErrorClass
     * @type {string}
     */
    defaultErrorClass: readOnly("config.errorClass"),

    /**
     * Default css class for the wrapper of an image which loaded successfully
     * @property defaultSuccessClass
     * @type {string}
     */
    defaultSuccessClass: readOnly("config.successClass"),


    /**
     * Get the img source object for the given src
     *
     * @method imgSourceForSrc
     * @param {string} src
     * @return {ImgSource}
     */
    imgSourceForSrc: function (src) {
      var dict = this.get("_imgSources"),
          imgSource = dict.get(src);
      if (!imgSource) {
        dict.set(src, imgSource = src ? ImgSource['default'].create({
          src: src,
          manager: this
        }) : null);
        if (imgSource) {
          this.incrementProperty("totalSources");
          imgSource.one("didError", bind(this, "incrementProperty", "totalErrors", 1));
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
      var rules = Ember['default'].A(map(this.get("config.rules") || [], function (ruleConfig) {
        return ImgRule['default'].create({
          manager: _this,
          config: ruleConfig
        });
      }));
      // add a default rule matching everything
      rules.pushObject(ImgRule['default'].create({
        manager: this,
        config: { match: "*" }
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
      return this.get("rules").find(function (rule) {
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
      return new SimpleMap['default']();
    }).readOnly()
  });

});
define('pilas-website-test/services/videos', ['exports', 'ember'], function (exports, Ember) {

  'use strict';

  var videos = [{ id: 7, titulo: "Pilas en tv pública", tipo: "youtube", url: "http://www.youtube.com/embed/4KpLctdBrf8" }, { id: 8, titulo: "Pilas en WISIT 2014 (Argentina)", tipo: "youtube", url: "http://www.youtube.com/embed/l2nh3YYW29k" }, { id: 1, titulo: "Pilas en PyCon España 2013 (Madrid, España)", tipo: "youtube", url: "http://www.youtube.com/embed/bjlWZjTZLmQ" }, { id: 2, titulo: "Pilas en PyCon Argentina 2013 (Rosario, Argentina)", tipo: "youtube", url: "http://www.youtube.com/embed/tXA2BgzrvzA" }, { id: 3, titulo: "Pilas en PyCon Argentina 2012", tipo: "youtube", url: "http://www.youtube.com/embed/sQhxjLoJlZs" }, { id: 4, titulo: "Presentación de pilas en betabeers Bs. As. Marzo 2012", tipo: "youtube", url: "http://www.youtube.com/embed/-Z6Qi_B9QSA" }, { id: 5, titulo: "Haciendo videojuegos con pilas (pyday 2011)", tipo: "vimeo", url: "http://player.vimeo.com/video/23735704?title=0&amp;byline=0&amp;portrait=0" }, { id: 6, titulo: "Presentación Conurbania 2010", tipo: "vimeo", url: "http://player.vimeo.com/video/17273297" }];

  exports['default'] = Ember['default'].Object.extend({
    getVideobyIndex: function (id) {
      var record = null;

      videos.forEach(function (e) {
        if (e.id === id) {
          record = e;
        }
      });

      return record;
    },
    getVideos: function () {
      return videos;
    }
  });

});
define('pilas-website-test/templates/acercade', ['exports', 'ember'], function (exports, Ember) {

  'use strict';

  exports['default'] = Ember['default'].Handlebars.template(function anonymous(Handlebars,depth0,helpers,partials,data
  /**/) {
  this.compilerInfo = [4,'>= 1.0.0'];
  helpers = this.merge(helpers, Ember['default'].Handlebars.helpers); data = data || {};
    var buffer = '', stack1, helper, options, self=this, helperMissing=helpers.helperMissing;

  function program1(depth0,data) {
    
    
    data.buffer.push("Lider de proyecto y desarrollador.");
    }

  function program3(depth0,data) {
    
    
    data.buffer.push("Ilustrador");
    }

  function program5(depth0,data) {
    
    
    data.buffer.push("Desarrollador");
    }

  function program7(depth0,data) {
    
    var buffer = '';
    return buffer;
    }

    data.buffer.push("<div class=\"page-header center\">\n  <h1>Acerca de pilas</h1>\n</div>\n\n\n<div class='row'>\n  <h2>¿Que es pilas-engine?</h2>\n</div>\n\n<div class='row'>\n  <p>\n  Pilas es una herramienta para construir videojuegos de manera sencilla y divertida.\n  </p>\n\n  <p>\n  Ideamos esta herramienta para que los jóvenes puedan descubrir y\n  aprender a programar computadoras. Creemos que aprender a programar es\n  espectacular, porque les permite tener el control de las computadora, inventar\n  y desarrollar cualquier tipo de software.\n  </p>\n\n  <p>\n    <div class='sprite acercade-preview'></div>\n  </p>\n\n</div>\n\n\n<div class='row'>\n  <h1>El equipo principal</h1>\n\n  <p>\n  En el desarrollo de pilas participamos varias personas, somos una comunidad\n  abierta y colaborativa de programadores, docentes y estudiates de distintas\n  partes del mundo:\n  </p>\n</div>\n\n<div class='row'>\n  ");
    stack1 = (helper = helpers['pilas-miembro'] || (depth0 && depth0['pilas-miembro']),options={hash:{
      'nombre': ("Hugo Ruscitti"),
      'email': ("hugoruscitti@gmail.com"),
      'github': ("hugoruscitti")
    },hashTypes:{'nombre': "STRING",'email': "STRING",'github': "STRING"},hashContexts:{'nombre': depth0,'email': depth0,'github': depth0},inverse:self.noop,fn:self.program(1, program1, data),contexts:[],types:[],data:data},helper ? helper.call(depth0, options) : helperMissing.call(depth0, "pilas-miembro", options));
    if(stack1 || stack1 === 0) { data.buffer.push(stack1); }
    data.buffer.push("\n  ");
    stack1 = (helper = helpers['pilas-miembro'] || (depth0 && depth0['pilas-miembro']),options={hash:{
      'nombre': ("Walter Velazquez"),
      'email': ("wgv_4810@hotmail.com"),
      'github': ("")
    },hashTypes:{'nombre': "STRING",'email': "STRING",'github': "STRING"},hashContexts:{'nombre': depth0,'email': depth0,'github': depth0},inverse:self.noop,fn:self.program(3, program3, data),contexts:[],types:[],data:data},helper ? helper.call(depth0, options) : helperMissing.call(depth0, "pilas-miembro", options));
    if(stack1 || stack1 === 0) { data.buffer.push(stack1); }
    data.buffer.push("\n  ");
    stack1 = (helper = helpers['pilas-miembro'] || (depth0 && depth0['pilas-miembro']),options={hash:{
      'nombre': ("Enrique Porta"),
      'email': ("quiqueporta@gmail.com"),
      'github': ("quiqueporta")
    },hashTypes:{'nombre': "STRING",'email': "STRING",'github': "STRING"},hashContexts:{'nombre': depth0,'email': depth0,'github': depth0},inverse:self.noop,fn:self.program(5, program5, data),contexts:[],types:[],data:data},helper ? helper.call(depth0, options) : helperMissing.call(depth0, "pilas-miembro", options));
    if(stack1 || stack1 === 0) { data.buffer.push(stack1); }
    data.buffer.push("\n  ");
    stack1 = (helper = helpers['pilas-miembro'] || (depth0 && depth0['pilas-miembro']),options={hash:{
      'nombre': ("Fernando Salamero"),
      'email': ("fsalamero@gmail.com"),
      'github': ("fsalamero")
    },hashTypes:{'nombre': "STRING",'email': "STRING",'github': "STRING"},hashContexts:{'nombre': depth0,'email': depth0,'github': depth0},inverse:self.noop,fn:self.program(5, program5, data),contexts:[],types:[],data:data},helper ? helper.call(depth0, options) : helperMissing.call(depth0, "pilas-miembro", options));
    if(stack1 || stack1 === 0) { data.buffer.push(stack1); }
    data.buffer.push("\n  ");
    stack1 = (helper = helpers['pilas-miembro'] || (depth0 && depth0['pilas-miembro']),options={hash:{
      'nombre': ("Irving Rodriguez"),
      'email': ("irving.prog@gmail.com"),
      'github': ("irvingprog")
    },hashTypes:{'nombre': "STRING",'email': "STRING",'github': "STRING"},hashContexts:{'nombre': depth0,'email': depth0,'github': depth0},inverse:self.noop,fn:self.program(5, program5, data),contexts:[],types:[],data:data},helper ? helper.call(depth0, options) : helperMissing.call(depth0, "pilas-miembro", options));
    if(stack1 || stack1 === 0) { data.buffer.push(stack1); }
    data.buffer.push("\n</div>\n\n<div class='row center'>\n  <h1>El equipo de colaboradores</h1>\n</div>\n\n<div class='row'>\n  ");
    stack1 = (helper = helpers['pilas-colaborador'] || (depth0 && depth0['pilas-colaborador']),options={hash:{
      'nombre': ("Marcos Vanetta"),
      'email': ("marcosvanetta@gmail.com"),
      'github': ("malev")
    },hashTypes:{'nombre': "STRING",'email': "STRING",'github': "STRING"},hashContexts:{'nombre': depth0,'email': depth0,'github': depth0},inverse:self.noop,fn:self.program(7, program7, data),contexts:[],types:[],data:data},helper ? helper.call(depth0, options) : helperMissing.call(depth0, "pilas-colaborador", options));
    if(stack1 || stack1 === 0) { data.buffer.push(stack1); }
    data.buffer.push("\n  ");
    stack1 = (helper = helpers['pilas-colaborador'] || (depth0 && depth0['pilas-colaborador']),options={hash:{
      'nombre': ("Luciano Baraglia"),
      'email': (""),
      'github': ("lucianobaraglia")
    },hashTypes:{'nombre': "STRING",'email': "STRING",'github': "STRING"},hashContexts:{'nombre': depth0,'email': depth0,'github': depth0},inverse:self.noop,fn:self.program(7, program7, data),contexts:[],types:[],data:data},helper ? helper.call(depth0, options) : helperMissing.call(depth0, "pilas-colaborador", options));
    if(stack1 || stack1 === 0) { data.buffer.push(stack1); }
    data.buffer.push("\n  ");
    stack1 = (helper = helpers['pilas-colaborador'] || (depth0 && depth0['pilas-colaborador']),options={hash:{
      'nombre': ("Hernan Lozano"),
      'email': ("hernantz@gmail.com"),
      'github': ("hernantz")
    },hashTypes:{'nombre': "STRING",'email': "STRING",'github': "STRING"},hashContexts:{'nombre': depth0,'email': depth0,'github': depth0},inverse:self.noop,fn:self.program(7, program7, data),contexts:[],types:[],data:data},helper ? helper.call(depth0, options) : helperMissing.call(depth0, "pilas-colaborador", options));
    if(stack1 || stack1 === 0) { data.buffer.push(stack1); }
    data.buffer.push("\n  ");
    stack1 = (helper = helpers['pilas-colaborador'] || (depth0 && depth0['pilas-colaborador']),options={hash:{
      'nombre': ("Pablo Mouzo"),
      'email': ("pablomouzo@gmail.com"),
      'github': ("pablomouzo")
    },hashTypes:{'nombre': "STRING",'email': "STRING",'github': "STRING"},hashContexts:{'nombre': depth0,'email': depth0,'github': depth0},inverse:self.noop,fn:self.program(7, program7, data),contexts:[],types:[],data:data},helper ? helper.call(depth0, options) : helperMissing.call(depth0, "pilas-colaborador", options));
    if(stack1 || stack1 === 0) { data.buffer.push(stack1); }
    data.buffer.push("\n  ");
    stack1 = (helper = helpers['pilas-colaborador'] || (depth0 && depth0['pilas-colaborador']),options={hash:{
      'nombre': ("Diego Accorinti"),
      'email': ("diegoacco@gmail.com"),
      'github': ("DiegoAccorinti")
    },hashTypes:{'nombre': "STRING",'email': "STRING",'github': "STRING"},hashContexts:{'nombre': depth0,'email': depth0,'github': depth0},inverse:self.noop,fn:self.program(7, program7, data),contexts:[],types:[],data:data},helper ? helper.call(depth0, options) : helperMissing.call(depth0, "pilas-colaborador", options));
    if(stack1 || stack1 === 0) { data.buffer.push(stack1); }
    data.buffer.push("\n  ");
    stack1 = (helper = helpers['pilas-colaborador'] || (depth0 && depth0['pilas-colaborador']),options={hash:{
      'nombre': ("Diego Riquelme"),
      'email': (""),
      'github': ("diego_rr")
    },hashTypes:{'nombre': "STRING",'email': "STRING",'github': "STRING"},hashContexts:{'nombre': depth0,'email': depth0,'github': depth0},inverse:self.noop,fn:self.program(7, program7, data),contexts:[],types:[],data:data},helper ? helper.call(depth0, options) : helperMissing.call(depth0, "pilas-colaborador", options));
    if(stack1 || stack1 === 0) { data.buffer.push(stack1); }
    data.buffer.push("\n</div>\n\n<div class='row'>\n  ");
    stack1 = (helper = helpers['pilas-colaborador'] || (depth0 && depth0['pilas-colaborador']),options={hash:{
      'nombre': ("Felipe Gonzalez"),
      'email': (""),
      'github': ("felipe")
    },hashTypes:{'nombre': "STRING",'email': "STRING",'github': "STRING"},hashContexts:{'nombre': depth0,'email': depth0,'github': depth0},inverse:self.noop,fn:self.program(7, program7, data),contexts:[],types:[],data:data},helper ? helper.call(depth0, options) : helperMissing.call(depth0, "pilas-colaborador", options));
    if(stack1 || stack1 === 0) { data.buffer.push(stack1); }
    data.buffer.push("\n  ");
    stack1 = (helper = helpers['pilas-colaborador'] || (depth0 && depth0['pilas-colaborador']),options={hash:{
      'nombre': ("binary-sequence"),
      'email': ("sergiolindo.empresa@gmail.com"),
      'github': ("binary-sequence")
    },hashTypes:{'nombre': "STRING",'email': "STRING",'github': "STRING"},hashContexts:{'nombre': depth0,'email': depth0,'github': depth0},inverse:self.noop,fn:self.program(7, program7, data),contexts:[],types:[],data:data},helper ? helper.call(depth0, options) : helperMissing.call(depth0, "pilas-colaborador", options));
    if(stack1 || stack1 === 0) { data.buffer.push(stack1); }
    data.buffer.push("\n  ");
    stack1 = (helper = helpers['pilas-colaborador'] || (depth0 && depth0['pilas-colaborador']),options={hash:{
      'nombre': ("JuanBC"),
      'email': ("jbc.develop@gmail.com"),
      'github': ("leliel12")
    },hashTypes:{'nombre': "STRING",'email': "STRING",'github': "STRING"},hashContexts:{'nombre': depth0,'email': depth0,'github': depth0},inverse:self.noop,fn:self.program(7, program7, data),contexts:[],types:[],data:data},helper ? helper.call(depth0, options) : helperMissing.call(depth0, "pilas-colaborador", options));
    if(stack1 || stack1 === 0) { data.buffer.push(stack1); }
    data.buffer.push("\n  ");
    stack1 = (helper = helpers['pilas-colaborador'] || (depth0 && depth0['pilas-colaborador']),options={hash:{
      'nombre': ("Ivan Pedrazas"),
      'email': (""),
      'github': ("ipedrazas")
    },hashTypes:{'nombre': "STRING",'email': "STRING",'github': "STRING"},hashContexts:{'nombre': depth0,'email': depth0,'github': depth0},inverse:self.noop,fn:self.program(7, program7, data),contexts:[],types:[],data:data},helper ? helper.call(depth0, options) : helperMissing.call(depth0, "pilas-colaborador", options));
    if(stack1 || stack1 === 0) { data.buffer.push(stack1); }
    data.buffer.push("\n  ");
    stack1 = (helper = helpers['pilas-colaborador'] || (depth0 && depth0['pilas-colaborador']),options={hash:{
      'nombre': ("Jairo Trad"),
      'email': (""),
      'github': ("jairot")
    },hashTypes:{'nombre': "STRING",'email': "STRING",'github': "STRING"},hashContexts:{'nombre': depth0,'email': depth0,'github': depth0},inverse:self.noop,fn:self.program(7, program7, data),contexts:[],types:[],data:data},helper ? helper.call(depth0, options) : helperMissing.call(depth0, "pilas-colaborador", options));
    if(stack1 || stack1 === 0) { data.buffer.push(stack1); }
    data.buffer.push("\n  ");
    stack1 = (helper = helpers['pilas-colaborador'] || (depth0 && depth0['pilas-colaborador']),options={hash:{
      'nombre': ("Matías Iturburu"),
      'email': (""),
      'github': ("tutuca")
    },hashTypes:{'nombre': "STRING",'email': "STRING",'github': "STRING"},hashContexts:{'nombre': depth0,'email': depth0,'github': depth0},inverse:self.noop,fn:self.program(7, program7, data),contexts:[],types:[],data:data},helper ? helper.call(depth0, options) : helperMissing.call(depth0, "pilas-colaborador", options));
    if(stack1 || stack1 === 0) { data.buffer.push(stack1); }
    data.buffer.push("\n</div>\n\n<div class='row'>\n</div>\n");
    return buffer;
    
  });

});
define('pilas-website-test/templates/application', ['exports', 'ember'], function (exports, Ember) {

  'use strict';

  exports['default'] = Ember['default'].Handlebars.template(function anonymous(Handlebars,depth0,helpers,partials,data
  /**/) {
  this.compilerInfo = [4,'>= 1.0.0'];
  helpers = this.merge(helpers, Ember['default'].Handlebars.helpers); data = data || {};
    var buffer = '', stack1, helper, options, self=this, helperMissing=helpers.helperMissing;

  function program1(depth0,data) {
    
    
    data.buffer.push("<a href=#>Principal</a>");
    }

  function program3(depth0,data) {
    
    
    data.buffer.push("<a href=#>Noticias</a>");
    }

  function program5(depth0,data) {
    
    
    data.buffer.push("<a href=\"\">Foro</a>");
    }

  function program7(depth0,data) {
    
    
    data.buffer.push("<a href=\"\">Descargas</a>");
    }

  function program9(depth0,data) {
    
    
    data.buffer.push("<a href=\"\">Docs</a>");
    }

  function program11(depth0,data) {
    
    
    data.buffer.push("<a href=\"\">Galería</a>");
    }

  function program13(depth0,data) {
    
    
    data.buffer.push("<a href=\"\">Videos</a>");
    }

  function program15(depth0,data) {
    
    
    data.buffer.push("<a href=\"\">Acerca de ...</a>");
    }

    data.buffer.push("<div class=\"navbar navbar-default navbar-fixed-top\">\n      <div class=\"container\">\n\n        <div class=\"navbar-header\">\n          <a href='/' class=\"navbar-brand\">pilas-engine</a>\n          <button class=\"navbar-toggle\" type=\"button\" data-toggle=\"collapse\" data-target=\"#navbar-main\">\n            <span class=\"icon-bar\"></span>\n            <span class=\"icon-bar\"></span>\n            <span class=\"icon-bar\"></span>\n          </button>\n        </div>\n\n        <div class=\"navbar-collapse collapse\" id=\"navbar-main\">\n          <ul class=\"nav navbar-nav\">\n\n            ");
    stack1 = (helper = helpers['link-to'] || (depth0 && depth0['link-to']),options={hash:{
      'tagName': ("li"),
      'href': (false)
    },hashTypes:{'tagName': "STRING",'href': "BOOLEAN"},hashContexts:{'tagName': depth0,'href': depth0},inverse:self.noop,fn:self.program(1, program1, data),contexts:[depth0],types:["STRING"],data:data},helper ? helper.call(depth0, "index", options) : helperMissing.call(depth0, "link-to", "index", options));
    if(stack1 || stack1 === 0) { data.buffer.push(stack1); }
    data.buffer.push("\n            ");
    stack1 = (helper = helpers['link-to'] || (depth0 && depth0['link-to']),options={hash:{
      'tagName': ("li"),
      'href': (false)
    },hashTypes:{'tagName': "STRING",'href': "BOOLEAN"},hashContexts:{'tagName': depth0,'href': depth0},inverse:self.noop,fn:self.program(3, program3, data),contexts:[depth0],types:["STRING"],data:data},helper ? helper.call(depth0, "blog", options) : helperMissing.call(depth0, "link-to", "blog", options));
    if(stack1 || stack1 === 0) { data.buffer.push(stack1); }
    data.buffer.push("\n\n            ");
    stack1 = (helper = helpers['link-to'] || (depth0 && depth0['link-to']),options={hash:{
      'tagName': ("li"),
      'href': (false)
    },hashTypes:{'tagName': "STRING",'href': "BOOLEAN"},hashContexts:{'tagName': depth0,'href': depth0},inverse:self.noop,fn:self.program(5, program5, data),contexts:[depth0],types:["STRING"],data:data},helper ? helper.call(depth0, "foro", options) : helperMissing.call(depth0, "link-to", "foro", options));
    if(stack1 || stack1 === 0) { data.buffer.push(stack1); }
    data.buffer.push("\n            ");
    stack1 = (helper = helpers['link-to'] || (depth0 && depth0['link-to']),options={hash:{
      'tagName': ("li")
    },hashTypes:{'tagName': "STRING"},hashContexts:{'tagName': depth0},inverse:self.noop,fn:self.program(7, program7, data),contexts:[depth0],types:["STRING"],data:data},helper ? helper.call(depth0, "descargas", options) : helperMissing.call(depth0, "link-to", "descargas", options));
    if(stack1 || stack1 === 0) { data.buffer.push(stack1); }
    data.buffer.push("\n\n            ");
    stack1 = (helper = helpers['link-to'] || (depth0 && depth0['link-to']),options={hash:{
      'tagName': ("li")
    },hashTypes:{'tagName': "STRING"},hashContexts:{'tagName': depth0},inverse:self.noop,fn:self.program(9, program9, data),contexts:[depth0],types:["STRING"],data:data},helper ? helper.call(depth0, "docs", options) : helperMissing.call(depth0, "link-to", "docs", options));
    if(stack1 || stack1 === 0) { data.buffer.push(stack1); }
    data.buffer.push("\n            ");
    stack1 = (helper = helpers['link-to'] || (depth0 && depth0['link-to']),options={hash:{
      'tagName': ("li")
    },hashTypes:{'tagName': "STRING"},hashContexts:{'tagName': depth0},inverse:self.noop,fn:self.program(11, program11, data),contexts:[depth0],types:["STRING"],data:data},helper ? helper.call(depth0, "galeria", options) : helperMissing.call(depth0, "link-to", "galeria", options));
    if(stack1 || stack1 === 0) { data.buffer.push(stack1); }
    data.buffer.push("\n            ");
    stack1 = (helper = helpers['link-to'] || (depth0 && depth0['link-to']),options={hash:{
      'tagName': ("li")
    },hashTypes:{'tagName': "STRING"},hashContexts:{'tagName': depth0},inverse:self.noop,fn:self.program(13, program13, data),contexts:[depth0],types:["STRING"],data:data},helper ? helper.call(depth0, "videos", options) : helperMissing.call(depth0, "link-to", "videos", options));
    if(stack1 || stack1 === 0) { data.buffer.push(stack1); }
    data.buffer.push("\n            ");
    stack1 = (helper = helpers['link-to'] || (depth0 && depth0['link-to']),options={hash:{
      'tagName': ("li")
    },hashTypes:{'tagName': "STRING"},hashContexts:{'tagName': depth0},inverse:self.noop,fn:self.program(15, program15, data),contexts:[depth0],types:["STRING"],data:data},helper ? helper.call(depth0, "acercade", options) : helperMissing.call(depth0, "link-to", "acercade", options));
    if(stack1 || stack1 === 0) { data.buffer.push(stack1); }
    data.buffer.push("\n\n          </ul>\n        </div>\n      </div>\n    </div>\n\n<div class=\"container\"  id='top'>\n  <div class=\"bs-docs-section clearfix\">\n        <div class=\"row\">\n\n          <div class=\"col-lg-12\">\n\n	     ");
    stack1 = helpers._triageMustache.call(depth0, "liquid-outlet", {hash:{},hashTypes:{},hashContexts:{},contexts:[depth0],types:["ID"],data:data});
    if(stack1 || stack1 === 0) { data.buffer.push(stack1); }
    data.buffer.push("\n\n          </div>\n        </div>\n      </div>\n\n  <footer>\n    <div class=\"row center\">\n      <div class=\"col-lg-12\">\n\n        <a href=\"#\" class=\"sprite logo-pilas-footer\"><span class=\"hide\">pilas engine</span></a>\n\n            <div class='copyright'>&copy; Hugo Ruscitti</div>\n\n\n          <div id='github-footer'>\n            <div id=\"github-star\"><iframe src=\"http://ghbtns.com/github-btn.html?user=hugoruscitti&repo=pilas&type=watch&count=true\" allowtransparency=\"true\" frameborder=\"0\" scrolling=\"0\" width=\"110\" height=\"20\"></iframe></div>\n            <div id=\"github-fork\"><iframe src=\"http://ghbtns.com/github-btn.html?user=hugoruscitti&repo=pilas&type=fork&count=true\" allowtransparency=\"true\" frameborder=\"0\" scrolling=\"0\" width=\"95\" height=\"20\"></iframe></div>\n          </div>\n\n          <!--\n          <div style=\"margin: 10px;\">Con el respaldo de <a target=\"_blank\" href=\"http://www.conectarigualdad.gob.ar\">Conectar Igualdad</a></div>\n        -->\n\n\n      </div>\n    </div>\n\n  </footer>\n\n</div>\n");
    return buffer;
    
  });

});
define('pilas-website-test/templates/blog', ['exports', 'ember'], function (exports, Ember) {

  'use strict';

  exports['default'] = Ember['default'].Handlebars.template(function anonymous(Handlebars,depth0,helpers,partials,data
  /**/) {
  this.compilerInfo = [4,'>= 1.0.0'];
  helpers = this.merge(helpers, Ember['default'].Handlebars.helpers); data = data || {};
    var buffer = '', stack1, helper, options, self=this, functionType="function", blockHelperMissing=helpers.blockHelperMissing;

  function program1(depth0,data) {
    
    var buffer = '', stack1;
    data.buffer.push("\n        ");
    stack1 = helpers._triageMustache.call(depth0, "n", {hash:{},hashTypes:{},hashContexts:{},contexts:[depth0],types:["ID"],data:data});
    if(stack1 || stack1 === 0) { data.buffer.push(stack1); }
    data.buffer.push("\n      ");
    return buffer;
    }

  function program3(depth0,data) {
    
    var buffer = '';
    return buffer;
    }

    data.buffer.push("<div class=\"page-header center\">\n  <h1>Noticias</h1>\n</div>\n\n<div class=\"bs-component\">\n  <div class='row'>\n\n    <div class=\"col-lg-12\">\n\n      <a href='http://pilas-engine.tumblr.com/rss'>Suscribirse al RSS</a>\n\n      ");
    stack1 = helpers.each.call(depth0, "n", "in", "model", {hash:{},hashTypes:{},hashContexts:{},inverse:self.noop,fn:self.program(1, program1, data),contexts:[depth0,depth0,depth0],types:["ID","ID","ID"],data:data});
    if(stack1 || stack1 === 0) { data.buffer.push(stack1); }
    data.buffer.push("\n\n\n\n      ");
    options={hash:{},hashTypes:{},hashContexts:{},inverse:self.noop,fn:self.program(3, program3, data),contexts:[],types:[],data:data}
    if (helper = helpers['pilas-noticias']) { stack1 = helper.call(depth0, options); }
    else { helper = (depth0 && depth0['pilas-noticias']); stack1 = typeof helper === functionType ? helper.call(depth0, options) : helper; }
    if (!helpers['pilas-noticias']) { stack1 = blockHelperMissing.call(depth0, 'pilas-noticias', {hash:{},hashTypes:{},hashContexts:{},inverse:self.noop,fn:self.program(3, program3, data),contexts:[],types:[],data:data}); }
    if(stack1 || stack1 === 0) { data.buffer.push(stack1); }
    data.buffer.push("\n\n      <p><a href='http://pilas-engine.tumblr.com'>Ver noticias anteriores</a>\n\n    </div>\n  </div>\n</div>\n");
    return buffer;
    
  });

});
define('pilas-website-test/templates/components/img-wrap', ['exports', 'ember'], function (exports, Ember) {

  'use strict';

  exports['default'] = Ember['default'].Handlebars.template(function anonymous(Handlebars,depth0,helpers,partials,data
  /**/) {
  this.compilerInfo = [4,'>= 1.0.0'];
  helpers = this.merge(helpers, Ember['default'].Handlebars.helpers); data = data || {};
    var buffer = '';


    return buffer;
    
  });

});
define('pilas-website-test/templates/components/liquid-bind-c', ['exports', 'ember'], function (exports, Ember) {

  'use strict';

  exports['default'] = Ember['default'].Handlebars.template(function anonymous(Handlebars,depth0,helpers,partials,data
  /**/) {
  this.compilerInfo = [4,'>= 1.0.0'];
  helpers = this.merge(helpers, Ember['default'].Handlebars.helpers); data = data || {};
    var buffer = '', stack1, helper, options, self=this, helperMissing=helpers.helperMissing;

  function program1(depth0,data) {
    
    var buffer = '', stack1;
    data.buffer.push("\n  ");
    stack1 = helpers._triageMustache.call(depth0, "boundValue", {hash:{},hashTypes:{},hashContexts:{},contexts:[depth0],types:["ID"],data:data});
    if(stack1 || stack1 === 0) { data.buffer.push(stack1); }
    data.buffer.push("\n");
    return buffer;
    }

    stack1 = (helper = helpers['liquid-with'] || (depth0 && depth0['liquid-with']),options={hash:{
      'class': ("innerClass"),
      'use': ("use"),
      'containerless': ("containerless")
    },hashTypes:{'class': "ID",'use': "ID",'containerless': "ID"},hashContexts:{'class': depth0,'use': depth0,'containerless': depth0},inverse:self.noop,fn:self.program(1, program1, data),contexts:[depth0,depth0,depth0],types:["ID","ID","ID"],data:data},helper ? helper.call(depth0, "value", "as", "boundValue", options) : helperMissing.call(depth0, "liquid-with", "value", "as", "boundValue", options));
    if(stack1 || stack1 === 0) { data.buffer.push(stack1); }
    data.buffer.push("\n");
    return buffer;
    
  });

});
define('pilas-website-test/templates/components/liquid-measured', ['exports', 'ember'], function (exports, Ember) {

  'use strict';

  exports['default'] = Ember['default'].Handlebars.template(function anonymous(Handlebars,depth0,helpers,partials,data
  /**/) {
  this.compilerInfo = [4,'>= 1.0.0'];
  helpers = this.merge(helpers, Ember['default'].Handlebars.helpers); data = data || {};
    var stack1;


    stack1 = helpers._triageMustache.call(depth0, "yield", {hash:{},hashTypes:{},hashContexts:{},contexts:[depth0],types:["ID"],data:data});
    if(stack1 || stack1 === 0) { data.buffer.push(stack1); }
    else { data.buffer.push(''); }
    
  });

});
define('pilas-website-test/templates/components/liquid-modal', ['exports', 'ember'], function (exports, Ember) {

  'use strict';

  exports['default'] = Ember['default'].Handlebars.template(function anonymous(Handlebars,depth0,helpers,partials,data
  /**/) {
  this.compilerInfo = [4,'>= 1.0.0'];
  helpers = this.merge(helpers, Ember['default'].Handlebars.helpers); data = data || {};
    var buffer = '', stack1, helper, options, escapeExpression=this.escapeExpression, helperMissing=helpers.helperMissing, self=this;

  function program1(depth0,data) {
    
    var buffer = '', stack1, helper, options;
    data.buffer.push("\n  ");
    stack1 = (helper = helpers['lm-container'] || (depth0 && depth0['lm-container']),options={hash:{
      'action': ("escape")
    },hashTypes:{'action': "STRING"},hashContexts:{'action': depth0},inverse:self.noop,fn:self.program(2, program2, data),contexts:[],types:[],data:data},helper ? helper.call(depth0, options) : helperMissing.call(depth0, "lm-container", options));
    if(stack1 || stack1 === 0) { data.buffer.push(stack1); }
    data.buffer.push("\n");
    return buffer;
    }
  function program2(depth0,data) {
    
    var buffer = '', helper, options;
    data.buffer.push("\n    <div ");
    data.buffer.push(escapeExpression(helpers['bind-attr'].call(depth0, {hash:{
      'class': (":lf-dialog cc.options.dialogClass")
    },hashTypes:{'class': "STRING"},hashContexts:{'class': depth0},contexts:[],types:[],data:data})));
    data.buffer.push(" role=\"dialog\" ");
    data.buffer.push(escapeExpression(helpers['bind-attr'].call(depth0, {hash:{
      'aria-labelledby': ("cc.options.ariaLabelledBy"),
      'aria-label': ("cc.options.ariaLabel")
    },hashTypes:{'aria-labelledby': "STRING",'aria-label': "STRING"},hashContexts:{'aria-labelledby': depth0,'aria-label': depth0},contexts:[],types:[],data:data})));
    data.buffer.push(">\n      ");
    data.buffer.push(escapeExpression(helpers.view.call(depth0, "innerView", {hash:{
      'dismiss': ("dismiss")
    },hashTypes:{'dismiss': "STRING"},hashContexts:{'dismiss': depth0},contexts:[depth0],types:["ID"],data:data})));
    data.buffer.push("\n    </div>\n    ");
    data.buffer.push(escapeExpression((helper = helpers['lf-overlay'] || (depth0 && depth0['lf-overlay']),options={hash:{
      'clickAway': ("outsideClick")
    },hashTypes:{'clickAway': "STRING"},hashContexts:{'clickAway': depth0},contexts:[],types:[],data:data},helper ? helper.call(depth0, options) : helperMissing.call(depth0, "lf-overlay", options))));
    data.buffer.push("\n  ");
    return buffer;
    }

    stack1 = (helper = helpers['liquid-with'] || (depth0 && depth0['liquid-with']),options={hash:{
      'class': ("lm-with"),
      'containerless': (true)
    },hashTypes:{'class': "STRING",'containerless': "BOOLEAN"},hashContexts:{'class': depth0,'containerless': depth0},inverse:self.noop,fn:self.program(1, program1, data),contexts:[depth0,depth0,depth0],types:["ID","ID","ID"],data:data},helper ? helper.call(depth0, "currentContext", "as", "cc", options) : helperMissing.call(depth0, "liquid-with", "currentContext", "as", "cc", options));
    if(stack1 || stack1 === 0) { data.buffer.push(stack1); }
    data.buffer.push("\n");
    return buffer;
    
  });

});
define('pilas-website-test/templates/components/liquid-spacer', ['exports', 'ember'], function (exports, Ember) {

  'use strict';

  exports['default'] = Ember['default'].Handlebars.template(function anonymous(Handlebars,depth0,helpers,partials,data
  /**/) {
  this.compilerInfo = [4,'>= 1.0.0'];
  helpers = this.merge(helpers, Ember['default'].Handlebars.helpers); data = data || {};
    var stack1, helper, options, self=this, helperMissing=helpers.helperMissing;

  function program1(depth0,data) {
    
    var buffer = '', stack1;
    data.buffer.push("\n  ");
    stack1 = helpers._triageMustache.call(depth0, "yield", {hash:{},hashTypes:{},hashContexts:{},contexts:[depth0],types:["ID"],data:data});
    if(stack1 || stack1 === 0) { data.buffer.push(stack1); }
    data.buffer.push("\n");
    return buffer;
    }

    stack1 = (helper = helpers['liquid-measured'] || (depth0 && depth0['liquid-measured']),options={hash:{
      'width': ("width"),
      'height': ("height")
    },hashTypes:{'width': "ID",'height': "ID"},hashContexts:{'width': depth0,'height': depth0},inverse:self.noop,fn:self.program(1, program1, data),contexts:[],types:[],data:data},helper ? helper.call(depth0, options) : helperMissing.call(depth0, "liquid-measured", options));
    if(stack1 || stack1 === 0) { data.buffer.push(stack1); }
    else { data.buffer.push(''); }
    
  });

});
define('pilas-website-test/templates/components/photo-coleccion', ['exports', 'ember'], function (exports, Ember) {

  'use strict';

  exports['default'] = Ember['default'].Handlebars.template(function anonymous(Handlebars,depth0,helpers,partials,data
  /**/) {
  this.compilerInfo = [4,'>= 1.0.0'];
  helpers = this.merge(helpers, Ember['default'].Handlebars.helpers); data = data || {};
    var buffer = '', stack1, escapeExpression=this.escapeExpression, helperMissing=helpers.helperMissing, self=this;

  function program1(depth0,data) {
    
    var buffer = '', helper, options;
    data.buffer.push("\n     <div class='contenedor-img'>\n      <a ");
    data.buffer.push(escapeExpression(helpers.action.call(depth0, "visualizar", "m.media$group.media$content.0.url", {hash:{},hashTypes:{},hashContexts:{},contexts:[depth0,depth0],types:["STRING","ID"],data:data})));
    data.buffer.push(">\n        ");
    data.buffer.push(escapeExpression((helper = helpers['img-wrap'] || (depth0 && depth0['img-wrap']),options={hash:{
      'class': ("imagen"),
      'src': ("m.media$group.media$thumbnail.0.url"),
      'alt': ("Landscape")
    },hashTypes:{'class': "STRING",'src': "ID",'alt': "STRING"},hashContexts:{'class': depth0,'src': depth0,'alt': depth0},contexts:[],types:[],data:data},helper ? helper.call(depth0, options) : helperMissing.call(depth0, "img-wrap", options))));
    data.buffer.push("\n      </a>\n     </div>\n    ");
    return buffer;
    }

    data.buffer.push("\n\n<div class='row'>\n  <h3>");
    stack1 = helpers._triageMustache.call(depth0, "titulo", {hash:{},hashTypes:{},hashContexts:{},contexts:[depth0],types:["ID"],data:data});
    if(stack1 || stack1 === 0) { data.buffer.push(stack1); }
    data.buffer.push("</h3>\n\n  <div class=\"col-lg-12\">\n    ");
    stack1 = helpers.each.call(depth0, "m", "in", "model", {hash:{},hashTypes:{},hashContexts:{},inverse:self.noop,fn:self.program(1, program1, data),contexts:[depth0,depth0,depth0],types:["ID","ID","ID"],data:data});
    if(stack1 || stack1 === 0) { data.buffer.push(stack1); }
    data.buffer.push("\n  </div>\n</div>\n");
    return buffer;
    
  });

});
define('pilas-website-test/templates/components/pilas-colaborador', ['exports', 'ember'], function (exports, Ember) {

  'use strict';

  exports['default'] = Ember['default'].Handlebars.template(function anonymous(Handlebars,depth0,helpers,partials,data
  /**/) {
  this.compilerInfo = [4,'>= 1.0.0'];
  helpers = this.merge(helpers, Ember['default'].Handlebars.helpers); data = data || {};
    var buffer = '', stack1, helper, options, escapeExpression=this.escapeExpression, helperMissing=helpers.helperMissing;


    data.buffer.push("<a ");
    data.buffer.push(escapeExpression(helpers['bind-attr'].call(depth0, {hash:{
      'href': ("href_github")
    },hashTypes:{'href': "ID"},hashContexts:{'href': depth0},contexts:[],types:[],data:data})));
    data.buffer.push(" target=\"_blank\">");
    data.buffer.push(escapeExpression((helper = helpers['gravatar-image'] || (depth0 && depth0['gravatar-image']),options={hash:{
      'email': ("email"),
      'size': (76),
      'default': ("identicon"),
      'class': ("img-circle")
    },hashTypes:{'email': "ID",'size': "INTEGER",'default': "STRING",'class': "STRING"},hashContexts:{'email': depth0,'size': depth0,'default': depth0,'class': depth0},contexts:[],types:[],data:data},helper ? helper.call(depth0, options) : helperMissing.call(depth0, "gravatar-image", options))));
    data.buffer.push("</a>\n\n<div>\n  <a ");
    data.buffer.push(escapeExpression(helpers['bind-attr'].call(depth0, {hash:{
      'href': ("href_github")
    },hashTypes:{'href': "ID"},hashContexts:{'href': depth0},contexts:[],types:[],data:data})));
    data.buffer.push(" target=\"_blank\">");
    stack1 = helpers._triageMustache.call(depth0, "nombre", {hash:{},hashTypes:{},hashContexts:{},contexts:[depth0],types:["ID"],data:data});
    if(stack1 || stack1 === 0) { data.buffer.push(stack1); }
    data.buffer.push("</a>\n</div>\n");
    return buffer;
    
  });

});
define('pilas-website-test/templates/components/pilas-miembro', ['exports', 'ember'], function (exports, Ember) {

  'use strict';

  exports['default'] = Ember['default'].Handlebars.template(function anonymous(Handlebars,depth0,helpers,partials,data
  /**/) {
  this.compilerInfo = [4,'>= 1.0.0'];
  helpers = this.merge(helpers, Ember['default'].Handlebars.helpers); data = data || {};
    var buffer = '', stack1, helper, options, escapeExpression=this.escapeExpression, helperMissing=helpers.helperMissing;


    data.buffer.push("<a ");
    data.buffer.push(escapeExpression(helpers['bind-attr'].call(depth0, {hash:{
      'href': ("href_github")
    },hashTypes:{'href': "ID"},hashContexts:{'href': depth0},contexts:[],types:[],data:data})));
    data.buffer.push(" target=\"_blank\">");
    data.buffer.push(escapeExpression((helper = helpers['gravatar-image'] || (depth0 && depth0['gravatar-image']),options={hash:{
      'email': ("email"),
      'size': (100),
      'default': ("identicon"),
      'class': ("img-circle")
    },hashTypes:{'email': "ID",'size': "INTEGER",'default': "STRING",'class': "STRING"},hashContexts:{'email': depth0,'size': depth0,'default': depth0,'class': depth0},contexts:[],types:[],data:data},helper ? helper.call(depth0, options) : helperMissing.call(depth0, "gravatar-image", options))));
    data.buffer.push("</a>\n\n<div class='miembro-nombre'><a ");
    data.buffer.push(escapeExpression(helpers['bind-attr'].call(depth0, {hash:{
      'href': ("href_github")
    },hashTypes:{'href': "ID"},hashContexts:{'href': depth0},contexts:[],types:[],data:data})));
    data.buffer.push(" target=\"_blank\">");
    stack1 = helpers._triageMustache.call(depth0, "nombre", {hash:{},hashTypes:{},hashContexts:{},contexts:[depth0],types:["ID"],data:data});
    if(stack1 || stack1 === 0) { data.buffer.push(stack1); }
    data.buffer.push("</a></div>\n\n<p class='miembro-descripcion'>");
    stack1 = helpers._triageMustache.call(depth0, "yield", {hash:{},hashTypes:{},hashContexts:{},contexts:[depth0],types:["ID"],data:data});
    if(stack1 || stack1 === 0) { data.buffer.push(stack1); }
    data.buffer.push("</p>\n");
    return buffer;
    
  });

});
define('pilas-website-test/templates/components/pilas-noticias', ['exports', 'ember'], function (exports, Ember) {

  'use strict';

  exports['default'] = Ember['default'].Handlebars.template(function anonymous(Handlebars,depth0,helpers,partials,data
  /**/) {
  this.compilerInfo = [4,'>= 1.0.0'];
  helpers = this.merge(helpers, Ember['default'].Handlebars.helpers); data = data || {};
    var buffer = '', stack1, helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, self=this;

  function program1(depth0,data) {
    
    var buffer = '', stack1, helper, options;
    data.buffer.push("\n\n<div class='pilas-noticia'>\n\n  <div class='meta'>\n    <i class='glyphicon glyphicon-time'></i>\n    ");
    data.buffer.push(escapeExpression((helper = helpers.ago || (depth0 && depth0.ago),options={hash:{},hashTypes:{},hashContexts:{},contexts:[depth0,depth0],types:["ID","STRING"],data:data},helper ? helper.call(depth0, "noticia.date-gmt", "es", options) : helperMissing.call(depth0, "ago", "noticia.date-gmt", "es", options))));
    data.buffer.push("\n  </div>\n\n  <div class='contenido'>\n    <h3>");
    stack1 = helpers._triageMustache.call(depth0, "noticia.regular-title", {hash:{},hashTypes:{},hashContexts:{},contexts:[depth0],types:["ID"],data:data});
    if(stack1 || stack1 === 0) { data.buffer.push(stack1); }
    data.buffer.push("</h3>\n\n    <p>\n      ");
    data.buffer.push(escapeExpression((helper = helpers['safe-html'] || (depth0 && depth0['safe-html']),options={hash:{
      'value': ("noticia.regular-body")
    },hashTypes:{'value': "ID"},hashContexts:{'value': depth0},contexts:[],types:[],data:data},helper ? helper.call(depth0, options) : helperMissing.call(depth0, "safe-html", options))));
    data.buffer.push("\n    </p>\n\n    <p>\n      <a ");
    data.buffer.push(escapeExpression(helpers['bind-attr'].call(depth0, {hash:{
      'href': ("noticia.url-with-slug")
    },hashTypes:{'href': "STRING"},hashContexts:{'href': depth0},contexts:[],types:[],data:data})));
    data.buffer.push(" target=\"_blank\">ver mas ...</a>\n    </p>\n  </div>\n\n</div>\n\n");
    return buffer;
    }

    stack1 = helpers.each.call(depth0, "noticia", "in", "logs", {hash:{},hashTypes:{},hashContexts:{},inverse:self.noop,fn:self.program(1, program1, data),contexts:[depth0,depth0,depth0],types:["ID","ID","ID"],data:data});
    if(stack1 || stack1 === 0) { data.buffer.push(stack1); }
    data.buffer.push("\n");
    return buffer;
    
  });

});
define('pilas-website-test/templates/components/safe-html', ['exports', 'ember'], function (exports, Ember) {

  'use strict';

  exports['default'] = Ember['default'].Handlebars.template(function anonymous(Handlebars,depth0,helpers,partials,data
  /**/) {
  this.compilerInfo = [4,'>= 1.0.0'];
  helpers = this.merge(helpers, Ember['default'].Handlebars.helpers); data = data || {};
    var buffer = '', stack1;


    stack1 = helpers._triageMustache.call(depth0, "contenido", {hash:{},hashTypes:{},hashContexts:{},contexts:[depth0],types:["ID"],data:data});
    if(stack1 || stack1 === 0) { data.buffer.push(stack1); }
    data.buffer.push("\n\n");
    stack1 = helpers._triageMustache.call(depth0, "yield", {hash:{},hashTypes:{},hashContexts:{},contexts:[depth0],types:["ID"],data:data});
    if(stack1 || stack1 === 0) { data.buffer.push(stack1); }
    data.buffer.push("\n");
    return buffer;
    
  });

});
define('pilas-website-test/templates/descargas', ['exports', 'ember'], function (exports, Ember) {

  'use strict';

  exports['default'] = Ember['default'].Handlebars.template(function anonymous(Handlebars,depth0,helpers,partials,data
  /**/) {
  this.compilerInfo = [4,'>= 1.0.0'];
  helpers = this.merge(helpers, Ember['default'].Handlebars.helpers); data = data || {};
    var buffer = '', stack1, helper, options, helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;


    data.buffer.push("<div class=\"page-header center\">\n  <h1>Descargas</h1>\n</div>\n\n<div class=\"bs-component\">\n\n  <div class='row'>\n    <p>Elegí tu sabor favorito de pilas-engine. La versión\n      mas reciente para descargar es la <code>");
    stack1 = helpers._triageMustache.call(depth0, "version", {hash:{},hashTypes:{},hashContexts:{},contexts:[depth0],types:["ID"],data:data});
    if(stack1 || stack1 === 0) { data.buffer.push(stack1); }
    data.buffer.push("</code> (publicada\n      en ");
    stack1 = helpers._triageMustache.call(depth0, "fecha", {hash:{},hashTypes:{},hashContexts:{},contexts:[depth0],types:["ID"],data:data});
    if(stack1 || stack1 === 0) { data.buffer.push(stack1); }
    data.buffer.push(" ):</p>\n  </div>\n\n  <div class='row'>\n    <ul id='descargas'>\n      <li><a class='btn btn-info btn-lg' ");
    data.buffer.push(escapeExpression((helper = helpers.bindAttr || (depth0 && depth0.bindAttr),options={hash:{
      'href': ("link_windows")
    },hashTypes:{'href': "STRING"},hashContexts:{'href': depth0},contexts:[],types:[],data:data},helper ? helper.call(depth0, options) : helperMissing.call(depth0, "bindAttr", options))));
    data.buffer.push("><div class='sprite windows'></div> Windows</a></li>\n      <li><a class='btn btn-warning btn-lg' ");
    data.buffer.push(escapeExpression((helper = helpers.bindAttr || (depth0 && depth0.bindAttr),options={hash:{
      'href': ("link_mac")
    },hashTypes:{'href': "STRING"},hashContexts:{'href': depth0},contexts:[],types:[],data:data},helper ? helper.call(depth0, options) : helperMissing.call(depth0, "bindAttr", options))));
    data.buffer.push("><div class='sprite platform_mac'></div> Mac OS X</a></li>\n      <li><a class='btn btn-success btn-lg' ");
    data.buffer.push(escapeExpression((helper = helpers.bindAttr || (depth0 && depth0.bindAttr),options={hash:{
      'href': ("link_deb")
    },hashTypes:{'href': "STRING"},hashContexts:{'href': depth0},contexts:[],types:[],data:data},helper ? helper.call(depth0, options) : helperMissing.call(depth0, "bindAttr", options))));
    data.buffer.push("><div class='sprite huayra'></div> Huayra Linux</a></li>\n      <li><a class='btn btn-danger btn-lg' ");
    data.buffer.push(escapeExpression((helper = helpers.bindAttr || (depth0 && depth0.bindAttr),options={hash:{
      'href': ("link_deb")
    },hashTypes:{'href': "STRING"},hashContexts:{'href': depth0},contexts:[],types:[],data:data},helper ? helper.call(depth0, options) : helperMissing.call(depth0, "bindAttr", options))));
    data.buffer.push("><div class='sprite ico-ubuntu'></div> Ubuntu Linux</a></li>\n    </ul>\n  </div>\n\n  <div class='row'>\n\n    <div class=\"col-lg-3\"></div>\n\n    <div class=\"col-lg-6\">\n    <p>También podés encontrar las versiones anteriores de pilas en <a href='https://www.dropbox.com/sh/pv0vu4id6dqqojh/AACy-7fqG1CpJlHXbqgOR2q6a?dl=0' target=\"_blank\">este link</a>.</p>\n    </div>\n\n    <div class=\"col-lg-3\"></div>\n  </div>\n</div>\n");
    return buffer;
    
  });

});
define('pilas-website-test/templates/docs', ['exports', 'ember'], function (exports, Ember) {

  'use strict';

  exports['default'] = Ember['default'].Handlebars.template(function anonymous(Handlebars,depth0,helpers,partials,data
  /**/) {
  this.compilerInfo = [4,'>= 1.0.0'];
  helpers = this.merge(helpers, Ember['default'].Handlebars.helpers); data = data || {};
    


    data.buffer.push("<div class=\"page-header center\">\n  <h1>Documentación</h1>\n</div>\n\n<div class='row'>\n  <p>\n    Un buen punto de inicio para comenzar a utilizar pilas es explorar el manual completo en español.\n    Este manual recorre toda la funcionalidad de pilas, y explica con ejemplos cómo utilizar cada parte del motor.\n  </p>\n</div>\n\n\n<div class=\"panel-botones-documentacion center\">\n  <p>\n  <strong>Versión actual de pilas (recomendados)</strong>\n  </p>\n\n  <a target=\"_blank\" class='btn btn-success btn-lg' href='http://manual.pilas-engine.com.ar'>Ver el manual</a>\n  <a target=\"_blank\" class='btn btn-warning btn-lg' href='http://pilas-engine.com.ar/apuntes/pilas-engine-general-brochure.pdf'>Mini-tutorial (blanco)</a>\n  <a target=\"_blank\" class='btn btn-warning btn-lg' href='http://pilas-engine.com.ar/apuntes/pilas-engine-general-brochure-huayra.pdf'>Mini-tutorial (huayra)</a>\n</div>\n\n<div class=\"panel-botones-documentacion center\">\n  <p>\n  <strong>Versión 0.83.0 (en desuso)</strong>\n  </p>\n  <a target=\"_blank\" class='btn btn-info btn-lg' href='https://pilas.readthedocs.org/en/latest/'>Ver el manual</a>\n  <a target=\"_blank\" class='btn btn-warning btn-lg' href='./docs/api-0.83.0/index.html'>Ver API</a>\n</div>\n\n<div class=\"row\">\n\n  <h2>Tutoriales</h2>\n\n<p>\n  También puedes seguir nuestros tutoriales paso a paso para aprender\n  sobre pilas haciendo juegos:\n</p>\n\n  <table class='tutoriales'>\n\n  <tr>\n      <td>\n        <img style='border: 1px solid #A8A8A8;' src='./images/tutoriales/disparar_a_monos-61805426fc179d587d4e26962720a517.png'>\n      </td>\n\n      <td>\n       <h4>Disparar a Monos</h4>\n\n          <p>Una introducción a pilas-engine utilizando un juego de disparos.\n          <ul style='margin-left: 1em; list-style-type: disc'>\n         <li><a href=\"tutoriales/disparar_a_monos.pdf\">Abrir PDF</a></li>\n       </ul>\n      </td>\n  </tr>\n\n\n\n  <tr>\n<td>\n <img style='border: 1px solid #A8A8A8;' src='./images/tutoriales/asteroides-cfd9e3e6401e7096e9c5eede26079394.png'>\n</td>\n\n<td>\n\n <h4>Asteroides</h4>\n\n <p>Una guia para construir un juego como el original asteroides.\n <ul style='margin-left: 1em; list-style-type: disc'>\n  <li><a href=\"tutoriales/Asteroides.pdf\">Abrir PDF</a></li>\n  <li><a href=\"tutoriales/recursos_asteroides.zip\">Descargar recursos adicionales</a></li>\n </ul>\n</td>\n\n</tr>\n\n\n<tr>\n\n<td>\n <img style='border: 1px solid #A8A8A8;' src='./images/tutoriales/mario-ff08294aab1e74c3443e3a12b5afb79c.png'>\n</td>\n<td>\n <h4>Sprites y Física</h4>\n\n <p>Muestra los primeros pasos con actores, el motor de física y una comparativa entre pilas y pygame.\n <ul style='margin-left: 1em; list-style-type: disc'>\n  <li><a href=\"tutoriales/mario.pdf\">Abrir PDF</a></li>\n  <li><a href=\"tutoriales/recursos_mario.zip\">Descargar recursos adicionales</a></li>\n </ul>\n</td>\n\n</tr>\n\n\n<tr>\n\n<td>\n <img style='border: 1px solid #A8A8A8;' src='./images/tutoriales/grillas-41ce2e4df1ce99fe7da6cad6aff55849.png'>\n</td>\n<td>\n <h4>Grillas y Animación</h4>\n\n <p>Guia paso a paso para construir animaciones mediante grillas de gráficos.\n <ul style='margin-left: 1em; list-style-type: disc'>\n  <li><a href=\"tutoriales/grillas.pdf\">Abrir PDF</a></li>\n  <li><a href=\"tutoriales/recursos_grillas.zip\">Descargar recursos adicionales</a></li>\n </ul>\n</td>\n\n</tr>\n\n<tr>\n\n<td>\n <img style='border: 1px solid #A8A8A8;' src='./images/tutoriales/scrolling-0c649c2812a42f3113044f6fa5f01582.png'>\n</td>\n\n<td>\n <h4>Scrolling</h4>\n\n <p>Muestra cómo generar el efecto desplazamiento de múltiples capas.\n <ul style='margin-left: 1em; list-style-type: disc'>\n  <li><a href=\"tutoriales/scrolling.pdf\">Abrir PDF</a></li>\n  <li><a href=\"tutoriales/recursos_scrolling.zip\">Descargar recursos adicionales</a></li>\n </ul>\n</td>\n\n</tr>\n\n\n</table>\n\n\n\n\n\n\n</div>\n");
    
  });

});
define('pilas-website-test/templates/foro', ['exports', 'ember'], function (exports, Ember) {

  'use strict';

  exports['default'] = Ember['default'].Handlebars.template(function anonymous(Handlebars,depth0,helpers,partials,data
  /**/) {
  this.compilerInfo = [4,'>= 1.0.0'];
  helpers = this.merge(helpers, Ember['default'].Handlebars.helpers); data = data || {};
    


    data.buffer.push("<div class=\"page-header center\">\n  <h1>Foro de la comunidad</h1>\n</div>\n\n<div class=\"bs-component\">\n  <div class='row'>\n\n    <div style='text-align: center'>\n     <a class=\"aligncenter\" href='http://foro.pilas-engine.com.ar/' target=\"_blank\"><img class=\"aligncenter\" src=\"./images/completamente-castellano-7e8ab71f8cbaedfd2e3e10d60fa1541c.png\" alt=\"Completamente es castellano\" /></a>\n     <p>\n     <a class=\"aligncenter\" href='http://foro.pilas-engine.com.ar/' target=\"_blank\">Abrir el foro en una ventana nueva</a>\n    </div>\n\n\n  </div>\n</div>\n");
    
  });

});
define('pilas-website-test/templates/galeria', ['exports', 'ember'], function (exports, Ember) {

  'use strict';

  exports['default'] = Ember['default'].Handlebars.template(function anonymous(Handlebars,depth0,helpers,partials,data
  /**/) {
  this.compilerInfo = [4,'>= 1.0.0'];
  helpers = this.merge(helpers, Ember['default'].Handlebars.helpers); data = data || {};
    var buffer = '', stack1, helper, options, self=this, helperMissing=helpers.helperMissing;

  function program1(depth0,data) {
    
    var buffer = '';
    return buffer;
    }

    data.buffer.push("\n<div class=\"page-header center\">\n  <h1>Galería de imágenes</h1>\n</div>\n\n<div class=\"row\">\n\n  ");
    stack1 = (helper = helpers['photo-coleccion'] || (depth0 && depth0['photo-coleccion']),options={hash:{
      'titulo': ("Ejemplos"),
      'model': ("photosEjemplos")
    },hashTypes:{'titulo': "STRING",'model': "ID"},hashContexts:{'titulo': depth0,'model': depth0},inverse:self.noop,fn:self.program(1, program1, data),contexts:[],types:[],data:data},helper ? helper.call(depth0, options) : helperMissing.call(depth0, "photo-coleccion", options));
    if(stack1 || stack1 === 0) { data.buffer.push(stack1); }
    data.buffer.push("\n  ");
    stack1 = (helper = helpers['photo-coleccion'] || (depth0 && depth0['photo-coleccion']),options={hash:{
      'titulo': ("Equipos"),
      'model': ("photosEquipos")
    },hashTypes:{'titulo': "STRING",'model': "ID"},hashContexts:{'titulo': depth0,'model': depth0},inverse:self.noop,fn:self.program(1, program1, data),contexts:[],types:[],data:data},helper ? helper.call(depth0, options) : helperMissing.call(depth0, "photo-coleccion", options));
    if(stack1 || stack1 === 0) { data.buffer.push(stack1); }
    data.buffer.push("\n  ");
    stack1 = (helper = helpers['photo-coleccion'] || (depth0 && depth0['photo-coleccion']),options={hash:{
      'titulo': ("Eventos y talleres"),
      'model': ("photosEventos")
    },hashTypes:{'titulo': "STRING",'model': "ID"},hashContexts:{'titulo': depth0,'model': depth0},inverse:self.noop,fn:self.program(1, program1, data),contexts:[],types:[],data:data},helper ? helper.call(depth0, options) : helperMissing.call(depth0, "photo-coleccion", options));
    if(stack1 || stack1 === 0) { data.buffer.push(stack1); }
    data.buffer.push("\n  ");
    stack1 = (helper = helpers['photo-coleccion'] || (depth0 && depth0['photo-coleccion']),options={hash:{
      'titulo': ("Sistemas"),
      'model': ("photosSistemas")
    },hashTypes:{'titulo': "STRING",'model': "ID"},hashContexts:{'titulo': depth0,'model': depth0},inverse:self.noop,fn:self.program(1, program1, data),contexts:[],types:[],data:data},helper ? helper.call(depth0, options) : helperMissing.call(depth0, "photo-coleccion", options));
    if(stack1 || stack1 === 0) { data.buffer.push(stack1); }
    data.buffer.push("\n\n</div>\n");
    return buffer;
    
  });

});
define('pilas-website-test/templates/index', ['exports', 'ember'], function (exports, Ember) {

  'use strict';

  exports['default'] = Ember['default'].Handlebars.template(function anonymous(Handlebars,depth0,helpers,partials,data
  /**/) {
  this.compilerInfo = [4,'>= 1.0.0'];
  helpers = this.merge(helpers, Ember['default'].Handlebars.helpers); data = data || {};
    var buffer = '', stack1, helper, options, self=this, helperMissing=helpers.helperMissing;

  function program1(depth0,data) {
    
    
    data.buffer.push("descargar");
    }

  function program3(depth0,data) {
    
    
    data.buffer.push("ver los videos");
    }

    data.buffer.push("<div class=\"jumbotron center\">\n\n  <h1>¡Crea tus propios videojuegos!</h1>\n  <p>pilas-engine te permite crear tus propios videojuegos de manera didáctica y divertida</p>\n\n  <div class=\"panel-botones-descargas center\">\n    ");
    stack1 = (helper = helpers['link-to'] || (depth0 && depth0['link-to']),options={hash:{
      'class': ("btn btn-success btn-lg")
    },hashTypes:{'class': "STRING"},hashContexts:{'class': depth0},inverse:self.noop,fn:self.program(1, program1, data),contexts:[depth0],types:["STRING"],data:data},helper ? helper.call(depth0, "descargas", options) : helperMissing.call(depth0, "link-to", "descargas", options));
    if(stack1 || stack1 === 0) { data.buffer.push(stack1); }
    data.buffer.push("\n    ");
    stack1 = (helper = helpers['link-to'] || (depth0 && depth0['link-to']),options={hash:{
      'class': ("btn btn-warning btn-lg")
    },hashTypes:{'class': "STRING"},hashContexts:{'class': depth0},inverse:self.noop,fn:self.program(3, program3, data),contexts:[depth0],types:["STRING"],data:data},helper ? helper.call(depth0, "videos", options) : helperMissing.call(depth0, "link-to", "videos", options));
    if(stack1 || stack1 === 0) { data.buffer.push(stack1); }
    data.buffer.push("\n  </div>\n\n</div>\n\n<div class='features'>\n\n\n\n  <div class='row'>\n    <h3>Características</h3>\n\n    <div class='col-md-4'>\n\n      <div class='aligncenter sprite primeros-pasos'></div>\n      <p>Está dirigido a personas que comienzan a programar videojuegos y quieren lograr resultados sorprendentes y divertidos en poco tiempo.</p>\n    </div>\n\n    <div class=\"col-md-4\">\n      <div class='aligncenter sprite multiplataforma'></div>\n      <p>Es multiplataforma: funciona en Windows, Gnu/Linux y Mac OS X. Cualquier persona puede utilizar el motor :).</p>\n    </div>\n\n    <div class=\"col-md-4\">\n      <div class='aligncenter sprite completamente-castellano'></div>\n      <p>Completamente en castellano: la documentación, los tutoriales y el código programado están en tu idioma.</p>\n    </div>\n  </div>\n\n\n  <div class='row'>\n    <div class='col-md-4'>\n      <div class='aligncenter sprite interactiva'></div>\n      <p>Es interactiva: puedes programar mientras observas resultados. </p>\n    </div>\n    <div class='col-md-4'>\n      <div class='aligncenter sprite actores-incluidos'></div>\n      <p>Incluye actores y ejemplos prediseñados: para que puedas comenzar a crear muchas variedades de juegos rápidamente.</p>\n    </div>\n    <div class='col-md-4'>\n      <div class='aligncenter sprite libre-gratuita'></div>\n      <p>Libre y gratuita: Es software libre bajo la LGPL, así que puedes copiar, modificar y distribuir el motor libremente.</p>\n    </div>\n  </div>\n");
    return buffer;
    
  });

});
define('pilas-website-test/templates/liquid-with-self', ['exports', 'ember'], function (exports, Ember) {

  'use strict';

  exports['default'] = Ember['default'].Handlebars.template(function anonymous(Handlebars,depth0,helpers,partials,data
  /**/) {
  this.compilerInfo = [4,'>= 1.0.0'];
  helpers = this.merge(helpers, Ember['default'].Handlebars.helpers); data = data || {};
    var buffer = '', stack1;


    stack1 = helpers._triageMustache.call(depth0, "value", {hash:{},hashTypes:{},hashContexts:{},contexts:[depth0],types:["ID"],data:data});
    if(stack1 || stack1 === 0) { data.buffer.push(stack1); }
    data.buffer.push("\n");
    return buffer;
    
  });

});
define('pilas-website-test/templates/liquid-with', ['exports', 'ember'], function (exports, Ember) {

  'use strict';

  exports['default'] = Ember['default'].Handlebars.template(function anonymous(Handlebars,depth0,helpers,partials,data
  /**/) {
  this.compilerInfo = [4,'>= 1.0.0'];
  helpers = this.merge(helpers, Ember['default'].Handlebars.helpers); data = data || {};
    var buffer = '', stack1;


    stack1 = helpers._triageMustache.call(depth0, "with-apply", {hash:{},hashTypes:{},hashContexts:{},contexts:[depth0],types:["ID"],data:data});
    if(stack1 || stack1 === 0) { data.buffer.push(stack1); }
    data.buffer.push("\n\n\n");
    return buffer;
    
  });

});
define('pilas-website-test/templates/tmp-videos', ['exports', 'ember'], function (exports, Ember) {

  'use strict';

  exports['default'] = Ember['default'].Handlebars.template(function anonymous(Handlebars,depth0,helpers,partials,data
  /**/) {
  this.compilerInfo = [4,'>= 1.0.0'];
  helpers = this.merge(helpers, Ember['default'].Handlebars.helpers); data = data || {};
    var buffer = '', stack1, self=this, helperMissing=helpers.helperMissing;

  function program1(depth0,data) {
    
    var buffer = '', stack1, helper, options;
    data.buffer.push("\n            ");
    stack1 = (helper = helpers['link-to'] || (depth0 && depth0['link-to']),options={hash:{
      'class': ("list-group-item")
    },hashTypes:{'class': "STRING"},hashContexts:{'class': depth0},inverse:self.noop,fn:self.program(2, program2, data),contexts:[depth0,depth0],types:["STRING","ID"],data:data},helper ? helper.call(depth0, "videos.play", "v", options) : helperMissing.call(depth0, "link-to", "videos.play", "v", options));
    if(stack1 || stack1 === 0) { data.buffer.push(stack1); }
    data.buffer.push("\n          ");
    return buffer;
    }
  function program2(depth0,data) {
    
    var buffer = '', stack1;
    data.buffer.push(" ");
    stack1 = helpers._triageMustache.call(depth0, "v.titulo", {hash:{},hashTypes:{},hashContexts:{},contexts:[depth0],types:["ID"],data:data});
    if(stack1 || stack1 === 0) { data.buffer.push(stack1); }
    data.buffer.push(" ");
    return buffer;
    }

    data.buffer.push("<div class=\"page-header center\">\n  <h1>Videos</h1>\n</div>\n\n<div class=\"bs-component\">\n  <div class='row'>\n    <div class=\"col-lg-4\">\n      <div class=\"bs-component\">\n\n        <div class=\"list-group\">\n          ");
    stack1 = helpers.each.call(depth0, "v", "in", "model", {hash:{},hashTypes:{},hashContexts:{},inverse:self.noop,fn:self.program(1, program1, data),contexts:[depth0,depth0,depth0],types:["ID","ID","ID"],data:data});
    if(stack1 || stack1 === 0) { data.buffer.push(stack1); }
    data.buffer.push("\n        </div>\n\n      </div>\n    </div>\n\n    <div class=\"col-lg-7\">\n      ");
    stack1 = helpers._triageMustache.call(depth0, "outlet", {hash:{},hashTypes:{},hashContexts:{},contexts:[depth0],types:["ID"],data:data});
    if(stack1 || stack1 === 0) { data.buffer.push(stack1); }
    data.buffer.push("\n    </div>\n\n  </div>\n\n  <div class='row'>\n\n\n\n    <div class=\"col-lg-12\">\n      <h2>Videos</h2>\n\nEn esta sección vas a encontar video-tutoriales y charlas sobre pilas.\n\n\n<div class=\"post\" id=\"presentacion-de-pilas-en-pyconES-2013\">\n <h3>Pilas en PyCon España 2013 (Madrid)</h3>\n\n <iframe width=\"420\" height=\"315\" src=\"http://www.youtube.com/embed/bjlWZjTZLmQ\" frameborder=\"0\" allowfullscreen></iframe>\n\n <p>\n    Puedes ver mas información en el <a href='http://2013.es.pycon.org/'>sitio del evento</a>.\n</div>\n\n\n<div class=\"post\" id=\"presentacion-de-pilas-en-pycon-2013\">\n <h3>Pilas en PyCon Argentina 2013 (Rosario)</h3>\n\n <iframe width=\"420\" height=\"315\" src=\"//www.youtube.com/embed/tXA2BgzrvzA\" frameborder=\"0\" allowfullscreen></iframe>\n\n <p>\n    Puedes ver mas información en el <a href='http://ar.pycon.org/2013'>sitio del evento</a>.\n</div>\n\n\n\n\n<div class=\"post\" id=\"presentacion-de-pilas-en-betabeers-bs-as-marzo-2012\">\n <h3>Pilas en PyCon Argentina 2012</h3>\n <iframe width=\"640\" height=\"480\" src=\"http://www.youtube.com/embed/sQhxjLoJlZs\" frameborder=\"0\" allowfullscreen></iframe>\n\n <p>\n    Puedes ver mas información en el <a href='http://ar.pycon.org/2012/default/index'>sitio del evento</a>.\n</div>\n\n<div class=\"post\" id=\"presentacion-de-pilas-en-betabeers-bs-as-marzo-2012\">\n <h3>Presentación de pilas en betabeers Bs. As. Marzo 2012</h3>\n <iframe width=\"420\" height=\"315\" src=\"http://www.youtube.com/embed/-Z6Qi_B9QSA\" frameborder=\"0\" allowfullscreen=\"1\"></iframe>\n</div>\n\n\n\n<div class=\"post\" id=\"haciendo-videojuegos-con-pilas-pyday-2011\">\n <h3>Haciendo videojuegos con pilas (pyday 2011)</h3>\n <iframe src=\"http://player.vimeo.com/video/23735704?title=0&amp;byline=0&amp;portrait=0\" width=\"400\" height=\"300\" frameborder=\"0\"></iframe>\n <p class=\"small\"><a href=\"http://vimeo.com/23735704\">Haciendo videojuegos con pilas</a> from <a href=\"http://vimeo.com/user5340810\">Hugo Ruscitti</a> on <a href=\"http://vimeo.com\">Vimeo</a>.</p>\n <p class=\"small\">También puedes ver las diapositivas de esta charla <a class=\"reference external\" href=\"/doc/pilas_pyday_04_2011.pdf\">aquí</a>.</p>\n</div>\n\n<div class=\"post\" id=\"presentacion-conurbania-2010\">\n <h3>Presentación Conurbania 2010</h3>\n <iframe src=\"http://player.vimeo.com/video/17273297\" width=\"400\" height=\"300\" frameborder=\"0\"></iframe>\n <p class=\"small\">También puedes ver este video desde <a class=\"reference external\" href=\"http://vimeo.com/17273297\">vimeo</a>.</p>\n</div>\n\n\n\n    </div>\n  </div>\n</div>\n");
    return buffer;
    
  });

});
define('pilas-website-test/templates/videos', ['exports', 'ember'], function (exports, Ember) {

  'use strict';

  exports['default'] = Ember['default'].Handlebars.template(function anonymous(Handlebars,depth0,helpers,partials,data
  /**/) {
  this.compilerInfo = [4,'>= 1.0.0'];
  helpers = this.merge(helpers, Ember['default'].Handlebars.helpers); data = data || {};
    var buffer = '', stack1, self=this, helperMissing=helpers.helperMissing;

  function program1(depth0,data) {
    
    var buffer = '', stack1, helper, options;
    data.buffer.push("\n            ");
    stack1 = (helper = helpers['link-to'] || (depth0 && depth0['link-to']),options={hash:{
      'class': ("list-group-item")
    },hashTypes:{'class': "STRING"},hashContexts:{'class': depth0},inverse:self.noop,fn:self.program(2, program2, data),contexts:[depth0,depth0],types:["STRING","ID"],data:data},helper ? helper.call(depth0, "videos.play", "v", options) : helperMissing.call(depth0, "link-to", "videos.play", "v", options));
    if(stack1 || stack1 === 0) { data.buffer.push(stack1); }
    data.buffer.push("\n          ");
    return buffer;
    }
  function program2(depth0,data) {
    
    var buffer = '', stack1;
    data.buffer.push(" ");
    stack1 = helpers._triageMustache.call(depth0, "v.titulo", {hash:{},hashTypes:{},hashContexts:{},contexts:[depth0],types:["ID"],data:data});
    if(stack1 || stack1 === 0) { data.buffer.push(stack1); }
    data.buffer.push(" ");
    return buffer;
    }

    data.buffer.push("<div class=\"page-header center\">\n  <h1>Videos</h1>\n</div>\n\n<div class=\"bs-component\">\n  <div class='row'>\n\n    <div class=\"col-lg-5 col-md-5 col-sm-5\">\n      \n      <h3>&nbsp;</h3>\n\n      <div class=\"bs-component\">\n        <div class=\"list-group\">\n          ");
    stack1 = helpers.each.call(depth0, "v", "in", "model", {hash:{},hashTypes:{},hashContexts:{},inverse:self.noop,fn:self.program(1, program1, data),contexts:[depth0,depth0,depth0],types:["ID","ID","ID"],data:data});
    if(stack1 || stack1 === 0) { data.buffer.push(stack1); }
    data.buffer.push("\n        </div>\n\n      </div>\n    </div>\n\n    <div class=\"col-lg-7 col-md-7 col-sm-7\">\n      ");
    stack1 = helpers._triageMustache.call(depth0, "outlet", {hash:{},hashTypes:{},hashContexts:{},contexts:[depth0],types:["ID"],data:data});
    if(stack1 || stack1 === 0) { data.buffer.push(stack1); }
    data.buffer.push("\n    </div>\n\n  </div>\n</div>\n");
    return buffer;
    
  });

});
define('pilas-website-test/templates/videos/index', ['exports', 'ember'], function (exports, Ember) {

  'use strict';

  exports['default'] = Ember['default'].Handlebars.template(function anonymous(Handlebars,depth0,helpers,partials,data
  /**/) {
  this.compilerInfo = [4,'>= 1.0.0'];
  helpers = this.merge(helpers, Ember['default'].Handlebars.helpers); data = data || {};
    


    data.buffer.push("<p>Seleccioná un video de la izquierda.</p>\n");
    
  });

});
define('pilas-website-test/templates/videos/play', ['exports', 'ember'], function (exports, Ember) {

  'use strict';

  exports['default'] = Ember['default'].Handlebars.template(function anonymous(Handlebars,depth0,helpers,partials,data
  /**/) {
  this.compilerInfo = [4,'>= 1.0.0'];
  helpers = this.merge(helpers, Ember['default'].Handlebars.helpers); data = data || {};
    var buffer = '', stack1, helper, options, helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;


    data.buffer.push("<h3>");
    stack1 = helpers._triageMustache.call(depth0, "model.titulo", {hash:{},hashTypes:{},hashContexts:{},contexts:[depth0],types:["ID"],data:data});
    if(stack1 || stack1 === 0) { data.buffer.push(stack1); }
    data.buffer.push("</h3>\n\n<iframe width=\"420\" height=\"315\" ");
    data.buffer.push(escapeExpression((helper = helpers.bindAttr || (depth0 && depth0.bindAttr),options={hash:{
      'src': ("model.url")
    },hashTypes:{'src': "STRING"},hashContexts:{'src': depth0},contexts:[],types:[],data:data},helper ? helper.call(depth0, options) : helperMissing.call(depth0, "bindAttr", options))));
    data.buffer.push(" frameborder=\"0\" allowfullscreen></iframe>\n");
    return buffer;
    
  });

});
define('pilas-website-test/transitions', ['exports'], function (exports) {

  'use strict';

  exports['default'] = function () {
    this.transition(this.use("fade"));
  };

});
define('pilas-website-test/transitions/cross-fade', ['exports', 'liquid-fire'], function (exports, liquid_fire) {

  'use strict';

  // BEGIN-SNIPPET cross-fade-definition
  function crossFade(oldView, insertNewView, opts) {
    liquid_fire.stop(oldView);
    return insertNewView().then(function (newView) {
      return liquid_fire.Promise.all([liquid_fire.animate(oldView, { opacity: 0 }, opts), liquid_fire.animate(newView, { opacity: [1, 0] }, opts)]);
    });
  }
  exports['default'] = crossFade;
  // END-SNIPPET

});
define('pilas-website-test/transitions/fade', ['exports', 'liquid-fire'], function (exports, liquid_fire) {

  'use strict';

  // BEGIN-SNIPPET fade-definition
  function fade(oldView, insertNewView, opts) {
    var firstStep,
        outOpts = opts;

    if (liquid_fire.isAnimating(oldView, "fade-out")) {
      // if the old view is already fading out, let it finish.
      firstStep = liquid_fire.finish(oldView, "fade-out");
    } else {
      if (liquid_fire.isAnimating(oldView, "fade-in")) {
        // if the old view is partially faded in, scale its fade-out
        // duration appropriately.
        outOpts = { duration: liquid_fire.timeSpent(oldView, "fade-in") };
      }
      liquid_fire.stop(oldView);
      firstStep = liquid_fire.animate(oldView, { opacity: 0 }, outOpts, "fade-out");
    }

    return firstStep.then(insertNewView).then(function (newView) {
      return liquid_fire.animate(newView, { opacity: [1, 0] }, opts, "fade-in");
    });
  }
  exports['default'] = fade;
  // END-SNIPPET

});
define('pilas-website-test/transitions/flex-grow', ['exports', 'liquid-fire'], function (exports, liquid_fire) {

  'use strict';

  function flexGrow(oldView, insertNewView, opts) {
    liquid_fire.stop(oldView);
    return insertNewView().then(function (newView) {
      return liquid_fire.Promise.all([liquid_fire.animate(oldView, { "flex-grow": 0 }, opts), liquid_fire.animate(newView, { "flex-grow": [1, 0] }, opts)]);
    });
  }
  exports['default'] = flexGrow;

});
define('pilas-website-test/transitions/modal-popup', ['exports', 'ember', 'liquid-fire'], function (exports, Ember, liquid_fire) {

  'use strict';

  var Velocity = Ember['default'].$.Velocity;

  function hideModal(oldView) {
    var box, obscure;
    if (!oldView || !(box = oldView.$(".lm-container > div")) || !(box = box[0]) || !(obscure = oldView.$(".lf-overlay")) || !(obscure = obscure[0])) {
      return liquid_fire.Promise.resolve();
    }

    return liquid_fire.Promise.all([Velocity.animate(obscure, { opacity: [0, 0.5] }, { duration: 250 }), Velocity.animate(box, { scale: [0, 1] }, { duration: 250 })]);
  }

  function revealModal(insertNewView) {
    return insertNewView().then(function (newView) {
      var box, obscure;
      if (!newView || !(box = newView.$(".lm-container > div")[0]) || !(obscure = newView.$(".lf-overlay")[0])) {
        return;
      }

      // we're not going to animate the whole view, rather we're going
      // to animate two pieces of it separately. So we move the view
      // properties down onto the individual elements, so that the
      // animate function can reveal them at precisely the right time.
      Ember['default'].$(box).css({
        display: "none"
      });

      Ember['default'].$(obscure).css({
        display: "none"
      });
      newView.$().css({
        display: "",
        visibility: ""
      });

      return liquid_fire.Promise.all([Velocity.animate(obscure, { opacity: [0.5, 0] }, { duration: 250, display: "" }), Velocity.animate(box, { scale: [1, 0] }, { duration: 250, display: "" })]);
    });
  }

  function modalPopup(oldView, insertNewView) {
    return hideModal(oldView).then(function () {
      return revealModal(insertNewView);
    });
  }
  exports['default'] = modalPopup;

});
define('pilas-website-test/transitions/move-over', ['exports', 'liquid-fire'], function (exports, liquid_fire) {

  'use strict';

  function moveOver(oldView, insertNewView, dimension, direction, opts) {
    var oldParams = {},
        newParams = {},
        firstStep,
        property,
        measure;

    if (dimension.toLowerCase() === "x") {
      property = "translateX";
      measure = "width";
    } else {
      property = "translateY";
      measure = "height";
    }

    if (liquid_fire.isAnimating(oldView, "moving-in")) {
      firstStep = liquid_fire.finish(oldView, "moving-in");
    } else {
      liquid_fire.stop(oldView);
      firstStep = liquid_fire.Promise.resolve();
    }


    return firstStep.then(insertNewView).then(function (newView) {
      if (newView && newView.$() && oldView && oldView.$()) {
        var sizes = [parseInt(newView.$().css(measure), 10), parseInt(oldView.$().css(measure), 10)];
        var bigger = Math.max.apply(null, sizes);
        oldParams[property] = bigger * direction + "px";
        newParams[property] = ["0px", -1 * bigger * direction + "px"];
      } else {
        oldParams[property] = 100 * direction + "%";
        newParams[property] = ["0%", -100 * direction + "%"];
      }

      return liquid_fire.Promise.all([liquid_fire.animate(oldView, oldParams, opts), liquid_fire.animate(newView, newParams, opts, "moving-in")]);
    });
  }
  exports['default'] = moveOver;

});
define('pilas-website-test/transitions/scroll-then', ['exports', 'ember'], function (exports, Ember) {

  'use strict';

  exports['default'] = function () {
    Ember['default'].assert("You must provide a transition name as the first argument to scrollThen. Example: this.use('scrollThen', 'toLeft')", "string" === typeof arguments[2]);

    var el = document.getElementsByTagName("html"),
        transitionArgs = Array.prototype.slice.call(arguments, 0, 2),
        nextTransition = this.lookup(arguments[2]),
        self = this,
        options = arguments[3] || {};

    Ember['default'].assert("The second argument to scrollThen is passed to Velocity's scroll function and must be an object", "object" === typeof options);

    // set scroll options via: this.use('scrollThen', 'ToLeft', {easing: 'spring'})
    options = Ember['default'].merge({ duration: 500, offset: 0 }, options);

    // additional args can be passed through after the scroll options object
    // like so: this.use('scrollThen', 'moveOver', {duration: 100}, 'x', -1);
    transitionArgs.push.apply(transitionArgs, Array.prototype.slice.call(arguments, 4));

    return window.$.Velocity(el, "scroll", options).then(function () {
      nextTransition.apply(self, transitionArgs);
    });
  };

});
define('pilas-website-test/transitions/to-down', ['exports', 'liquid-fire'], function (exports, liquid_fire) {

	'use strict';

	exports['default'] = liquid_fire.curryTransition("move-over", "y", 1);

});
define('pilas-website-test/transitions/to-left', ['exports', 'liquid-fire'], function (exports, liquid_fire) {

	'use strict';

	exports['default'] = liquid_fire.curryTransition("move-over", "x", -1);

});
define('pilas-website-test/transitions/to-right', ['exports', 'liquid-fire'], function (exports, liquid_fire) {

	'use strict';

	exports['default'] = liquid_fire.curryTransition("move-over", "x", 1);

});
define('pilas-website-test/transitions/to-up', ['exports', 'liquid-fire'], function (exports, liquid_fire) {

	'use strict';

	exports['default'] = liquid_fire.curryTransition("move-over", "y", -1);

});
define('pilas-website-test/utils/img-manager/dom-helpers', ['exports'], function (exports) {

  'use strict';

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
      } else if (node.attachEvent) {
        node.attachEvent("on" + event, handler);
      } else {
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
      } else if (node.detachEvent) {
        node.detachEvent("on" + event, handler);
      } else {
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
      var wrapper = function () {
        helpers.detach(node, event, wrapper);
        handler.apply(this, arguments);
      };

      return helpers.attach(node, event, wrapper);
    }
  };

  exports['default'] = helpers;

});
define('pilas-website-test/utils/img-manager/img-clone-holder', ['exports', 'ember', 'pilas-website-test/utils/img-manager/img-node-factory'], function (exports, Ember, imgFactory) {

  'use strict';

  // this class is in purpose not Ember, for faster processing
  var EnumerableUtils = Ember['default'].EnumerableUtils;
  var assert = Ember['default'].assert;
  var forEach = EnumerableUtils.forEach;
  var filter = EnumerableUtils.filter;
  var hasOwn = ({}).hasOwnProperty;
  var run = Ember['default'].run;
  var next = run.next;

  var TRANSPARENT_PIXEL = "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7";

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
    } else {
      return function (node, name, value) {
        node[name] = value;
      };
    }
  })(typeof document.createElement("img").setAttribute === "function");


  /**
   * @class ImgCloneHolder
   * @constructor
   */
  function ImgCloneHolder() {
    this.handler = Ember['default'].K;
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
      var i,
          len,
          attrNames = this.attributeNames;
      if (this.node) {
        for (i = 0, len = attrNames.length; i < len; i++) {
          this.node.removeAttribute(attrNames[i]);
        }
        this.attributeNames = [];
        imgFactory['default'].free(this.src, this.node);
        this.node = this.src = null;
        this.handler = Ember['default'].K;
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
      assert("[img-manager] Trying to switch the source of a clone holder with no node.", this.node);
      if (!newSrc) {
        newSrc = TRANSPARENT_PIXEL;
      }
      if (this.src !== newSrc) {
        oldImg = this.node;
        this.node = newImg = imgFactory['default'].forSrc(newSrc, original);
        hasChanged = false;
        attrNames = [];
        forEach(this.attributeNames, function (name) {
          var attr = oldImg.getAttributeNode(name);
          if (attr) {
            attr = oldImg.removeAttributeNode(attr);
            newImg.setAttributeNode(attr);
            attrNames.push(name);
          } else {
            hasChanged = true;
          }
        });
        if (hasChanged) {
          this.attributeNames = attrNames;
        }
        imgFactory['default'].free(this.src, oldImg);
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
      assert("[img-manager] Clone already used for src `" + this.src + "`.", !this.src);
      this.src = src || TRANSPARENT_PIXEL;
      this.node = imgFactory['default'].forSrc(this.src, original);
      this.handler = handler || Ember['default'].K;
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
      if (name === "src") {
        this.switchToSrc(value);
      }
      if (value == null) {
        if (index !== -1) {
          attrNames.splice(index, 1);
          this.node.removeAttribute(name);
        }
      } else {
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
        } else {
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
          if (name !== "src" && value != null) {
            attrNames.push(name);
            setAttr(node, name, value);
          }
        }
      }
    };
  })(ImgCloneHolder.prototype);

  exports['default'] = ImgCloneHolder;

  exports.TRANSPARENT_PIXEL = TRANSPARENT_PIXEL;

});
define('pilas-website-test/utils/img-manager/img-node-factory', ['exports', 'ember', 'pilas-website-test/utils/img-manager/simple-map'], function (exports, Ember, SimpleMap) {

  'use strict';

  var assert = Ember['default'].assert;


  exports['default'] = {
    /**
     * Our nodes collection
     * @property index
     * @type {SimpleMap.<{src: string, node: HTMLDivElement.<HTMLImageElement>, original: HTMLImageElement}>}
     */
    index: new SimpleMap['default'](),

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
        this.container = document.createElement("div");
      }
      idx = this.index.get(src);
      if (!idx) {
        if (!createIfNotExists) {
          return;
        }
        idx = Object.create(null);
        idx.src = src;
        idx.node = document.createElement("div");
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
      assert("[img-manager] Can't get a clone with no `src`.", src);
      idx = this.indexFor(src, true);
      if (idx && (img = idx.node.lastChild)) {
        idx.node.removeChild(img);
        return img;
      }
      if (original) {
        img = original.cloneNode(true);
      } else {
        if (!idx.original) {
          idx.original = document.createElement("img");
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
      assert("[img-manager] Can't free a clone with no `src`.", src);
      assert("[img-manager] Can't free a clone with undefined node for src `" + src + "`.", img);
      this.indexFor(src, true).node.appendChild(img);
    }
  };

});
define('pilas-website-test/utils/img-manager/img-rule', ['exports', 'ember'], function (exports, Ember) {

  'use strict';

  var slice = [].slice;
  var run = Ember['default'].run;
  var next = run.next;
  var debounce = run.debounce;
  var computed = Ember['default'].computed;
  var readOnly = computed.readOnly;


  function starMatcher() {
    return true;
  }
  function noneMatcher() {
    return false;
  }

  function callQueueItem(item) {
    var target = item[0],
        method = item[1],
        args = item[2];
    if (!target || !target.isDestroyed && !target.isDestroying) {
      try {
        if (typeof method === "string") {
          method = target[method];
        }
        return method.apply(target, args);
      } catch (e) {
        Ember['default'].warn("[img-manager] Error invoking load queue item: " + e);
      }
    }
  }

  function anyDefined() {
    var props = Array.prototype.slice.call(arguments);
    return computed.apply(Ember['default'], props.concat([function () {
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
  exports['default'] = Ember['default'].Object.extend({
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
    batchSize: computed("config.batchSize", "manager.defaultBatchSize", function () {
      var batchSize = this.get("config.batchSize");
      if (batchSize === undefined) {
        batchSize = this.get("manager.defaultBatchSize");
      }
      return batchSize;
    }).readOnly(),

    /**
     * Match used to filter on `src`
     * @property match
     * @type {string|RegExp|Function}
     */
    match: readOnly("config.match"),

    /**
     * How many milliseconds to wait before loading next batch
     * @property delay
     * @type {number}
     */
    delay: anyDefined("config.delay", "manager.defaultDelay"),

    /**
     * Should we lazy load the image?
     * @property lazyLoad
     * @type {number}
     */
    lazyLoad: anyDefined("config.lazyLoad", "manager.defaultLazyLoad"),

    /**
     * The maximum number of time to try to load an image
     * @property maxTries
     * @type {number}
     */
    maxTries: anyDefined("config.maxTries", "manager.defaultMaxTries"),

    /**
     * The src to use when loading the image
     * @property loadingSrc
     * @type {string}
     */
    loadingSrc: anyDefined("config.loadingSrc", "manager.defaultLoadingSrc"),

    /**
     * The src to use when the image failed loading
     * @property errorSrc
     * @type {string}
     */
    errorSrc: anyDefined("config.errorSrc", "manager.defaultErrorSrc"),

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
          next(this, "processLoadQueue");
        }
        return value;
      } else {
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
      this.incrementProperty("loadQueuePausedCount");
    },

    /**
     * Continue the load queue processing
     *
     * @method continueLoadQueue
     */
    continueLoadQueue: function () {
      this.incrementProperty("loadQueuePausedCount", -1);
    },


    /**
     * Matcher used to find out if given src matches the rule
     * @property matcher
     * @type {Function}
     */
    matcher: computed("match", function () {
      var match = this.get("match");
      if (match === undefined || match === "*") {
        return starMatcher;
      }
      switch (typeof match) {
        case "string":
          return function (src) {
            return src.indexOf(match) !== -1;
          };
        case "function":
          return match;
        default:
          if (match instanceof RegExp) {
            return function (src) {
              return match.test(src);
            };
          } else {
            Ember['default'].warn("[img-manager] Invalid rule `match`: " + match);
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
      return this.get("matcher")(src);
    },

    /**
     * Schedule the given function for load
     *
     * @method scheduleForLoad
     * @param {Object} [target]
     * @param {Function|string} method
     * @param {*} [...args]
     */
    scheduleForLoad: function (target, method /*, args*/) {
      var args;
      if (arguments.length < 2) {
        method = target;
        target = null;
        args = [];
      } else {
        args = slice.call(arguments, 2);
      }
      this.get("_loadQueue").pushObject([target, method, args]);
      this.processLoadQueue();
    },

    /**
     * Process our loading queue
     *
     * @method processLoadQueue
     */
    processLoadQueue: function () {
      var opt = this.getProperties("_loadQueue", "delay", "loadQueuePausedCount");
      if (!opt._loadQueue.length || opt.loadQueuePausedCount > 0) {
        return;
      }
      this._timer = debounce(this, "_processLoadQueue", opt.delay || 1);
    },

    /**
     * Our load queue
     * @property _loadQueue
     * @type {Array.<Function>}
     * @private
     */
    _loadQueue: computed(function () {
      return Ember['default'].A([]);
    }),

    /**
     * Our load queue processor
     *
     * @method _processLoadQueue
     * @private
     */
    _processLoadQueue: function () {
      var batchSize = this.get("batchSize"),
          queue = this.get("_loadQueue"),
          items;
      if (this.get("loadQueuePausedCount") === 0) {
        items = queue.splice(0, batchSize || queue.length);
        for (var i = 0; i < items.length; i++) {
          callQueueItem(items[i]);
        }
      }
      next(this, "processLoadQueue");
    }
  });

});
define('pilas-website-test/utils/img-manager/img-source', ['exports', 'ember', 'pilas-website-test/utils/img-manager/dom-helpers', 'pilas-website-test/utils/img-manager/img-clone-holder'], function (exports, Ember, helpers, ImgCloneHolder) {

  'use strict';

  var assert = Ember['default'].assert;
  var observer = Ember['default'].observer;
  var computed = Ember['default'].computed;
  var oneWay = computed.oneWay;
  var or = computed.or;
  var on = Ember['default'].on;
  var bind = Ember['default'].run.bind;
  var next = Ember['default'].run.next;


  var uuid = 0;
  function appendDummyQP(url) {
    if (typeof url === "string") {
      url = url.split("#");
      if (url[0].indexOf("?") === -1) {
        url[0] += "?";
      } else {
        url[0] += "&";
      }
      url[0] += "__dummy_eim__=" + ++uuid;
      url = url.join("#");
    }
    return url;
  }

  /**
   * @module img-manager
   * @class ImgSource
   * @extends Ember.Object
   * @uses Ember.Evented
   */
  exports['default'] = Ember['default'].Object.extend(Ember['default'].Evented, {
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
      var opt = this.getProperties("manager", "src");
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
    isReady: or("isError", "isSuccess"),

    /**
     * Whether we are loaded successfully or not
     * @property isSuccess
     * @type {boolean}
     */
    isSuccess: computed("isLoading", "isError", function () {
      return !this.get("isLoading") && !this.get("isError");
    }),

    /**
     * Our source node
     * @property node
     * @type {HTMLImageElement}
     */
    node: computed(function () {
      return document.createElement("img");
    }).readOnly(),

    /**
     * Loads the image
     *
     * @method load
     */
    load: function () {
      var node, opt, src;
      if (!this.get("isInitiated")) {
        this.set("isInitiated", true);
        opt = this.getProperties("src", "_onLoadHandler", "_onErrorHandler", "_onProgressHandler", "maxTries");
        node = this.get("node");
        this.trigger("willLoad");
        if (opt.maxTries) {
          this.set("isLoading", true);
          this.set("progress", undefined);
          helpers['default'].attachOnce(node, "load", opt._onLoadHandler);
          helpers['default'].attachOnce(node, "error", opt._onErrorHandler);
          helpers['default'].attachOnce(node, "progress", opt._onProgressHandler);
          if (this.get("errorCount")) {
            src = appendDummyQP(opt.src);
          } else {
            src = opt.src;
          }
          this.set("modifiedSrc", src);
          node.src = src;
        } else {
          // do not even try to load the image, and directly fires the ready event
          next(this, function () {
            this.setProperties({ isError: true, isLoading: false });
            this.trigger("ready");
          });
        }
      }
    },

    /**
     * Maximum number of load tries
     * @property maxTries
     * @type {number}
     */
    maxTries: oneWay("rule.maxTries"),

    /**
     * Should we lazy load the image?
     * @property lazyLoad
     * @type {number}
     */
    lazyLoad: oneWay("rule.lazyLoad"),

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
    virtualSrc: computed("isLoading", "isError", "rule.errorSrc", "rule.loadingSrc", function () {
      var opt = this.getProperties("isLoading", "isError");
      if (opt.isLoading) {
        return this.get("rule.loadingSrc");
      } else if (opt.isError) {
        return this.get("rule.errorSrc");
      } else {
        // use the node.src since we might have added some parameters for another try
        return this.get("modifiedSrc");
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
      cloneHolder = this.get("freeCloneHolders").pop();
      original = this.get("isSuccess") ? this.get("node") : null;
      if (!cloneHolder) {
        cloneHolder = new ImgCloneHolder['default']();
      }
      this.get("cloneHolders").push(cloneHolder);
      this.incrementProperty("hits");
      cloneHolder.useWith(this.get("virtualSrc"), attributes, original, handler);
      cloneHolder.triggerOnce(this.get("cloneHolderEvent"), "change");
      return cloneHolder;
    },

    /**
     * The event reference when calling triggerOnce
     * @property cloneHolderEvent
     * @type {string}
     */
    cloneHolderEvent: computed("isSuccess", "isError", function () {
      if (this.get("isSuccess")) {
        return "success";
      } else if (this.get("isError")) {
        return "error";
      }
      return "loading";
    }),


    /**
     * Release a clone
     *
     * @method releaseClone
     * @param {ImgCloneHolder} cloneHolder
     */
    releaseClone: function (cloneHolder) {
      var cloneHolders = this.get("cloneHolders"),
          index = cloneHolders.indexOf(cloneHolder);
      assert("[img-manager] Clone holder asked to be released does not belong to this source", index !== -1);
      cloneHolder.release();
      cloneHolders.splice(index, 1);
      this.get("freeCloneHolders").push(cloneHolder);
    },

    /**
     * Schedule a switch of src for all the clones when the ready event is fired
     *
     * @method switchClonesSrc
     */
    switchClonesSrc: on("ready", observer("virtualSrc", function () {
      next(this, "_switchClonesSrc");
    })),

    /**
     * Switch the clones' src
     *
     * @method _switchClonesSrc
     * @private
     */
    _switchClonesSrc: function () {
      var opt, original, i, len, event;
      opt = this.getProperties("cloneHolders", "virtualSrc", "manager", "isSuccess", "node", "isError");
      if (opt.isSuccess) {
        original = opt.node;
      }
      event = this.get("cloneHolderEvent");
      for (i = 0, len = opt.cloneHolders.length; i < len; i++) {
        opt.cloneHolders[i].switchSrc(opt.virtualSrc, original);
        opt.cloneHolders[i].triggerOnce(event, "change");
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
          this.set("progress", event.loaded / event.total * 100);
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
        var opt = this.getProperties("node", "_onErrorHandler", "_onProgressHandler");
        helpers['default'].detach(opt.node, "error", opt._onErrorHandler);
        helpers['default'].detach(opt.node, "progress", opt._onProgressHandler);
        this.setProperties({
          isError: false,
          isLoading: false,
          progress: 100
        });
        this.trigger("didLoad", event);
        this.trigger("ready", event);
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
        var opt = this.getProperties("node", "_onLoadHandler", "_onProgressHandler", "maxTries", "rule");
        helpers['default'].detach(opt.node, "load", opt._onLoadHandler);
        helpers['default'].detach(opt.node, "progress", opt._onProgressHandler);
        if (this.incrementProperty("errorCount") < opt.maxTries) {
          this._continueRuleProcessingQueue();
          this.scheduleLoad(true);
        } else {
          // we're done trying, trigger the `didError` event
          this.setProperties({
            isError: true,
            isLoading: false
          });
          this.trigger("didError", event);
          this.trigger("ready", event);
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
      var initiated = this.get("isInitiated");
      if (initiated && forceReload) {
        this.set("isInitiated", initiated = false);
      }
      if (!initiated) {
        this.get("rule").scheduleForLoad(this, "load");
      }
    },

    /**
     * Pauses the load processing queue
     *
     * @method _pauseRuleProcessingQueue
     * @private
     */
    _pauseRuleProcessingQueue: on("willLoad", function () {
      this.get("rule").pauseLoadQueue();
    }),

    /**
     * Continues the load processing queue
     *
     * @method _continueRuleProcessingQueue
     * @private
     */
    _continueRuleProcessingQueue: on("ready", function () {
      this.get("rule").continueLoadQueue();
    })
  });

});
define('pilas-website-test/utils/img-manager/simple-map', ['exports'], function (exports) {

  'use strict';

  function SimpleMap() {
    this.keys = [];
    this.values = [];
  }

  (function (proto) {
    proto.set = function (key, value) {
      var index = this.indexOfKey(key);
      if (index === -1) {
        this.keys.push(key);
        this.values.push(value);
      } else {
        this.values[index] = value;
      }
    };

    proto.get = function (key) {
      var index = this.indexOfKey(key);
      if (index !== -1) {
        return this.values[index];
      }
    };

    proto.unset = function (key) {
      var index = this.indexOfKey(key);
      if (index !== -1) {
        this.keys.splice(index, 1);
        return this.values.splice(index, 1)[0];
      }
    };

    proto.has = function (key) {
      return this.indexOfKey(key) !== -1;
    };

    proto.indexOfKey = function (key) {
      return this.keys.indexOf(key);
    };

    proto.indexOfValue = function (value) {
      return this.values.indexOf(value);
    };

    proto.size = function () {
      return this.keys.length;
    };
  })(SimpleMap.prototype);

  exports['default'] = SimpleMap;

});
define('pilas-website-test/views/liquid-child', ['exports', 'ember'], function (exports, Ember) {

  'use strict';

  exports['default'] = Ember['default'].ContainerView.extend({
    classNames: ["liquid-child"],
    resolveInsertionPromise: Ember['default'].on("didInsertElement", function () {
      // Children start out hidden and invisible.
      // Measurement will `show` them and Velocity will make them visible.
      // This prevents a flash of pre-animated content.
      this.$().css({ visibility: "hidden" }).hide();
      if (this._resolveInsertion) {
        this._resolveInsertion(this);
      }
    })
  });

});
define('pilas-website-test/views/liquid-if', ['exports', 'pilas-website-test/views/liquid-outlet', 'ember'], function (exports, LiquidOutlet, Ember) {

  'use strict';

  var isHTMLBars = !!Ember['default'].HTMLBars;

  exports['default'] = LiquidOutlet['default'].extend({
    liquidUpdate: Ember['default'].on("init", Ember['default'].observer("showFirst", function () {
      var template = this.get("templates")[this.get("showFirst") ? 0 : 1];
      if (!template || !isHTMLBars && template === Ember['default'].Handlebars.VM.noop) {
        this.set("currentView", null);
        return;
      }
      var view = Ember['default']._MetamorphView.create({
        container: this.container,
        template: template,
        liquidParent: this,
        contextBinding: "liquidParent.context",
        liquidContext: this.get("showFirst"),
        hasLiquidContext: true
      });
      this.set("currentView", view);
    }))

  });

});
define('pilas-website-test/views/liquid-outlet', ['exports', 'ember', 'liquid-fire'], function (exports, Ember, liquid_fire) {

  'use strict';

  var capitalize = Ember['default'].String.capitalize;

  exports['default'] = Ember['default'].ContainerView.extend({
    classNames: ["liquid-container"],
    growDuration: 250,
    growPixelsPerSecond: 200,
    growEasing: "slide",
    enableGrowth: true,

    init: function () {
      // The ContainerView constructor normally sticks our "currentView"
      // directly into _childViews, but we want to leave that up to
      // _currentViewDidChange so we have the opportunity to launch a
      // transition.
      this._super();
      Ember['default'].A(this._childViews).clear();

      if (this.get("containerless")) {
        // This prevents Ember from throwing an assertion when we try to
        // render as a virtual view.
        this.set("innerClassNameBindings", this.get("classNameBindings"));
        this.set("classNameBindings", Ember['default'].A());
      }
    },

    // Deliberately overriding a private method from
    // Ember.ContainerView!
    //
    // We need to stop it from destroying our outgoing child view
    // prematurely.
    _currentViewWillChange: Ember['default'].beforeObserver("currentView", function () {}),

    // Deliberately overriding a private method from
    // Ember.ContainerView!
    _currentViewDidChange: Ember['default'].on("init", Ember['default'].observer("currentView", function () {
      // Normally there is only one child (the view we're
      // replacing). But sometimes there may be two children (because a
      // transition is already in progress). In any case, we tell all of
      // them to start heading for the exits now.

      var oldView = this.get("childViews.lastObject"),
          newView = this.get("currentView"),
          firstTime;

      // For the convenience of the transition rules, we explicitly
      // track our first transition, which happens at initial render.
      firstTime = !this._hasTransitioned;
      this._hasTransitioned = true;

      // Idempotence
      if (!oldView && !newView || oldView && oldView.get("currentView") === newView || this._runningTransition && this._runningTransition.oldView === oldView && this._runningTransition.newContent === newView) {
        return;
      }

      // `transitions` comes from dependency injection, see the
      // liquid-fire app initializer.
      var transition = this.get("transitions").transitionFor(this, oldView, newView, this.get("use"), firstTime);

      if (this._runningTransition) {
        this._runningTransition.interrupt();
      }

      this._runningTransition = transition;
      transition.run()["catch"](function (err) {
        // Force any errors through to the RSVP error handler, because
        // of https://github.com/tildeio/rsvp.js/pull/278.  The fix got
        // into Ember 1.7, so we can drop this once we decide 1.6 is
        // EOL.
        Ember['default'].RSVP.Promise.resolve()._onerror(err);
      });
    })),

    _liquidChildFor: function (content) {
      if (content && !content.get("hasLiquidContext")) {
        content.set("liquidContext", content.get("context"));
      }
      var LiquidChild = this.container.lookupFactory("view:liquid-child");
      var childProperties = {
        currentView: content
      };
      if (this.get("containerless")) {
        childProperties.classNames = this.get("classNames").without("liquid-container");
        childProperties.classNameBindings = this.get("innerClassNameBindings");
      }
      return LiquidChild.create(childProperties);
    },

    _pushNewView: function (newView) {
      if (!newView) {
        return liquid_fire.Promise.resolve();
      }
      var child = this._liquidChildFor(newView),
          promise = new liquid_fire.Promise(function (resolve) {
        child._resolveInsertion = resolve;
      });
      this.pushObject(child);
      return promise;
    },

    cacheSize: function () {
      var elt = this.$();
      if (elt) {
        // Measure original size.
        this._cachedSize = getSize(elt);
      }
    },

    unlockSize: function () {
      var doUnlock = function () {
        var elt = self.$();
        if (elt) {
          elt.css({ width: "", height: "" });
        }
      };

      var self = this;
      if (this._scaling) {
        this._scaling.then(doUnlock);
      } else {
        doUnlock();
      }
    },

    _durationFor: function (before, after) {
      return Math.min(this.get("growDuration"), 1000 * Math.abs(before - after) / this.get("growPixelsPerSecond"));
    },

    _adaptDimension: function (dimension, before, after) {
      if (before[dimension] === after[dimension] || !this.get("enableGrowth")) {
        var elt = this.$();
        if (elt) {
          elt[dimension](after[dimension]);
        }
        return liquid_fire.Promise.resolve();
      } else {
        // Velocity deals in literal width/height, whereas jQuery deals
        // in box-sizing-dependent measurements.
        var target = {};
        target[dimension] = [after["literal" + capitalize(dimension)], before["literal" + capitalize(dimension)]];
        return liquid_fire.animate(this, target, {
          duration: this._durationFor(before[dimension], after[dimension]),
          queue: false,
          easing: this.get("growEasing")
        });
      }
    },

    adaptSize: function () {
      liquid_fire.stop(this);

      var elt = this.$();
      if (!elt) {
        return;
      }

      // Measure new size.
      var newSize = getSize(elt);
      if (typeof this._cachedSize === "undefined") {
        this._cachedSize = newSize;
      }

      // Now that measurements have been taken, lock the size
      // before the invoking the scaling transition.
      elt.width(this._cachedSize.width);
      elt.height(this._cachedSize.height);

      this._scaling = liquid_fire.Promise.all([this._adaptDimension("width", this._cachedSize, newSize), this._adaptDimension("height", this._cachedSize, newSize)]);
    }

  });

  // We're tracking both jQuery's box-sizing dependent measurements and
  // the literal CSS properties, because it's nice to get/set dimensions
  // with jQuery and not worry about boz-sizing *but* Velocity needs the
  // raw values.
  function getSize(elt) {
    return {
      width: elt.width(),
      literalWidth: parseInt(elt.css("width"), 10),
      height: elt.height(),
      literalHeight: parseInt(elt.css("height"), 10)
    };
  }

});
define('pilas-website-test/views/liquid-with', ['exports', 'pilas-website-test/views/liquid-outlet', 'ember'], function (exports, LiquidOutlet, Ember) {

  'use strict';

  exports['default'] = LiquidOutlet['default'].extend({
    liquidUpdate: Ember['default'].on("init", Ember['default'].observer("boundContext", function () {
      var context = this.get("boundContext");
      if (Ember['default'].isEmpty(context)) {
        this.set("currentView", null);
        return;
      }
      var view = Ember['default']._MetamorphView.create({
        container: this.container,
        templateName: "liquid-with",
        boundContext: context,
        liquidWithParent: this,
        liquidContext: context,
        hasLiquidContext: true });
      this.set("currentView", view);
    }))

  });

});
/* jshint ignore:start */

/* jshint ignore:end */

/* jshint ignore:start */

define('pilas-website-test/config/environment', ['ember'], function(Ember) {
  var prefix = 'pilas-website-test';
/* jshint ignore:start */

try {
  var metaName = prefix + '/config/environment';
  var rawConfig = Ember['default'].$('meta[name="' + metaName + '"]').attr('content');
  var config = JSON.parse(unescape(rawConfig));

  return { 'default': config };
}
catch(err) {
  throw new Error('Could not read config from meta tag with name "' + metaName + '".');
}

/* jshint ignore:end */

});

if (runningTests) {
  require("pilas-website-test/tests/test-helper");
} else {
  require("pilas-website-test/app")["default"].create({});
}

/* jshint ignore:end */
