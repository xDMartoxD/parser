import re

definedFunctions = set()
commands = {'walk', 'rotate', 'look', 'drop', 'free', 'peek', 'grab', 'walkTo', 'NOP', 'block'}
variables = dict({"var": 1})
conditions = {'blocked?', 'facing?', 'can', 'not'}


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


def everyThingInsideParenthesis(code: str) -> bool:
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


def checkConditionals(conditional: str, separatedConditional: list) -> tuple:
    badToken = False
    message = ''
    if separatedConditional[0] not in conditions:
        badToken = True
        message = 'Se esperaba un condicional pero se obtuvo {}'.format(conditional)
    if not badToken:
        if separatedConditional[0] == 'not':
            badToken = not bool(re.match(r'^\s*not\s*[(]\n*.+\n*[)]$', conditional))
            message = 'error en  {}'.format(conditional)
            if not badToken:
                conditional = ' '.join(separatedConditional[1:])
                conditional, separatedConditional = formatToken(conditional)
                badToken, message = checkConditionals(conditional, separatedConditional)
        elif separatedConditional[0] == 'can':
            badToken = not bool(re.match(r'\s*(can)\s+((grab|drop|free|peek)\s*)$', conditional))
            message = 'error en el token {}'.format(conditional)
        elif separatedConditional[0] == 'facing?':
            badToken = not bool(re.match(r'\s*(facing[?])\s+((N|E|W|S)\s*)$', conditional))
            message = 'Error en el token {}'.format(conditional)
        elif separatedConditional[0] == 'blocked?':
            badToken = not bool(re.match(r'^\s*blocked[?]\s*$', conditional))
            message = 'Error en el token {}'.format(conditional)

    return badToken, message


def formatToken(token: str) -> tuple:
    token = token[1: len(token) - 1]
    separatedToken = token.split()
    return token, separatedToken


