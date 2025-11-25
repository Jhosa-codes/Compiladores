# Compilador Mini-Lang

Um compilador completo e organizado para a linguagem Mini-Lang, desenvolvido em Python.

## Visão Geral

Este é um compilador educacional completo para a linguagem Mini-Lang, desenvolvido como trabalho acadêmico do curso de Compiladores. O projeto implementa todas as fases de compilação: análise léxica, sintática, semântica, geração de código e interpretação.

### Funcionalidades Principais

- **Análise Léxica** com detecção de erros e localização (linha/coluna)
- **Análise Sintática** com mensagens de erro detalhadas
- **Árvore Sintática Abstrata (AST)** com visualização em árvore ASCII
- **Análise Semântica** com verificação de tipos e escopos
- **Tabela de Símbolos** hierárquica com exibição formatada
- **Interpretador** funcional com curto-circuito e bounds check
- **Gerador de Código** Python equivalente
- **Interface CLI** completa e amigável

## Requisitos

### Requisitos Mínimos
- Python 3.14


##  Instalação

### 1. Clone ou Baixe o Projeto

```bash
# Opção 1: Via Git
git clone <url-do-repositorio>
cd mini-lang-compiler

# Opção 2: Download ZIP
# Extraia o arquivo ZIP e navegue até a pasta
cd mini-lang-compiler
```

### 2. Verifique a Instalação do Python

```bash
# Verificar versão do Python
python --version
# ou
python3 --version

# Deve mostrar Python 3.14 ou superior
```

### 3. Pronto para Usar!

Não há dependências externas para instalar. O projeto usa apenas bibliotecas padrão do Python.

##  Uso

### Comandos Básicos

#### 1. Compilação Completa (Padrão)

Executa todas as fases: análise léxica, sintática, semântica e exibe AST e tabela de símbolos.

```bash
python src/cli.py tests/ok_hello.min
```

**Saída esperada:**
```
============================================================
COMPILADOR MINI-LANG
============================================================
✓ Arquivo 'tests/ok_hello.min' carregado com sucesso

============================================================
ANÁLISE LÉXICA
============================================================
✓ Análise léxica concluída com sucesso
  Total de tokens: 5

============================================================
ANÁLISE SINTÁTICA
============================================================
✓ Análise sintática concluída com sucesso

============================================================
ÁRVORE SINTÁTICA ABSTRATA (AST)
============================================================
Program
├── PrintStatement
│   ├── Literal: Hello, World! (string)

============================================================
ANÁLISE SEMÂNTICA
============================================================
✓ Análise semântica concluída com sucesso

============================================================
TABELA DE SÍMBOLOS
============================================================
Escopo (nível 0):

============================================================
COMPILAÇÃO CONCLUÍDA COM SUCESSO
============================================================
```

#### 2. Compilar e Executar

```bash
python src/cli.py tests/ok_factorial.min -r
```

Adiciona a execução do programa ao final da compilação.

**Exemplo de saída:**
```
...
============================================================
EXECUÇÃO
============================================================

Saída do programa:
----------------------------------------
Fatorial de 5:
120
----------------------------------------

============================================================
COMPILAÇÃO CONCLUÍDA COM SUCESSO
============================================================
```

#### 3. Gerar Código Python

```bash
python src/cli.py tests/ok_factorial.min -o output.py
```

Gera arquivo `output.py` com código Python equivalente.

#### 4. Compilar, Gerar e Executar

```bash
python src/cli.py tests/ok_factorial.min -o output.py -r
```

Gera o código Python e executa o programa original.

### Comandos Específicos

#### Visualizar Apenas a AST

```bash
python src/cli.py tests/ok_factorial.min --ast
```

Mostra apenas a árvore sintática sem outras informações.

#### Visualizar Apenas os Tokens

```bash
python src/cli.py tests/ok_hello.min --tokens
```

Mostra todos os tokens gerados pela análise léxica.

**Exemplo de saída:**
```
Tokens:
  Token(PRINT, 'print', 1:1)
  Token(LPAREN, '(', 1:6)
  Token(STRING_LITERAL, 'Hello, World!', 1:7)
  Token(RPAREN, ')', 1:22)
  Token(SEMICOLON, ';', 1:23)
  Token(EOF, None, 1:24)
```

