from errors import InterpretError
from evals import *
from Token import Token
from tokenTypes import tokenTypes
from typing import Any, Dict, cast, Optional

class Environment:
    def __init__(self, enclosing: Optional["Environment"] = None):
        self.values: Dict[str, Any] = {}
        self.enclosing = enclosing

    def __getitem__(self, name: Token):
        if name.lexeme in self.values:
            return self.values[name.lexeme]

        if self.enclosing is not None:
            return self.enclosing[name]

        raise InterpretError(name, f"Undefined variable: '{name.lexeme}'")

    def __setitem__(self, name: str, value: Any):
        self.values[name] = value

    def assign(self, name: Token, value: Any):
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return

        if self.enclosing is not None:
            self.enclosing.assign(name, value)
            return

        raise InterpretError(name, f"Undefined variable '{name.lexeme}'")

    def ancestor(self, distance: int) -> "Environment":
        env = self

        for _ in range(distance):
            # Of course is not None
            env = cast(Environment, env.enclosing)

        return env

    def get_at(self, distance: int, name: str) -> Any:
        return self.ancestor(distance).values[name]

    def assign_at(self, distance: int, name: str, value: Any):
        self.ancestor(distance).values[name] = value