% Miguel Romao -- ist1109593
:-use_module(library(clpfd)).
:-set_prolog_flag(answer_write_options,[max_depth(0)]).
:-['puzzlesAcampar.pl'].
% Segue-se o codigo


% Predicado que devolve a Vizinhanca de uma coordenada
% (cima,baixo,esquerda,direita) pela ordem de leitura do tabuleiro.
vizinhanca((L,C),Vizinhanca):-
    L1 is L+1, C1 is C-1,
    L2 is L-1, C2 is C+1,
    Vizinhanca = [(L2,C),(L,C1),(L,C2),(L1,C)].

% Predicado que devolve a Vizinhanca alargada de uma coordenada
% (cima,baixo,esquerda,direita e diagonais) pela ordem de leitura do
% tebuleiro.
vizinhancaAlargada((L,C),VizinhancaAlargada):-
    L1 is L+1, C1 is C+1,
    L2 is L-1, C2 is C-1,
    VizinhancaAlargada = [(L2,C2),(L2,C),(L2,C1),
                          (L,C2),(L,C1),
                          (L1,C2),(L1,C),(L1,C1)].


% Predicado que devolve um lista contendo todas as coordenadas do
% tabuleiro segundo a ordem de leitura do mesmo.
todasCelulas(Tabuleiro,TodasCelulas):-
    length(Tabuleiro,Max),
    % O findall vai usar o predicado between para criar todas as coordenadas do tabuleiro e vai inseri-las na lista coordenadas.
    findall((L,C),(between(1,Max,L),between(1,Max,C)),Coordenadas),
    Coordenadas = TodasCelulas.

% Predicado que vai devolver todas as coordenadas das celulas que tem um
% Objecto igual ao argumento "Objecto" na lista TodasCelulas, segundo a
% ordem de leitura do tabuleiro.
todasCelulas(Tabuleiro,TodasCelulas,Objecto):-
    todasCelulas(Tabuleiro,Coordenadas),
    % Findall usado para criar a Lista TodasCelulas com as coordenas cujo elemento da celula correspondente e igual ao Objecto dado como argumento.
    findall((L,C),
            %Primeira parte do findall usa member para percorrer todos os elementos da lista Coordenadas (percorre as coordenadas todas do tabuleiro).
            (member((L,C),Coordenadas),
             %  Dois nth1 para obter o elemento que se encontra em cada Celula do tabuleiro.
             nth1(L,Tabuleiro,Linha),nth1(C,Linha,Elemento),
             %Verificacao da igualdade Elemento/Objecto, verificando primeiro o caso em que o Objecto e uma variavel atraves do predicado var(Objecto).
             ((var(Objecto),var(Elemento));Elemento == Objecto)),TodasCelulas).


% Predicado que vai criar duas listas "ContagemLinhas" e
% "ContagemColunas" cujos elementos correspondem a quantidade de tendas
% por linha.
calculaObjectosTabuleiro(Tabuleiro,ContagemLinhas,ContagemColunas,Objecto):-
    length(Tabuleiro,Tam),
    todasCelulas(Tabuleiro,CelulasObjeto,Objecto),
    % Utilizacao do findall para criar as Listas ContagemLinhas e ContagemColunas.
    findall(X,
            (between(1,Tam,Linha),
             % Findall para criar uma lista com todos os elementos da lista com todos os elementos da Linha que esta a ser analisada que tem um Objecto
             findall((L,C),(member((L,C),CelulasObjeto),L = Linha),Lista),
             %Uso length para saber quantas celulas com tendas ha por linha
             length(Lista,X)),ContagemLinhas),
    %Utilizacao do findall para fazer o mesmo para as colunas
    findall(X,(between(1,Tam,Coluna),findall((L,C),(member((L,C),CelulasObjeto),C = Coluna),Lista1),length(Lista1,X)),ContagemColunas).

% Predicado que e verdade se as celulas das coordenadas (L,C) estiver
% vazia ou for relva
celulaVazia(Tabuleiro,(L,C)):-
    nth1(L,Tabuleiro,Linha),
    nth1(C,Linha,Elemento),
    (var(Elemento);Elemento == r),
    !.

