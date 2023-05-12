import random
import numpy as np
import time

baslangic_zamani = time.time()

# Ant Colony Algoritmasının Parametreleri
alpha = 1.0  # feromon izlerinin önem derecesi
beta = 2.0  # maddi değerin önem derecesi
evaporation = 0.5  # feromon izlerinin buharlaşma oranı
Q = 500.0  # tek bir yolla bırakılacak feromon miktarı
num_ants = 50  # karınca sayısı
num_iterations = 100  # iterasyon sayısı

# feromon izlerini başlatalım
pheromone_trails = None

# en iyi çözümü başlatalım
best_solution = {"weight": 0, "value": 0, "items": []}

# değer ve ağırlık hesaplayan fonksiyonu tanımlayalım 
def compute_solution(items, indices):
    solution = {"weight": 0, "value": 0, "items": []}
    for index in indices:
        solution["weight"] += items[index]["weight"]
        solution["value"] += items[index]["value"]
        solution["items"].append(index)
    return solution

# feromon izlerini güncelleyen fonksiyon
def update_pheromone_trails(trails, solutions, evaporation, Q):
    for i in range(len(trails)):
        trails[i] *= (1.0 - evaporation)
   
    for solution in solutions:
        for index in solution["items"]:
            trails[index] += Q / solution["value"]
    return trails

# feromon izlerine göre item seçen fonksiyonu tanımlayalım
def select_item(trails, items, used_items, alpha, beta):
    remaining_items = set(range(len(items))).difference(used_items)
    total_pheromone = sum([pow(trails[i], alpha) * pow(1.0 / items[i]["weight"], beta) for i in remaining_items])
    probabilities = [0.0 for i in range(len(items))]
    for i in remaining_items:
        probabilities[i] = (pow(trails[i], alpha) * pow(1.0 / items[i]["weight"], beta)) / total_pheromone
    roulette_wheel = random.random()
    total = 0.0
    for i in remaining_items:
        total += probabilities[i]
        if total >= roulette_wheel:
            return i

# txt dosyasından verileri okuyalım
with open("ks_4_0.txt", "r") as file:
    # eşya sayısı ve çantaın kapasitesini alalım
    num_items, capacity = map(int, file.readline().split())

    # her bir item değerini ve ağırlığını alalım
    items = {}
    for i in range(num_items):
        value, weight = map(int, file.readline().split())
        items[i] = {"weight": weight, "value": value}

    #  feromon izlerini başlatalım
    pheromone_trails = [1.0 for i in range(num_items)]

# ant colony algoritmasını çalıştıralım
for iteration in range(num_iterations):
    solutions = []
    for ant in range(num_ants):
        solution = {"weight": 0, "value": 0, "items": []}

        # en mantıklı seçimi belirleyelim
        while solution["weight"] < capacity:
            item = select_item(pheromone_trails, items, set(solution["items"]), alpha, beta)
            if item is None:
                break
            solution["weight"] += items[item]["weight"]
            solution["value"] += items[item]["value"]
            solution["items"].append(item)

        # sonucu ekleyelim
        solutions.append(solution)

    # feromon izlerini güncelleyelim
    pheromone_trails = update_pheromone_trails(pheromone_trails, solutions, evaporation, Q)

    # en iyi çözümü bulalım
    for solution in solutions:
        if solution["value"] > best_solution["value"] and solution["weight"] <= capacity:
            best_solution = solution
    
    # eşyaların listesini numpy dizisine dönüştürelim [0 0 1 1] gibi 
    items_arr = np.zeros(num_items, dtype=int)
    items_arr[best_solution["items"]] = 1
        
bitis_zamani = time.time()
gecen_zaman = bitis_zamani - baslangic_zamani

# sonucu ekrana yazdıralım
print("Toplam Değer: ", best_solution["value"])
print("Toplam Ağırlık: ", best_solution["weight"])
print("Seçilen Eşyalar: ", " ".join(map(str, items_arr)))
print("Programin çalisma süresi: {:.2f} saniye".format(gecen_zaman))
