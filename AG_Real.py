import random
import math
import sys


#x∈[−10,+10]
limites = (-10.0,10.0)
alfa = 0.5

class Individual(object):
    
    def __init__(self, cromossomo = None, x= None):
        self.score = None
        #self.x = x or self._criaNumAleatorio()
        self.cromossomo = cromossomo or self._criaCromossomo()

    def _criaNumAleatorio(self):
        numero = random.uniform(limites[0],limites[1])
        return numero

    #Cria um novo cromossomo do tamanho máximo definido anteriormente.
    def _criaCromossomo(self):
        x = self._criaNumAleatorio()
        return x

    #fitness
    def fitness(self):
        #Decodificação do cromossomo
        #Função objetivo
        x = self.cromossomo
        y = x**2 - 3*x + 4
        #fitness score
        self.score = y
        
    
    def blend_crossover(self,other):
        beta = random.uniform(-alfa,1+ alfa)
        p1 = self.cromossomo
        p2 = other.cromossomo        
        c1 = p1 + beta*(p2-p1)
        c2 = p2 + beta*(p1-p2)
        return c1,c2

    
    
    #crossover
    def crossover_1ponto(self,other):
        #60% de cross
        ponto = random.randint(1, tam_cromossomo - 1)
        
        def mate(p0,p1):
            #Cria uma copia de p0 
            chromosome = p0.cromossomo[:]
            
            chromosome[:ponto] = p1.cromossomo[:ponto]
            child = p0.__class__(chromosome)
            return child
        return mate(self,other), mate(other,self)

    #mutação
    def mutacao(self,gene):
       	self.cromossomo[gene] = int(not self.cromossomo[gene])

    #Função auxiliar para copiar o individuo
    def copy(self):
        clone = self.__class__(self.cromossomo)
        clone.score = self.score
        return clone


class AlgoritmoGenetico(object):

    result = {}

    def __init__(self, tam_populacao, max_geracoes, tx_crossover, tx_mutacao):
        self.tam_populacao = tam_populacao
        self.max_geracoes = max_geracoes
        self.tx_crossover = tx_crossover
        self.tx_mutacao = tx_mutacao
        self.populacao = self._criaPopulacao()

        #inicia o cálculo de fitness 
        for individual in self.populacao:
            individual.fitness()

        #Inicialização da geração
        self.geracao = 0

    #Cria a população com seus individuos/cromossomos
    def _criaPopulacao(self):
        return [Individual() for individual in range(self.tam_populacao)]

    #Condição de parada
    def _objetivo(self):
        return (self.geracao >= self.max_geracoes)

    def auxSort(self):
        for final in range(len(self.populacao), 0, -1):
            exchanging = False

            for current in range(0, final - 1):
                if self.populacao[current].score > self.populacao[current + 1].score:
                    self.populacao[current + 1], self.populacao[current] = self.populacao[current], self.populacao[current + 1]
                    exchanging = True

            if not exchanging:
                break

    #Um passo do algoritmo
    def step(self):
        #Ordenação dos individuos segundo o score
        self.auxSort()
        self._crossover()
        self.geracao += 1
        #self.report()
        self.report2()

    def printPopulacao(self):
        for i in range(self.tam_populacao):
            print(self.populacao[i].x, end = '\t')

    #Crossover proccess
    def _crossover(self):
        #Elistismo
        next_population = [self.best.copy()]
        while len(next_population) < self.tam_populacao:
            mate1 = self._select()
            if random.random() < self.tx_crossover:
                mate2 = self._select()
                #offspring = mate1.crossover_1ponto(mate2)
                offspring = mate1.blend_crossover(mate2)
            else:
                #copia o individuo
                offspring = [mate1.copy()]
            
            
            for individual in offspring:
                print(individual)
                self._mutate(individual)
                individual.fitness()
                next_population.append(individual)
        self.populacao = next_population[:self.tam_populacao]

    #Seleção dos individuos
    def _select(self):
        return self.torneio()

    #roleta/seleção
    def roleta(self):
        competitors = []
        total_score = sum([math.ceil(self.populacao[i].score) for i in range(self.tam_populacao)])
        for index in range(self.tam_populacao):
            temp = [index] * int((math.ceil(self.populacao[index].score /total_score) * 100))
            competitors.extend(temp)
        
        return self.populacao[random.choice(competitors)]

    #torneio/seleção
    def torneio(self):
        k=0.75
        for index in range(self.tam_populacao):
            individuo1 = self.populacao[random.randint(0,self.tam_populacao-1)]
            individuo2 = self.populacao[random.randint(0,self.tam_populacao-1)]
            
            if individuo1.score < individuo2.score:
                melhor = individuo1
                pior = individuo2
            else:
                pior = individuo1
                melhor = individuo2

            r = random.choice(bin_values)    
            if r < k :
                return melhor
            else:
                return pior

    #Executa a mutação na população
    def _mutate(self,individual):
        if random.random() < self.tx_mutacao:
            #individual.mutacao(gene)
            mutacao_nao_uniforme(individual)

    #Mutacao não uniforme
    def mutacao_nao_uniforme(self,individual):
        r1 = random.random(0,1)
        r2 = random.random(0,1)
        fG = (r2*(1-(self.geracao/self.max_geracoes)))**limites[1]
        c = 0.0
        if(r1<0.5):
            individual.cromossomo = individual.cromossomo + (limites[1] - individual.cromossomo)*fG
        elif(r1>=0.5):
            individual.cromossomo = individual.cromossomo - (individual.cromossomo - limites[0])*fG

    #Pega o melhor individuo de toda a população
    def best():
        def fget(self):
            return self.populacao[0]
        return locals()
    best = property(**best())

    #Exibe resultados
    def report(self):
        print("="*70)
        print("geração: " , self.geracao)
        self.printPopulacao()
        print("\nmelhor x:       " , self.best.cromossomo)
        print("\nmelhor fitness:       " , self.best.score)  

    def report2(self):
        for i in range(self.tam_populacao):
            if i in list(self.result.keys()):
                self.result[i].append(self.populacao[i].cromossomo)
            else:
                self.result[i] = [self.populacao[i].cromossomo]

        if i+1 not in list(self.result.keys()) and i+2 not in list(self.result.keys()):
            self.result[i+1] = [self.best.cromossomo]
            self.result[i+2] = [self.best.score]
        else:
            self.result[i+1].append(self.best.cromossomo)
            self.result[i+2].append(self.best.score)



    #Roda o algoritmo
    def run(self):
        while not self._objetivo():
            self.step()

def printPorLinha(dic):
    aux= ''
    lst = []
    for key in dic:

        if key == len(dic) - 2:
            aux += "Melhor x"
        elif key == len(dic) - 1:
            aux += "Melhor fitness"
        else:
            aux += str(key)
        for valor in dic[key]:
            aux += "\t" + str(valor)
        lst.append(aux)
        aux= ''
    for valor in lst:
        print(valor.replace('.', ','))


if __name__ == "__main__":
    STR_DELIMITER = ''
    #TAM_POPULACAO = int(input("Tamanho da população: "))
    #NR_GERACOES = int(input("Número de gerações: "))

    TAM_POPULACAO = int(sys.argv[1])
    NR_GERACOES = int(sys.argv[2])
    TX_CROSSOVER = 0.6
    PROB_MUTACAO = 0.01
    #possíveis valores dos genes
    bin_values = (0,1)
    

    #Tamanho do cromossomo
    tam_cromossomo = 10
    AG = AlgoritmoGenetico(TAM_POPULACAO,NR_GERACOES,TX_CROSSOVER,PROB_MUTACAO)
    AG.run()
    printPorLinha(AG.result)