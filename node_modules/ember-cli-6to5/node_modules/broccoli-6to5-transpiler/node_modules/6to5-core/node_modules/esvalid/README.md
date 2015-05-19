# esvalid

## Install

    npm install esvalid

## Usage

#### `esvalid.isValid(node)` :: Spidermonkey AST Node → Boolean

Returns true if and only if the given AST node represents a valid ECMAScript
program.

#### `esvalid.isValidExpression(node)` :: Spidermonkey AST Node → Boolean

Returns true if and only if the given AST node represents a valid ECMAScript
expression.

#### `esvalid.errors(node)` :: Spidermonkey AST Node → [InvalidAstError]

Returns an array of `InvalidAstError` objects representing the errors in the
given AST. An effort is made to continue collecting errors in the face of
malformed ASTs. If an empty array is returned, it is implied that the given AST
node is error free.

#### `new esvalid.InvalidAstError(node, message)` :: Node -> String -> InvalidAstError

Constructs a new `InvalidAstError` instance. `node` must be non-null.

##### Example

```
var esvalid = require("esvalid");
var esprima = require("esprima");

var program = esprima.parse(fs.readFileSync(require.resolve("esprima")));
esvalid.isValid(program); // true

esvalid.isValid({type: "Program", body: []}); // true
esvalid.isValid({type: "Program", body: null}); // false

esvalid.isValidExpression({type: "Program", body: []}); // false
esvalid.isValidExpression({type: "Literal", value: 0}); // true

esvalid.errors({type: "Program", body: []}); // []
var error = esvalid.errors({type: "Program", body: null})[0];
error instanceof esvalid.InvalidAstError; // true
error.node; // {type: "Program", body: null}
error.message; // "Program `body` member must be non-null"
```

## Validity Tests

This is a list of all esvalid validity tests other than `null` tests and type checks.

* BreakStatement must have an IterationStatement or SwitchStatement as an ancestor
* labelled BreakStatement must have a matching LabeledStatement ancestor
* ContinueStatement must have an IterationStatement as an ancestor
* labelled ContinueStatement must have a matching LabeledStatement ancestor
* Identifier `name` member must be a valid IdentifierName
* Identifier `name` member must not be a ReservedWord
* IfStatement with null `alternate` must not be the `consequent` of an IfStatement with a non-null `alternate`
* LabeledStatement must not be nested within a LabeledStatement with the same label
* numeric Literal nodes must not be NaN
* numeric Literal nodes must be non-negative
* numeric Literal nodes must be finite
* static MemberExpression `property` member must have a valid IdentifierName `name` member
* ObjectExpression getter property `value` member must have zero parameters
* ObjectExpression setter property `value` member must have exactly one parameter
* ObjectExpression must not have more than one data property with the same name in strict mode
* ObjectExpression must not have data and getter properties with the same name
* ObjectExpression must not have data and setter properties with the same name
* ObjectExpression must not have data and getter properties with the same name
* ObjectExpression must not have multiple getters with the same name
* ObjectExpression must not have data and setter properties with the same name
* ObjectExpression must not have multiple setters with the same name
* ReturnStatement must be nested within a FunctionExpression or FunctionDeclaration node
* SequenceExpression `expressions` member length must be >= 2
* SwitchStatement `cases` member must contain no more than one SwitchCase with a null `test` member
* TryStatement must have a non-null `handler` member or a non-null `finalizer` member
* `delete` with unqualified identifier not allowed in strict mode
* VariableDeclaration `declarations` member must be non-empty
* WithStatement not allowed in strict mode
