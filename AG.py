import random
import math

STR_DELIMITER = ''
TAM_POPULACAO = int(input("Tamanho da população: "))
NR_GERACOES = int(input("Número de gerações: "))
TX_CROSSOVER = 0.6
PROB_MUTACAO = 0.01
#possíveis valores dos genes
bin_values = (0,1)
#x∈[−10,+10]
limites = (-10.0,10.0)

#Tamanho do cromossomo
tam_cromossomo = 10

class Individual(object):

    


    



    def __init__(self, cromossomo = None, x= None):
        self.score = None
        self.x = x or self._criaNumAleatorio()
        self.cromossomo = cromossomo or self._criaCromossomo()



    def _criaNumAleatorio(self):
        numero = random.uniform(limites[0],limites[1])
        return numero

    #Cria um novo cromossomo do tamanho máximo definido anteriormente.
    def _criaCromossomo(self):

        parteInteira = int(self.x)
        parteDecimal = int(str(self.x-parteInteira)[3:])

        strbinParteInteira = bin(parteInteira)[2:]
        strbinParteDecimal = bin(parteDecimal)[2:]
        strbinParteInteira = strbinParteInteira.zfill(5)
        strbinParteDecimal = strbinParteDecimal.zfill(5)
        strbin = strbinParteInteira+strbinParteDecimal
        listabin = []

        for numero in strbin:
            listabin.append(numero)
        return listabin
        #return [random.choice(bin_values) for gene in range(self.tam_cromossomo)]


    #fitness
    def fitness(self):
        #Decodificação do cromossomo
        #coff = float(int(STR_DELIMITER.join(map(str,self.cromossomo)),2)) / float(pow(2,self.tam_cromossomo) - 1)
        #x = limites[0] + (limites[1] - limites[0]) * coff
        #Função objetivo
        x = self.x
        y =   x**2 - 3*x + 4
        #fitness score
        self.score = y
        
    #crossover
    def crossover_1ponto(self,other):
        #60% de cross
        ponto = random.randint(1, tam_cromossomo - 1)
        
        # filho1 = self.cromossomo[:]
        # filho2 = other.cromossomo[:]

        # filho1[:ponto] = self.cromossomo[:ponto]
        # filho1[ponto:] = other.cromossomo[ponto:]

        # filho2[:ponto] = other.cromossomo[:ponto]
        # filho2[ponto:] = self.cromossomo[ponto:]
        # return filho1,filho2
        
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
        clone = self.__class__(self.cromossomo[:])
        clone.score = self.score
        clone.x = self.x
        return clone


class AlgoritmoGenetico(object):

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

        self.geracao+=1


        self.report()

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
                offspring = mate1.crossover_1ponto(mate2)
            else:
                #copia o individuo
                offspring = [mate1.copy()]
            for individual in offspring:
                self._mutate(individual)
                individual.fitness()
                next_population.append(individual)
        self.populacao = next_population[:self.tam_populacao]

    #Seleção dos individuos
    def _select(self):
        #return self.roleta()
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
        for gene in range(tam_cromossomo):
            if random.random() < self.tx_mutacao:
                individual.mutacao(gene)

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
        print("\nmelhor x:       " , self.best.x)
        print("\nmelhor fitness:       " , self.best.score)    

    #Roda o algoritmo
    def run(self):
        while not self._objetivo():
            self.step()


if __name__ == "__main__":
   AG = AlgoritmoGenetico(TAM_POPULACAO,NR_GERACOES,TX_CROSSOVER,PROB_MUTACAO)
   AG.run()