from random import uniform, random, sample, randint, gauss
from operator import itemgetter
import math
import matplotlib.pyplot as plt
import copy

def sea(numb_generations,size_pop, size_cromo, prob_mut,prob_cross,sel_parents,mutation,sel_survivors, fitness_func, arithmetic_a, start, stop, croos_func, pop):
    # inicializa população: indiv = (cromo,fit)
    populacao = copy.deepcopy(pop)
    # avalia população
    populacao = [(indiv[0], fitness_func(indiv[0])) for indiv in populacao]


    # para a estatística
    stat = [best_pop(populacao)[1]]
    aux_best = best_pop(populacao)[1]
    ger = 0
    for j in range(numb_generations):
        # selecciona progenitores
        mate_pool = sel_parents(populacao)
    	# Variation
	    # ------ Crossover
        progenitores = []
        for i in range(0,size_pop-1,2):
            cromo_1= mate_pool[i]
            cromo_2 = mate_pool[i+1]
            #filhos = one_point_cross(cromo_1,cromo_2, prob_cross)
            filhos = croos_func(cromo_1,cromo_2, prob_cross, arithmetic_a)
            progenitores.extend(filhos) 
        # ------ Mutation
        descendentes = []
        for indiv,fit in progenitores:
            novo_indiv = mutation(indiv,prob_mut, start, stop)
            descendentes.append((novo_indiv,fitness_func(novo_indiv)))
        # New population
        populacao = sel_survivors(populacao,descendentes)
        # Avalia nova _população
        populacao = [(indiv[0], fitness_func(indiv[0])) for indiv in populacao] 

        b = best_pop(populacao)
        if b[1] < aux_best:
            aux_best = b[1]
            ger = j
	
	# Estatística
        stat.append(best_pop(populacao)[1])
    return best_pop(populacao), stat, ger


# Initialize population
def gera_pop(size_pop,size_cromo, start, stop):
    return [(gera_indiv(size_cromo, start, stop),0) for i in range(size_pop)]

def gera_indiv(size_cromo, start, stop):
    # random initialization
    indiv = [uniform(start, stop) for i in range(size_cromo)]
    return indiv

def rastrigin(x):
    var = 10 * len(x)
    for i in range(0, len(x)):
        var += x[i]**2.0 - (10 * math.cos(2 * math.pi * x[i]))
    return var

def schwefel(x):
    var = 0
    for i in range(0, len(x)):
        var += -x[i]*math.sin(math.sqrt(abs(x[i])))
    return var + 418.982887*len(x)


def griewank(xs):
    sum = 0
    for x in xs:
        sum += x * x
    product = 1
    for i in range(len(xs)):
        product *= math.cos(xs[i] / math.sqrt(i + 1))
    return 1 + sum / 4000 - product
    
def best_pop(populacao):
    populacao.sort(key=itemgetter(1),reverse=False)
    return populacao[0]

# Parents Selection: tournament
def tour_sel(t_size):
    def tournament(pop):
        size_pop= len(pop)
        mate_pool = []
        for i in range(size_pop):
            winner = one_tour(pop,t_size)
            mate_pool.append(winner)
        return mate_pool
    return tournament

def one_tour(population,size):
    """Maximization Problem. Deterministic"""
    pool = sample(population, size)
    pool.sort(key=itemgetter(1), reverse=False)
    return pool[0]

# Variation operators: ------ > gaussian float mutation	    
def muta_float_gaussian(indiv, prob_muta, start, stop):
    cromo = indiv[:]
    for i in range(len(cromo)):
        cromo[i] = muta_float_gene(cromo[i],prob_muta, start, stop)
    return cromo

def muta_float_gene(gene,prob_muta, start, stop):
    value = random()
    new_gene = gene
    if value < prob_muta:
        muta_value = gauss(0, 1)
        new_gene = gene + muta_value
        if new_gene < start:
            new_gene = start
        elif new_gene > stop:
            new_gene = stop
    return new_gene

# Survivals Selection: elitism
def sel_survivors_elite(elite):
    def elitism(parents,offspring):
        size = len(parents)
        comp_elite = int(size* elite)
        offspring.sort(key=itemgetter(1), reverse=False)
        parents.sort(key=itemgetter(1), reverse=False)
        new_population = parents[:comp_elite] + offspring[:size - comp_elite]
        return new_population
    return elitism

    
# Variation Operators :Crossover
def one_point_cross(indiv_1, indiv_2,prob_cross, a):
	value = random()
	if value < prob_cross:
	    cromo_1 = indiv_1[0]
	    cromo_2 = indiv_2[0]
	    pos = randint(0,len(cromo_1))
	    f1 = cromo_1[0:pos] + cromo_2[pos:]
	    f2 = cromo_2[0:pos] + cromo_1[pos:]
	    return ((f1,0),(f2,0))
	else:
	    return (indiv_1,indiv_2)