def analyzeToken(token: str, parameters={}) -> tuple:
    token, separatedToken = formatToken(token)
    badToken: bool = False
    message: str = ''
    if separatedToken[0] in commands:
        if separatedToken[0] == 'walk':
            if len(separatedToken) != 2:
                badToken = True
                message = 'Faltan o sobran variables en {}'.format(token)
            else:
                if not separatedToken[1].isdigit():
                    key = separatedToken[1]
                    value = variables.get(separatedToken[1])
                    if key in parameters:
                        value = 0
                    if type(value) == int:
                        separatedToken[1] = str(value)
                        token = ' '.join(separatedToken)

                    else:
                        badToken = True
                        message = 'en ({}) se esparaba un numero o una variable de tipo entero pero se obtuvo {}'.format(
                            token, value)

                if not badToken:
                    badToken = not bool(re.match(r'\s*(walk)\s+([0-9]+\s*)$', token))
                    message = 'Error en {}'.format(token)
                if badToken:
                    return badToken, message
        elif separatedToken[0] == 'rotate':
            if len(separatedToken) != 2:
                badToken = True
                message = 'Faltan o sobran variables en {}'.format(token)
            else:
                badToken = not bool(re.match(r'\s*(rotate)\s+((left|right|back)\s*)$', token))
                message = 'Error en {}'.format(token)
            if badToken:
                return badToken, message
        elif separatedToken[0] == 'look':
            if len(separatedToken) != 2:
                badToken = True
                message = 'Faltan o sobran variables en {}'.format(token)
            else:
                badToken = not bool(re.match(r'\s*(look)\s+((N|E|W|S)\s*)$', token))
                message = "Error en {}".format(token)
            if badToken:
                return badToken, message
        elif separatedToken[0] == 'drop':
            if len(separatedToken) != 2:
                badToken = True
                message = 'Faltan o sobran variables en {}'.format(token)
            else:
                if not separatedToken[1].isdigit():
                    key = separatedToken[1]
                    value = variables.get(separatedToken[1])
                    if key in parameters:
                        value = 0
                    if type(value) == int:
                        separatedToken[1] = str(value)
                        token = ' '.join(separatedToken)

                    else:
                        badToken = True
                        message = 'en ({}) se esparaba un numero o una variable de tipo entero pero se obtuvo {}'.format(
                            token, value)
                if not badToken:
                    badToken = not bool(re.match(r'\s*(drop)\s+([0-9]+\s*)$', token))
                    message = 'Error en {}'.format(token)
                if badToken:
                    return badToken, message
        elif separatedToken[0] == 'free':
            if len(separatedToken) != 2:
                badToken = True
                message = 'Faltan o sobran variables en {}'.format(token)
            else:
                if not separatedToken[1].isdigit():
                    key = separatedToken[1]
                    value = variables.get(separatedToken[1])
                    if key in parameters:
                        value = 0
                    if type(value) == int:
                        separatedToken[1] = str(value)
                        token = ' '.join(separatedToken)

                    else:
                        badToken = True
                        message = 'en ({}) se esparaba un numero o una variable de tipo entero pero se obtuvo {}'.format(
                            token, value)
                if not badToken:
                    badToken = not bool(re.match(r'\s*(free)\s+([0-9]+\s*)$', token))
                    message = 'Error en {}'.format(token)
                if badToken:
                    return badToken, message
        elif separatedToken[0] == 'peek':
            if len(separatedToken) != 2:
                badToken = True
                message = 'Faltan o sobran variables en  {}'.format(token)
            else:
                if not separatedToken[1].isdigit():
                    key = separatedToken[1]
                    value = variables.get(separatedToken[1])
                    if key in parameters:
                        value = 0
                    if type(value) == int:
                        separatedToken[1] = str(value)
                        token = ' '.join(separatedToken)

                    else:
                        badToken = True
                        message = 'en ({}) se esparaba un numero o una variable de tipo entero pero se obtuvo {}'.format(
                            token, value)
                if not badToken:
                    badToken = not bool(re.match(r'\s*(peek)\s+([0-9]+\s*)$', token))
                    message = 'Error en {}'.format(token)
                if badToken:
                    return badToken, message
        elif separatedToken[0] == 'grab':
            if len(separatedToken) != 2:
                badToken = True
                message = 'Faltan o sobran variables'
            else:
                if not separatedToken[1].isdigit():
                    key = separatedToken[1]
                    value = variables.get(separatedToken[1])
                    if key in parameters:
                        value = 0
                    if type(value) == int:
                        separatedToken[1] = str(value)
                        token = ' '.join(separatedToken)

                    else:
                        badToken = True
                        message = 'en ({}) se esparaba un numero o una variable de tipo entero pero se obtuvo {}'.format(
                            token, value)
                if not badToken:
                    badToken = not bool(re.match(r'\s*(grab)\s+([0-9]+\s*)$', token))
                    message = 'Error en {}'.format(token)
                if badToken:
                    return badToken, message
        elif separatedToken[0] == 'walkTo':
            if len(separatedToken) != 3:
                badToken = True
                message = 'Faltan o sobran variables en {}'.format(token)
            else:
                if not separatedToken[2].isdigit():
                    key = separatedToken[2]
                    value = variables.get(separatedToken[2])
                    if key in parameters:
                        value = 0
                    if type(value) == int:
                        separatedToken[1] = str(value)
                        token = ' '.join(separatedToken)
                        
                    else:
                        badToken = True
                        message = 'en ({}) se esperaba un numero o una variable de tipo entero pero se obtuvo {}'.format(
                            token, value)
                if not badToken:
                    badToken = not bool(re.match(r'\s*(walkTo)\s+(W|E|N|S)\s+([0-9]+\s*)$', token))
                    message = 'Error en {}'.format(token)
                if badToken:
                    return badToken, message

        elif separatedToken[0] == 'NOP':
            if len(separatedToken) != 1:
                badToken = True
                message = 'se espeaba solo un argumento pero se obtuvo {}'.format(token)
            else:
                badToken = not bool(re.match(r'^\s*(NOP)\s*$', token))
                message = 'error en {}'.format(token)
            if badToken:
                return badToken, message
        elif separatedToken[0] == 'block':
            token = token.replace('block', '')
            separatedTokens = splitByParenthesis(token)
            for separatedToken in separatedTokens:
                badToken, message = analyzeToken(separatedToken, parameters=parameters)
                if badToken:
                    return badToken, message
    else:
        if separatedToken[0] == 'define':
            if bool(re.match(r'\s*(define)\s*([a-zA-Z]+[a-zA-Z0-9]*)\s+[(][a-zA-Z0-9\s]*[)]\s+([(].*[)]\s*)$', token)):
                funcName = separatedToken[1]
                definedFunctions.add(funcName)
                token = token.replace('define', '')
                token = token.replace(funcName, '', 1)
                [params, instructions] = splitByParenthesis(token)
                badToken = not bool(re.match(r'[(][a-zA-Z\s]*[)]', params))
                message = 'Error en el token {}'.format(token)
                params, separatedParams = formatToken(params)
                paramsSet = set(separatedParams)

                if not badToken:
                    _, separatedInstructions = formatToken(instructions)
                    if len(separatedInstructions) < 1:
                        badToken = True
                        message = ' no hay instrucciones'
                        return badToken, message
                    else:
                        badToken, message = analyzeToken(instructions, parameters=paramsSet)
                        if badToken:
                            return badToken, message

            elif bool(re.match(r'\s*(define)\s*([a-zA-Z]+[a-zA-Z0-9]*)\s+([a-zA-z0-9]+\s*)$', token)):
                key = separatedToken[1]
                val = separatedToken[2]
                try:
                    variables[key] = int(val)
                except ValueError:
                    message = 'Todas las varaibles deberian de ser numeros enteros'
                    badToken = True
                    return badToken, message
            else:
                badToken = True
                message = 'no se reconoce si es funcion o variabe {}'.format(token)
                return badToken, message
        elif separatedToken[0] == 'if':
            token = token.replace('if', '')
            newTokens = splitByParenthesis(token)
            if len(newTokens) != 3:
                badToken = True
                message = "debe haber un condicional y dos comandos {}".format(newTokens)
                return badToken, message
            newConditional, separatedConditional = formatToken(newTokens[0])
            badToken, message = checkConditionals(newConditional, separatedConditional)
            if badToken:
                return badToken, message
            for i in [1, 2]:
                newCommand, separatedCommand = formatToken(newTokens[i])
                if separatedCommand[0] not in commands and separatedCommand[0] not in definedFunctions:
                    badToken = True
                    message = 'se esparaba un comando pero se obtuvo {}'.format(newCommand)
                    return badToken, message
            if not badToken:
                for newToken in newTokens[1:]:
                    badToken, message = analyzeToken(newToken, parameters=parameters)
                    if badToken:
                        return badToken, message

        else:
            if separatedToken[0] not in definedFunctions:
                badToken = True
            message = 'No se reconoce el token {}'.format(token)

    return badToken, message


def colored(r, g, b, text):
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)


def checkSyntax(code: str) -> None:
    # if not code.startswith('(') or not code.endswith(')'):
    #     print('el archivo debe empezar con un parentesis de apertura y terminar con un parentesis de cierre')
    #     return
    # print('parentesis de inicio y fin correctos')
    isBalanced = checkBalancedParenthesis(code)
    if not isBalanced:
        print('Los parentesis no estan balanceados')
        return
    if not everyThingInsideParenthesis(code):
        print('todos los caracteres deben estar dentro de algun parentesis')
        return
    tokens = splitByParenthesis(code)
    print('--------------------------------------------------------------------------------------------------')
    for token in tokens:
        badToken, message = analyzeToken(token)
        if badToken:
            print(colored(200, 0, 0, 'EL TOKEN {} NO HACE PARTE DEL LENGUAJE'.format(token)))
            print(colored(200, 0, 0, message))
            print('--------------------------------------------------------------------------------------------------')
            break
        else:
            print(colored(0, 200, 000, 'EL TOKEN {} HACE PARTE DEL LENGUAJE'.format(token)))
            print('--------------------------------------------------------------------------------------------------')


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