% Predicado que vai inserir uma tenda (t) ou relva (r) na celula com
% coordenada (L,C).
insereObjectoCelula(Tabuleiro,TendaOuRelva,(L,C)):-
    %Utilizacao do celulaVazia para verificar a disponibilidade da celula
    celulaVazia(Tabuleiro,(L,C)),
    %Colocacao do objeto na Celula
    nth1(L,Tabuleiro,Linha),
    nth1(C,Linha,Local),
    Local = TendaOuRelva.

% Predicado que vai inserir um determinado objecto entre duas posicoes,
% que tambem sao alteradas se estiverem vazias. este e feito usando
% recursao.
insereObjectoCelula(_,_,(_,_)):-!.
insereObjectoEntrePosicoes(_,_,(_,C1),(_,C2)):-
    C1 > C2.
insereObjectoEntrePosicoes(Tabuleiro,TendaOuRelva,(L,C1),(L,C2)):-
    C1 =< C2,
    insereObjectoCelula(Tabuleiro,TendaOuRelva,(L,C1)),
    NovoC is C1+1,
    insereObjectoEntrePosicoes(Tabuleiro,TendaOuRelva,(L,NovoC),(L,C2)).

% Predicado auxiliar que e responsavel por colocar relva em todas as
% celulas cujas coordenadas estao contidas na lista dada como argumento.
colocaRelvaNaLinha([],_,_).
colocaRelvaNaLinha([H|T],Limite,Tabuleiro):-
    insereObjectoEntrePosicoes(Tabuleiro,r,(H,1),(H,Limite)),
    colocaRelvaNaLinha(T,Limite,Tabuleiro).

% Predicado que recebe um puzzle e coloca relvas nas linhas onde nao
% podem ser inseridas mais tendas
relva((Tabuleiro,MaxLinhas,MaxColunas)):-
    calculaObjectosTabuleiro(Tabuleiro,ContagemLinhas,ContagemColunas,t),
    length(Tabuleiro,MaxIndex),
    % Uso do findall para criar uma lista que contenha os indices de todas as linhas onde foi atingido o numero maximo de tendas.
    findall(L,(nth1(L,ContagemLinhas,X),nth1(L,MaxLinhas,X)),LinhasParaRelva),
    % Colocacao de relva nessas linhas usando o predicado auxiliar "colocaRelvaNaLinha"
    colocaRelvaNaLinha(LinhasParaRelva,MaxIndex,Tabuleiro),
    % Uso da funcao transpose para transpor o Tabuleiro.
    transpose(Tabuleiro,TabTransposto),
    % Repeticao do mesmo processo para as colunas.
    findall(C,(nth1(C,ContagemColunas,Y),nth1(C,MaxColunas,Y)),ColunasParaRelva),
    colocaRelvaNaLinha(ColunasParaRelva,MaxIndex,TabTransposto).



% Predicado inacessiveis recebe como argumento um tabuleiro e vai
% colocar relva em todas as posicoes inacessiveis do mesmo.
colocaRelva([],_).
colocaRelva([H|T],Tabuleiro):-
    insereObjectoCelula(Tabuleiro,r,H),
    colocaRelva(T,Tabuleiro).

% Predicado que vai identificar as posicoes inacessiveis e vai colocar
% relva nas mesmas.
inacessiveis(Tabuleiro):-
    todasCelulas(Tabuleiro,Arvores,a),
    todasCelulas(Tabuleiro,TodasCelulas),
    % Uso da funcao subtract para retirar da lista com todas as coordenadas do tabuleiro, as coordenadas correspondentes a celulascom arvores.
    subtract(TodasCelulas,Arvores,TodasCelulasSemArvore),
    % Uso do findall para criar uma lista que contem as vizinhancas de todas as arvores do tabuleiro.
    findall(Vizinhanca,(member((L,C),Arvores),vizinhanca((L,C),Vizinhanca)),Vizinhancas),
    % Uso do predicado flatten para converter a lista "Vizinhancas", composta por outras listas, numa unica lista composta por todas as coordenadas
    %que pertenciam as vizinhancas das arvores (coordenadas acessiveis).
    flatten(Vizinhancas,Acessiveis),
    % Uso de funcao subtract para retirar da lista que cintem todas as celulas do tabuleiro exceto as que tem arvores, todas as celulas
    % que pertencem as vizinhancas das arvores, sendo, por isso, acessiveis.
    subtract(TodasCelulasSemArvore,Acessiveis,Inacessiveis),
    % Posto isto podemos usar o predicado auxiliar "colocaRelva" para colocar relva em todas as celulas inacessiveis.
    colocaRelva(Inacessiveis,Tabuleiro).


