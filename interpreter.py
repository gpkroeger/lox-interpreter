from errors import *
from evals import *
from Token import Token
from tokenTypes import tokenTypess
from env import Environment
from enum import Enum, auto
from collections import deque

class rException(Exception):
    def __init__(self, val):
        self.val = val

def isNumber(value):
    return isinstance(value, int) or isinstance(value, float)

def isEqual(left, right):
    return left == right

def isOperandNumber(token, operand):
    if isNumber(operand):
        return
    raise InterpretError(token, "Operand must be a number.")

def checkBothOperand(token, left, right):
    if isNumber(left) and isNumber(right):
        return
    raise InterpretError(token, "Operands must be numbers.")

def stringify(value):
    if value is None:
        return "nil"
    elif isinstance(value, bool):
        return str(value).lower()
    elif isNumber(value):
        return str(value)
    else:
        return str(value)


class LoxFunction(LoxCallable):
    def __init__(
        self, declaration: Function, closure: Environment, is_initializer: bool
    ):
        self.declaration = declaration
        self.closure = closure
        self.is_initializer = is_initializer

    @property
    def arity(self) -> int:
        return len(self.declaration.params)

    def call(self, interpreter: AbstractInterpreter[Any], arguments: List[Any]) -> Any:
        local = Environment(self.closure)
        for (param, arg) in zip(self.declaration.params, arguments):
            local[param.lexeme] = arg
        try:
            interpreter.visit_statements(self.declaration.body, local)
        except rException as ret:
            if self.is_initializer:
                return self.closure.get_at(0, "this")

            return ret.value

        if self.is_initializer:
            return self.closure.get_at(0, "this")

        return None

    def bind(self, instance: "LoxInstance"):
        env = Environment(self.closure)
        env["this"] = instance
        return LoxFunction(self.declaration, env, self.is_initializer)

def iTruth(value):
    if (value is None) or (value is False):
        return False

    return True

class LoxClass(LoxCallable):
    def __init__(self, name: str, superclass: Optional["LoxClass"], methods):
        self.name = name
        self.superclass = superclass
        self.methods = methods

    def find_method(self, name: str) -> Optional[LoxFunction]:
        if name in self.methods:
            return self.methods[name]

        if self.superclass:
            return self.superclass.find_method(name)

    def __str__(self):
        return f"<class {self.name}>"

    def call(self, interpreter: AbstractInterpreter[Any], arguments: List[Any]) -> Any:
        instance = LoxInstance(self)
        initializer = self.find_method("init")
        if initializer:
            initializer.bind(instance).call(interpreter, arguments)
        return instance

    @property
    def arity(self) -> int:
        initializer = self.find_method("init")
        if initializer:
            return initializer.arity
        return 0


class LoxInstance:
    def __init__(self, klass: LoxClass):
        self.klass = klass
        self.fields = {}

    def __getitem__(self, key: Token):
        if key.lexeme in self.fields:
            return self.fields[key.lexeme]

        method = self.klass.find_method(key.lexeme)

        if method:
            return method.bind(self)

        raise InterpretError(key, f"Undefined property '{key.lexeme}'.")

    def __setitem__(self, key: Token, value: Any):
        self.fields[key.lexeme] = value

    def __str__(self):
        return f"<instance of {self.klass.name}>"


import time


class NativeFunction(LoxCallable):
    def __init__(self, arity, f):
        self._arity = arity
        self._f = f

    @property
    def arity(self) -> int:
        return self._arity

    def call(self, _: AbstractInterpreter[Any], arguments: List[Any]) -> Any:
        return self._f(*arguments)


def gen_globals():
    env = Environment()
    env["clock"] = NativeFunction(0, lambda: time.time())
    return env


