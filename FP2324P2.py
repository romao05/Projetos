''' Este programa tem como objetivo possibiltar a realização do jogo
go num computador de acordo com todas as regras do jogo.'''



''' TAD Interseção'''


''' Esta função recebe um caracter e um inteiro e após fazer a validação dos
argumentos vai devolver a representação interna de uma interseção do goban.'''
def cria_intersecao (col, lin):
    if type (col) != str or type (lin) != int or len (col) != 1\
             or not 0 < lin < 20 or ord (col) - 65 not in range (26):
        raise ValueError ("cria_intersecao: argumentos invalidos")
    return (col,lin)

''' Esta função recebe uma interseção e devolve a coluna a que esta pertence.'''
def obtem_col (i):
    return i[0]


''' Esta função recebe uma interseção e devolve a linha a que esta pertence.'''
def obtem_lin (i):
    return i[1]


''' Esta função recebe um agrumento de qualquer tipo e devolve True se este
 corresponder à representação interna de uma interseção. caso contrário 
 irá devolver o booleano False.'''
def eh_intersecao (arg):
    if type (arg) != tuple or len (arg) != 2 or type (obtem_col (arg)) != str\
          or type (obtem_lin (arg)) != int or len (obtem_col (arg)) != 1\
              or not 0 < obtem_lin (arg) < 20\
                  or not ord ("A") <= ord(obtem_col (arg)) <= ord ("S"):
        return False
    return True


''' Esta função recebe duas interseções e devolve True se estas forem iguais
e False caso contrário.'''
def intersecoes_iguais (i1, i2):
    if not eh_intersecao (i1) or not eh_intersecao (i2):
        return False
    return i1 [0] == i2[0] and i1 [1] == i2[1]


''' Esta função recebe uma interseção e devolve uma representação da mesma
em forma de string.'''    
def intersecao_para_str (i):
    return f"{obtem_col (i)}{obtem_lin (i)}"


''' Esta função recebe uma string que representa uma interseção e devolve
a mesma na sua representação interna (lista onde o 1º elemento corresponde à 
coluna e o segundo 
á linha).'''
def str_para_intersecao (s):
    return cria_intersecao (s[0], int(s[1:]))


''' Esta função recebe como argumentos uma interseção e a última interseção
do goban onde se encontra a intersecao no 1º argumento. esta função vai 
devolver as interseções do goban que são adjacentes à introduzida
ordenadas consoante a ordem de leitura do tabuleiro do jogo.'''
def obtem_intersecoes_adjacentes (i,l):
# Criar lista para ver quais das 4 operações definidas acima podem ser realizadas
# e realizar as operações para criar as interceções adjacentes
    possiveis_adj = []
    try:
        possiveis_adj += [cria_intersecao(obtem_col (i), obtem_lin (i) - 1)]
    except ValueError:
        pass 
    try:
        possiveis_adj += [cria_intersecao(chr(ord(obtem_col (i)) - 1), obtem_lin (i))]
    except ValueError:
        pass
    try:
        possiveis_adj += [cria_intersecao(chr(ord(obtem_col (i)) + 1), obtem_lin (i))]
    except ValueError:
        pass 
    try:    
        possiveis_adj += [cria_intersecao (obtem_col (i), obtem_lin (i) + 1)]
    except ValueError:
        pass
    adjs = ()
# Formulação de uma lista com os pontos adjacentes a i que pertencem ao território
    for adj in possiveis_adj:
        if 0 < obtem_lin (adj) <= obtem_lin (l)\
              and 64 < ord(obtem_col (adj)) <= ord (obtem_col (l)):
            adjs += (adj,) 
    return adjs


''' Esta função recebe como argumento um tuplo com várias interseções
e vai devolver um tuplo com todas essas interseções ordenadas consoante
a ordem de leitura de um goban.'''
def ordena_intersecoes (t):
 # Uso a função lambda dentro do sort para indicar que a ordenação da
 #  minha lista deve ser feita com base nos números e quando estes são
 #  iguais, a organização é feita por ordem alfabética
    ordem_leitura = sorted(list (t), key= lambda x: (obtem_lin (x), obtem_col (x)))
    return tuple(ordem_leitura)


''' TAD Pedra'''


''' Esta função devolve a representação interna de uma pedra branca.'''
def cria_pedra_branca ():
    return "O"


''' Esta função devolve a representação interna de uma pedra preta.'''
def cria_pedra_preta ():
    return "X"


''' Esta função devolve a representação interna de uma pedra neutra.'''
def cria_pedra_neutra ():
    return "."


