/*
 *
 * IMPORTANTE: basado en el código de 'JS Bin Console' del
 * sitio http://jsconsole.com
 *
 */

//= require "../vendor/prettyprint"
//= require "../vendor/stacktrace"
		
function traducir_mensaje_excepcion(mensaje) {
    var traducciones = [
        {de: "is not defined", a: "no está definido"},
        {de: "Unexpected token ILLEGAL", a: "hay un elemento no reconocido en la sintaxis"},
        {de: "Unexpected end of input", a: "la linea parece incompleta"},
        {de: "Unexpected token", a: "El elemento que sigue no se esperaba:"},
        {de: "Unexpected", a: "Este elemento no se esperaba:"},
        {de: "Invalid left-hand side in assignment", a: "No se esperaba un elemento a la izquierda de la asignación"},
    ];
        
    for (var i=0; i<traducciones.length; i++)
        mensaje = mensaje.replace(traducciones[i].de, traducciones[i].a);
    
    return mensaje;
}
		
		
var modulo_jsconsole = function (window) {

function sortci(a, b) {
  return a.toLowerCase() < b.toLowerCase() ? -1 : 1;
}

function htmlEntities(str) {
    return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

// custom because I want to be able to introspect native browser objects *and* functions
function stringify(o, simple, visited) {
  var json = '', i, vi, type = '', parts = [], names = [], circular = false;
  visited = visited || [];
  
  try {
    type = ({}).toString.call(o);
  } catch (e) { // only happens when typeof is protected (...randomly)
    type = '[object Object]';
  }

  // check for circular references
  for (vi = 0; vi < visited.length; vi++) {
    if (o === visited[vi]) {
      circular = true;
      break;
    }
  }

  if (circular) {
    json = '[circular ' + type.slice(1);
    if (o.outerHTML) {
      json += ":\n" + htmlEntities(o.outerHTML);
    }
  } else if (type == '[object String]') {
    json = '"' + htmlEntities(o.replace(/"/g, '\\"')) + '"';
  } else if (type == '[object Array]') {
    visited.push(o);

    json = '[';
    for (i = 0; i < o.length; i++) {
      parts.push(stringify(o[i], simple, visited));
    }
    json += parts.join(', ') + ']';
  } else if (type == '[object Object]') {
		
		json = "[Instancia de objeto]";
		
		/*
    visited.push(o);

    json = '{';
    for (i in o) {
      names.push(i);
    }
    names.sort(sortci);
    for (i = 0; i < names.length; i++) {
      parts.push( stringify(names[i], undefined, visited) + ': ' + stringify(o[ names[i] ], simple, visited) );
    }
    json += parts.join(', ') + '}';
		*/
		
  } else if (type == '[object Number]') {
    json = o+'';
  } else if (type == '[object Boolean]') {
    json = o ? 'true' : 'false';
  } else if (type == '[object Function]') {
    json = o.toString();
  } else if (o === null) {
    json = 'null';
  } else if (o === undefined) {
    json = 'undefined';
  } else if (simple === undefined) {
    visited.push(o);

    json = type + '{\n';
    for (i in o) {
      names.push(i);
    }
    names.sort(sortci);
    for (i = 0; i < names.length; i++) {
      try {
        parts.push(names[i] + ': ' + stringify(o[names[i]], true, visited)); // safety from max stack
      } catch (e) {
        if (e.name == 'NS_ERROR_NOT_IMPLEMENTED') {
          // do nothing - not sure it's useful to show this error when the variable is protected
          // parts.push(names[i] + ': NS_ERROR_NOT_IMPLEMENTED');
        }
      }
    }
    json += parts.join(',\n') + '\n}';
  } else {
    visited.push(o);
    try {
      json = stringify(o, true, visited)+''; // should look like an object
    } catch (e) {

    }
  }
  return json;
}

function cleanse(s) {
  return (s||'').replace(/[<&]/g, function (m) { return {'&':'&amp;','<':'&lt;'}[m];});
}

function run(cmd) {
  var rawoutput = null,
      className = 'response',
      internalCmd = internalCommand(cmd);
  
      var cursor = $("#cursor");
      //document.getElementById("cursor").innerHTML="";
      cursor.text("");
      var consola = document.getElementById("consola") || document.getElementById('console');

      consola.onclick = function() {
        $("#exec").click();
      }

  if (internalCmd) {
    return ['info', internalCmd];
  } else {
    try {
          //rawoutput = sandboxframe.contentWindow.eval(cmd);
          
          /* Emite un evento alertando lo que el usuario quiere ejecutar */
					var entrada = new Event('entrada');
          entrada.texto = cmd;
          consola.dispatchEvent(entrada);
			
					if (cmd == 'clear' || cmd == 'limpiar') {
						js_console.clear();
						return;
					}
			
          /* EJECUTA LO QUE EL USUARIO ESCRIBE */
					if (window.ejecutar_codigo_python !== undefined)
						rawoutput = ejecutar_codigo_python_sync(cmd);
					else
          	rawoutput = window.eval(cmd);
          
          /* Emite un evento alertando lo que el usuario quiere ejecutar */
  		  	var salida = new Event('salida');
          salida.texto = rawoutput;
          consola.dispatchEvent(salida);
			
    } catch (e) {
      rawoutput = traducir_mensaje_excepcion(e.message);
      className = 'error';
    }
    return [className, cleanse(stringify(rawoutput))];
  }
}

function post(cmd, blind, response /* passed in when echoing from remote console */) {
  cmd = trim(cmd);

  if (blind === undefined) {
    history.push(cmd);
    setHistory(history);
  } 

  echo(cmd);

  // order so it appears at the top
  var el = document.createElement('div'),
      li = document.createElement('li'),
      span = document.createElement('span'),
      parent = output.parentNode;

  if (!internalCommand(cmd)) {

    // Fix console not having iframe
    if (!(sandboxframe && sandboxframe.contentWindow)) {
      // Boo. There must be a nice way to do this.
      
      //sandboxframe = $live.find('iframe')[0];
      
      // Only force it to render if there's no live iframe
      if (!(sandboxframe && sandboxframe.contentWindow)) {
        ////renderLivePreview(false);
        //sandboxframe = $live.find('iframe')[0];
      }
      //jsconsole.setSandbox(sandboxframe);
    }
  }

  // In a setTimeout so that renderLivePreview has time for the iframe to load
  setTimeout(function () {
    response = response || run(cmd);
    
    if (response !== undefined) {
      el.className = 'response';
      span.innerHTML = response[1];

      if (response[0] != 'info') prettyPrint([span]);
      el.appendChild(span);

      li.className = response[0];
      li.innerHTML = '<span class="gutter"></span>';
      li.appendChild(el);

      appendLog(li);

      exec.value = '';
      if (enableCC) {
        try {
          // document.getElementsByTagName('a')[0].focus();
          if (jsbin.panels.focused.id === 'console') {
            cursor.focus();
            document.execCommand('selectAll', false, null);
            document.execCommand('delete', false, null);          
          }
        } catch (e) {}
      }
    }
    pos = history.length;
  }, 0);

}

function log(msg, className) {
  var li = document.createElement('li'),
      div = document.createElement('div');

  div.innerHTML = msg;
  prettyPrint([div]);
  li.className = className || 'log';
  li.innerHTML = '<span class="gutter"></span>';
  li.appendChild(div);

  appendLog(li);
}

function echo(cmd) {
  var li = document.createElement('li');

  li.className = 'echo';
  li.innerHTML = '<span class="gutter"></span><div>' + cleanse(cmd) + '</div>';

  logAfter = null;
	
  appendLog(li, true);
}

window.info = function(cmd) {
  var li = document.createElement('li');

  li.className = 'info';
  li.innerHTML = '<span class="gutter"></span><div>' + cleanse(cmd) + '</div>';

  appendLog(li);
};

function appendLog(el, echo) {
  output.appendChild(el);
  output.parentNode.scrollTop = output.parentNode.scrollHeight + 1000;
  return;

  if (echo) {
    if (!output.firstChild) {
      output.appendChild(el);
    } else {
      output.insertBefore(el, output.firstChild);
    }
  } else {
    if (!output.lastChild) {
      output.appendChild(el);
    } else {
      // console.log(output.lastChild.nextSibling);
      output.insertBefore(el, logAfter ? logAfter : output.lastChild.nextSibling); //  ? output.lastChild.nextSibling : output.firstChild
    }
  }
}

function internalCommand(cmd) {
  var parts = [], c;
  if (cmd.substr(0, 1) == ':') {
    parts = cmd.substr(1).split(' ');
    c = parts.shift();
    return (commands[c] || noop).apply(this, parts);
  }
}

function noop() {
}

function trim(s) {
  return (s||"").replace(/^\s+|\s+$/g,"");
}

var ccCache = {};
var ccPosition = false;

window._console = {
  log: function () {
    var l = arguments.length, i = 0;
    for (; i < l; i++) {
      log(stringify(arguments[i], true));
    }
    window.console.log.apply(window.console, arguments);
  },
  dir: function () {
    var l = arguments.length, i = 0;
    for (; i < l; i++) {
      log(stringify(arguments[i]));
    }
    window.console.dir.apply(window.console, arguments);
  },
  props: function (obj) {
    var props = [], realObj;
    try {
      for (var p in obj) props.push(p);
    } catch (e) {}
    window.console.props.apply(window.console, arguments);
    return props;
  },
  error: function (err) {
    log(err.message, 'error');
    window.console.error.apply(window.console, arguments);
  }
};

function setHistory(history) {
  if (typeof JSON == 'undefined') return;
  
  try {
    // because FF with cookies disabled goes nuts, and because sometimes WebKit goes nuts too...
    sessionStorage.setItem('history', JSON.stringify(history));
  } catch (e) {}
}

function getHistory() {
  var history = [''];
  
  if (typeof JSON == 'undefined') return history;
  
  try {
    // because FF with cookies disabled goes nuts, and because sometimes WebKit goes nuts too...
    history = JSON.parse(sessionStorage.getItem('history') || '[""]');
  } catch (e) {}
  return history;
}

function showHistory() {
  var h = getHistory();
  h.shift();
  return h.join("\n");
}

var exec = document.getElementById('exec'),
    form = exec.form || {},
    output = null,
    sandboxframe = null,
    sandbox = null,
    history = getHistory(),
    codeCompleteTimer = null,
    fakeConsole = 'window.top._console',
    body = document.getElementsByTagName('body')[0],
    logAfter = null,
    lastCmd = null,
    commands = {
      clear: function (on_clear) {
        setTimeout(function () { output.innerHTML = ''; if(on_clear) {on_clear();} }, 10);
        return 'clearing...';
      },
      reset: function () {
        output.innerHTML = '';
        jsconsole.init(output, true);
        return 'Context reset';
      }
    },
    fakeInput = null,
    // I hate that I'm browser sniffing, but there's issues with Firefox and execCommand so code completion won't work
    iOSMobile = navigator.userAgent.indexOf('AppleWebKit') !== -1 && navigator.userAgent.indexOf('Mobile') !== -1,
    // FIXME Remy, seriously, don't sniff the agent like this, it'll bite you in the arse.
    enableCC = navigator.userAgent.indexOf('AppleWebKit') !== -1 && navigator.userAgent.indexOf('Mobile') === -1 || navigator.userAgent.indexOf('OS 5_') !== -1;

if (enableCC) {
  exec.parentNode.innerHTML = '<div autofocus id="exec" autocapitalize="off" spellcheck="false"><span id="cursor" spellcheck="false" autocapitalize="off" autocorrect="off"' + (iOSMobile ? '' : ' contenteditable') + '></span></div>';
  exec = document.getElementById('exec');
  cursor = document.getElementById('cursor');
} else {
  $('#console').addClass('plain');
}

if (enableCC && iOSMobile) {
  fakeInput = document.createElement('input');
  fakeInput.className = 'fakeInput';
  fakeInput.setAttribute('spellcheck', 'false');
  fakeInput.setAttribute('autocorrect', 'off');
  fakeInput.setAttribute('autocapitalize', 'off');
  exec.parentNode.appendChild(fakeInput);
}

// sandbox = sandboxframe.contentDocument || sandboxframe.contentWindow.document;

// tweaks to interface to allow focus
// if (!('autofocus' in document.createElement('input'))) exec.focus();

function whichKey(event) {
  var keys = {38:1, 40:1, Up:38, Down:40, Enter:10, 'U+0009':9, 'U+0008':8, 'U+0190':190, 'Right':39, 
      // these two are ignored
      'U+0028': 57, 'U+0026': 55 }; 
  return keys[event.keyIdentifier] || event.which || event.keyCode;
}

function setCursorTo(str) {
  str = enableCC ? cleanse(str) : str;
  exec.value = str;
  
  if (enableCC) {
    document.execCommand('selectAll', false, null);
    document.execCommand('delete', false, null);
    document.execCommand('insertHTML', false, str);
  } else {
    var rows = str.match(/\n/g);
    exec.setAttribute('rows', rows !== null ? rows.length + 1 : 1);
  }
  cursor.focus();
}


exec.ontouchstart = function () {
  window.scrollTo(0,0);
};

exec.onkeyup = function (event) {
  var which = whichKey(event);

  if (enableCC && which != 9 && which != 16) {
    clearTimeout(codeCompleteTimer);
    codeCompleteTimer = setTimeout(function () {
      codeComplete(event);
    }, 200);
  } 
};

if (enableCC) {
  // disabled for now
  cursor.__onpaste = function (event) {
    setTimeout(function () {
      // this causes the field to lose focus - I'll leave it here for a while, see how we get on.
      // what I need to do is rip out the contenteditable and replace it with something entirely different
      cursor.innerHTML = cursor.innerText;
      // setCursorTo(cursor.innerText);
    }, 10);
  };
}

function findNode(list, node) {
  var pos = 0;
  for (var i = 0; i < list.length; i++) {
    if (list[i] == node) {
      return pos;
    }
    pos += list[i].nodeValue.length;
  }
  return -1;
};

exec.onkeydown = function (event) {
  event = event || window.event;
  var keys = {38:1, 40:1}, 
      wide = body.className == 'large', 
      which = whichKey(event);

  if (typeof which == 'string') which = which.replace(/\/U\+/, '\\u');
  if (keys[which]) {
    if (event.shiftKey) {
      // changeView(event);
    } else if (!wide) { // history cycle
      if (enableCC && window.getSelection) {
        window.selObj = window.getSelection();
        var selRange = selObj.getRangeAt(0);
        
        cursorPos =  findNode(selObj.anchorNode.parentNode.childNodes, selObj.anchorNode) + selObj.anchorOffset;
        var value = exec.value,
            firstnl = value.indexOf('\n'),
            lastnl = value.lastIndexOf('\n');

        if (firstnl !== -1) {
          if (which == 38 && cursorPos > firstnl) {
            return;
          } else if (which == 40 && cursorPos < lastnl) {
            return;
          }
        }
      }
      
      if (which == 38) { // cycle up
        pos--;
        if (pos < 0) pos = 0; //history.length - 1;
      } else if (which == 40) { // down
        pos++;
        if (pos >= history.length) pos = history.length; //0;
      } 
      if (history[pos] != undefined && history[pos] !== '') {
        removeSuggestion();
        setCursorTo(history[pos])
        return false;
      } else if (pos == history.length) {
        removeSuggestion();
        setCursorTo('');
        return false;
      }
    }
  } else if ((which == 13 || which == 10) && event.shiftKey == false) { // enter (what about the other one)
    removeSuggestion();
    if (event.shiftKey == true || event.metaKey || event.ctrlKey || !wide) {
      var command = exec.textContent || exec.value;
      if (command.length) post(command);
      return false;
    }
  } else if ((which == 13 || which == 10) && !enableCC && event.shiftKey == true) {
    // manually expand the textarea when we don't have code completion turned on
    var rows = exec.value.match(/\n/g);
    rows = rows != null ? rows.length + 2 : 2;
    exec.setAttribute('rows', rows);
  } else if (which == 9 && wide) {
    checkTab(event);
  } else if (event.shiftKey && event.metaKey && which == 8) {
    output.innerHTML = '';
  } else if ((which == 39 || which == 35) && ccPosition !== false) { // complete code
    completeCode();
  } else if (event.ctrlKey && which == 76) {
    output.innerHTML = '';
  } else if (enableCC) { // try code completion
    if (ccPosition !== false && which == 9) {
      codeComplete(event); // cycles available completions
      return false;
    } else if (ccPosition !== false && cursor.nextSibling) {
      removeSuggestion();
    }
  }
};

if (enableCC && iOSMobile) {
  fakeInput.onkeydown = function (event) {
    removeSuggestion();
    var which = whichKey(event);
    
    if (which == 13 || which == 10) {
      post(this.value);
      this.value = '';
      cursor.innerHTML = '';
      return false;
    }
  };

  fakeInput.onkeyup = function (event) {
    cursor.innerHTML = cleanse(this.value);
    var which = whichKey(event);
    if (enableCC && which != 9 && which != 16) {
      clearTimeout(codeCompleteTimer);
      codeCompleteTimer = setTimeout(function () {
        codeComplete(event);
      }, 200);
    } 
  };

  var fakeInputFocused = false;

  var dblTapTimer = null,
      taps = 0;

  form.addEventListener('touchstart', function (event) {
    // window.scrollTo(0,0);
    if (ccPosition !== false) {
      event.preventDefault();
      clearTimeout(dblTapTimer);
      taps++;

      if (taps === 2) {
        completeCode();
        fakeInput.value = cursor.textContent;
        removeSuggestion();
        fakeInput.focus();
      } else {
        dblTapTimer = setTimeout(function () {
          taps = 0;
          codeComplete({ which: 9 });
        }, 200);
      }
    }

    return false;
  });
}

function completeCode(focus) {
  var tmp = exec.textContent, l = tmp.length;
  removeSuggestion();
  
  cursor.innerHTML = tmp;
  ccPosition = false;
  
  // daft hack to move the focus elsewhere, then back on to the cursor to
  // move the cursor to the end of the text.
  document.getElementsByTagName('a')[0].focus();
  cursor.focus();
  
  var range, selection;
  if (document.createRange) {//Firefox, Chrome, Opera, Safari, IE 9+
    range = document.createRange();//Create a range (a range is a like the selection but invisible)
    range.selectNodeContents(cursor);//Select the entire contents of the element with the range
    range.collapse(false);//collapse the range to the end point. false means collapse to end rather than the start
    selection = window.getSelection();//get the selection object (allows you to change selection)
    selection.removeAllRanges();//remove any selections already made
    selection.addRange(range);//make the range you have just created the visible selection
  } else if (document.selection) {//IE 8 and lower
    range = document.body.createTextRange();//Create a range (a range is a like the selection but invisible)
    range.moveToElementText(cursor);//Select the entire contents of the element with the range
    range.collapse(false);//collapse the range to the end point. false means collapse to end rather than the start
    range.select();//Select the range (make it the visible selection
  }
}

form.onsubmit = function (event) {
  event = event || window.event;
  event.preventDefault && event.preventDefault();
  removeSuggestion();
  post(exec.textContent || exec.value);
  return false;
};

document.onkeydown = function (event) {
  event = event || window.event;
  var which = event.which || event.keyCode;
  
  if (event.shiftKey && event.metaKey && which == 8) {
    output.innerHTML = '';
    cursor.focus();
  } else if (event.target == output.parentNode && which == 32) { // space
    output.parentNode.scrollTop += 5 + output.parentNode.offsetHeight * (event.shiftKey ? -1 : 1);
  }
  
  // return changeView(event);
};

exec.onclick = function () {
  cursor.focus();
}

function getProps(cmd, filter) {
  var surpress = {}, props = [];
  
  if (!ccCache[cmd]) {
    try {
      // surpress alert boxes because they'll actually do something when we're looking
      // up properties inside of the command we're running
      surpress.alert = sandboxframe.contentWindow.alert;
      sandboxframe.contentWindow.alert = function () {};
      
      // loop through all of the properties available on the command (that's evaled)
      ccCache[cmd] = sandboxframe.contentWindow.eval('console.props(' + cmd + ')').sort();
      
      // return alert back to it's former self
      delete sandboxframe.contentWindow.alert;
    } catch (e) {
      ccCache[cmd] = [];
    }
    
    // if the return value is undefined, then it means there's no props, so we'll 
    // empty the code completion
    if (ccCache[cmd][0] == 'undefined') ccOptions[cmd] = [];    
    ccPosition = 0;
    props = ccCache[cmd];
  } else if (filter) {
    // console.log('>>' + filter, cmd);
    for (var i = 0, p; i < ccCache[cmd].length, p = ccCache[cmd][i]; i++) {
      if (p.indexOf(filter) === 0) {
        if (p != filter) {
          props.push(p.substr(filter.length, p.length));
        }
      }
    }
  } else {
    props = ccCache[cmd];
  }
  
  return props; 
}

function codeComplete(event) {
  var cmd = cursor.textContent.split(/[;\s]+/g).pop(),
      parts = cmd.split('.'),
      which = whichKey(event),
      cc,
      props = [];

  if (cmd) {
    // get the command without the dot to allow us to introspect
    if (cmd.substr(-1) == '.') {
      // get the command without the '.' so we can eval it and lookup the properties
      cmd = cmd.substr(0, cmd.length - 1);
      
      // returns an array of all the properties from the command
      props = getProps(cmd);
    } else {
      props = getProps(parts.slice(0, parts.length - 1).join('.') || 'window', parts[parts.length - 1]);
    }
    if (props.length) {
      if (which == 9) { // tabbing cycles through the code completion
        // however if there's only one selection, it'll auto complete
        if (props.length === 1) {
          ccPosition = false;
        } else {
          if (event.shiftKey) {
            // backwards
            ccPosition = ccPosition == 0 ? props.length - 1 : ccPosition-1;
          } else {
            ccPosition = ccPosition == props.length - 1 ? 0 : ccPosition+1;
          }
        }      
      } else {
        ccPosition = 0;
      }
    
      if (ccPosition === false) {
        completeCode();
      } else {
        // position the code completion next to the cursor
        if (!cursor.nextSibling) {
          cc = document.createElement('span');
          cc.className = 'suggest';
          exec.appendChild(cc);
        } 

        cursor.nextSibling.innerHTML = props[ccPosition];
        exec.value = exec.textContent;
      }

      if (which == 9) return false;
    } else {
      ccPosition = false;
    }
  } else {
    ccPosition = false;
  }
  
  if (ccPosition === false && cursor.nextSibling) {
    removeSuggestion();
  }
  
  exec.value = exec.textContent;
}

function removeSuggestion() {
  if (!enableCC) exec.setAttribute('rows', 1);
  if (enableCC && cursor.nextSibling) cursor.parentNode.removeChild(cursor.nextSibling);
}

var jsconsole = {
  run: post,
  clear: commands.clear,
  reset: function () {
    this.run(':reset');
  },
  focus: function () {
    if (enableCC) {
      cursor.focus();
    } else {
      $(exec).focus();
    }
  },
  echo: echo,
  setSandbox: function (newSandbox) {
    // sandboxframe.parentNode.removeChild(sandboxframe);
    sandboxframe = newSandbox;

    sandbox = sandboxframe.contentDocument || sandboxframe.contentWindow.document;
		
    sandboxframe.contentWindow.eval('(function () { var fakeConsole = ' + fakeConsole + '; if (window.console != undefined) { for (var k in fakeConsole) { console[k] = fakeConsole[k]; } } else { console = fakeConsole; } })();');

    this.sandboxframe = sandboxframe;

    if (sandbox.readyState !== 'complete') {
      this.ready = false;
    } else {
      jsconsole.onload();
    }

    sandbox.onreadystatechange = function () {
      if (sandbox.readyState === 'complete') {
        jsconsole.ready = true;
        jsconsole.onload();
      }
    };

    getProps('window'); // cache 
  },
  _onloadQueue: [],
  onload: function (fn) {
    var i = 0, length = this._onloadQueue.length;
    if (this.ready === false && fn) { // if not ready and callback passed - cache it
      this._onloadQueue.push(fn);
    } else if (this.ready === true && !fn) { // if ready and not callback - flush cache
      for (; i < length; i++) {
        this._onloadQueue[i].call(this);
      }
      this._onloadQueue = [];      
    } else if (fn) { // if callback and ready - run callback
      fn.call(this);
    }
  },
  init: function (outputElement, nohelp) {
    output = outputElement;
  },
  rawMessage: function (data) {
    if (data.type && data.type == 'error') {
      post(data.cmd, true, ['error', data.response]);
    } else if (data.type && data.type == 'info') {
      window.top.info(data.response);
    } else {
      if (data.cmd.indexOf('console.log') === -1) data.response = data.response.substr(1, data.response.length - 2); // fiddle to remove the [] around the repsonse
      echo(data.cmd);
      log(data.response, 'response');
    }
  },
  stringify: stringify
};

return jsconsole;
};
								 
								 
								 
								 
								 
								 
iniciar_jsconsole = function() {
	
	var jsconsole = modulo_jsconsole(this);
	var msgType = '';

	jsconsole.init(document.getElementById('output'));
	jsconsole.queue = [];
	
	return jsconsole;
}
