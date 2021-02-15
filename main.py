import re

definedFunctions = set()
commands = {'walk', 'rotate', 'look', 'drop', 'free', 'peek', 'grab', 'walkTo', 'NOP'}
variables = dict({"var": 1})
conditions = {'blocked', 'facing', 'can', 'not'}


def checkBalancedParenthesis(code: str) -> bool:
    stack = []
    isBalanced = True
    i = 0
    while i < len(code) and isBalanced:
        char = code[i]
        if char == '(':
            stack.append(char)
        elif char == ')':
            if not stack:
                isBalanced = False
            else:
                stack.pop()
        i += 1
    return isBalanced and not stack


def splitByParenthesis(code: str) -> []:
    code = code.replace('\n', '')

    tokens = []
    stack = []
    i = 0
    start: int = 0
    end: int = 0
    while i < len(code):
        char = code[i]
        if char == '(':
            if not stack:
                start = i
            stack.append('(')
        if char == ')':
            stack.pop()
        if not stack and char != ' ':
            end = i
            token = code[start: end + 1]

            tokens.append(token)
        i += 1
    return tokens


def everyThingInsideParenthesis(code: str) -> str:
    code = code.replace('\n', '')
    stack = []
    i = 0
    everythingInside: bool = True
    while i < len(code) and everythingInside:
        char = code[i]
        if char == '(':
            stack.append('(')
        if char == ')':
            stack.pop()
        if not stack and char not in ' )':
            everythingInside = False
        i += 1
    return everythingInside


