from stat_alunos import *
import random
import copy
import operator
import math

# H0 - there's no differences between the runs. alpha = 0.05, se p value < alpha -> rejeitar nula e aceitar a H2

# fazer experiencias para as distribuiçoes. definir alpha -> se p value for inferior -> pode se rejeitar hipotese nula (é diferente)
def analysis():

    print("Escolha a funçao")
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

    print("Escolha o que quer analisar")
    print("[1] Fitness")
    print("[2] Geraçao com melhor fitness")
    tipo = int(input())


    significance_alpha = 0.05
    one_cross = [[float(x.split(' ')[tipo-1].rstrip()) for x in open(function + "_one.txt").readlines()]]
    ari_cross = [[float(x.split(' ')[tipo-1].rstrip()) for x in open(function + "_arit.txt").readlines()]]
    all_rastrigin_data = [one_cross[0], ari_cross[0]]
    

    #DATA DESCRIPTION
    """ print('\n')
    describe_data(one_cross[0])
    print('\n')
    describe_data(ari_cross[0])
    print('\n') """
    #################
    data = [one_cross[0], ari_cross[0]]
    plt.subplot(221)
    histogram_norm(data[0], "Histogram", "value", "quantity")

    plt.subplot(222)
    histogram_norm(data[1], "Histogram", "value", "quantity")

    plt.subplot(223)
    plt.boxplot(data[0], labels=[function + " One Point"])

    plt.subplot(224)
    plt.boxplot(data[1], labels=[function + " Arithmetical"])

    plt.show()
        
    test_statistic_one, p_value_one_point = test_normal_sw(one_cross)
    test_statistic_ari, p_value_ari = test_normal_sw(ari_cross)
    test_statistic_levene, p_value_levene = levene(all_rastrigin_data)
    print("shapiro p_value one: ", p_value_one_point)
    print("shapiro p_value ari: ", p_value_ari)
    print("levene p_value: ", p_value_levene)
    if(p_value_one_point >= significance_alpha and p_value_ari >= significance_alpha and p_value_levene >= significance_alpha):
        #Parametric
        print("Parametric")
        #final_ts, final_pv = one_way_ind_anova(file_data)
        #t_test_ind(one_cross, ari_cross)
        final_ts, final_pv = t_test_dep(one_cross[0], ari_cross[0])
    else:
        #Non-parametric
        print("Non-parametric")
        #final_ts, final_pv = kruskal_wallis(file_data)
        #final_ts, final_pv = mann_whitney(one_cross[0], ari_cross[0])
        #final_ts, final_pv = t_test_ind(one_cross, ari_cross)
        final_ts, final_pv = wilcoxon(one_cross[0], ari_cross[0])
    
    print(final_ts, final_pv)
    
    if(final_pv < significance_alpha):
        print('Null hypothesis (H0) rejected. Accept H1 -> Different')
    elif (final_pv >= significance_alpha):
        print('H0 accepted. Theres probably no difference!')


if __name__ == '__main__':
    analysis()