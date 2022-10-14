from typing import Generic, Union, List, Optional, TypeVar, Union, Any
from dataclasses import dataclass
from Token import Token
import abc

Expr = Union[
    "Binary",
    "Grouping",
    "Literal",
    "Unary",
    "Call",
    "Variable",
    "Assign",
    "Logical",
    "Get",
    "Set",
    "This",
    "Super",
]
T = TypeVar("T")

@dataclass
class Binary:
    left: Expr
    operator: Token
    right: Expr

    def accept(self, visitor: "ExprVisitor[T]") -> T:
        return visitor.visit_binary(self)


@dataclass
class Logical:
    left: Expr
    operator: Token
    right: Expr

    def accept(self, visitor: "ExprVisitor[T]") -> T:
        return visitor.visit_logical(self)


@dataclass
class Grouping:
    expression: Expr

    def accept(self, visitor: "ExprVisitor[T]") -> T:
        return visitor.visit_grouping(self)


@dataclass
class Literal:
    value: Any

    def accept(self, visitor: "ExprVisitor[T]") -> T:
        return visitor.visit_literal(self)


@dataclass
class Variable:
    name: Token

    def accept(self, visitor: "ExprVisitor[T]") -> T:
        return visitor.visit_variable(self)


@dataclass
class Unary:
    operator: Token
    right: Expr

    def accept(self, visitor: "ExprVisitor[T]") -> T:
        return visitor.visit_unary(self)


@dataclass
class Call:
    callee: Expr
    token: Token
    arguments: List[Expr]

    def accept(self, visitor: "ExprVisitor[T]") -> T:
        return visitor.visit_call(self)


@dataclass
class Assign:
    name: Token
    value: Expr

    def accept(self, visitor: "ExprVisitor[T]") -> T:
        return visitor.visit_assign(self)


@dataclass
class Set:
    object: Expr
    name: Token
    value: Expr

    def accept(self, visitor: "ExprVisitor[T]") -> T:
        return visitor.visit_set(self)


@dataclass
class Get:
    object: Expr
    name: Token

    def accept(self, visitor: "ExprVisitor[T]") -> T:
        return visitor.visit_get(self)


@dataclass
class This:
    keyword: Token

    def accept(self, visitor: "ExprVisitor[T]") -> T:
        return visitor.visit_this(self)


@dataclass
class Super:
    keyword: Token
    method: Token

    def accept(self, visitor: "ExprVisitor[T]") -> T:
        return visitor.visit_super(self)


class ExprVisitor(abc.ABC, Generic[T]):
    @abc.abstractmethod
    def visit_binary(self, expr: Binary) -> T:
        pass

    @abc.abstractmethod
    def visit_grouping(self, expr: Grouping) -> T:
        pass

    @abc.abstractmethod
    def visit_literal(self, expr: Literal) -> T:
        pass

    @abc.abstractmethod
    def visit_unary(self, expr: Unary) -> T:
        pass

    @abc.abstractmethod
    def visit_call(self, expr: Call) -> T:
        pass

    @abc.abstractmethod
    def visit_variable(self, expr: Variable) -> T:
        pass

    @abc.abstractmethod
    def visit_assign(self, expr: Assign) -> T:
        pass

    @abc.abstractmethod
    def visit_logical(self, expr: Logical) -> T:
        pass

    @abc.abstractmethod
    def visit_set(self, expr: Set) -> T:
        pass

    @abc.abstractmethod
    def visit_get(self, expr: Get) -> T:
        pass

    @abc.abstractmethod
    def visit_this(self, expr: This) -> T:
        pass

    @abc.abstractmethod
    def visit_super(self, expr: Super) -> T:
        pass