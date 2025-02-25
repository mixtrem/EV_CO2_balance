# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 19:58:51 2025

@author: P50
"""

import matplotlib.pyplot as plt

class ElectricCar:
    def __init__(self, model, battery_capacity, avg_consumption, co2_battery_production):
        self.model = model
        self.battery_capacity = battery_capacity
        self.avg_consumption = avg_consumption
        self.co2_battery_production = co2_battery_production

    def calculate_co2_emissions(self, distance, co2_per_kwh):
        total_energy_used = self.avg_consumption * distance
        operational_emissions = total_energy_used * co2_per_kwh
        production_emissions = self.battery_capacity * self.co2_battery_production
        return operational_emissions + production_emissions, production_emissions


class PetrolCar:
    def __init__(self, model, avg_co2_per_km, fuel_consumption=None, thg_emissions_per_liter=None):
        self.model = model
        self.avg_co2_per_km = avg_co2_per_km
        self.fuel_consumption = fuel_consumption
        self.thg_emissions_per_liter = thg_emissions_per_liter

    def calculate_co2_emissions(self, distance):
        fuel_used = (self.fuel_consumption * distance) / 100
        fuel_emissions = fuel_used * self.thg_emissions_per_liter
        emissions = self.avg_co2_per_km * distance
        return emissions + fuel_emissions


# Пример данных
distance = 150000

electric_cars = [
    ElectricCar("Tesla Model 3", 79, 0.215, 145.1),
    ElectricCar("Nissan Leaf", 40, 0.178, 145.1),
]

petrol_cars = [
    PetrolCar("VW Tiguan Allspace 2.0 TDI", 0.168, 6.4, 0.43),
    PetrolCar("Toyota Aygo X Air", 0.112, 4.9, 0.36),
]

countries_co2 = {
    "Germany": 0.445,
    "China": 0.582,
    "France": 0.056,
    "World Average": 0.481
}

# Создание списка для графика
labels = []
electric_emissions = []
petrol_emissions = []

# Вычисление выбросов для электромобилей
for e_car in electric_cars:
    labels.append(e_car.model)
    emissions_germany = e_car.calculate_co2_emissions(distance, countries_co2["Germany"])[0]
    electric_emissions.append(emissions_germany)

# Вычисление выбросов для конвенциональных автомобилей
for p_car in petrol_cars:
    labels.append(p_car.model)
    emissions = p_car.calculate_co2_emissions(distance)
    petrol_emissions.append(emissions)

# Построение графика
plt.figure(figsize=(10, 6))
plt.bar(labels[:len(electric_cars)], electric_emissions, color='blue', label='Electric Cars (Germany)', alpha=0.7)
plt.bar(labels[len(electric_cars):], petrol_emissions, color='red', label='Conventional Cars', alpha=0.7)

# Подписи и заголовки
plt.title(f"CO2 Emissions Comparison for {distance} km")
plt.xlabel("Car Models")
plt.ylabel("Total CO2 Emissions (kg)")
plt.xticks(rotation=45, ha="right")
plt.legend()

# Показ графика
plt.tight_layout()
plt.show()
