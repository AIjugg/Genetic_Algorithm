#coding=utf-8
from PIL import Image
from pil_draw import drawByPil
import numpy as np
import time
import random
import os
from copy import deepcopy


class Population:
    def __init__(self, target_img, population_num = 20, max_polygon_num = 100, init_polygon_num = 100):
        self.target_img = target_img
        
        # 种群大小
        self.population_num = population_num
        # 初始化基因数
        self.init_polygon_num = init_polygon_num
        # 最多基因数
        self.max_polygon_num = max_polygon_num
        
        self.best_unit = None
        
        self.best_fitness = None
        
        self.best_canvas = None
        
        # 适应度接连没有提升的轮次
        self.unchanged_rounds = 0
        
        self.rounds = 0
        
        # init population 种群
        self.population = [drawByPil(init_polygon_num, target_img, max_polygon_num, 3) for p in range(population_num)]
    

    # 根据适应度排行
    def fitness_sort(self):
        if self.population_num > 1:
            self.population = sorted(self.population, key = lambda p: p.fitness)
        
        best = self.population[0]
        return best.fitness
        
    
    # 交叉
    def mate(self):
        if self.population_num < 2:
            return False
        dad, mom = self.choose()
        dad = self.population[dad]
        mom = self.population[mom]
        
        child = deepcopy(dad.mating(dad, mom))
        
        # 变异规划
        var_rate, scale = get_variation_rate(self.rounds)
        child.variation(var_rate, scale)
        self.population.append(child)
        
    
    def variation(self, rate = 0.15, scale = 1):
        for draw in self.population:
            draw.variation(rate, scale)
    
    
    # 计算适应度
    def fit(self):
        for p in self.population:
            p.fit()
            #print(p.fitness)
    
    
    # 适应度最低的个体被淘汰
    def weed_out(self):
        if len(self.population) > self.population_num:
            for i in range(len(self.population) - self.population_num):
                self.population.pop()
    
    
    
    # 交叉+变异+选择+淘汰
    def behavior(self, mate_num = 2):
        self.rounds += 1
        for i in range(mate_num):
            self.mate()
        
        self.pick_best()
        self.weed_out()


    # 选择
    def choose(self):
        # 当前种群数量
        population_num = len(self.population)
        # 选择概率
        weights = np.append(np.array([8, 6, 4, 3, 2]), np.ones(int(population_num)))
        weights = weights[:population_num]
        weights = weights / np.sum(weights)
        
        index_array = np.array(range(population_num))
        return np.random.choice(index_array, size=2, replace=False, p=weights)
        

    # 纯变异
    def behavior_var(self):
        self.rounds += 1
        var_rate, scale = get_variation_rate(self.rounds)
        self.variation(var_rate, scale)
        self.pick_best_var()
    
    
    def pick_best(self):
        self.fit()
        fitness = self.fitness_sort()
        if self.best_fitness == None or self.best_fitness -1 > fitness:
            self.best_canvas = self.population[0].img
            self.best_fitness = fitness


    def pick_best_var(self):
        self.fit()
        fitness = self.fitness_sort()
        if self.best_fitness == None or self.best_fitness -1 > fitness:
            self.best_canvas = self.population[0].img
            self.best_fitness = fitness
            self.unchanged_rounds = 0
            self.best_unit = copy.deepcopy(self.population[0])
        else:
            self.unchanged_rounds += 1
            if self.unchanged_rounds > 3:
                self.population[0] = copy.deepcopy(self.best_unit)
    
    
    
# 概率计算公式
def roll(rate):
    return True if random.random() < rate else False
    
   
# 变异规划
def get_variation_rate(rounds):
    var_rate_list = [0.1,0.05,0.04,0.03,0.02,0.01,0.01]
    scale_list = [1, 0.9, 0.8, 0.7, 0.5, 0.3, 0.2]
    iter_list = [200,300,500,700,900,1000,2000]
    for i in range(len(iter_list)):
        if iter_list[i] > rounds:
            return var_rate_list[i], scale_list[i]
    return 0.01,0.1
    
def main():
    # 目标图片转换为四通道
    target_img = Image.open("material/juliet_100_100.png").convert('RGBA')
    my_population = Population(target_img, 8)
    
    # 创建文件夹
    dirname = 'ga_output_' + time.strftime('%Y-%m-%d_%H_%M', time.localtime(time.time()))
    if not os.path.exists(dirname):
        os.makedirs(dirname)
        

    # ================记录开始时间=============
    start = time.time()
    # 10w轮更迭
    for i in range(100000):
        my_population.behavior()
        #windows cls
        #time.sleep(1)
        os.system('cls')
        #linux clear
        #os.system('clear')
        print(i)
        print(my_population.best_fitness)
        
        if i % 250 == 0:
            img = my_population.best_canvas
            img_name = dirname + '//' + str(i) + '_' + str(int(my_population.best_fitness)) + ".png"
            img.save(img_name, 'PNG')
            
    print("cost:",time.time() - start)
    
    
if __name__ == '__main__':
    main()