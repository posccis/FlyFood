import itertools as it
import operator #Importando a biblioteca itertools
import random as rm
import time



ini = time.time()
'''__Abrindo e lendo o arquivo de texto com a matriz__'''
with open("rota.txt", "r") as rotas:
    rota = rotas.read()


'''__Transformando a matriz do arquivo em uma matriz para o codigo__'''
rota = [x.split() for x in rota.split('\n')]



'''___Função procurando por pontos___'''
def lookingForPointsOut(i, j, pontos, allcomb):
    global rota
    
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
    j =0
    i += 1
    if i < len(rota):

        lookingForPointsOut(i, j, pontos, allcomb)
    else:
        pass
    #Aqui utilizando a biblioteca itertools para fazer a permutação de cada ponto
    #gerando cada percurso possivel
    allcomb = list(it.permutations(pontos))
    allcomb1 = []
    for i in allcomb:
        allcomb1.append(list(i))
        
    pop = allcomb1[rm.randrange(len(allcomb))]
    return pop 


'''__ Criação da classe Fitness
   __ Aqui será avaliada a aptidão das soluções, ou dos conjuntos de rotas __'''
class Fitness():
    def __init__(self, populacao, pontoR):
        #Os atributos iniciais
        self.populacao = populacao
        self.pontoR = pontoR
        self.dronometros = 0
        self.point = ()
        self.i = -1
        
    '''__Função que calcula a distancia entre os pontos__'''
    def Distance(self, i, ponto, pontoP, linha):
        
        #Armazena na variável 'momentum' a localização
        #do proximo ponto a ser calculado
        momentum = (i, linha.index(ponto))
        #O calculo da distancia entre os dois pontos
        #que é o mesmo da diferença entre os dois
        p1 = abs(pontoP[0] - momentum[0])   
        p2 = abs(pontoP[1] - momentum[1])


        #Caso os valores da subtração dem negativos, é utilizado a função "abs()" do python
        #essa função tranforma o valor em absoluto
        #Após conseguir a diferença, se soma os valores
        point_value = p1 + p2

        return momentum, point_value


    '''__Função que calcula o retorno ao ponto R__'''
    def comeBack(self, ponto, pointr):
        
        
        #O calculo é o mesmo da função Distance, porém apenas com o Ponto R
        p1 = abs(pointr[0] - ponto[0])   
        p2 = abs(pointr[1] - ponto[1])


        
        point_value = p1 + p2

        return point_value


    '''__Função que calcula a distancia atraves da chamada da função 'distance'__'''
    def calcDis(self, i):
        global rota

        #Caso não tenha recebido nenhum ponto, o primeiro ponto é o R
        if self.point == ():
            self.point = self.pontoR
        #O For Loop vai iterar pelo percurso ou sequencia que foi entregue
        for k in self.populacao:
            #Aqui vai iterar por cada linha até encontrar a linha na qual o ponto 'k' está
            for i in range(len(rota)):
                if k in rota[i]:
                    #Quando encontrado a linha, ele entrega e chama a função 'Distance'
                    ponto, ponto_valor = self.Distance(i, k, self.point, rota[i])
                    self.dronometros += ponto_valor
                    self.point = ponto
            else:
                pass
        
        #Após ter passado por todos os pontos do percurso, ele faz o calculo do retorno ao ponto 'R'
        ponto_valor = self.comeBack(self.point, self.pontoR)
        self.dronometros += ponto_valor
        #Retorna a distancia
        return self.dronometros
    '''__ Aqui é calculada a aptidão da população e é feita a chamada da função 'calcDis'__'''
    def fitnessValue(self):
        self.i += 1
        
        distancia = float(self.calcDis(self.i))

        if distancia == 0.0: 
            fitness = 1 
            return fitness
        else:
            fitness = 1/distancia      
            return fitness
            

'''__ Função que procura pela posição do R na matriz __'''
def lookingForR(i):
    global rota, pointr
    if i < len(rota):
        if 'R' in rota[i]:
            #Procura por R na matriz
            pointr = (i, rota[i].index('R'))
            
        else:
            lookingForR(i+1)
    return pointr

'''__ Função que gera a população incial __'''
def popInitial(tamanho):
    populacao = []
    for i in range(0, tamanho):
        #Cria a população chamando a função lookingForPointsOut
        #que retorna um conjunto aleatorio de possiveis soluções
        populacao.append(lookingForPointsOut(i=0, j=0, pontos = [], allcomb = []))
    return populacao

    
'''__ Aqui é instanciada a classe Fitness para obter a aptidão de cada possivel solução da populaçãp e listar em um dicionario'''
def bestFitness(populacao):
    lista = {}
    for i in range(0, len(populacao)):
        lista[i] = Fitness(populacao[i], lookingForR(i=0)).fitnessValue()
    return sorted(lista.items(), key=operator.itemgetter(1), reverse=True)