% Predicado auxiliar para colocar tendas nas celulas correspondentes a
% as coordenadas que se encontram na lista dada como argumento.
colocaTendas([],_).
colocaTendas([H|T],Tabuleiro):-
    insereObjectoCelula(Tabuleiro,t,H),
    colocaTendas(T,Tabuleiro).


% Predicado auxiliar responsavel por verificar linha a linha, se o
% numero de tendas em falta e igual ao numero de lugares vazios e quando
% isso acontecer, vai colocar as tendas nos devidos locais.
aproveitaaux(_,[],_,_).
aproveitaaux(Tabuleiro,[H|T],Livres,Max):-
    H = [Linha,TendasEmFalta],
    % Uso do findall para obter uma lista com as coordenadas das celulas livres da linha que esta
    % a ser verificada.
    findall((Linha,C),member((Linha,C),Livres),LivresNaLinha),
    length(LivresNaLinha,X),
    % Comparacao entre o numero de tendas em falta e o numero de celulas vazias na linha a ser estudada
    X \= TendasEmFalta,
    % Chamada recursiva para avaliar a linha seguinte.
    aproveitaaux(Tabuleiro,T,Livres,Max).

aproveitaaux(Tabuleiro,[H|T],Livres,Max):-
    H = [Linha,_],
    % Uso do findall para obter uma lista com as coordenadas das celulas vazias da linha a avaliar.
    findall((Linha,C),member((Linha,C),Livres),LivresNaLinha),
    % Devido ao caso estudado acima, podemos concluir que o numero de celulas livres na linha em estudo
    % e igual ao numero de tendas em falta por isso as tendas sao colocadas pelo predicado
    %auxiliar aproveitaaux.
    colocaTendas(LivresNaLinha,Tabuleiro),
    % Uso da funcao subtract para retirar da lista de celulas livres aquelas onde forma
    % colocadas tendas.
    subtract(Livres,LivresNaLinha,NovoLivres),
    %Chamada recursiva para avaliar a linha seguinte.
    aproveitaaux(Tabuleiro,T,NovoLivres,Max).

% Predicado responsavel colocar tendas nas linhas e colunas onde o
% numero de tendas em falta e igual ao numero de celulas vazias
aproveita(Puzzle):-
    Puzzle = (Tabuleiro,MaxLinhas,_),
    % Uso de funcao todasCelulas para obter uma lista com todas as coordenadas livres do tabuleiro.
    todasCelulas(Tabuleiro,Livres,_),
    length(Tabuleiro,Max),
    % Uso da funcao calculaObjectosTabuleiro para obter o numero de tendas que existem em cada linha do tabuleiro.
    calculaObjectosTabuleiro(Tabuleiro,ContagemLinhas,_,t),
    % Uso do findall para criar uma lista de listas com cada uma tem dois elemento, o primeiro indica o indice de uma linha
    % Onde ainda falta colocar tendas e o segundo indica o numero de tendas que faltam colocar na respetiva linha.
    findall([L,TendasEmFalta],(nth1(L,ContagemLinhas,X),nth1(L,MaxLinhas,Y),X\=Y,TendasEmFalta is Y - X),LinhasParaTendas),
    % Chamada ao predicaod auxiliar aproveitaaux que vai vazer as restantes verificacoes e vai colocar as tendas nos devidos lugares.
    aproveitaaux(Tabuleiro,LinhasParaTendas,Livres,Max).


