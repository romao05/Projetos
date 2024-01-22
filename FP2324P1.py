''' Este algoritmo é constituido por 14 funções distintas que podem
ser usadas para descobrir várias características de um território,
que corresponde a um tuplo que é constituido por um determinadoa 
nº de linhas horizontais e verticais, sendo que as primeiras não
podem ser mais de 99 e menos de 1, enquanto que as segundas não 
podem ser menos do que 1 e mais do que 26. Cada interceção entre
linhas verticais e horizontais pode conter uma montanha 
(representada por um 1 dentro do tuplo) ou um vale 
(reprersentado por um 0 dentro do tuplo).
As características que o código identifica atravéz de várias funções
são o número de montanhas, o número de vales, o número de cadeias de montanhas,
pode também verificar a existencia de ligações entre duas interseções,
entre outras.'''




def eh_territorio (arg):

    ''' A função eh_territorio vai receber um argumento e vai verificar se
     este cumpre com os requisitos que determinam um território.
     Se o tuplo introduzido for um território a função devolve
     True e se não for vai devovler False'''
    
    if not isinstance (arg,tuple) or arg == () or not isinstance (arg[0],tuple):
        return False
# Verificar se o tuplo tem o nº mínimo de caminhos para ser um território
    if len (arg) > 0 and len(arg[0]) > 0 and len(arg) < 27 and len(arg[0]) < 100:
        for i in range(len(arg)):
            if not isinstance(arg[i], tuple):
                return False
# Função if para verificar se o Nh é igual para todos os Nv
            if len (arg[0]) == len (arg[i]):
                for j in range(len(arg[i])):
                    if not isinstance (arg [i] [j], int) or \
                        (arg [i] [j] != 0  and arg [i] [j] != 1):
# Verifica se o valor da interseção é um inteiro e se este é igual a 0 ou 1
                        return False
            else:
                return False
        return True
    return False



def obtem_ultima_intersecao (t):

    ''' Esta função recebe como argumento um territótio e vai devolver
    a última interceção do respetivo território.'''

    intercecao = (chr(64 + len(t)), len (t[0]))
    return intercecao



def eh_intersecao (arg):

    ''' Esta função recebe um argumento de qualquer tipo e vai verificar se
    este corresponde a uma interceção. Se o argumento for uma
    interceção a função vai devolver o boleano True, caso contrário
    irá devolver False.'''

# Função if para verificar se as coordenadas inseridas correspondem a 
# uma string seguida de um número inteiro e nada mais
    if  not isinstance (arg,tuple) or len(arg) != 2 or \
        not isinstance (arg[0],str)  or type (arg [1]) != int:
        return False
# Função if para verificar se os valores inseridos correspondem aos de
#uma interceção do território
    if len(arg[0]) != 1 or arg [1] < 1 or arg [1] > 99 or \
        ord(arg[0]) < 65 or ord(arg[0]) > 90 :
        return False
    return True




def eh_intersecao_valida (t, i):

    ''' Esta função recebe um teritótio e uma interseção e vai verificar
    se a interseção inserida pertence ao território inserido. Se pertencer vai
     devolver o boleano True e se não perterncer devolve False.'''
    
    if i [1] <= len(t[0]) and i[1] > 0 and (ord(i[0]) - 65) in range(len(t)):
        return True
    return False



def eh_intersecao_livre (t,i):

    ''' Esta função vai receber um território e uma interseção do mesmo 
    e verifica se esta corresponde a uma interseção vazia/ livre. Se esta
    condição se verificar a função devolve o boleano True, caso contrário
    vai devolver False.'''

    if t[ord(i[0]) - 65] [i[1] - 1] == 1:
        return False
    return True



def obtem_intersecoes_adjacentes (t,i):

    ''' Esta função recebe dois argumentos, um tuplo correspondente
    a um território e uma interseção do mesmo e vai devolver um tuplo
    que contém as interceções adjacentes ao ponto dado como argumento.'''