#### Visualizar Apenas a Tabela de Símbolos

```bash
python src/cli.py tests/ok_functions.min --symbols
```

Mostra a tabela de símbolos com variáveis e funções declaradas.

#### Ver Todas as Opções

```bash
python src/cli.py -h
```

**Saída:**
```
usage: cli.py [-h] [-o OUTPUT] [-r] [--ast] [--tokens] [--symbols] input

Compilador para a linguagem Mini-Lang

positional arguments:
  input                 Arquivo de entrada (.min)

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Arquivo de saída para código gerado
  -r, --run             Executar o programa
  --ast                 Mostrar apenas a AST
  --tokens              Mostrar apenas os tokens
  --symbols             Mostrar apenas a tabela de símbolos

Exemplos de uso:
  cli.py programa.min                    # Compila e analisa
  cli.py programa.min -o saida.py        # Gera código Python
  cli.py programa.min -r                 # Compila e executa
  cli.py programa.min -o saida.py -r     # Gera código e executa
  cli.py programa.min --ast              # Mostra apenas a AST
  cli.py programa.min --tokens           # Mostra apenas os tokens
```

## Estrutura do Projeto

```
├── src/                      # Código-fonte do compilador
│   ├── __init__.py          # Marca o diretório como pacote Python
│   ├── lexer.py             # Analisador léxico (tokenização)
│   ├── parser.py            # Analisador sintático (parsing)
│   ├── ast_nodes.py         # Definição dos nós da AST
│   ├── sema.py              # Análise semântica (tipos e escopos)
│   ├── interp.py            # Interpretador
│   ├── codegen.py           # Gerador de código Python
│   ├── cli.py               # Interface de linha de comando
│   └── pretty.py            # Visualizador de AST em árvore ASCII
│
├── grammar/                  # Gramática da linguagem
│   └── mini_lang.ebnf       # Especificação EBNF completa
│
├── tests/                    # Casos de teste
│   ├── ok_hello.min         # Hello World básico
│   ├── ok_variables.min     # Teste de variáveis e tipos
│   ├── ok_if_else.min       # Estruturas condicionais
│   ├── ok_while.min         # Laços while
│   ├── ok_for.min           # Laços for
│   ├── ok_functions.min     # Declaração e chamada de funções
│   ├── ok_arrays.min        # Operações com arrays
│   ├── ok_factorial.min     # Fatorial recursivo
│   ├── ok_fibonacci.min     # Sequência de Fibonacci
│   ├── ok_bubble_sort.min   # Ordenação bubble sort
│   ├── ok_complex.min       # Números primos (mais complexo)
│   ├── ok_short_circuit.min # Teste de curto-circuito
│   ├── err_lexical.min      # Erro léxico (caractere inválido)
│   ├── err_syntax.min       # Erro sintático (falta ;)
│   ├── err_undeclared.min   # Erro: variável não declarada
│   ├── err_type_mismatch.min # Erro: tipos incompatíveis
│   ├── err_function_args.min # Erro: argumentos incorretos
│   ├── err_return_type.min  # Erro: tipo de retorno incompatível
│   └── err_array_bounds.min # Erro: acesso fora dos limites
│
└── README.md               
```

## Características da Linguagem

### Tipos de Dados

- `int` - Números inteiros (ex: `42`, `-10`)
- `float` - Números de ponto flutuante (ex: `3.14`, `-0.5`)
- `bool` - Booleanos (`true`, `false`)
- `string` - Strings (ex: `"Hello"`, `'World'`)
- `array<T>` - Arrays tipados (ex: `int[5]`, `array<float>[10]`)

### Estruturas de Controle

```javascript
// Condicional
if (x > 5) {
    print("x é maior que 5");
} else {
    print("x é menor ou igual a 5");
}

// Laço while
while (x > 0) {
    print(x);
    x = x - 1;
}

// Laço for
for (int i = 0; i < 10; i = i + 1) {
    print(i);
}
```

### Funções