class Interpreter(StmtVisitor[None], ExprVisitor[Any], AbstractInterpreter[Any]):
    def __init__(self):
        self.globals = gen_globals()
        self.environment = self.globals
        self.local_vars = {}

    def visit_statements(self, stmts: List[Stmt], env: Optional[Environment] = None):
        if env is None:
            env = self.environment

        previous = self.environment

        try:
            self.environment = env
            for stmt in stmts:
                self.visit_stmt(stmt)
        except InterpretError as err:
            runtimeError(err)
        finally:
            self.environment = previous

    def visit_stmt(self, stmt: Stmt):
        stmt.accept(self)

    def visit_expr(self, expr: Expr):
        return expr.accept(self)

    def visit_block(self, block: Block):
        self.visit_statements(block.statements, Environment(self.environment))

    def visit_print(self, print_stmt: Print):
        value = self.visit_expr(print_stmt.expression)
        print(stringify(value))

    def visit_expression(self, expr: Expression):
        return self.visit_expr(expr.expression)

    def visit_if(self, if_stmt: If):
        if iTruth(self.visit_expr(if_stmt.condition)):
            self.visit_stmt(if_stmt.then_branch)
        elif if_stmt.else_branch:
            self.visit_stmt(if_stmt.else_branch)

    def visit_while(self, while_stmt: While):
        while iTruth(self.visit_expr(while_stmt.condition)):
            self.visit_stmt(while_stmt.body)

    def visit_var(self, var_stmt: Var):
        value = None
        if var_stmt.initializer is not None:
            value = self.visit_expr(var_stmt.initializer)
        self.environment[var_stmt.name.lexeme] = value

    def visit_function(self, func_stmt: Function):
        self.environment[func_stmt.name.lexeme] = LoxFunction(
            func_stmt, self.environment, False
        )

    def visit_variable(self, expr: Variable) -> Any:
        return self.lookup_variable(expr.name, expr)

    def lookup_variable(self, name: Token, expr: Expr) -> Any:
        distance = self.local_vars.get(id(expr), None)
        if distance is not None:
            return self.environment.get_at(distance, name.lexeme)
        else:
            return self.globals[name]

    def visit_assign(self, expr: Assign):
        value = self.visit_expr(expr.value)
        distance = self.local_vars.get(id(expr), None)

        if distance is not None:
            self.environment.assign_at(distance, expr.name.lexeme, value)
        else:
            self.globals[expr.name.lexeme] = value
        return value

    def visit_return(self, return_stmt: Return):
        value = None
        if return_stmt.value is not None:
            value = self.visit_expr(return_stmt.value)
        raise rException(value)

    def visit_call(self, call_expr: Call):
        callee = self.visit_expr(call_expr.callee)
        arguments = [self.visit_expr(arg) for arg in call_expr.arguments]

        if not isinstance(callee, LoxCallable):
            raise InterpretError(call_expr.token, f"{callee} is not callable")

        if len(arguments) != callee.arity:
            raise InterpretError(
                call_expr.token,
                f"Expected {callee.arity} arguments, but got {len(arguments)}.",
            )

        return callee.call(self, arguments)

    def visit_literal(self, literal: Literal):
        return literal.value

    def visit_grouping(self, grouping: Grouping):
        return self.visit_expr(grouping.expression)

    def visit_unary(self, unary: Unary):
        right = self.visit_expr(unary.right)
        if unary.operator.ttype == tokenTypes.MINUS:
            return -right
        elif unary.operator.ttype == tokenTypes.BANG:
            return not iTruth(right)
        else:
            raise InterpretError(unary.operator, "Invalid unary operator")

    def visit_binary(self, binary: Binary):
        left = self.visit_expr(binary.left)
        right = self.visit_expr(binary.right)

        if binary.operator.ttype == tokenTypes.MINUS:
            checkBothOperand(binary.operator, left, right)
            return left - right
        elif binary.operator.ttype == tokenTypes.SLASH:
            checkBothOperand(binary.operator, left, right)
            if right == 0:
                raise InterpretError(binary.operator, "Division by zero")
            return left / right
        elif binary.operator.ttype == tokenTypes.STAR:
            checkBothOperand(binary.operator, left, right)
            return left * right
        elif binary.operator.ttype == tokenTypes.PLUS:
            if isinstance(left, str) and isinstance(right, str):
                return left + right
            checkBothOperand(binary.operator, left, right)
            return left + right
        elif binary.operator.ttype == tokenTypes.GREATER:
            checkBothOperand(binary.operator, left, right)
            return left > right
        elif binary.operator.ttype == tokenTypes.GREATER_EQUAL:
            checkBothOperand(binary.operator, left, right)
            return left >= right
        elif binary.operator.ttype == tokenTypes.LESS:
            checkBothOperand(binary.operator, left, right)
            return left < right
        elif binary.operator.ttype == tokenTypes.LESS_EQUAL:
            checkBothOperand(binary.operator, left, right)
            return left <= right
        elif binary.operator.ttype == tokenTypes.BANG_EQUAL:
            return not isEqual(left, right)
        elif binary.operator.ttype == tokenTypes.EQUAL_EQUAL:
            return isEqual(left, right)
        else:
            raise InterpretError(binary.operator, "Unsupported binary operator")

    def visit_logical(self, logical: Logical):
        if logical.operator.ttype == tokenTypes.OR:
            left = self.visit_expr(logical.left)
            if iTruth(left):
                return left
            return self.visit_expr(logical.right)
        elif logical.operator.ttype == tokenTypes.AND:
            left = self.visit_expr(logical.left)
            if iTruth(left):
                return self.visit_expr(logical.right)
            return left
        else:
            raise InterpretError(logical.operator, "Invalid logical operator")

    def visit_class(self, stmt: Class) -> Any:
        superclass: Optional[LoxClass] = None
        if stmt.superclass:
            superclass = self.visit_expr(stmt.superclass)
            if not isinstance(superclass, LoxClass):
                raise InterpretError(
                    stmt.superclass.name, "Superclass must be a class."
                )

        self.environment[stmt.name.lexeme] = None

        if stmt.superclass:
            self.environment = Environment(self.environment)
            self.environment["super"] = superclass

        klass = LoxClass(
            stmt.name.lexeme,
            superclass,
            {
                f.name.lexeme: LoxFunction(f, self.environment, f.name.lexeme == "init")
                for f in stmt.methods
            },
        )

        if stmt.superclass and self.environment.enclosing:
            self.environment = self.environment.enclosing

        self.environment[stmt.name.lexeme] = klass

    def visit_get(self, expr: Get) -> Any:
        instance = self.visit_expr(expr.object)

        if not isinstance(instance, LoxInstance):
            raise InterpretError(expr.name, "Only instances have properties")

        return instance[expr.name]

    def visit_set(self, expr: Set) -> Any:
        object = self.visit_expr(expr.object)
        value = self.visit_expr(expr.value)

        if not isinstance(object, LoxInstance):
            raise InterpretError(expr.name, "Only instances have fields")

        object[expr.name] = value
        return value

    def visit_this(self, expr: This) -> Any:
        return self.lookup_variable(expr.keyword, expr)

    def visit_super(self, expr: Super) -> Any:
        distance = self.local_vars[id(expr)]
        superclass = cast(LoxClass, self.environment.get_at(distance, "super"))
        object = cast(LoxInstance, self.environment.get_at(distance - 1, "this"))

        method = superclass.find_method(expr.method.lexeme)

        if not method:
            raise InterpretError(
                expr.method, f"Undefined property '{expr.method.lexeme}'."
            )
        return method.bind(object)