# Operações para verificar as interceções adjacentes
    direita = (chr(ord(i[0]) + 1), i[1] )   
    esq = (chr(ord(i[0]) - 1), i[1] )
    cima = (i[0], i[1] + 1)
    baixo = (i[0], i[1] - 1) 
# Criar lista para ver quais das 4 operações definidas acima podem ser realizadas
    possiveis_adj = [baixo, esq, direita, cima]

    adj = []
# Formulação de uma lista com os pontos adjacentes a i que pertencem ao território
    for l in possiveis_adj:
        if l[1] > 0 and l[1] < len(t[0]) + 1 and ord(l[0]) - 65 in range(len(t)):
            adj.append(l) 
    return tuple(adj)



def ordena_intersecoes (tup):

    ''' Esta função recebe como argumento um tuplo de interceções que pode
    ou não estar vazio e vai devolver um tuplo com as mesmas interseções
    ordenadas pela ordem de leitura do território.'''

    if len(tup) == 0:   
        return ()
    lista = list (tup)  
 # Uso a função lambda dentro do sort para indicar que a ordenação da
 #  minha lista deve ser feita com base nos números e quando estes são
 #  iguais, a organização é feita por ordem alfabética
    ordem_leitura = sorted(lista, key= lambda x: (x[1], x[0]))
    return tuple(ordem_leitura)



def territorio_para_str (t):

    ''' Esta função recebe um argumento qualquer e vai verificar se este
    corresponde a um território. Caso seja um território, a função
    vai devolver uma linha de texto que representa o território graficamente.'''

    if not eh_territorio (t):
        raise ValueError ("territorio_para_str: argumento invalido")
    string = "  "
    vertical = ""
    linhas_horizontais = len (t[0])
 # String que vai conter todas as letras correspondentes a caminhos verticais
    for i in range(len(t)):
          vertical += f" {chr(65 + i)}" 
    string += vertical + "\n"
# Criação de um loop que vai fazer a parte interior da sting visto que esta
# é repetitiva em termos estruturais
    for j in range(len(t[0]) - 1, -1 ,-1):  
        meio_str = ""
        for g in range(len(t)):
            if t [g] [j] == 0:
                marca = ". "
            elif t [g] [j] == 1:
                marca = "X "
            meio_str += marca
# criação de uma f string para garantir igualdade estrutural no interior da str
        if linhas_horizontais  > 9:
            string += f"{j+1:2d} {meio_str}{j+1:2d}\n"
        if linhas_horizontais < 10:
            string += f" {j+1} {meio_str} {j+1}\n"             
    string += "  " + vertical
    return string


def obtem_cadeia (t,i):
    
    ''' Esta função vai receber um território e uma interseção que pode estar
    ocupada por uma montanha ou pode estar livre e vai devolver um tuplo
    constituido por todas as interceções que estão conectadas ao
    ponto inserido na ordem de leitura do território.'''

    if not eh_territorio (t) or not eh_intersecao (i) or\
        not eh_intersecao_valida (t,i):
        raise ValueError ("obtem_cadeia: argumentos invalidos")
    int_conetadas = [i]
    for k in int_conetadas:  
            int_adjs = list(obtem_intersecoes_adjacentes (t,k)) 
# Lista com interseções adjacentes
            for l in int_adjs:
                if l not in int_conetadas and\
                    t [ord(l[0]) - 65] [l[1]-1] == t [ord(k [0]) - 65] [k [1] - 1]:
# Condição que impede o aparecimento de interceções iguais na lista final
# vai também verificar se estas são ou não montanhas
                    int_conetadas += (l,)  
    return tuple (ordena_intersecoes(int_conetadas))



