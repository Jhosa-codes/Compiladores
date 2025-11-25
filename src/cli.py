import sys
import argparse
from pathlib import Path

# Importar módulos do compilador
from lexer import Lexer, LexerError
from parser import Parser, ParserError
from ast_nodes import Program
from sema import SemanticAnalyzer, SemanticError
from interp import Interpreter
from codegen import CodeGenerator
from pretty import ASTPrinter

class CompilerCLI:
    def __init__(self):
        self.source_code = ""
        self.tokens = []
        self.ast = None
        self.semantic_analyzer = None
        self.errors = []
    
    def read_file(self, filepath: str) -> bool:
        """Lê o arquivo de código fonte"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                self.source_code = f.read()
            print(f"✓ Arquivo '{filepath}' carregado com sucesso")
            return True
        except FileNotFoundError:
            print(f"✗ Erro: Arquivo '{filepath}' não encontrado")
            return False
        except Exception as e:
            print(f"✗ Erro ao ler arquivo: {e}")
            return False
    
    def lex(self) -> bool:
        """Executa análise léxica"""
        print("\n" + "="*60)
        print("ANÁLISE LÉXICA")
        print("="*60)
        
        try:
            lexer = Lexer(self.source_code)
            self.tokens = lexer.tokenize()
            print(f"✓ Análise léxica concluída com sucesso")
            print(f"  Total de tokens: {len(self.tokens)}")
            return True
        except LexerError as e:
            print(f"✗ {e}")
            self.errors.append(str(e))
            return False
    
    def parse(self) -> bool:
        """Executa análise sintática"""
        print("\n" + "="*60)
        print("ANÁLISE SINTÁTICA")
        print("="*60)
        
        try:
            parser = Parser(self.tokens)
            self.ast = parser.parse()
            print(f"✓ Análise sintática concluída com sucesso")
            return True
        except ParserError as e:
            print(f"✗ {e}")
            self.errors.append(str(e))
            return False
    
    def show_ast(self):
        """Exibe a AST em formato de árvore"""
        if not self.ast:
            print("✗ AST não disponível")
            return
        
        print("\n" + "="*60)
        print("ÁRVORE SINTÁTICA ABSTRATA (AST)")
        print("="*60)
        
        printer = ASTPrinter()
        tree = printer.print_tree(self.ast)
        print(tree)
    
    def analyze(self) -> bool:
        """Executa análise semântica"""
        if not self.ast:
            print("✗ AST não disponível para análise semântica")
            return False
        
        print("\n" + "="*60)
        print("ANÁLISE SEMÂNTICA")
        print("="*60)
        
        self.semantic_analyzer = SemanticAnalyzer()
        success = self.semantic_analyzer.analyze(self.ast)
        
        if success:
            print(f"✓ Análise semântica concluída com sucesso")
            return True
        else:
            print(f"✗ Erros encontrados na análise semântica:")
            for error in self.semantic_analyzer.errors:
                print(f"  - {error}")
            return False
    
    def show_symbols(self):
        """Exibe a tabela de símbolos"""
        if not self.semantic_analyzer:
            print("✗ Tabela de símbolos não disponível")
            return
        
        print("\n" + "="*60)
        print("TABELA DE SÍMBOLOS")
        print("="*60)
        print(self.semantic_analyzer.global_table)
    
    def execute(self):
        """Executa o código interpretado"""
        if not self.ast:
            print("✗ AST não disponível para execução")
            return
        
        print("\n" + "="*60)
        print("EXECUÇÃO")
        print("="*60)
        
        interpreter = Interpreter()
        output = interpreter.interpret(self.ast)
        
        if output:
            print("\nSaída do programa:")
            print("-" * 40)
            print(output)
            print("-" * 40)
        else:
            print("✓ Programa executado sem saída")
    
    def generate_code(self, output_file: str = None):
        """Gera código Python equivalente"""
        if not self.ast:
            print("✗ AST não disponível para geração de código")
            return
        
        print("\n" + "="*60)
        print("GERAÇÃO DE CÓDIGO")
        print("="*60)
        
        codegen = CodeGenerator()
        generated_code = codegen.generate(self.ast)
        
        if output_file:
            try:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(generated_code)
                print(f"✓ Código gerado salvo em '{output_file}'")
            except Exception as e:
                print(f"✗ Erro ao salvar código gerado: {e}")
        else:
            print("\nCódigo Python gerado:")
            print("-" * 40)
            print(generated_code)
            print("-" * 40)
    
    def compile_full(self, filepath: str, output: str = None, execute: bool = False):
        """Pipeline completo de compilação"""
        print("="*60)
        print("COMPILADOR MINI-LANG")
        print("="*60)
        
        # 1. Ler arquivo
        if not self.read_file(filepath):
            return False
        
        # 2. Análise léxica
        if not self.lex():
            return False
        
        # 3. Análise sintática
        if not self.parse():
            return False
        
        # 4. Mostrar AST (opcional)
        self.show_ast()
        
        # 5. Análise semântica
        if not self.analyze():
            return False
        
        # 6. Mostrar tabela de símbolos
        self.show_symbols()
        
        # 7. Geração de código
        if output:
            self.generate_code(output)
        
        # 8. Execução (opcional)
        if execute:
            self.execute()
        
        print("\n" + "="*60)
        print("COMPILAÇÃO CONCLUÍDA COM SUCESSO")
        print("="*60)
        
        return True

def main():
    parser = argparse.ArgumentParser(
        description='Compilador para a linguagem Mini-Lang',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  %(prog)s programa.min                    # Compila e analisa
  %(prog)s programa.min -o saida.py        # Gera código Python
  %(prog)s programa.min -r                 # Compila e executa
  %(prog)s programa.min -o saida.py -r     # Gera código e executa
  %(prog)s programa.min --ast              # Mostra apenas a AST
  %(prog)s programa.min --tokens           # Mostra apenas os tokens
        """
    )
    
    parser.add_argument('input', help='Arquivo de entrada (.min)')
    parser.add_argument('-o', '--output', help='Arquivo de saída para código gerado')
    parser.add_argument('-r', '--run', action='store_true', help='Executar o programa')
    parser.add_argument('--ast', action='store_true', help='Mostrar apenas a AST')
    parser.add_argument('--tokens', action='store_true', help='Mostrar apenas os tokens')
    parser.add_argument('--symbols', action='store_true', help='Mostrar apenas a tabela de símbolos')
    
    args = parser.parse_args()
    
    cli = CompilerCLI()
    
    # Modos especiais
    if args.tokens:
        if cli.read_file(args.input) and cli.lex():
            print("\nTokens:")
            for token in cli.tokens:
                print(f"  {token}")
        return
    
    if args.ast:
        if cli.read_file(args.input) and cli.lex() and cli.parse():
            cli.show_ast()
        return
    
    if args.symbols:
        if cli.read_file(args.input) and cli.lex() and cli.parse() and cli.analyze():
            cli.show_symbols()
        return
    
    # Modo completo
    cli.compile_full(args.input, args.output, args.run)

if __name__ == '__main__':
    main()