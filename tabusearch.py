import numpy as np
import time

baslangic_zamani = time.time()

# Verileri dosyadan okuyalım
with open("ks_4_0.txt", "r") as f:
    n, capacity = map(int, f.readline().split())
    values = np.zeros(n)
    weights = np.zeros(n)
    for i in range(n):
        values[i], weights[i] = map(int, f.readline().split())

# Genetik algoritma için gerekli parametreler
population_size = 100
mutation_rate = 0.01
generations = 100

# Başlangıçta rastgele bir popülasyon oluşturalım
population = np.random.randint(2, size=(population_size, n))

# En iyi çözümü tutacak değişkeni tanımlayalım
best_solution = np.zeros(n)

# Her jenerasyonda en iyi çözümü güncelleyelim
for i in range(generations):
    # Popülasyondaki her bireyin objektif fonksiyonunu hesaplayalım
    fitness = np.zeros(population_size)
    for j in range(population_size):
        weight = np.sum(weights * population[j])
        if weight > capacity:
            fitness[j] = 0.3
        else:
            fitness[j] = np.sum(values * population[j])

    # En iyi çözümü popülasyondan seçelim
    best_index = np.argmax(fitness)
    if fitness[best_index] > np.sum(values * best_solution):
        best_solution = population[best_index].copy()

    # Yeni popülasyonu oluşturmak için ebeveynler seçelim
    parent_indices = np.random.choice(population_size, size=2*population_size, p=fitness/np.sum(fitness))

    # Ebeveynler arasında tek noktadan kesme yapalım
    crossover_point = np.random.randint(0, n, size=2*population_size)
    children = np.zeros((2*population_size, n))
    for j in range(population_size):
        parent1 = population[parent_indices[j*2]]
        parent2 = population[parent_indices[j*2+1]]
        children[j*2, :crossover_point[j*2]] = parent1[:crossover_point[j*2]]
        children[j*2, crossover_point[j*2]:] = parent2[crossover_point[j*2]:]
        children[j*2+1, :crossover_point[j*2+1]] = parent2[:crossover_point[j*2+1]]
        children[j*2+1, crossover_point[j*2+1]:] = parent1[crossover_point[j*2+1]:]

    # Mutasyon işlemini gerçekleştirelim
    for j in range(population_size):
        if np.random.rand() < mutation_rate:
            index = np.random.randint(n)
            children[j] = 1 - children[j]
            children[j, index] = 1 - children[j, index]

    # Yeni popülasyonu oluşturalım
    population = children

# En iyi çözümün toplam değerini ve ağırlığını hesaplayalım
total_value = 0
total_weight = 0
for i in range(n):
    if best_solution[i] == 1:
        total_value += values[i]
        total_weight += weights[i]

bitis_zamani = time.time()
gecen_zaman = bitis_zamani - baslangic_zamani

# Sonucu ekrana yazdıralım
print("Toplam değer: ", total_value)
print("Toplam ağırlık: ", total_weight)
print("En iyi çözüm: ", best_solution)
print("Programin çalisma süresi: {:.2f} saniye".format(gecen_zaman))