```javascript
// Função com retorno
function soma(int a, int b): int {
    return a + b;
}

// Função void
function imprimirMsg(string msg) {
    print(msg);
}

// Chamada de função
int resultado = soma(10, 20);
imprimirMsg("Olá!");
```

### Arrays

```javascript
// Declaração e inicialização
int[5] numeros = [1, 2, 3, 4, 5];

// Acesso
print(numeros[0]);  // 1

// Atribuição
numeros[2] = 10;

// Iteração
for (int i = 0; i < 5; i = i + 1) {
    print(numeros[i]);
}
```

### Operadores

**Aritméticos:** `+`, `-`, `*`, `/`, `%`

**Relacionais:** `<`, `<=`, `>`, `>=`, `==`, `!=`

**Lógicos:** `and`, `or`, `not`

**Atribuição:** `=`

### Entrada e Saída

```javascript
// Saída
print("Hello, World!");
print(42);

// Entrada (simulada no interpretador)
string nome = input("Digite seu nome: ");
```

### Comentários

```javascript
# Este é um comentário de linha
int x = 10;  # Comentário no final da linha
```

## Exemplos

### Exemplo 1: Hello World

```javascript
# Arquivo: tests/ok_hello.min
print("Hello, World!");
```

**Executar:**
```bash
python src/cli.py tests/ok_hello.min -r
```

**Saída:**
```
Hello, World!
```

### Exemplo 2: Fatorial Recursivo

```javascript
# Arquivo: tests/ok_factorial.min
function fatorial(int n): int {
    if (n <= 1) {
        return 1;
    }
    return n * fatorial(n - 1);
}

int resultado = fatorial(5);
print("Fatorial de 5:");
print(resultado);
```

**Executar:**
```bash
python src/cli.py tests/ok_factorial.min -r
```

**Saída:**
```
Fatorial de 5:
120
```

### Exemplo 3: Arrays e Loops

```javascript
# Arquivo: tests/ok_arrays.min
int[5] numeros = [1, 2, 3, 4, 5];

print(numeros[0]);
print(numeros[2]);

numeros[2] = 10;
print(numeros[2]);

int i = 0;
while (i < 5) {
    print(numeros[i]);
    i = i + 1;
}
```

**Executar:**
```bash
python src/cli.py tests/ok_arrays.min -r
```

**Saída:**
```
1
3
10
1
2
10
4
5
```

### Exemplo 4: Fibonacci

```javascript
# Arquivo: tests/ok_fibonacci.min
function fibonacci(int n): int {
    if (n <= 1) {
        return n;
    }
    return fibonacci(n - 1) + fibonacci(n - 2);
}

for (int i = 0; i < 10; i = i + 1) {
    print(fibonacci(i));
}
```

**Executar:**
```bash
python src/cli.py tests/ok_fibonacci.min -r
```

**Saída:**
```
0
1
1
2
3
5
8
13
21
34
```

## Arquitetura

### Pipeline de Compilação

```
Código Fonte (.min)
      ↓
[1. LEXER] - Tokenização
      ↓
   Tokens
      ↓
[2. PARSER] - Análise Sintática
      ↓
    AST
      ↓
[3. SEMANTIC ANALYZER] - Análise Semântica
      ↓
AST + Tabela de Símbolos
      ↓
[4. CODE GENERATOR] - Geração de Código Python
      ↓
Código Python
      ↓
[5. INTERPRETER] - Execução (Opcional)
      ↓
   Saída
```

### Descrição dos Módulos

#### 1. Lexer (lexer.py)
- Tokeniza o código-fonte
- Identifica palavras-chave, identificadores, literais, operadores
- Reporta erros léxicos com linha e coluna

#### 2. Parser (parser.py)
- Análise sintática descendente recursiva
- Constrói a AST
- Reporta erros sintáticos com contexto

#### 3. AST Nodes (ast_nodes.py)
- Define todos os nós da árvore sintática
- Implementa padrão Visitor
- Classes para statements, expressions, declarations

#### 4. Semantic Analyzer (sema.py)
- Verifica tipos e compatibilidade
- Gerencia tabela de símbolos com escopos
- Valida declarações, chamadas de função, operações

