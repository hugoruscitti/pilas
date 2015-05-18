"use strict";
var esutils = require("esutils");
var merge = Object.assign || require("object-assign");

// getClass :: Object -> String
function getClass(obj) {
  return {}.toString.call(obj).slice(8, -1);
}

// any :: forall a. [a] -> (a -> Boolean) -> Boolean
function any(predicate, xs) {
  for (var i = 0, l = xs.length; i < l; ++i) {
    if (predicate(xs[i])) return true;
  }
  return false;
}

// concatMap :: forall a b. -> (a -> [b]) -> [a] -> [b]
function concatMap(fn, xs) {
  var result = [];
  for (var i = 0, l = xs.length; i < l; ++i) {
    [].push.apply(result, fn(xs[i]));
  }
  return result;
}

// filter :: forall a. (a -> Boolean) -> [a] -> [a]
function filter(xs, predicate) {
  var filtered = [];
  for (var i = 0, l = xs.length; i < l; ++i) {
    if (predicate(xs[i])) filtered.push(xs[i]);
  }
  return filtered;
}

// isExpression :: Node -> Boolean
var isExpression = esutils.ast.isExpression;
// isStatement :: Node -> Boolean
var isStatement = esutils.ast.isStatement;
// isSourceElement :: Node -> Boolean
var isSourceElement = esutils.ast.isSourceElement;
// directives :: [Maybe Node] -> [Node]
function directives(stmts) {
  if (stmts && stmts.length > 0) {
    var s = stmts[0];
    if (s && s.type === "ExpressionStatement" && s.expression && s.expression.type === "Literal" && typeof s.expression.value === "string")
      return [s.expression.value].concat(directives([].slice.call(stmts, 1)));
  }
  return [];
}

var OBJECT_PROPERTY_KINDS = ["init", "get", "set"];
var VARIABLE_DECLARATION_KINDS = ["var", "let", "const"];

var ASSIGNMENT_OPERATORS = ["=", "+=", "-=", "*=", "/=", "%=", "<<=", ">>=", ">>>=", "|=", "^=", "&="];
var BINARY_OPERATORS = ["==", "!=", "===", "!==", "<", "<=", ">", ">=", "<<", ">>", ">>>", "+", "-", "*", "/", "%", "|", "^", "&", "in", "instanceof"];
var LOGICAL_OPERATORS = ["||", "&&"];
var UNARY_OPERATORS = ["-", "+", "!", "~", "typeof", "void", "delete"];
var UPDATE_OPERATORS = ["++", "--"];

// isAssignmentOperator :: String -> Boolean
function isAssignmentOperator(op) { return ASSIGNMENT_OPERATORS.indexOf(op) >= 0; }
// isBinaryOperator :: String -> Boolean
function isBinaryOperator(op) { return BINARY_OPERATORS.indexOf(op) >= 0; }
// isLogicalOperator :: String -> Boolean
function isLogicalOperator(op) { return LOGICAL_OPERATORS.indexOf(op) >= 0; }
// isUnaryOperator :: String -> Boolean
function isUnaryOperator(op) { return UNARY_OPERATORS.indexOf(op) >= 0; }
// isUpdateOperator :: String -> Boolean
function isUpdateOperator(op) { return UPDATE_OPERATORS.indexOf(op) >= 0; }


var E, InvalidAstError = E = (function() {
  function C(){}
  C.prototype = Error.prototype;
  function InvalidAstError(node, message) {
    Error.call(this);
    this.node = node;
    this.message = message;
  }
  InvalidAstError.prototype = new C;
  InvalidAstError.prototype.constructor = InvalidAstError;
  InvalidAstError.prototype.name = "InvalidAstError";
  return InvalidAstError;
}());