'''__ Função que atraves de eleitismo deve separar dos melhores individuos/soluções da população que foi analisada __'''
def elitismo(bestFitness, bestLen):
    resultado = []
    a = bestFitness[rm.randint(0, len(bestFitness) - 1)]
    b = bestFitness[rm.randint(0, len(bestFitness) - 1)]
    for i in range(0, bestLen):
        resultado.append(bestFitness[i][0])
    for i in range(0, len(bestFitness) - bestLen):
        a =bestFitness[rm.randint(0, len(bestFitness) - 1)][0]
        b = bestFitness[rm.randint(0, len(bestFitness) - 1)][0]
        while b == a:
            b = bestFitness[rm.randint(0, len(bestFitness) - 1)][0]
        if a >= b:
            resultado.append(a)
        else:
            resultado.append(b)
    return resultado
 
'''__ Função que irá determinar os individuos que farão parte do cruzamento __'''   
def seleCross(populacao, resultado):
    selecao = []
    for i in range(0, len(resultado)):
        index = resultado[i]
        selecao.append(populacao[index])
    return selecao   



'''__ Função que irá fazer o cruzamento atraves de cross over entre cada par de individuos que receber e retornar o seu 'filho' __'''
def crossOver(solA, solB):
    filho = []
    childSA = []
    childSB = []
    
    geneA = int(rm.random() * len(solA))
    geneB = int(rm.random() * len(solB))
    
    inicio = min(geneA, geneB)
    fim = max(geneA, geneB)
    
    for i in range(inicio, fim):
        childSA.append(solA[i])
        
    childSB = [item for item in solB if item not in childSA]
    
    filho = childSA + childSB
    
    return filho


'''__ Função que irá iterar entre todos os selecionados da função 'elitismo' e passa-los para função de cruzamento CrossOver afum de gerar o restante da nova geração __'''
def popCrossOver(selecao, bestLen):
    filhos = []
    lgth = len(selecao) - bestLen
    pool = rm.sample(selecao, len(selecao))
    
    for i in range(0, bestLen):
        filhos.append(selecao[i])
        
    for i in range(0, lgth):
        filho = crossOver(pool[i], pool[len(selecao) - i - 1])
        filhos.append(filho)
    
    return filhos

'''__ Função que vai testar se o individuo ta dentro da taxa de mutação e, caso esteja, aplicar a mutação trocando a posição de um ponto da rota por outro __'''
def mutacao(individuo, taxa_mutacao):
    for i in range(len(individuo)):
        if(rm.random() < taxa_mutacao):
            prox = int(rm.random() * len(individuo))
            
            pontoa = individuo[i]
            pontob = individuo[prox]
            
            individuo[i] = pontob    
            individuo[prox] = pontoa
    
    return individuo
'''__ Função encarregada de iterar por todos os individuos e aplicar a função 'mutacao' __'''
def popMut(populacao, taxa_mutacao):
    mut = []
    
    for i in range(0, len(populacao)):
        individuo = mutacao(populacao[i], taxa_mutacao)
        mut.append(individuo)
    
    return mut

'''__ Função responsavel por chamar cada função necessária para criar uma nova geração e determinar seus resultados __'''
def novaGeracao(pop, bestLen, taxa_mutacao):
    best = bestFitness(pop)
    resultado = elitismo(best, bestLen)
    selecaoCross = seleCross(pop, resultado)
    filhos = popCrossOver(selecaoCross, bestLen)
    proxima = popMut(filhos, taxa_mutacao)
    return proxima

'''__ Função principal que vai criar a população inicial e, dentro do paramentro de parada, vai criar as proximas gerações para retornar a melhor rota __'''
def run(tamanho, bestLen, taxa_mutacao, parada):
    pop = popInitial(tamanho)
    melhor_dis = [1 / bestFitness(pop)[0][1]]
    
   
    
    for i in range(1, parada + 1):
        pop = novaGeracao(pop, bestLen, taxa_mutacao)
        
        melhor_dis.append(1/bestFitness(pop)[0][1])
        
    bestrouteIndex = bestFitness(pop)[0][0]
    bestroute = pop[bestrouteIndex]
    print(melhor_dis[bestrouteIndex])
    return bestroute


#Declaração da função que vai receber a localização do ponto R
pointr = ()

'''__ A chamada da função principal e os atributos de tamanho da população, tamanho do elitismo, a taxa de mutação e a quantidade de gerações
   __ que também é o parametro de parada __'''
valor_final = run(100, 50, 0.5, 50)
end = time.time()
print(end - ini)
print(valor_final)
    

        