def analyzeToken(token: str) -> tuple:
    token = token[1: len(token) - 1]
    separatedToken = token.split()
    badToken: bool = False
    message: str = ''

    if separatedToken[0] not in commands:
        if separatedToken[0] == 'define':
            if bool(re.match(r'\s*(define)\s+([a-zA-Z]+[a-zA-Z0-9]*)\s+[(][a-zA-Z0-9\s]*[)]\s+([(].*[)])$', token)):
                funcName = separatedToken[1]
                definedFunctions.add(funcName)
            elif bool(re.match(r'\s*(define)\s+([a-zA-Z]+[a-zA-Z0-9]*)\s+([a-zA-z0-9]+\s*)$', token)):
                key = separatedToken[1]
                val = separatedToken[2]
                try:
                    variables[key] = int(val)
                except ValueError:
                    message = 'Todas las varaibles deberian de ser numeros enteros'
                    badToken = True
            else:
                badToken = True
                message = 'no se reconoce si es funcion o variabe {}'.format(token)

    elif separatedToken[0] == 'walk':
        if len(separatedToken) != 2:
            badToken = True
            message = 'Faltan o sobran variables en {}'.format(token)
        else:
            if not separatedToken[1].isdigit():
                key = separatedToken[1]
                value = variables.get(separatedToken[1])
                if bool(value) and type(value) == int:
                    token = token.replace(str(key), str(value))
                else:
                    badToken = True
                    message = 'en ({}) se esparaba un numero o una variable de tipo entero pero se obtuvo {}'.format(
                        token, value)
            if not badToken:
                badToken = not bool(re.match(r'\s*(walk)\s+([0-9]+\s*)$', token))
                message = 'Error en {}'.format(token)
    elif separatedToken[0] == 'rotate':
        if len(separatedToken) != 2:
            badToken = True
            message = 'Faltan o sobran variables en {}'.format(token)
        else:
            badToken = not bool(re.match(r'\s*(rotate)\s+((left|right|back)\s*)$', token))
            message = 'Error en {}'.format(token)
    elif separatedToken[0] == 'look':
        if len(separatedToken) != 2:
            badToken = True
            message = 'Faltan o sobran variables en {}'.format(token)
        else:
            badToken = not bool(re.match(r'\s*(look)\s+((N|E|W|S)\s*)$', token))
            message = "Error en {}".format(token)
    elif separatedToken[0] == 'drop':

        if len(separatedToken) != 2:
            badToken = True
            message = 'Faltan o sobran variables en {}'.format(token)
        else:
            if not separatedToken[1].isdigit():
                key = separatedToken[1]
                value = variables.get(separatedToken[1])
                if bool(value) and type(value) == int:
                    token = token.replace(str(key), str(value))
                else:
                    badToken = True
                    message = 'en ({}) se esparaba un numero o una variable de tipo entero pero se obtuvo {}'.format(
                        token, value)
            if not badToken:
                badToken = not bool(re.match(r'\s*(drop)\s+([0-9]+\s*)$', token))
                message = 'Error en {}'.format(token)
    elif separatedToken[0] == 'free':
        if len(separatedToken) != 2:
            badToken = True
            message = 'Faltan o sobran variables en {}'.format(token)
        else:
            if not separatedToken[1].isdigit():
                key = separatedToken[1]
                value = variables.get(separatedToken[1])
                if bool(value) and type(value) == int:
                    token = token.replace(str(key), str(value))
                else:
                    badToken = True
                    message = 'en ({}) se esparaba un numero o una variable de tipo entero pero se obtuvo {}'.format(
                        token, value)
            if not badToken:
                badToken = not bool(re.match(r'\s*(free)\s+([0-9]+\s*)$', token))
                message = 'Error en {}'.format(token)
    elif separatedToken[0] == 'peek':
        if len(separatedToken) != 2:
            badToken = True
            message = 'Faltan o sobran variables en  {}'.format(token)
        else:
            if not separatedToken[1].isdigit():
                key = separatedToken[1]
                value = variables.get(separatedToken[1])
                if bool(value) and type(value) == int:
                    token = token.replace(str(key), str(value))
                else:
                    badToken = True
                    message = 'en ({}) se esparaba un numero o una variable de tipo entero pero se obtuvo {}'.format(
                        token, value)
            if not badToken:
                badToken = not bool(re.match(r'\s*(peek)\s+([0-9]+\s*)$', token))
                message = 'Error en {}'.format(token)
    elif separatedToken[0] == 'grab':
        if len(separatedToken) != 2:
            badToken = True
            message = 'Faltan o sobran variables'
        else:
            if not separatedToken[1].isdigit():
                key = separatedToken[1]
                value = variables.get(separatedToken[1])
                if bool(value) and type(value) == int:
                    token = token.replace(str(key), str(value))
                else:
                    badToken = True
                    message = 'en ({}) se esparaba un numero o una variable de tipo entero pero se obtuvo {}'.format(
                        token, value)
            if not badToken:
                badToken = not bool(re.match(r'\s*(grab)\s+([0-9]+\s*)$', token))
                message = 'Error en {}'.format(token)
    elif separatedToken[0] == 'walkTo':
        if len(separatedToken) != 3:
            badToken = True
            message = 'Faltan o sobran variables en {}'.format(token)
        else:
            if not separatedToken[2].isdigit():
                key = separatedToken[2]
                value = variables.get(separatedToken[2])
                if bool(value) and type(value) == int:
                    token = token.replace(str(key), str(value))
                else:
                    badToken = True
                    message = 'en ({}) se esperaba un numero o una variable de tipo entero pero se obtuvo {}'.format(
                        token, value)
            if not badToken:
                badToken = not bool(re.match(r'\s*(walkTo)\s+(W|E|N|S)\s+([0-9]+\s*)$', token))
                message = 'Error en {}'.format(token)

    elif separatedToken[0] == 'NOP':
        badToken = not bool(re.match(r'^\s*(NOP)\s*$', token))
        message = 'error en {}'.format(token)
    elif token.startswith('block'):
        pass

    elif token.startswith('define'):
        parts = token.split()
        definedFunctions.add(parts[1])
    else:
        parts = token.split()
        functionName = parts[0]
        if functionName not in definedFunctions:
            message = 'Funcion {} indefinida'.format(functionName)

    return badToken, message


def checkSyntax(code: str) -> None:
    # if not code.startswith('(') or not code.endswith(')'):
    #     print('el archivo debe empezar con un parentesis de apertura y terminar con un parentesis de cierre')
    #     return
    # print('parentesis de inicio y fin correctos')
    isBalanced = checkBalancedParenthesis(code)
    if not isBalanced:
        print('Los parentesis no estan balanceados')
        return
    print('parentesis balanceados')
    if not everyThingInsideParenthesis(code):
        print('todos los caracteres deben estar dentro de algun parentesis')
        return
    tokens = splitByParenthesis(code)

    for token in tokens:
        badToken, message = analyzeToken(token)
        if badToken:
            print(message)
            return


print('Bienvenido')
print('el primer paso es pasar un archivo con extension .txt')
print(
    'Puede no pasar nada y automaticamente el programa leera un archivo test.txt en el directorio (presione enter 2 '
    'veces)')
print('puede parar una ruta relativa el programa leera el archivo con la ruta relativa en el direcotorio (xd.txt)')
print('o puede pasar una ruta absoluta')
ruta = input('digite la ruta del archivo \n')
if not ruta:
    ruta = 'test.txt'

with open(ruta, 'r') as file:
    checkSyntax(file.read())
