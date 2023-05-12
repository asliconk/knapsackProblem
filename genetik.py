import random
import time

baslangic_zamani =time.time()

# Dosyadan verileri okuyalım
with open("ks_4_0.txt", "r") as f:
    data = f.readlines()

# Toplam eşya sayısı ve çantanın toplam ağırlığı
n_items, capacity = map(int, data[0].split())

# Eşya verileri (değer, ağırlık)
items = [tuple(map(int, line.split())) for line in data[1:]]

# Sabitler
POPULATION_SIZE = 100
GENERATIONS = 100
MUTATION_RATE = 0.1

# Fitness fonksiyonu oluşturalım
def fitness(individual):
    total_weight = 0
    total_value = 0
    for i in range(len(individual)):
        if individual[i] == 1:
            total_weight += items[i][1]
            total_value += items[i][0]
    if total_weight > capacity:
        return 0
    return total_value

# Popülasyonu oluşturalım
def create_population(size):
    population = []
    for i in range(size):
        individual = [random.randint(0, 1) for i in range(n_items)]
        population.append(individual)
    return population

# Crossover işlemini tanımlayalım
def crossover(parent1, parent2):
    split_index = random.randint(1, len(parent1) - 1)
    child1 = parent1[:split_index] + parent2[split_index:]
    child2 = parent2[:split_index] + parent1[split_index:]
    return child1, child2

# Mutasyon işlemini tanımlayalım
def mutate(individual):
    for i in range(len(individual)):
        if random.random() < MUTATION_RATE:
            individual[i] = 1 - individual[i]

# En uygun bireyleri seçelim
def select(population):
    fitnesses = [fitness(individual) for individual in population]
    max_fitness = max(fitnesses)
    selected = []
    for i in range(len(population)):
        if fitnesses[i] == max_fitness:
            selected.append(population[i])
    return selected

# Genetik programlama algoritması
def genetic_algorithm():
    population = create_population(POPULATION_SIZE)
    for generation in range(GENERATIONS):
        new_population = []
        for i in range(int(POPULATION_SIZE / 2)):
            parent1 = random.choice(population)
            parent2 = random.choice(population)
            child1, child2 = crossover(parent1, parent2)
            mutate(child1)
            mutate(child2)
            new_population.extend([child1, child2])
        population = select(population) + select(new_population)
        if len(population) > POPULATION_SIZE:
            population = random.sample(population, POPULATION_SIZE)
    best_individual = max(population, key=fitness)
    return best_individual, fitness(best_individual)

# Genetik programlama algoritmasını çalıştıralım
best_individual, best_fitness = genetic_algorithm()

bitis_zamani = time.time()
gecen_zaman = bitis_zamani - baslangic_zamani

# Sonuçları ekrana yazdırıyoruz
print("Toplam değer:", best_fitness)
print("Seçilen Eşyalar", " ".join(map(str, best_individual)))
print("Programin calisma süresi: {:.2f} saniye".format(gecen_zaman))