''' Esta função recebe um argumento de qualquer tipo e devolve True se
este for um pedra.'''
def eh_pedra (arg):
    return arg in [cria_pedra_preta (), cria_pedra_branca (), cria_pedra_neutra ()]


''' Esta função recebe como argumento uma pedra e devolve True se
esta for branca, caso contrário devolve False.'''
def eh_pedra_branca (p):
    return p == cria_pedra_branca ()


''' Esta função recebe como argumento uma pedra e devolveTrue se
esta for perta, caso contrário devolve False.'''
def eh_pedra_preta (p):
    return p == cria_pedra_preta ()


''' Esta função recebe como argumentos duas pedras e devolve True
se estas forem iguais, caso contrário devolve False.'''
def pedras_iguais (p1,p2):
    if not eh_pedra (p1) or not eh_pedra (p2):
        return False
    return p1 == p2


''' Esta função recebe uma pedra na sua representação interna
e devolve a mesma na sua representação externa'''
def pedra_para_str (p):
    if eh_pedra_preta (p):
        return "X"
    if eh_pedra_branca (p):
        return "O"
    return "."


''' esta função recebe uma pedra e devolve True se ela pertencer
a um jogador e False se ela for neutra.'''
def eh_pedra_jogador (p):
    return eh_pedra_branca (p) or eh_pedra_preta (p)


''' TAD Goban'''


''' Esta função recebe como argumento um inteiro e após fazer a
 validação de daods vai devolver a representação interna de
   um goban n x n vazio.'''
def cria_goban_vazio (n):
    if type (n) != int or n not in [9,13,19]:
        raise ValueError ("cria_goban_vazio: argumento invalido")
    goban = []
    for linha in range(n):
        line = []
        for coluna in range (n):
            line += [cria_pedra_neutra ()]
        goban += [line, ]
    return goban


''' Esta função recebe como argumentos um inteiro e dois tuplos
constituidos por interseções fazendo inicialmente uma validação
 dos dados introduzidos. Posto isto a função vai devolver a
 representação interna de um goban com as interseções do 1º
 tuplo ocupadas por pedras brancas e as do 2º ocupadas por pedras
 pretas.'''
def cria_goban (n, ib, ip):
# Verificação dos dados introduzidos
    if type (n) != int or n not in [9,13,19]:
        raise ValueError ("cria_goban: argumentos invalidos")
    if not isinstance (ib, tuple) or not isinstance (ip, tuple):
        raise ValueError ("cria_goban: argumentos invalidos")
    goban = cria_goban_vazio (n)
    intersecoes_validadas = []
    if ib != ():
        for i in list (ib):
# Validação das interseções contidas no tuplo
            if not eh_intersecao (i) \
                or obtem_lin (i) > n or\
                n - 1 < ord (obtem_col (i)) - ord ("A")\
                    or i in intersecoes_validadas:
                raise ValueError ("cria_goban: argumentos invalidos")
            goban [obtem_lin (i) - 1] [ord (obtem_col (i)) - ord("A")] = cria_pedra_branca ()
            intersecoes_validadas += [i,]
    if ip != ():
        for intersecao in list (ip):
# Validação das interseções contidas no tuplo
            if not eh_intersecao (intersecao)\
                or n < obtem_lin (intersecao)\
                or n - 1 < ord (obtem_col (intersecao)) - ord ("A") \
                    or intersecao in intersecoes_validadas:
                raise ValueError ("cria_goban: argumentos invalidos")
            goban [obtem_lin (intersecao) - 1] [ord (obtem_col (intersecao)) - ord("A")] = cria_pedra_preta ()
            intersecoes_validadas += [intersecao,]
    return goban


''' Esta função cria uma deep copy do goban que é dado como argumento.
Uma deep copy é uma cópia que permanece inalterada quando fazemos
modificações no elemento original.'''
def cria_copia_goban (g):
    g_copiado = cria_goban_vazio (len(g))
    for linha in range (len (g)):
        for coluna in range (len(g)):
            g_copiado [linha] [coluna] = obtem_pedra (g, cria_intersecao (chr (coluna + 65), linha +1))
    return g_copiado


''' Esta função recebe um goban e devolve a representação interna da última
interseção do mesmo.'''
def obtem_ultima_intersecao (g):
    return cria_intersecao (chr (64 + len (g[0])), len (g[0]))


''' Esta função recebe um goban e uma interseção e devolve a pedra que se
encontra na mesma.'''
def obtem_pedra (g,i):
    return g[obtem_lin (i) -1] [ord (obtem_col (i)) - 65]


