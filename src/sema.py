from typing import Dict, List, Optional, Any
from ast_nodes import *

class SemanticError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(f"Erro semântico: {message}")

class Symbol:
    def __init__(self, name: str, sym_type: str, value: Any = None, is_function: bool = False):
        self.name = name
        self.type = sym_type
        self.value = value
        self.is_function = is_function
        self.params = []  # Para funções
        self.return_type = None  # Para funções

class SymbolTable:
    def __init__(self, parent: Optional['SymbolTable'] = None):
        self.symbols: Dict[str, Symbol] = {}
        self.parent = parent
        self.children: List['SymbolTable'] = []
        if parent:
            parent.children.append(self)
    
    def define(self, symbol: Symbol):
        if symbol.name in self.symbols:
            raise SemanticError(f"Variável '{symbol.name}' já declarada neste escopo")
        self.symbols[symbol.name] = symbol
    
    def resolve(self, name: str) -> Optional[Symbol]:
        if name in self.symbols:
            return self.symbols[name]
        if self.parent:
            return self.parent.resolve(name)
        return None
    
    def __str__(self):
        return self._to_string(0)
    
    def _to_string(self, level: int) -> str:
        indent = "  " * level
        result = f"{indent}Escopo (nível {level}):\n"
        for name, symbol in self.symbols.items():
            if symbol.is_function:
                params_str = ", ".join([f"{p[0]}: {p[1]}" for p in symbol.params])
                result += f"{indent}  {name}: função({params_str}) -> {symbol.return_type}\n"
            else:
                result += f"{indent}  {name}: {symbol.type}\n"
        
        for child in self.children:
            result += child._to_string(level + 1)
        
        return result