#### 5. Interpreter (interp.py)
- Executa o código diretamente da AST
- Implementa curto-circuito para operadores lógicos
- Bounds check para arrays

#### 6. Code Generator (codegen.py)
- Gera código Python equivalente
- Traduz AST para código Python válido

#### 7. Pretty Printer (pretty.py)
- Visualiza AST em formato de árvore ASCII
- Hierarquia visual clara

#### 8. CLI (cli.py)
- Interface de linha de comando
- Orquestra todas as fases
- Opções configuráveis

### Padrão Visitor

Todos os módulos de análise usam o padrão Visitor para percorrer a AST:

```python
class ASTVisitor(ABC):
    def visit_program(self, node: Program): pass
    def visit_var_declaration(self, node: VarDeclaration): pass
    def visit_function_declaration(self, node: FunctionDeclaration): pass
    # ... outros métodos visit
```

## Testes

### Executar Todos os Testes Válidos

```bash
# Windows (CMD)
for %f in (tests\ok_*.min) do python src\cli.py %f -r

```

### Executar Testes de Erro

Os arquivos `err_*.min` devem gerar erros específicos:

```bash
# Erro léxico
python src/cli.py tests/err_lexical.min

# Erro sintático
python src/cli.py tests/err_syntax.min

# Erro semântico - variável não declarada
python src/cli.py tests/err_undeclared.min

# Erro semântico - tipos incompatíveis
python src/cli.py tests/err_type_mismatch.min

# Erro semântico - argumentos de função
python src/cli.py tests/err_function_args.min

# Erro semântico - tipo de retorno
python src/cli.py tests/err_return_type.min

# Erro de execução - array bounds
python src/cli.py tests/err_array_bounds.min -r
```

### Exemplos de Saídas de Erro

**Erro Léxico:**
```
✗ Erro léxico na linha 3, coluna 5: Caractere inesperado: '@'
  --> Token(IDENTIFIER, 'y', 3:3)
```

**Erro Sintático:**
```
✗ Erro sintático na linha 2, coluna 1: Esperado SEMICOLON, encontrado PRINT
  --> Token(PRINT, 'print', 2:1)
```

**Erro Semântico:**
```
✗ Erros encontrados na análise semântica:
  - Variável 'y' não declarada
```

## Pontos Extras Implementados

### 1. Erros Amigáveis com Linha/Coluna

Todos os erros (léxicos, sintáticos e semânticos) reportam:
- Linha exata do erro
- Coluna exata do erro
- Contexto (token atual)
- Mensagem descritiva

**Implementação:**
- `LexerError`: linha e coluna do caractere problemático
- `ParserError`: linha e coluna do token inesperado
- `SemanticError`: mensagens claras sobre o problema

### 2. Exibição Amigável da AST

A AST é exibida em formato de árvore ASCII visual com símbolos de desenho:

```
Program
├── VarDeclaration: int x
│   ├── Initializer:
│   │   ├── Literal: 10 (int)
├── PrintStatement
│   ├── Variable: x
```

### 3. Documentação Detalhada

- README completo com instruções de instalação
- Exemplos práticos de todos os comandos
- Documentação da gramática (mini_lang.ebnf)
- Explicação da arquitetura
- Comentários no código-fonte

### 4. Testes Abrangentes

- **11 casos válidos** cobrindo todas as funcionalidades
- **7 casos de erro** testando detecção de erros
- Testes simples a complexos (bubble sort, números primos)

### 5. CLI Completa e Versátil

Múltiplas opções de uso:
- Compilação completa padrão
- Visualização seletiva (--tokens, --ast, --symbols)
- Execução opcional (-r)
- Geração de código (-o)
- Ajuda integrada (-h)

### 6. Organização Excepcional

- Código modular em arquivos separados
- Separação clara de responsabilidades
- Padrão de projeto (Visitor) bem implementado
- Fácil manutenção e extensão
- Estrutura de pastas organizada

## Funcionalidades Especiais

### Curto-circuito

Os operadores lógicos `and` e `or` implementam avaliação de curto-circuito:

