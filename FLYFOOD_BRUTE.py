import itertools as it #Importando a biblioteca itertools
import time

ini = time.time()
'''__Abrindo e lendo o arquivo de texto com a matriz__'''
with open("rota.txt", "r") as rotas:
    rota = rotas.read()


'''__Transformando a matriz do arquivo em uma matriz para o codigo__'''
rota = [x.split() for x in rota.split('\n')]


'''___Função procurando por pontos___'''
def lookingForPointsOut(i, j, pontos = [], allcomb = []):
    global rota
    j +=1
    #Aqui vai ler cada item de cada linha da matriz recursivamente
    def lookingForPointsIn(i, j):
        if j < len(rota[i]):
            #Vai considerar apenas ods itens que não forem O's ou um R
            if rota[i][j] != 'R' and rota[i][j] != '0':
                pontos.append(rota[i][j])
            else:
                pass
            lookingForPointsIn(i, j+1)
        else:
            return 0
    #Aqui vai acessar cada linha da matriz recursivamente
    lookingForPointsIn(i, j)
    j = -1
    i += 1
    if i < len(rota):

        lookingForPointsOut(i, j, pontos)
    else:
        pass
    #Aqui utilizando a biblioteca itertools para fazer a permutação de cada ponto
    #gerando cada percurso possivel
    allcomb = list(it.permutations(pontos))
    return pontos, allcomb


'''___Função procurando pelo ponto de inicio___'''
def lookingForR(i):
    global rota, pointr
    if 'R' in rota[i]:
        #Procura por R na matriz
        pointr = (i, rota[i].index('R'))
        
    else:
        lookingForR(i+1)
    return pointr


'''__Função que calcula a distancia entre os pontos__'''
def Distance( i, ponto, pontoP, linha):
    
    #Armazena na variável 'momentum' a localização
    #do proximo ponto a ser calculado
    momentum = (i, linha.index(ponto))
    #O calculo da distancia entre os dois pontos
    #que é o mesmo da diferença entre os dois
    p1 = (pontoP[0] - momentum[0])   
    p2 = (pontoP[1] - momentum[1])

    if pontoP[0] - momentum[0] < 0:
        p1 = abs(pontoP[0] - momentum[0])
    if pontoP[1] - momentum[1] < 0:
        p2 = abs(pontoP[1] - momentum[1])
    #Caso os valores da subtração dem negativos, é utilizado a função "abs()" do python
    #essa função tranforma o valor em absoluto
    #Após conseguir a diferença, se soma os valores
    point_value = p1 + p2

    return momentum, point_value


'''__Função que calcula o retorno ao ponto R__'''
def comeBack( ponto, pointr):
    
    
    #O calculo é o mesmo da função Distance, porém apenas com o Ponto R
    p1 = (pointr[0] - ponto[0])   
    p2 = (pointr[1] - ponto[1])

    if p1 < 0:
        p1 = abs(pointr[0] - ponto[0])
    if p2 < 0:
        p2 = abs(pointr[1] - ponto[1])
    
    point_value = p1 + p2

    return point_value


'''__Função que chama a função 'Distance' e conferir se o percurso entregue é mais curto que o calculado anterior__'''
def calcDis(i, point, dronometros_m, ponto, seq, pontoR, caminho, dronometros):
    global pontos
    #O For Loop vai iterar pelo percurso ou sequencia que foi entregue
    for k in seq:
        #Aqui vai iterar por cada linha até encontrar a linha na qual o ponto 'k' está
        for i in range(len(rota)):
            if k in rota[i]:
                #Quando encontrado a linha, ele entrega e chama a função 'Distance'
                ponto, ponto_valor = Distance(i, k, point, rota[i])
                dronometros_m += ponto_valor
                point = ponto
        else:
            pass
    
    #Após ter passado por todos os pontos do percurso, ele faz o calculo do retorno ao ponto 'R'
    ponto_valor = comeBack(point, pontoR)
    dronometros_m += ponto_valor

    #Com os calculos concluidos é comparado com o melhor percurso encontro até o momento
    if dronometros_m < dronometros or dronometros == 0:
        #Caso seja, as váriaveis que armazenavam os melhores valores recebem os valores calculados agora
        dronometros = dronometros_m
        caminho = []
        caminho += seq
        #e é retornado os novos valores
        return caminho, dronometros
    
    else:
        #Caso não, são retornados os valores anteriores
        return caminho, dronometros
    


'''__Função que irá iniciar o codigo e chamar as outras funções'''        
def Start(caminho = [], pointr = (), dronometros = 0):

    #Aqui é chamada a função que irá entregar todos os pontos e a permutação
    pontos, allcomb = lookingForPointsOut(0, -1)

    #Aqui é chamada a função que irá devolver a localização do ponto R
    pontoR = lookingForR(0)
    pointr = pontoR


    #variável que irá receber a sequencia em formato de String
    caminho_st = ''

    #Esse For Loop irá iterar por cada um dos percursos
    for i in range(len(allcomb)):
        #Aqui cada um dos percursos irá ser entregue para a função 'CalcDis' 
        #e irá armazenar os valores armazenados nas váriaveis 'Caminho' e 'Dronometros'
        caminho, dronometros = calcDis(0, pointr, 0, (), allcomb[i], pontoR, caminho, dronometros)
    
    #Esse For Loop irá passa cada ponto dentro do caminho para uma String
    for j in caminho:
        caminho_st += j + ' '

    return caminho_st, dronometros
        
        


#Aqui a função 'Start' é chamada e armazena os valores nas váriaveis 'Caminho' e 'Dronometros'
caminho, dronometros = Start()
print(caminho)
end = time.time()
print(end - ini)