%Predicado que coloca relva nas vizinhancas alargadas de todas as tendas
limpaVizinhancas((Tabuleiro,_,_)):-
    todasCelulas(Tabuleiro,Tendas,t),
    length(Tabuleiro,Limite),
    % Uso do findall para criar uma lista de listas correspondentes as vizinhancas alargadas de
    %todas as tendas.
    findall(VizinhancaAlargada,(member((L,C),Tendas),vizinhancaAlargada((L,C),VizinhancaAlargada)),VizinhancasAl),
    % Uso do flatten para formar uma lista com todas as coordenadas que correspondem as celulas
    % das vizinhancas alargadas da stendas.
    flatten(VizinhancasAl,VizinhancasAlargadas),
    % Uso do findall para retirar da lista das vizinhancas todas as coordenadas nao pertencem ao tabuleiro
    findall((L,C),(member((L,C),VizinhancasAlargadas),0 < L,L < Limite+1, 0 < C, C < Limite+1),LocaisParaRelva),
    % Uso do predicado auxiliar "colocaRelva" para colocar relva em todos
    %os elementos da lista resultante da linha de codigo anterior.
    colocaRelva(LocaisParaRelva,Tabuleiro).


% Predicado que identifica todas as arvores que apenas tem uma celula
% vazia na sua vizinhanca onde se pode colocar uma tenda e coloca-a.
unicaHipotese((Tabuleiro,_,_)):-
    % Criacao de 3 listas de coordenadas, uma com as das celulas vazias, uma as das tendas e outra com as das arvores, respetivamente.
    todasCelulas(Tabuleiro,Vazias,_),
    todasCelulas(Tabuleiro,Tendas,t),
    todasCelulas(Tabuleiro,Arvores,a),
    % Uso do findall para criar uma lista com todas as vizinhancas de arvores onde apenas 1 dos 4 elementos corresponde a uma celula vazia.
    findall(Vizinhanca,(member(Arvore,Arvores),vizinhanca(Arvore,Vizinhanca),intersection(Vizinhanca,Vazias,VizVazia),length(VizVazia,1)),VizArv1Vaz),
    % Uso do findall para criar uma lista com todas as vizinhancas de arvores onde nenhum dos elementos corresponde a uma celula ocupada por uma tenda.
    findall(Vizinhanca,(member(Arvore,Arvores),vizinhanca(Arvore,VizinhancaArv),intersection(VizinhancaArv,Tendas,VizTendas),length(VizTendas,0)),Viz0Tendas),
    % Uso do intersection para criar uma lista que apenas contenha as vizinhancas de arvores
    % cujos elementos nao estao ocupados por tendas e apenas um deles corresponde a uma celula vazia.
    intersection(VizArv1Vaz,Viz0Tendas,VizUH),
    % Uso de flatten para obter uma lista com todas as coordenadas contidas na lista obtida no intersection.
    flatten(VizUH, VizinhancasUH),
    % Uso do intersection para obter uma lista com todas as celulas que correspondem as unicas hipoteses.
    intersection(VizinhancasUH,Vazias,UnicasHipoteses),
    %Uso do predicado auxiliar "colocaTendas" para colocar tendas em todos os elementos da lista "UnicasHipoteses".
    colocaTendas(UnicasHipoteses,Tabuleiro).


% Predicado que verifica se todas a sarvores podem ser associadas a uma
% unica tenda
valida([],_).
valida([H|T],LTen):-
    %Uso do findall para criar uma lista com todos os membros da vizinhanca da arvore que esta a ser estudada
    % que correspondem a tendas.
    findall(X,(vizinhanca(H,Vizinhanca),member(X,Vizinhanca),member(X,LTen)),TendasNaViz),
    flatten(TendasNaViz,TendasNaVizinhanca),
    % Para haver que seja possivel fazer a associacao o compirmento dessa lista tem que ser
    % maior ou igual a 1.
    length(TendasNaVizinhanca,X),
    X >= 1,
    valida(T,LTen).