```javascript
bool a = false;
bool b = true;

// O segundo operando não é avaliado se o primeiro for false
if (a and funcaoCaraDeExecutar()) {
    print("Não será executado");
}

// O segundo operando não é avaliado se o primeiro for true
if (b or funcaoCaraDeExecutar()) {
    print("Será executado, mas funcao não será chamada");
}
```

**Teste:**
```bash
python src/cli.py tests/ok_short_circuit.min -r
```

### Verificação de Limites de Array (Bounds Check)

Arrays são verificados em tempo de execução:

```javascript
int[3] arr = [1, 2, 3];
print(arr[0]);  // OK: índice 0 válido
print(arr[5]);  // ERRO: Índice 5 fora dos limites do array (tamanho 3)
```

**Teste:**
```bash
python src/cli.py tests/err_array_bounds.min -r
```

### Conversão Implícita int → float

```javascript
float x = 10;      // OK: int é convertido para float automaticamente
float y = 3 + 2.5; // OK: int 3 é convertido para float, resultado é 5.5
```

### Escopo Léxico

Variáveis respeitam escopo léxico (estático):

```javascript
int x = 10;

function teste() {
    int x = 20;  // Variável local, não afeta x global
    print(x);    // Imprime 20
}

teste();
print(x);        // Imprime 10
```

## Gramática

A gramática completa em EBNF está disponível em `grammar/mini_lang.ebnf`.

### Precedência de Operadores (do mais baixo para o mais alto)

1. Atribuição: `=` (associativa à direita)
2. OR lógico: `or`
3. AND lógico: `and`
4. Igualdade: `==`, `!=`
5. Relacional: `<`, `<=`, `>`, `>=`
6. Aditivos: `+`, `-`
7. Multiplicativos: `*`, `/`, `%`
8. Unários: `not`, `-` (negação)
9. Pós-fixos: `[]` (array access), `()` (function call)

### Tipos

```ebnf
type = basic_type [ array_suffix ]
     | "array" "<" type ">" [ array_suffix ] ;

basic_type = "int" | "float" | "bool" | "string" ;

array_suffix = "[" [ INT_LITERAL ] "]" ;
```

### Expressões

```ebnf
expression = assignment ;
assignment = logical_or [ "=" assignment ] ;
logical_or = logical_and { "or" logical_and } ;
logical_and = equality { "and" equality } ;
equality = relational { ( "==" | "!=" ) relational } ;
relational = additive { ( "<" | "<=" | ">" | ">=" ) additive } ;
additive = multiplicative { ( "+" | "-" ) multiplicative } ;
multiplicative = unary { ( "*" | "/" | "%" ) unary } ;
unary = ( "not" | "-" ) unary | postfix ;
postfix = primary { array_access | function_call } ;
```

## Solução de Problemas

### Problema: "python: command not found"

**Solução:** Tente usar `python3` ao invés de `python`:
```bash
python3 src/cli.py tests/ok_hello.min -r
```

### Problema: "No module named 'src'"

**Solução:** Certifique-se de estar executando o comando da raiz do projeto:
```bash
# Verifique se está no diretório correto
ls src/  # Deve listar os arquivos do compilador

# Execute novamente
python src/cli.py tests/ok_hello.min -r
```

### Problema: Caracteres estranhos na saída (Windows)

**Solução:** Configure o terminal para UTF-8:
```bash
# No CMD
chcp 65001

# No PowerShell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
```

## Desenvolvimento

### Adicionar Novo Tipo de Node

1. Adicionar classe em `src/ast_nodes.py`
2. Adicionar método `visit_*` em `ASTVisitor`
3. Implementar nos visitors (sema, interp, codegen, pretty)

### Adicionar Novo Operador

1. Adicionar token em `src/lexer.py` (TokenType e KEYWORDS)
2. Adicionar parsing em `src/parser.py`
3. Implementar semântica em `src/sema.py`
4. Implementar execução em `src/interp.py`
5. Implementar geração em `src/codegen.py`

## Licença

Este projeto foi desenvolvido para fins educacionais como trabalho do curso de Compiladores.

---

**Mini-Lang Compiler** - Compilador educacional completo e organizado 

**Desenvolvido com:**
- Python 3
- Padrão Visitor

- Análise descendente recursiva