''' Esta função recebe um goban e uma interseção e devolve um tuplo com
todas as interseções (em ordem de leitura)que que estão conectadas à introduzida
através de interseções adjacentes que contêm pedras iguasi à da interseção dada
como argumento.'''
def obtem_cadeia (g,i):
    cadeia = [i]
    for inter in cadeia:
        adj= obtem_intersecoes_adjacentes (inter, obtem_ultima_intersecao (g))
        for intersecao in adj:
            if pedras_iguais (obtem_pedra (g,intersecao), obtem_pedra (g,i))\
                  and intersecao not in cadeia:
                cadeia += [intersecao]
    return ordena_intersecoes (tuple(cadeia))



''' Esta função receb como argumentos um goban, uma interseção e uma pedra 
(respetivamente) e devolve o goban inicial com um modificação que corresponde à
colocação de pedra na interseção dada como argumento.'''
def coloca_pedra (g, i, p):
    g [obtem_lin (i) -1] [ord(obtem_col (i)) - 65] = p
    return g


''' Esta função recebe como argumentos um goban e uma interseção e vai devolver
o goban introduzido com uma alteração na interseção dada como argumento, alteração
esta que corresponde à remoção da pedra que se encontra na mesma.'''
def remove_pedra (g, i):
    g [obtem_lin (i) -1] [ord(obtem_col (i)) - 65] = cria_pedra_neutra ()
    return g


''' Esta função recebe um goban e tuplo de interseções e vai devolver o goban
introduzido com uma ou mais alterações que correspondem á remoção das pedras
que se encontram nas interseções contidas no tuplo introduzido.'''
def remove_cadeia (g, t):
    for intersecao in t:
        g = remove_pedra (g, intersecao)
    return g


''' Esta função recebe um argumento qualquer e devolve True se esta corresponder
a um goban, se não corresponder devolve False'''
def eh_goban (arg):
    if not isinstance (arg, list) or len (arg) not in [9,13,19]\
        or len(arg) != len (arg [0]):
            return False
    for linha in range (len (arg)):
        for coluna in range (len (arg)):
            if not eh_pedra (arg [linha] [coluna]):
                return False
    return True


''' Esta função recebe como argumento um goban e uma interseção e devolve
True se a interseção dada como argumento pertencer ao goban, caso contrário
vai devolver False'''
def eh_intersecao_valida (g,i):
    if not eh_intersecao (i) or not eh_goban (g):
        return False
    if obtem_lin (i) > len (g) or ord (obtem_col (i)) - ord ("A") not in range (len (g)):
        return False
    return True


'''Esta função recebe como argumentos dois gobans e devolve True se estes forem iguais, 
~caso contrário vai devolver False'''
def gobans_iguais (g1,g2):
    if not eh_goban (g1) or not eh_goban (g2) or len (g1) != len (g2):
        return False
    for linha in range(len (g1)):
        for coluna in range(len (g1)):
            i = cria_intersecao (chr (65 + linha), coluna +1)
            if not pedras_iguais (obtem_pedra (g1, i), obtem_pedra (g2, i)):
                return False
    return True



''' esta função recebe como argumento um goban na sua representação interna e devolve 
um string com a representação externa do mesmo'''
def goban_para_str (g):
    string = "  "
    colunas = ""
    for coluna in range (len(g)):
        colunas += f" {chr(65 + coluna)}"
    string += colunas + "\n"
    meio_str = ""
    for linha in range(len(g) - 1, -1, -1):
        meio_str = ""
        for col in range (len(g)):
            meio_str += f"{pedra_para_str (obtem_pedra (g, cria_intersecao (chr (col + 65), linha+1)))} "
        if len (g) == 9:
            string += f" {linha + 1} {meio_str} {linha + 1}\n"
        else:
            string += f"{linha + 1:2d} {meio_str}{linha + 1:2d}\n"
    string += "  " + colunas
    return string


''' esta função recebe como argumentos um goban e devolve um tuplo
constituido por um ou mais tuplos pequenos que correspondem a territórios
do tabuleiro do jogo introduzido'''
def obtem_territorios (g):
    territorios = ()
    intersecoes_vistas = ()
    for linha in range (len (g)):
        for coluna in range (len(g)):
            i = cria_intersecao (chr (65 + coluna), linha + 1)
            if not eh_pedra_jogador (obtem_pedra (g, i)) and i not in intersecoes_vistas:
                cadeia = obtem_cadeia (g, i)
                intersecoes_vistas += cadeia
                territorios +=  (cadeia,)
    return territorios