def obtem_vale (t,i):
    
    ''' Esta função vai receber um tuplo e uma interseção e se esta estiver 
    ocupada por uma montanha, a função vai devolver os vales da cadeia de 
    montanhas a que a interseção pertence, sendo que vales correspondem 
    a interceções adjacentes a interseções ocupadas por montanhas.'''
    
    if not eh_territorio (t) or not eh_intersecao(i) or \
        not eh_intersecao_valida (t,i) or eh_intersecao_livre (t,i):
        raise ValueError ("obtem_vale: argumentos invalidos")
    montanhas = obtem_cadeia (t,i) 
# Vai dar a cadeia de montanhas ordenada
    vales = ()
    for k in montanhas: 
# Vai ler a cadeia de montanhas e para cada "extremidade " vai ver 
# as respetivas interseções adjacentes
        possiveis_vales = obtem_intersecoes_adjacentes (t,k)
        for l in possiveis_vales: 
            if l not in vales and eh_intersecao_livre (t,l): 
# Faz a adição das interseções livres adjacentes a k, evitando repetições
                vales += (l,)
    return ordena_intersecoes (vales)



def verifica_conexao (t, i1, i2):
    
    ''' Esta função vai receber um tuplo e duas interseções, se os argumentos
    passarem na verificação de dados, esta vai devolver o boleano
    True se as duas interseções estiverem conectadas e False caso contrário.'''
    
    if not eh_territorio(t) or not eh_intersecao_valida(t,i1) or\
        not eh_intersecao_valida(t,i2):
        raise ValueError ("verifica_conexao: argumentos invalidos")
    cadeiai1 = obtem_cadeia (t,i1)
    if i2 in cadeiai1:
        return True
    return False

def calcula_numero_montanhas (t):
    
    ''' Esta função receb como argumento um tuplo e depois de verificar
    que este corresponde a um território vai devolver o numero
    de montanhas no território inserido.'''
    
    if not eh_territorio (t):
        raise ValueError ("calcula_numero_montanhas: argumento invalido")
    num = 0
    for k in range(len(t)):
        for l in range(len(t[0])):
            if not eh_intersecao_livre (t,(chr(65 + k), l+1)):
                num += 1
    return num


def calcula_numero_cadeias_montanhas (t):
    
    ''' Esta função recebe um tuplo e depois de verificar que este 
    corresponde a um território vai devolver o número de cadeias
    de montanhas do mesmo. Se o tuplo não corresponder a um
    teritório a função irá levantar um erro de valor.'''
    
    if not eh_territorio (t):
        raise ValueError ("calcula_numero_cadeias_montanhas: argumento invalido")
    intersecoes = []
    cadeias = 0
    for k in range(len(t[0])):
        for l in range(len(t)):
            intersecoes += ((chr(65 + l), k+1),) 
# Inserir na lista todas as interseções do território
    for z in intersecoes:
        if not eh_intersecao_livre (t, z): 
# Lê as interseções do território, e adiciona 1 ao nº de cadeias se encontrar uma
            cadeia = obtem_cadeia (t,z)    
            cadeias += 1
            for a in cadeia:
                intersecoes.remove (a) 
# Vai, também remover todas as interseções pertencentes a 
# essa cadeia da lista global de interseções
    return cadeias



def calcula_tamanho_vales (t):
    
    ''' Esta função recebe um tuplo e depois de verificar se este corresponde
    a um território vai dar erro, se esta condição não se verificar,
    ou caso o tuplo corresponda a um território, vai devolver
    o número de vales que existem no território inserido como argumento.'''
    
    if not eh_territorio (t):
        raise ValueError ("calcula_tamanho_vales: argumento invalido")
    vales = ()
    for k in range (len(t)):
        for p in range(len(t[0])):
            if t [k] [p] == 1:
                vales_possiveis = obtem_intersecoes_adjacentes (t,(chr(65 + k), p+1))
                for l in vales_possiveis:
                    if l not in vales and eh_intersecao_livre (t, l):
                        vales += (l,)
    return len(vales)