// errorsP :: {labels :: [Label], inFunc :: Boolean, inIter :: Boolean, inSwitch :: Boolean} -> Node -> [InvalidAstError]
function errorsP(state) {
  return function recurse(node) {
    var errors = [], line, column, strict, recursionFn;

    if (node.loc != null) {
      if (node.loc.source != null && typeof node.loc.source !== "string")
        errors.push(new E(node, "`loc.source` must be a string or null"));
      if (node.loc.start == null) {
        errors.push(new E(node, "`loc.start` must be non-null if `loc` is non-null"));
      } else {
        line = node.loc.start.line;
        column = node.loc.start.column;
        if (typeof line !== "number" || line % 1 !== 0 || line < 1)
          errors.push(new E(node, "`loc.start.line` must be a positive integer"));
        if (typeof column !== "number" || column % 1 !== 0 || column < 0)
          errors.push(new E(node, "`loc.start.column` must be a non-negative integer"));
      }
      if (node.loc.end == null) {
        errors.push(new E(node, "`loc.end` must be non-null if `loc` is non-null"));
      } else {
        line = node.loc.end.line;
        column = node.loc.end.column;
        if (typeof line !== "number" || line % 1 !== 0 || line < 1)
          errors.push(new E(node, "`loc.end.line` must be a positive integer"));
        if (typeof column !== "number" || column % 1 !== 0 || column < 0)
          errors.push(new E(node, "`loc.end.column` must be a non-negative integer"));
      }
    }

    switch (node.type) {

      case "ArrayExpression":
        if (node.elements == null)
          errors.push(new E(node, "ArrayExpression `elements` member must be non-null"));
        else
          [].push.apply(errors, concatMap(function(element) {
            if (element == null)
              return [];
            else if (!isExpression(element))
              return [new E(element, "non-null ArrayExpression elements must be expression nodes")];
            return recurse(element);
          }, node.elements));
        break;

      case "AssignmentExpression":
        if (!isAssignmentOperator(node.operator))
          errors.push(new E(node, "AssignmentExpression `operator` member must be one of " + JSON.stringify(ASSIGNMENT_OPERATORS)));
        if (!isExpression(node.left))
          errors.push(new E(node, "AssignmentExpression `left` member must be an expression node"));
        if (!isExpression(node.right))
          errors.push(new E(node, "AssignmentExpression `right` member must be an expression node"));
        if (node.left != null)
          [].push.apply(errors, recurse(node.left));
        if (node.right != null)
          [].push.apply(errors, recurse(node.right));
        break;

      case "BinaryExpression":
        if (!isBinaryOperator(node.operator))
          errors.push(new E(node, "BinaryExpression `operator` member must be one of " + JSON.stringify(BINARY_OPERATORS)));
        if (!isExpression(node.left))
          errors.push(new E(node, "BinaryExpression `left` member must be an expression node"));
        if (!isExpression(node.right))
          errors.push(new E(node, "BinaryExpression `right` member must be an expression node"));
        if (node.left != null)
          [].push.apply(errors, recurse(node.left));
        if (node.right != null)
          [].push.apply(errors, recurse(node.right));
        break;

      case "BlockStatement":
        if (node.body == null)
          errors.push(new E(node, "BlockStatement `body` member must be non-null"));
        else
          [].push.apply(errors, concatMap(function(stmt) {
            var es = [];
            if (!isStatement(stmt))
              es.push(new E(stmt != null ? stmt : node, "BlockStatement `body` member must only contain statement nodes"));
            if (stmt != null)
              [].push.apply(es, recurse(stmt));
            return es;
          }, node.body));
        break;

      case "BreakStatement":
        if (!state.inIter && !state.inSwitch)
          errors.push(new E(node, "BreakStatement must have an IterationStatement or SwitchStatement as an ancestor"));
        if (node.label != null) {
          if (node.label.type !== "Identifier")
            errors.push(new E(node.label, "BreakStatement `label` member must be an Identifier node"));
          else if (state.labels.indexOf(node.label.name) < 0)
            errors.push(new E(node.label, "labelled BreakStatement must have a matching LabeledStatement ancestor"));
          [].push.apply(errors, recurse(node.label));
        }
        break;

      case "CallExpression":
        if (!isExpression(node.callee))
          errors.push(new E(node, "CallExpression `callee` member must be an expression node"));
        if (node.arguments == null)
          errors.push(new E(node, "CallExpression `arguments` member must be non-null"));
        else
          [].push.apply(errors, concatMap(function(arg) {
            var es = [];
            if (!isExpression(arg))
              es.push(new E(arg != null ? arg : node, "CallExpression `arguments` member must only contain expression nodes"));
            if (arg != null)
              [].push.apply(es, recurse(arg));
            return es;
          }, node.arguments));
        if (node.callee != null)
          [].push.apply(errors, recurse(node.callee));
        break;

      case "CatchClause":
        if (!isExpression(node.param))
          errors.push(new E(node, "CatchClause `param` member must be an expression node"));
        if (node.body == null || node.body.type !== "BlockStatement")
          errors.push(new E(node, "CatchClause `body` member must be a BlockStatement node"));
        if (node.param != null)
          [].push.apply(errors, recurse(node.param));
        if (node.body != null)
          [].push.apply(errors, recurse(node.body));
        break;

      case "ConditionalExpression":
        if (!isExpression(node.test))
          errors.push(new E(node, "ConditionalExpression `test` member must be an expression node"));
        if (!isExpression(node.alternate))
          errors.push(new E(node, "ConditionalExpression `alternate` member must be an expression node"));
        if (!isExpression(node.consequent))
          errors.push(new E(node, "ConditionalExpression `consequent` member must be an expression node"));
        if (node.test != null)
          [].push.apply(errors, recurse(node.test));
        if (node.alternate != null)
          [].push.apply(errors, recurse(node.alternate));
        if (node.consequent != null)
          [].push.apply(errors, recurse(node.consequent));
        break;

      case "ContinueStatement":
        if (!state.inIter)
          errors.push(new E(node, "ContinueStatement must have an IterationStatement as an ancestor"));
        if (node.label != null) {
          if (node.label.type !== "Identifier")
            errors.push(new E(node.label, "ContinueStatement `label` member must be an Identifier node"));
          else if (state.labels.indexOf(node.label.name) < 0)
            errors.push(new E(node.label, "labelled ContinueStatement must have a matching LabeledStatement ancestor"));
          [].push.apply(errors, recurse(node.label));
        }
        break;

      case "DebuggerStatement":
        break;

      case "DoWhileStatement":
        if (!isStatement(node.body))
          errors.push(new E(node, "DoWhileStatement `body` member must be a statement node"));
        if (!isExpression(node.test))
          errors.push(new E(node, "DoWhileStatement `test` member must be an expression node"));
        if (node.body != null)
          [].push.apply(errors, errorsP(merge({}, state, {inIter: true}))(node.body));
        if (node.test != null)
          [].push.apply(errors, recurse(node.test));
        break;

      case "EmptyStatement":
        break;

      case "ExpressionStatement":
        if (!isExpression(node.expression))
          errors.push(new E(node, "ExpressionStatement `expression` member must be an expression node"));
        if (node.expression != null)
          [].push.apply(errors, recurse(node.expression));
        break;

      case "ForInStatement":
        if (node.left == null || !isExpression(node.left) && node.left.type !== "VariableDeclaration")
          errors.push(new E(node, "ForInStatement `left` member must be an expression or VariableDeclaration node"));
        if (!isExpression(node.right))
          errors.push(new E(node, "ForInStatement `right` member must be an expression node"));
        if (!isStatement(node.body))
          errors.push(new E(node, "ForInStatement `body` member must be a statement node"));
        if (node.left != null)
          [].push.apply(errors, recurse(node.left));
        if (node.right != null)
          [].push.apply(errors, recurse(node.right));
        if (node.body != null)
          [].push.apply(errors, errorsP(merge({}, state, {inIter: true}))(node.body));
        break;

      case "ForStatement":
        if (node.init != null && !isExpression(node.init) && node.init.type !== "VariableDeclaration")
          errors.push(new E(node, "ForStatement `init` member must be an expression or VariableDeclaration node or null"));
        if (node.test != null && !isExpression(node.test))
          errors.push(new E(node.test, "ForStatement `test` member must be an expression node or null"));
        if (node.update != null && !isExpression(node.update))
          errors.push(new E(node, "ForStatement `update` member must be an expression node or null"));
        if (!isStatement(node.body))
          errors.push(new E(node, "ForStatement `body` member must be a statement node"));
        if (node.init != null)
          [].push.apply(errors, recurse(node.init));
        if (node.test != null)
          [].push.apply(errors, recurse(node.test));
        if (node.update != null)
          [].push.apply(errors, recurse(node.update));
        if (node.body != null)
          [].push.apply(errors, errorsP(merge({}, state, {inIter: true}))(node.body));
        break;

      case "FunctionDeclaration":
        if (node.id == null || node.id.type !== "Identifier")
          errors.push(new E(node, "FunctionDeclaration `id` member must be an Identifier node"));
        if (node.params == null)
          errors.push(new E(node, "FunctionDeclaration `params` member must be non-null"));
        else
          [].push.apply(errors, concatMap(function(param) {
            if (param == null)
              return [new E(node, "FunctionDeclaration `params` member must not contain null values")];
            else if (!isExpression(param))
              return [new E(param, "FunctionDeclaration params must be expression nodes")];
            return recurse(param);
          }, node.params));
        if (node.body == null || node.body.type !== "BlockStatement")
          errors.push(new E(node, "FunctionDeclaration `body` member must be an BlockStatement node"));
        if (node.id != null)
          [].push.apply(errors, recurse(node.id));
        if (node.body != null) {
          recursionFn = errorsP(merge({}, state, {inFunc: true}));
          if (node.body.type === "BlockStatement") {
            strict = state.strict || any(function(d) { return d === "use strict"; }, directives(node.body.body));
            if (strict && !state.strict)
              recursionFn = errorsP(merge({}, state, {strict: true, inFunc: true}));
            [].push.apply(errors, recursionFn({type: "Program", body: node.body.body}));
          } else {
            [].push.apply(errors, recursionFn(node.body));
          }
        }
        break;

      case "FunctionExpression":
        if (node.id != null && node.id.type !== "Identifier")
          errors.push(new E(node, "FunctionExpression `id` member must be an Identifier node or null"));
        if (node.params == null)
          errors.push(new E(node, "FunctionExpression `params` member must be non-null"));
        else
          [].push.apply(errors, concatMap(function(param) {
            if (param == null)
              return [new E(node, "FunctionExpression `params` member must not contain null values")];
            else if (!isExpression(param))
              return [new E(param, "FunctionExpression params must be expression nodes")];
            return recurse(param);
          }, node.params));
        if (node.body == null || node.body.type !== "BlockStatement")
          errors.push(new E(node, "FunctionExpression `body` member must be an BlockStatement node"));
        if (node.id != null)
          [].push.apply(errors, recurse(node.id));
        if (node.body != null) {
          recursionFn = errorsP(merge({}, state, {inFunc: true}));
          if (node.body.type === "BlockStatement") {
            strict = state.strict || any(function(d) { return d === "use strict"; }, directives(node.body.body));
            if (strict && !state.strict)
              recursionFn = errorsP(merge({}, state, {strict: true, inFunc: true}));
            [].push.apply(errors, recursionFn({type: "Program", body: node.body.body}));
          } else {
            [].push.apply(errors, recursionFn(node.body));
          }
        }
        break;

      case "Identifier":
        if (node.name == null)
          errors.push(new E(node, "Identifier `name` member must be non-null"));
        else if (!esutils.keyword.isIdentifierName(node.name))
          errors.push(new E(node, "Identifier `name` member must be a valid IdentifierName"));
        else if (esutils.keyword.isReservedWordES5(node.name, state.strict))
          errors.push(new E(node, "Identifier `name` member must not be a ReservedWord"));
        break;

      case "IfStatement":
        if (!isExpression(node.test))
          errors.push(new E(node, "IfStatement `test` member must be an expression node"));
        if (!isStatement(node.consequent))
          errors.push(new E(node, "IfStatement `consequent` member must be a statement node"));
        if (node.alternate != null && !isStatement(node.alternate))
          errors.push(new E(node, "IfStatement `alternate` member must be a statement node or null"));
        if (node.alternate != null && node.consequent != null && esutils.ast.isProblematicIfStatement(node))
          errors.push(new E(node, "IfStatement with null `alternate` must not be the `consequent` of an IfStatement with a non-null `alternate`"));
        if (node.test != null)
          [].push.apply(errors, recurse(node.test));
        if (node.consequent != null)
          [].push.apply(errors, recurse(node.consequent));
        if (node.alternate != null)
          [].push.apply(errors, recurse(node.alternate));
        break;

      case "LabeledStatement":
        if (node.label == null) {
          errors.push(new E(node, "LabeledStatement `label` member must be an Identifier node"));
        } else {
          if (node.label.type !== "Identifier")
            errors.push(new E(node, "LabeledStatement `label` member must be an Identifier node"));
          else if (state.labels.indexOf(node.label.name) >= 0)
            errors.push(new E(node, "LabeledStatement must not be nested within a LabeledStatement with the same label"));
          [].push.apply(errors, recurse(node.label));
        }
        if (!isStatement(node.body))
          errors.push(new E(node, "LabeledStatement `body` member must be a statement node"));
        if (node.body != null) {
          if (node.label != null)
              [].push.apply(errors, errorsP(merge({}, state, {labels: state.labels.concat(node.label.name)}))(node.body));
          else
              [].push.apply(errors, recurse(node.body));
        }
        break;

      case "Literal":
        switch (getClass(node.value)) {
          case "Boolean":
          case "Null":
          case "RegExp":
          case "String":
            break;
          case "Number":
            if (node.value !== node.value) {
              errors.push(new E(node, "numeric Literal nodes must not be NaN"));
            } else {
              if (node.value < 0 || node.value === 0 && 1 / node.value < 0)
              errors.push(new E(node, "numeric Literal nodes must be non-negative"));
              if (!isFinite(node.value))
                errors.push(new E(node, "numeric Literal nodes must be finite"));
            }
            break;
          default:
            errors.push(new E(node, "Literal nodes must have a boolean, null, regexp, string, or number as the `value` member"));
        }
        break;

      case "LogicalExpression":
        if (!isLogicalOperator(node.operator))
          errors.push(new E(node, "LogicalExpression `operator` member must be one of " + JSON.stringify(LOGICAL_OPERATORS)));
        if (!isExpression(node.left))
          errors.push(new E(node, "LogicalExpression `left` member must be an expression node"));
        if (!isExpression(node.right))
          errors.push(new E(node, "LogicalExpression `right` member must be an expression node"));
        if (node.left != null)
          [].push.apply(errors, recurse(node.left));
        if (node.right != null)
          [].push.apply(errors, recurse(node.right));
        break;

      case "MemberExpression":
        if (!isExpression(node.object))
          errors.push(new E(node, "MemberExpression `object` member must be an expression node"));
        if (node.computed) {
          if (!isExpression(node.property))
            errors.push(new E(node, "computed MemberExpression `property` member must be an expression node"));
          if (node.property != null)
            [].push.apply(errors, recurse(node.property));
        } else if (node.property == null || node.property.type !== "Identifier") {
            errors.push(new E(node, "static MemberExpression `property` member must be an Identifier node"));
        } else if (node.property.name == null || !esutils.keyword.isIdentifierName(node.property.name)) {
            errors.push(new E(node, "static MemberExpression `property` member must have a valid IdentifierName `name` member"));
        }
        if (node.object != null)
          [].push.apply(errors, recurse(node.object));
        break;

      case "NewExpression":
        if (!isExpression(node.callee))
          errors.push(new E(node, "NewExpression `callee` member must be an expression node"));
        if (node.arguments == null)
          errors.push(new E(node, "NewExpression `arguments` member must be non-null"));
        else
          [].push.apply(errors, concatMap(function(arg) {
            var es = [];
            if (!isExpression(arg))
              es.push(new E(arg != null ? arg : node, "NewExpression `arguments` member must only contain expression nodes"));
            if (arg != null)
              [].push.apply(es, recurse(arg));
            return es;
          }, node.arguments));
        if (node.callee != null)
          [].push.apply(errors, recurse(node.callee));
        break;

      case "ObjectExpression":
        if (node.properties == null) {
          errors.push(new E(node, "ObjectExpression `properties` member must be non-null"));
        } else {
          var initKeySet = {}, getKeySet = {}, setKeySet = {};
          [].push.apply(errors, concatMap(function(property) {
            var es = [], key;
            if (property == null)
              return [new E(node, "ObjectExpression `properties` must not contain null values")];
            if (!isExpression(property.value))
              es.push(new E(property, "ObjectExpression property `value` member must be an expression node"));
            if (property.value != null)
              [].push.apply(es, recurse(property.value));
            switch (property.kind) {
              case "init": break;
              case "get":
                if (property.value != null) {
                  if (property.value.type !== "FunctionExpression")
                    es.push(new E(property.value, "ObjectExpression getter property `value` member must be a FunctionExpression node"));
                  else if (property.value.params == null || property.value.params.length !== 0)
                    es.push(new E(property.value, "ObjectExpression getter property `value` member must have zero parameters"));
                }
                break;
              case "set":
                if (property.value != null) {
                  if (property.value.type !== "FunctionExpression")
                    es.push(new E(property.value, "ObjectExpression setter property `value` member must be a FunctionExpression node"));
                  else if (property.value.params == null || property.value.params.length !== 1)
                    es.push(new E(property.value, "ObjectExpression setter property `value` member must have exactly one parameter"));
                }
                break;
              default:
                es.push(new E(property, "ObjectExpression property `kind` member must be one of " + JSON.stringify(OBJECT_PROPERTY_KINDS)));
            }
            if (property.key == null) {
              es.push(new E(property, "ObjectExpression property `key` member must be an Identifier or Literal node"));
            } else {
              switch (property.key.type) {
                case "Identifier":
                  if (property.key.name == null || !esutils.keyword.isIdentifierName(property.key.name))
                    es.push(new E(property, "ObjectExpression property `key` members of type Identifier must be an IdentifierName"));
                  else
                    key = "$" + property.key.name;
                  break;
                case "Literal":
                  if (["Number", "String"].indexOf(getClass(property.key.value)) < 0) {
                    es.push(new E(property, "ObjectExpression property `key` members of type Literal must have either a number or string `value` member"));
                  } else {
                    [].push.apply(es, recurse(property.key));
                    key = "$" + property.key.value;
                  }
                  break;
                default:
                  es.push(new E(property, "ObjectExpression property `key` member must be an Identifier or Literal node"));
              }
              if (key != null)
                switch (property.kind) {
                  case "init":
                    if (initKeySet.hasOwnProperty(key) && state.strict)
                      es.push(new E(property, "ObjectExpression must not have more than one data property with the same name in strict mode"));
                    if (getKeySet.hasOwnProperty(key))
                      es.push(new E(property, "ObjectExpression must not have data and getter properties with the same name"));
                    if (setKeySet.hasOwnProperty(key))
                      es.push(new E(property, "ObjectExpression must not have data and setter properties with the same name"));
                    initKeySet[key] = true;
                    break;
                  case "get":
                    if (initKeySet.hasOwnProperty(key))
                      es.push(new E(property, "ObjectExpression must not have data and getter properties with the same name"));
                    if (getKeySet.hasOwnProperty(key))
                      es.push(new E(property, "ObjectExpression must not have multiple getters with the same name"));
                    getKeySet[key] = true;
                    break;
                  case "set":
                    if (initKeySet.hasOwnProperty(key))
                      es.push(new E(property, "ObjectExpression must not have data and setter properties with the same name"));
                    if (setKeySet.hasOwnProperty(key))
                      es.push(new E(property, "ObjectExpression must not have multiple setters with the same name"));
                    setKeySet[key] = true;
                    break;
                }
            }
            return es;
          }, node.properties));
        }
        break;

      case "Program":
        if (node.body == null) {
          errors.push(new E(node, "Program `body` member must be non-null"));
        } else {
          strict = state.strict || any(function(d) { return d === "use strict"; }, directives(node.body));
          recursionFn = strict && !state.strict ? errorsP(merge({}, state, {strict: true})) : recurse;
          [].push.apply(errors, concatMap(function(sourceElement) {
            var es = [];
            if (!isSourceElement(sourceElement))
              es.push(new E(sourceElement != null ? sourceElement : node, "Program `body` member must only contain statement or function declaration nodes"));
            if (sourceElement != null)
              [].push.apply(es, recursionFn(sourceElement));
            return es;
          }, node.body));
        }
        break;

      case "ReturnStatement":
        if (!state.inFunc)
          errors.push(new E(node, "ReturnStatement must be nested within a FunctionExpression or FunctionDeclaration node"));
        if (node.argument != null) {
          if (!isExpression(node.argument))
            errors.push(new E(node, "ReturnStatement `argument` member must be an expression node or null"));
          [].push.apply(errors, recurse(node.argument));
        }
        break;

      case "SequenceExpression":
        if (node.expressions == null) {
          errors.push(new E(node, "SequenceExpression `expressions` member must be non-null"));
        } else {
          if (node.expressions.length < 2)
            errors.push(new E(node, "SequenceExpression `expressions` member length must be >= 2"));
          [].push.apply(errors, concatMap(function(expr) {
            var es = [];
            if (!isExpression(expr))
              es.push(new E(expr != null ? expr : node, "SequenceExpression `expressions` member must only contain expression nodes"));
            if (expr != null)
              [].push.apply(es, recurse(expr));
            return es;
          }, node.expressions));
        }
        break;

      case "SwitchCase":
        if (node.test != null) {
          if (!isExpression(node.test))
            errors.push(new E(node, "SwitchCase `test` member must be an expression node or null"));
          [].push.apply(errors, recurse(node.test));
        }
        if (node.consequent == null) {
          errors.push(new E(node, "SwitchCase `consequent` member must be non-null"));
        } else {
          recursionFn = errorsP(merge({}, state, {inSwitch: true}));
          [].push.apply(errors, concatMap(function(stmt) {
            var es = [];
            if (!isStatement(stmt))
              es.push(new E(stmt != null ? stmt : node, "SwitchCase `consequent` member must only contain statement nodes"));
            if (stmt != null)
              [].push.apply(es, recursionFn(stmt));
            return es;
          }, node.consequent));
        }
        break;

      case "SwitchStatement":
        if (!isExpression(node.discriminant))
          errors.push(new E(node, "SwitchStatement `discriminant` member must be an expression node"));
        if (node.cases == null) {
          errors.push(new E(node, "SwitchStatement `cases` member must be non-null"));
        } else {
          [].push.apply(errors, concatMap(function(switchCase) {
            var es = [];
            if (switchCase == null || switchCase.type !== "SwitchCase")
              es.push(new E(switchCase != null ? switchCase : node, "SwitchStatement `cases` member must only contain SwitchCase nodes"));
            if (switchCase != null)
              [].push.apply(es, recurse(switchCase));
            return es;
          }, node.cases));
          if (filter(node.cases, function(c) { return c != null && c.test == null; }).length > 1)
            errors.push(new E(node, "SwitchStatement `cases` member must contain no more than one SwitchCase with a null `test` member"));
        }
        if (node.discriminant != null)
          [].push.apply(errors, recurse(node.discriminant));
        break;

      case "ThisExpression":
        break;

      case "ThrowStatement":
        if (!isExpression(node.argument))
          errors.push(new E(node, "ThrowStatement `argument` member must be an expression node"));
        if (node.argument != null)
          [].push.apply(errors, recurse(node.argument));
        break;

      case "TryStatement":
        // NOTE: TryStatement interface changed from {handlers: [CatchClause]} to {handler: CatchClause}; we support both
        var handlers = node.handlers || (node.handler ? [node.handler] : []);
        if (node.block == null || node.block.type !== "BlockStatement")
          errors.push(new E(node.block != null ? node.block : node, "TryStatement `block` member must be a BlockStatement node"));
        if (node.finalizer != null && node.finalizer.type !== "BlockStatement")
          errors.push(new E(node.finalizer, "TryStatement `finalizer` member must be a BlockStatement node"));
        [].push.apply(errors, concatMap(function(handler) {
          var es = [];
          if (handler == null || handler.type !== "CatchClause")
            es.push(new E(handler != null ? handler : node, "TryStatement `handler` member must be a CatchClause node"));
          if (handler != null)
            [].push.apply(es, recurse(handler));
          return es;
        }, handlers));
        if (node.block != null)
          [].push.apply(errors, recurse(node.block));
        if (node.finalizer != null)
          [].push.apply(errors, recurse(node.finalizer));
        if (handlers.length < 1 && node.finalizer == null)
            errors.push(new E(node, "TryStatement must have a non-null `handler` member or a non-null `finalizer` member"));
        break;

      case "UnaryExpression":
        if (!isUnaryOperator(node.operator))
          errors.push(new E(node, "UnaryExpression `operator` member must be one of " + JSON.stringify(UNARY_OPERATORS)));
        if (!isExpression(node.argument))
          errors.push(new E(node, "UnaryExpression `argument` member must be an expression node"));
        if (node.argument != null) {
          [].push.apply(errors, recurse(node.argument));
          if (state.strict && node.operator === "delete" && node.argument.type === "Identifier")
            errors.push(new E(node, "`delete` with unqualified identifier not allowed in strict mode"));
        }
        break;

      case "UpdateExpression":
        if (!isUpdateOperator(node.operator))
          errors.push(new E(node, "UpdateExpression `operator` member must be one of " + JSON.stringify(UNARY_OPERATORS)));
        if (!isExpression(node.argument))
          errors.push(new E(node, "UpdateExpression `argument` member must be an expression node"));
        if (node.argument != null)
          [].push.apply(errors, recurse(node.argument));
        break;

      case "VariableDeclaration":
        if (node.declarations == null) {
          errors.push(new E(node, "VariableDeclaration `declarations` member must be non-null"));
        } else {
          if (node.declarations.length < 1)
            errors.push(new E(node, "VariableDeclaration `declarations` member must be non-empty"));
          if (VARIABLE_DECLARATION_KINDS.indexOf(node.kind) < 0)
            errors.push(new E(node, "VariableDeclaration `kind` member must be one of " + JSON.stringify(VARIABLE_DECLARATION_KINDS)));
          [].push.apply(errors, concatMap(function(decl) {
            var es = [];
            if (decl == null || decl.type !== "VariableDeclarator")
              es.push(new E(decl != null ? decl : node, "VariableDeclaration `declarations` member must contain only VariableDeclarator nodes"));
            if (decl != null)
              [].push.apply(es, recurse(decl));
            return es;
          }, node.declarations));
        }
        break;

      case "VariableDeclarator":
        if (!isExpression(node.id))
          errors.push(new E(node, "VariableDeclarator `id` member must be an expression node"));
        if (node.init != null) {
          if (!isExpression(node.init))
            errors.push(new E(node, "VariableDeclarator `init` member must be an expression node or null"));
          [].push.apply(errors, recurse(node.init));
        }
        if (node.id != null)
          [].push.apply(errors, recurse(node.id));
        break;

      case "WhileStatement":
        if (!isExpression(node.test))
          errors.push(new E(node, "WhileStatement `test` member must be an expression node"));
        if (!isStatement(node.body))
          errors.push(new E(node, "WhileStatement `body` member must be a statement node"));
        if (node.test != null)
          [].push.apply(errors, recurse(node.test));
        if (node.body != null)
          [].push.apply(errors, errorsP(merge({}, state, {inIter: true}))(node.body));
        break;

      case "WithStatement":
        if (state.strict)
          errors.push(new E(node, "WithStatement not allowed in strict mode"));
        if (!isExpression(node.object))
          errors.push(new E(node, "WithStatement `object` member must be an expression node"));
        if (!isStatement(node.body))
          errors.push(new E(node, "WithStatement `body` member must be a statement node"));
        if (node.object != null)
          [].push.apply(errors, recurse(node.object));
        if (node.body != null)
          [].push.apply(errors, errorsP(merge({}, state, {inIter: true}))(node.body));
        break;

      default:
        switch (getClass(node.type)) {
        case "String":
          errors.push(new E(node, "unrecognised node type: " + JSON.stringify(node.type)));
          break;
        case "Null":
        case "Undefined":
          errors.push(new E(node, "all AST nodes must have a `type` member"));
          break;
        default:
          errors.push(new E(node, "AST node `type` must be a string"));
        }
    }

    return errors;
  };
}

var START_STATE = {labels: [], inFunc: false, inIter: false, inSwitch: false, strict: false};

module.exports = {

  // isValid :: Maybe Node -> Boolean
  isValid: function isValid(node) {
    return node != null && node.type === "Program" &&
      errorsP(START_STATE)(node).length < 1;
  },

  // isValidExpression :: Maybe Node -> Boolean
  isValidExpression: function isValidExpression(node) {
    return isExpression(node) && errorsP(START_STATE)(node).length < 1;
  },

  // InvalidAstError :: Node -> String -> InvalidAstError
  InvalidAstError: InvalidAstError,

  // errors :: Maybe Node -> [InvalidAstError]
  errors: function errors(node) {
    var errors = [];
    if (node == null) {
      errors.push(new E(node, "given AST node should be non-null"));
    } else {
      if (node.type !== "Program")
        errors.push(new E(node, "given AST node should be of type Program"));
      [].push.apply(errors, errorsP(START_STATE)(node));
    }
    return errors;
  }

};