''' Esta função recebe como argumentos um goban e um tuplo de interseções
e, as interseções do tuplo estejam ocupadas por pedras de jogadores a função
devolve um tuplo com as interseções livres adjacentes às do tuplo. Caso
as interseções do tuplo sejam livres a função devolve as interseções
adjacentes às do tulo que estão ocupadas por pedras de jogadores '''
def obtem_adjacentes_diferentes (g, t):
    diferentes = ()
    for intersecao in t:
        for i in obtem_intersecoes_adjacentes  (intersecao, obtem_ultima_intersecao (g)):
            if i not in diferentes:
                if not eh_pedra_jogador (obtem_pedra (g, t[0])):
                    if eh_pedra_jogador (obtem_pedra (g, i)):
                        diferentes += (i,)
                if eh_pedra_jogador (obtem_pedra (g, t[0])):
                    if not eh_pedra_jogador (obtem_pedra (g, i)) :
                        diferentes += (i,)
    return ordena_intersecoes (diferentes)



''' Esta função recebe como argumentos um goban, uma interseção e uma pedra que
 vai ser colocada na mesma. Esta função modifica destrutivamente o goban inserido
 colocando a pedra na interseção inserida e removendo as pedras das cadieas
 adjacentes à da interseção inseriida que não possuem quaisquer liberdades.'''
def jogada (g, i,p):
    g = coloca_pedra (g, i, p)
    cadeia_iguais = obtem_cadeia (g, i)
    territorios_adjacentes = (obtem_adjacentes_diferentes (g, cadeia_iguais))
    for coordenada in cadeia_iguais:
        adjs = obtem_intersecoes_adjacentes (coordenada, obtem_ultima_intersecao (g))
        for inter in adjs:
# Só trabalha com as interseções adjacentes que não pertencem à cadeia e que não são livres
            if inter not in cadeia_iguais:
                if inter not in territorios_adjacentes:
                    fronteira = ()
                    cadeia_outro_jogador = obtem_cadeia (g, inter)
                    tamanho_fronteira = 0
                    for intersecao in cadeia_outro_jogador:
                        for e in obtem_intersecoes_adjacentes (intersecao, obtem_ultima_intersecao (g)):
                            if e not in cadeia_outro_jogador and e not in fronteira:
# tamanho fronteira calcula o número de interseções que rodeiam a cadeia do outro
# jogador e se todas elas estiverem ocupadas por pedras iguais à que foi inserida
#então a cadeia_outro_jogador não tem liberdades, ou seja, vai ser removida
                                    tamanho_fronteira += 1
                                    if eh_pedra_jogador (obtem_pedra (g,e)):
                                        fronteira +=(e,)
                    if len(fronteira) == tamanho_fronteira:
                        remove_cadeia (g,cadeia_outro_jogador)
    return g
     

''' esta função recebe como argumento um goban na sua representação
interna e devolve um tuplo de dois elementos em que o primeiro corresponde ao 
número de pedras brancas nesse goban e o segundos corresponde ao número
de pedras pretas.'''
def obtem_pedras_jogadores (g):
    brancas = 0
    pretas = 0
    for linha in range (len (g)):
        for coluna in range(len (g)):
            i = cria_intersecao (chr(coluna + 65),linha +1)
            if eh_pedra_branca (obtem_pedra (g, i)):
                brancas += 1
            elif eh_pedra_preta (obtem_pedra (g, i)):
                pretas += 1
    return (brancas, pretas)


''' Esta função recebe como argumento um goban na sua representação interna
e devolve um tuplo de dois argumentos em que o primeiro corresponde à 
pontuação do jogador com pedras brancas e o segundo corresponde à 
pontuação do jogador com pedras pretas'''
def calcula_pontos (g):
    final = list(obtem_pedras_jogadores (g))
    territorios = obtem_territorios (g)
    for territorio in territorios:
        fronteira = obtem_adjacentes_diferentes (g, territorio)
        brancas = 0
        pretas = 0
        if len (fronteira) == 0:
            return (0,0)
        for intersecao in fronteira:
                if eh_pedra_preta (obtem_pedra (g, intersecao)):
                    pretas += 1
                if eh_pedra_branca (obtem_pedra (g, intersecao)):
                    brancas += 1
        if len (fronteira) == brancas:
            final [0] += len (territorio)
        if len (fronteira) == pretas:
            final [1] += len (territorio)
    return tuple(final)