class SemanticAnalyzer(ASTVisitor):
    def __init__(self):
        self.global_table = SymbolTable()
        self.current_table = self.global_table
        self.current_function = None
        self.errors = []
    
    def push_scope(self):
        self.current_table = SymbolTable(self.current_table)
    
    def pop_scope(self):
        if self.current_table.parent:
            self.current_table = self.current_table.parent
    
    def error(self, message: str):
        self.errors.append(message)
    
    def get_type(self, node: ASTNode) -> str:
        if isinstance(node, Literal):
            return node.type
        elif isinstance(node, Variable):
            symbol = self.current_table.resolve(node.name)
            if not symbol:
                self.error(f"Variável '{node.name}' não declarada")
                return 'error'
            return symbol.type
        elif isinstance(node, BinaryOp):
            left_type = self.get_type(node.left)
            right_type = self.get_type(node.right)
            
            # Operadores aritméticos
            if node.operator in ['+', '-', '*', '/', '%']:
                if left_type in ['int', 'float'] and right_type in ['int', 'float']:
                    if left_type == 'float' or right_type == 'float':
                        return 'float'
                    return 'int'
                elif left_type == 'string' and right_type == 'string' and node.operator == '+':
                    return 'string'
                else:
                    self.error(f"Operador '{node.operator}' não suportado para tipos {left_type} e {right_type}")
                    return 'error'
            
            # Operadores relacionais
            elif node.operator in ['<', '<=', '>', '>=']:
                if left_type in ['int', 'float'] and right_type in ['int', 'float']:
                    return 'bool'
                else:
                    self.error(f"Operador '{node.operator}' requer tipos numéricos, recebeu {left_type} e {right_type}")
                    return 'error'
            
            # Operadores de igualdade
            elif node.operator in ['==', '!=']:
                if left_type == right_type or (left_type in ['int', 'float'] and right_type in ['int', 'float']):
                    return 'bool'
                else:
                    self.error(f"Não é possível comparar tipos {left_type} e {right_type}")
                    return 'error'
            
            # Operadores lógicos
            elif node.operator in ['and', 'or']:
                if left_type == 'bool' and right_type == 'bool':
                    return 'bool'
                else:
                    self.error(f"Operador '{node.operator}' requer tipos booleanos")
                    return 'error'
        
        elif isinstance(node, UnaryOp):
            operand_type = self.get_type(node.operand)
            if node.operator == 'not':
                if operand_type == 'bool':
                    return 'bool'
                else:
                    self.error(f"Operador 'not' requer tipo booleano")
                    return 'error'
            elif node.operator == '-':
                if operand_type in ['int', 'float']:
                    return operand_type
                else:
                    self.error(f"Operador '-' requer tipo numérico")
                    return 'error'
        
        elif isinstance(node, ArrayAccess):
            array_symbol = None
            if isinstance(node.array, Variable):
                array_symbol = self.current_table.resolve(node.array.name)
            
            if array_symbol:
                # Extrair tipo base do array
                array_type = array_symbol.type
                if array_type.startswith('array<') and array_type.endswith('>'):
                    return array_type[6:-1]  # Retorna tipo do elemento
            
            return 'error'
        
        elif isinstance(node, FunctionCall):
            symbol = self.current_table.resolve(node.name)
            if symbol and symbol.is_function:
                return symbol.return_type or 'void'
            return 'error'
        
        elif isinstance(node, InputExpression):
            return 'string'
        
        return 'error'
    
    def visit_program(self, node: Program):
        for stmt in node.statements:
            stmt.accept(self)
    
    def visit_var_declaration(self, node: VarDeclaration):
        var_type = str(node.type)
        
        if node.initializer:
            init_type = self.get_type(node.initializer)
            
            # Verificar compatibilidade de tipos
            if node.type.is_array:
                if isinstance(node.initializer, ArrayLiteral):
                    # Verificar tipo dos elementos
                    for elem in node.initializer.elements:
                        elem_type = self.get_type(elem)
                        if elem_type != node.type.name and not (node.type.name == 'float' and elem_type == 'int'):
                            self.error(f"Elemento do array incompatível: esperado {node.type.name}, encontrado {elem_type}")
                else:
                    self.error(f"Inicializador de array deve ser um literal de array")
            else:
                if init_type != var_type and not (var_type == 'float' and init_type == 'int'):
                    self.error(f"Tipo incompatível na declaração de '{node.name}': esperado {var_type}, encontrado {init_type}")
        
        symbol = Symbol(node.name, var_type)
        self.current_table.define(symbol)
    
    def visit_function_declaration(self, node: FunctionDeclaration):
        # Criar símbolo da função
        func_type = str(node.return_type) if node.return_type else 'void'
        symbol = Symbol(node.name, func_type, is_function=True)
        symbol.params = [(str(p[0]), p[1]) for p in node.params]
        symbol.return_type = func_type
        
        self.current_table.define(symbol)
        
        # Novo escopo para o corpo da função
        self.push_scope()
        old_function = self.current_function
        self.current_function = node
        
        # Adicionar parâmetros ao escopo
        for param_type, param_name in node.params:
            param_symbol = Symbol(param_name, str(param_type))
            self.current_table.define(param_symbol)
        
        # Analisar corpo
        for stmt in node.body:
            stmt.accept(self)
        
        self.current_function = old_function
        self.pop_scope()
    
    def visit_if_statement(self, node: IfStatement):
        cond_type = self.get_type(node.condition)
        if cond_type != 'bool':
            self.error(f"Condição do 'if' deve ser booleana, encontrado {cond_type}")
        
        self.push_scope()
        for stmt in node.then_branch:
            stmt.accept(self)
        self.pop_scope()
        
        if node.else_branch:
            self.push_scope()
            for stmt in node.else_branch:
                stmt.accept(self)
            self.pop_scope()
    
    def visit_while_statement(self, node: WhileStatement):
        cond_type = self.get_type(node.condition)
        if cond_type != 'bool':
            self.error(f"Condição do 'while' deve ser booleana, encontrado {cond_type}")
        
        self.push_scope()
        for stmt in node.body:
            stmt.accept(self)
        self.pop_scope()
    
    def visit_for_statement(self, node: ForStatement):
        self.push_scope()
        
        if node.init:
            node.init.accept(self)
        
        if node.condition:
            cond_type = self.get_type(node.condition)
            if cond_type != 'bool':
                self.error(f"Condição do 'for' deve ser booleana, encontrado {cond_type}")
        
        for stmt in node.body:
            stmt.accept(self)
        
        self.pop_scope()
    
    def visit_return_statement(self, node: ReturnStatement):
        if not self.current_function:
            self.error("'return' fora de uma função")
            return
        
        expected_type = str(self.current_function.return_type) if self.current_function.return_type else 'void'
        
        if node.expression:
            return_type = self.get_type(node.expression)
            if expected_type == 'void':
                self.error("Função void não deve retornar valor")
            elif return_type != expected_type and not (expected_type == 'float' and return_type == 'int'):
                self.error(f"Tipo de retorno incompatível: esperado {expected_type}, encontrado {return_type}")
        else:
            if expected_type != 'void':
                self.error(f"Função deve retornar {expected_type}")
    
    def visit_assignment(self, node: Assignment):
        if isinstance(node.target, Variable):
            symbol = self.current_table.resolve(node.target.name)
            if not symbol:
                self.error(f"Variável '{node.target.name}' não declarada")
                return
            
            target_type = symbol.type
            value_type = self.get_type(node.value)
            
            if target_type != value_type and not (target_type == 'float' and value_type == 'int'):
                self.error(f"Tipo incompatível na atribuição: {target_type} = {value_type}")
        
        elif isinstance(node.target, ArrayAccess):
            # Validar acesso ao array
            node.target.accept(self)
    
    def visit_array_access(self, node: ArrayAccess):
        index_type = self.get_type(node.index)
        if index_type != 'int':
            self.error(f"Índice do array deve ser inteiro, encontrado {index_type}")
    
    def visit_function_call(self, node: FunctionCall):
        symbol = self.current_table.resolve(node.name)
        if not symbol:
            self.error(f"Função '{node.name}' não declarada")
            return
        
        if not symbol.is_function:
            self.error(f"'{node.name}' não é uma função")
            return
        
        if len(node.arguments) != len(symbol.params):
            self.error(f"Função '{node.name}' espera {len(symbol.params)} argumentos, recebeu {len(node.arguments)}")
            return
        
        for i, (arg, (param_type, _)) in enumerate(zip(node.arguments, symbol.params)):
            arg_type = self.get_type(arg)
            if arg_type != param_type and not (param_type == 'float' and arg_type == 'int'):
                self.error(f"Argumento {i+1} de '{node.name}': esperado {param_type}, encontrado {arg_type}")
    
    def visit_expression_statement(self, node: ExpressionStatement):
        node.expression.accept(self)
    
    def visit_print_statement(self, node: PrintStatement):
        node.expression.accept(self)
    
    def visit_block(self, node: Block):
        self.push_scope()
        for stmt in node.statements:
            stmt.accept(self)
        self.pop_scope()
    
    def visit_binary_op(self, node: BinaryOp):
        node.left.accept(self)
        node.right.accept(self)
    
    def visit_unary_op(self, node: UnaryOp):
        node.operand.accept(self)
    
    def visit_variable(self, node: Variable):
        symbol = self.current_table.resolve(node.name)
        if not symbol:
            self.error(f"Variável '{node.name}' não declarada")
    
    def visit_literal(self, node: Literal):
        pass
    
    def visit_array_literal(self, node: ArrayLiteral):
        for elem in node.elements:
            elem.accept(self)
    
    def visit_input_expression(self, node: InputExpression):
        if node.prompt:
            node.prompt.accept(self)
    
    def visit_type(self, node: Type):
        pass
    
    def analyze(self, program: Program) -> bool:
        program.accept(self)
        return len(self.errors) == 0