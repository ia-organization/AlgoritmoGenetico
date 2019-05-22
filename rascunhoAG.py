
import random

def individuo(min,max):
	return [random.randint(min,max) for i in range(tam_individuo)]
	
def criarPopulacao():
	return[individuo(0,9) for i in range(tam_populacao)]
	
def funcaoFitness(individuo):
	fitness = 0
	for i in range(len(individuo)):
		if(individuo[i] == modelo[i]):
			fitness += 1
	return fitness

#crossover	
def selecaoEreproducao(populacao):
	pontuados = [(funcaoFitness(i),i)for i in populacao]
	pontuados = [i[1] for i in sorted(pontuados)]
	populacao = pontuados
	
	
	selecionados = pontuados[(len(pontuados) - pais):]
	
	for i in range(len(populacao) - pais):
		ponto = random.randint(1, tam_individuo - 1)
		pai = random.sample(selecionados,2)
		
		populacao[i][:ponto] = pai[0][:ponto]
		populacao[i][ponto:] = pai[1][ponto:]
		
	return populacao
	
	
def mutacao(populacao):
	for i in range(len(populacao) - pais):
		if(random.random() <= prob_mutacao):
			ponto = random.randint(0, tam_individuo - 1)
			novo_valor = random.randint(1,9)
			
			while(novo_valor == populacao[i][ponto]):
				novo_valor = random.randint(1,9)
				
			populacao[i][ponto] = novo_valor
			
	return populacao