''' Esta função recebe como argumentos um goban, uma interseção, uma pedra
e ourto goban, respetivamente. Nesta é feita a validação da jogada, ou
seja, esta devolve True se a jogada for de encontro com as regras do jogo
e devolve Falso se isso não se verificar'''
def eh_jogada_legal (g, i, p, l):
    goban = cria_copia_goban (g)
    if not eh_intersecao_valida (g,i) or gobans_iguais (jogada (goban, i, p), l ):
        return False
    if eh_pedra_jogador (obtem_pedra (g, i)):
        return False
    cadeia_i = obtem_cadeia (goban, i)
    if obtem_adjacentes_diferentes (goban, cadeia_i) == ():
        return False
    return True


'''Esta função recebe como argumentos um goban, uma pedra e outro goban,
respetivamente, e vai devolver True se todos os argumentos cumprirem com
os requisitos necessários para que se possa fazer uma jodada devolvendo 
True, caso contrário devolve False. Se todas os requisitos forem cumpridos
a jogada é ralizada antes da função devolver True'''
def turno_jogador (g, p, l):
    p = pedra_para_str (p)
    i = input (f"Escreva uma intersecao ou 'P' para passar [{p}]:")
    if i == "P":
        return False
    if i == ""  or len (i) not in [2,3]:
        return turno_jogador (g, p, l)
# Verifica se os caracteres a seguir à string são todos dígitos
    for car in i[1:]:
        if not 48 <= ord (car) <= 57:
            return turno_jogador (g, p, l)
    try:
        i = str_para_intersecao (i)
    except ValueError:
        return turno_jogador (g, p, l)
    if not eh_intersecao_valida (g, i) or not eh_jogada_legal (g, i, p, l):
        return turno_jogador (g, p, l)
    jogada (g,i,p)
    return True


'''Esta função recebe como argumentos um número inteiro e dois tuplos
após verificar que estes argumentos corresponde a um inteiro que 
indica as dimensões de um goban e a tuplos com interseções pertencentes
ao mesmo através da veriicação de dados, esta função vai fazer com que
seja possível realizar um jogo go entre dois jogadores'''
def go (n, tb, tp):
# Validação de argumentos
# Goban
    if type (n) != int or not isinstance (tb, tuple)\
            or not isinstance (tp,tuple) or n not in [9,13,19]:
        raise ValueError ("go: argumentos invalidos")
    ib = ()
    ip = ()
    goban = cria_goban_vazio (n)
    int_validadas = []
# Validação tuplo 1
    for i in tb:
        if not isinstance (i,str) or 2< len (i) > 3\
             or (n == 9 and len (i) != 2):
            raise ValueError ("go: argumentos invalidos")
        for car in i[1:]:
            if not 48 <= ord (car) <= 57:
                raise ValueError ("go: argumentos invalidos")
        i = str_para_intersecao (i)
        if  not eh_intersecao_valida (goban, i) or i in int_validadas:
            raise ValueError ("go: argumentos invalidos")
        ib += (i,)
        int_validadas += [i]
# Validação tuplo 2
    for intersecao in tp:
        if not isinstance (intersecao,str) or 2< len (intersecao) > 3\
             or (n == 9 and len (intersecao) != 2):
            raise ValueError ("go: argumentos invalidos")
        for char in intersecao[1:]:
            if not 48 <= ord (char) <= 57:
                raise ValueError ("go: argumentos invalidos")
        intersecao = str_para_intersecao (intersecao)
        if  not eh_intersecao_valida (goban, intersecao) or intersecao in int_validadas:
            raise ValueError ("go: argumentos invalidos")
        ip += (intersecao,)
        int_validadas += [intersecao]
# Realização do jogo
    goban = cria_goban (n, ib, ip)
    l = cria_copia_goban (goban)
    passagens = 0
    pedra = cria_pedra_preta ()
    jogadas = 0
    while passagens != 2:
        pontos = calcula_pontos (goban)
        print (f"Branco (O) tem {pontos [0]} pontos")
        print (f"Preto (X) tem {pontos [1]} pontos")
        print (goban_para_str (goban))
        if turno_jogador (goban, pedra, l):
            passagens = 0
            jogadas += 1
        else:
            passagens += 1
        copia_jogada = cria_copia_goban (goban)  
# Utilização da variável jogadas para que na segunda vez que as peças pretas jogarem
# O goban l seja o inicial
        if eh_pedra_preta (pedra):
            l_preta = copia_jogada
            pedra = cria_pedra_branca ()
            if jogadas > 1:
                l = l_preta
        else:
            pedra = cria_pedra_preta ()
            l_branca = copia_jogada
            if jogadas > 1:
                l = l_branca
    print (f"Branco (O) tem {pontos [0]} pontos")
    print (f"Preto (X) tem {pontos [1]} pontos")
    print (goban_para_str (goban))    
    return pontos [0] > pontos [1]