def arithmetic_cross(indiv_1, indiv_2,prob_cross, a):
    value = random()
    if value < prob_cross:
        f1=[]
        f2=[]
        for i in range(0, len(indiv_1[0])):
            f1.append( a*indiv_1[0][i] + (1-a)*indiv_2[0][i])
            f2.append( (1-a)*indiv_1[0][i] + a*indiv_2[0][i])         
        return ((f1,0),(f2,0))
    else:
        return (indiv_1,indiv_2)


if __name__ == '__main__':
    print('[1] Rastrigin')
    print('[2] Schwefel')
    print('[3] Griewangk')
    key = int(input())

    if key==1:
        function = "Rastrigin"
    elif key == 2:
        function = "Schwefel"
    elif key == 3:
        function = "Griewangk"

    file_one  = open(function + '_one.txt', 'w')
    file_arit  = open( function + '_arit.txt', 'w')

    for i in range(0, 30):
        if key == 1:
            generations = 800
            pop_size = 400
            cromo_size = 70
            prob_mut = 0.01
            prob_cross = 0.8
            tour_size = 5
            elite_percent = 0.01
            arithmetic_a = 0.7
            
            populacao = gera_pop(pop_size,cromo_size, -5.12, 5.12)
            best_one, stat_one, ger_one = sea(generations,pop_size, cromo_size, prob_mut,prob_cross,tour_sel(tour_size),muta_float_gaussian, sel_survivors_elite(elite_percent), rastrigin, arithmetic_a, -5.12, 5.12, one_point_cross, populacao)
            best_arit, stat_arit, ger_arit = sea(generations,pop_size, cromo_size, prob_mut,prob_cross,tour_sel(tour_size),muta_float_gaussian, sel_survivors_elite(elite_percent), rastrigin, arithmetic_a, -5.12, 5.12, arithmetic_cross, populacao)
        
        elif key == 2:
            generations = 1000
            pop_size = 500
            cromo_size = 25
            prob_mut = 0.02
            prob_cross = 0.8
            tour_size = 5
            elite_percent = 0.02
            arithmetic_a = 0.7
           
            populacao = gera_pop(pop_size,cromo_size, -500, 500)
            best_one, stat_one, ger_one = sea(generations,pop_size, cromo_size, prob_mut,prob_cross,tour_sel(tour_size),muta_float_gaussian, sel_survivors_elite(elite_percent), schwefel, arithmetic_a, -500, 500, one_point_cross, populacao)
            best_arit, stat_arit, ger_arit = sea(generations,pop_size, cromo_size, prob_mut,prob_cross,tour_sel(tour_size),muta_float_gaussian, sel_survivors_elite(elite_percent), schwefel, arithmetic_a, -500, 500, arithmetic_cross, populacao)

        elif key == 3:
            generations = 600
            pop_size = 300
            cromo_size = 90
            prob_mut = 0.02
            prob_cross = 0.8
            tour_size = 5
            elite_percent = 0.02
            arithmetic_a = 0.7
            
            populacao = gera_pop(pop_size,cromo_size, -600, 600)
            best_one, stat_one, ger_one = sea(generations,pop_size, cromo_size, prob_mut,prob_cross,tour_sel(tour_size),muta_float_gaussian, sel_survivors_elite(elite_percent), griewank, arithmetic_a, -600, 600, one_point_cross, populacao)
            best_arit, stat_arit, ger_arit = sea(generations,pop_size, cromo_size, prob_mut,prob_cross,tour_sel(tour_size),muta_float_gaussian, sel_survivors_elite(elite_percent), griewank, arithmetic_a, -600, 600, arithmetic_cross, populacao)

        print('One point Crossover')
        print(best_one[1])
        print(ger_one)
        print('Arithmetical Crossover')
        print(best_arit[1])
        print(ger_arit)
        file_one.write(str(best_one[1]) + ' ' + str(ger_one) + '\n')
        file_arit.write(str(best_arit[1]) + ' ' + str(ger_arit) + '\n')

    
    generations = list(range(len(stat_one)))
    plt.title('Performance over generations in One Point Crossover')
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.plot(generations, stat_one, label='Best')
    plt.legend(loc='best')
    plt.show()

    generations = list(range(len(stat_arit)))
    plt.title('Performance over generations in Arithmetical Crossover')
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.plot(generations, stat_arit, label='Best')
    plt.legend(loc='best')
    plt.show()

    file_one.close()
    file_arit.close()