class FunctionType(Enum):
    NONE = auto()
    FUNCTION = auto()
    METHOD = auto()
    INITIALIZER = auto()


class ClassType(Enum):
    NONE = auto()
    CLASS = auto()
    SUBCLASS = auto()


class Resolver(StmtVisitor[None], ExprVisitor[None]):
    def __init__(self, interpreter):
        self.scopes = deque()
        self.interpreter = interpreter
        self.current_function = FunctionType.NONE
        self.current_class = ClassType.NONE

    def begin_scope(self):
        self.scopes.append({})

    def end_scope(self):
        self.scopes.pop()

    def declare(self, name: Token) -> None:
        if len(self.scopes) == 0:
            return
        scope = self.scopes[-1]

        if name.lexeme in scope:
            newError(name, "Variable with this name already declared in this scope.")

        scope[name.lexeme] = False

    def define(self, name: Token) -> None:
        if len(self.scopes) == 0:
            return
        self.scopes[-1][name.lexeme] = True

    def resolve_local(self, expr: Expr, name: Token) -> None:
        for i, scope in enumerate(reversed(self.scopes)):
            if name.lexeme in scope:
                self.interpreter.local_vars[id(expr)] = i
                return

    def resolve_list(self, statements: List[Stmt]):
        for statement in statements:
            statement.accept(self)

    def resolve_function(self, func: Function, function_type: FunctionType) -> None:
        enclosing_function = self.current_function
        self.current_function = function_type

        self.begin_scope()
        for param in func.params:
            self.declare(param)
            self.define(param)
        self.resolve_list(func.body)
        self.end_scope()

        self.current_function = enclosing_function

    def visit_block(self, stmt: Block) -> None:
        self.begin_scope()
        self.resolve_list(stmt.statements)
        self.end_scope()

    def resolve_stmt(self, stmt: Stmt) -> None:
        stmt.accept(self)

    def resolve_expr(self, expr: Expr) -> None:
        expr.accept(self)

    def visit_var(self, stmt: Var) -> None:
        self.declare(stmt.name)
        if stmt.initializer:
            self.resolve_expr(stmt.initializer)
        self.define(stmt.name)

    def visit_variable(self, expr: Variable) -> None:
        if self.scopes and self.scopes[-1].get(expr.name.lexeme) is False:
            newError(expr.name, "Cannot read local variable in its own initializer.")
        self.resolve_local(expr, expr.name)

    def visit_assign(self, expr: Assign) -> None:
        self.resolve_expr(expr.value)
        self.resolve_local(expr, expr.name)

    def visit_function(self, func: Function) -> None:
        self.declare(func.name)
        self.define(func.name)

        self.resolve_function(func, FunctionType.FUNCTION)

    def visit_expression(self, expr: Expression) -> None:
        self.resolve_expr(expr.expression)

    def visit_if(self, stmt: If) -> None:
        self.resolve_expr(stmt.condition)
        self.resolve_stmt(stmt.then_branch)
        if stmt.else_branch:
            self.resolve_stmt(stmt.else_branch)

    def visit_print(self, stmt: Print) -> None:
        self.resolve_expr(stmt.expression)

    def visit_return(self, stmt: Return) -> None:
        if self.current_function == FunctionType.NONE:
            newError(stmt.keyword, "Cannot return from top-level code.")

        if stmt.value:
            if self.current_function == FunctionType.INITIALIZER:
                newError(stmt.keyword, "Can't return a value from an initializer.")

            self.resolve_expr(stmt.value)

    def visit_while(self, stmt: While) -> None:
        self.resolve_expr(stmt.condition)
        self.resolve_stmt(stmt.body)

    def visit_binary(self, expr: Binary) -> None:
        self.resolve_expr(expr.left)
        self.resolve_expr(expr.right)

    def visit_call(self, expr: Call) -> None:
        self.resolve_expr(expr.callee)
        for arg in expr.arguments:
            self.resolve_expr(arg)

    def visit_grouping(self, expr: Grouping) -> None:
        self.resolve_expr(expr.expression)

    def visit_literal(self, _: Literal) -> None:
        pass

    def visit_logical(self, expr: Logical) -> None:
        self.resolve_expr(expr.left)
        self.resolve_expr(expr.right)

    def visit_unary(self, expr: Unary) -> None:
        self.resolve_expr(expr.right)

    def visit_class(self, stmt: Class) -> None:
        enclosing = self.current_class
        self.current_class = ClassType.CLASS

        self.declare(stmt.name)
        self.define(stmt.name)

        if stmt.superclass:
            self.current_class = ClassType.SUBCLASS
            self.resolve_expr(stmt.superclass)
            if stmt.superclass.name.lexeme == stmt.name.lexeme:
                newError(stmt.superclass.name, "A class can't inherit from itself")

            self.begin_scope()
            self.scopes[-1]["super"] = True

        self.begin_scope()
        self.scopes[-1]["this"] = True

        for method in stmt.methods:
            declaration = FunctionType.METHOD
            if method.name.lexeme == "init":
                declaration = FunctionType.INITIALIZER
            self.resolve_function(method, declaration)

        if stmt.superclass:
            self.end_scope()

        self.end_scope()
        self.current_class = enclosing

    def visit_get(self, expr: Get) -> None:
        self.resolve_expr(expr.object)

    def visit_set(self, expr: Set) -> None:
        self.resolve_expr(expr.object)
        self.resolve_expr(expr.value)

    def visit_this(self, expr: This) -> None:
        if self.current_class == ClassType.NONE:
            newError(expr.keyword, "Can't use 'this' outside of a class.")

        self.resolve_local(expr, expr.keyword)

    def visit_super(self, expr: Super) -> None:
        if self.current_class == ClassType.NONE:
            newError(expr.keyword, "Can't use 'super' outside of a class.")
        elif self.current_class != ClassType.SUBCLASS:
            newError(expr.keyword, "Can't use 'super' in a class with no superclass.")

        self.resolve_local(expr, expr.keyword)