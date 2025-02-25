# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 19:20:48 2025

@author: avemaster
"""

class ElectricCar:
    def __init__(self, model, battery_capacity, avg_consumption, co2_battery_production):
        """
        Инициализация электромобиля.
        :param model: Название модели автомобиля.
        :param battery_capacity: Емкость батареи (кВт·ч).
        :param avg_consumption: Средний расход электроэнергии (кВт·ч/км).
        :param co2_battery_production: Выбросы CO2 при производстве батареи (кг/кВт·ч емкости).
        """
        self.model = model
        self.battery_capacity = battery_capacity
        self.avg_consumption = avg_consumption
        self.co2_battery_production = co2_battery_production

    def calculate_co2_emissions(self, distance, co2_per_kwh):
        """
        Рассчитывает выбросы CO2 на заданное расстояние, включая производство батареи.
        :param distance: Расстояние (км).
        :param co2_per_kwh: Выбросы CO2 при производстве 1 кВт·ч электроэнергии (кг).
        :return: Общие выбросы CO2 (кг).
        """
        # Выбросы CO2 при использовании электроэнергии
        total_energy_used = self.avg_consumption * distance
        operational_emissions = total_energy_used * co2_per_kwh

        # Выбросы CO2 при производстве батареи
        production_emissions = self.battery_capacity * self.co2_battery_production

        # Суммарные выбросы CO2
        return operational_emissions + production_emissions, production_emissions


class PetrolCar:
    def __init__(self, model, avg_co2_per_km, fuel_consumption=None, thg_emissions_per_liter=None):
        """
        Инициализация бензинового автомобиля.
        :param model: Название модели автомобиля.
        :param avg_co2_per_km: Средние выбросы CO2 на км (кг/км).
        :param fuel_consumption: Расход топлива (л/100 км).
        :param thg_emissions_per_liter: Выбросы CO2 с учетом предшествующих цепочек (кг CO2/л топлива).
        """
        self.model = model
        self.avg_co2_per_km = avg_co2_per_km
        self.fuel_consumption = fuel_consumption
        self.thg_emissions_per_liter = thg_emissions_per_liter

    def calculate_co2_emissions(self, distance):
        """
        Рассчитывает выбросы CO2 на заданное расстояние.
        :param distance: Расстояние (км).
        :return: Выбросы CO2 (кг).
        """
        # Расчёт выбросов CO2 на основе расхода топлива
        fuel_used = (self.fuel_consumption * distance) / 100  # литры топлива за всё расстояние
        fuel_emissions = fuel_used * self.thg_emissions_per_liter

        # Добавляем выбросы CO2 на км
        emissions = self.avg_co2_per_km * distance

        # Суммируем выбросы CO2 с учётом предшествующих цепочек
        return emissions + fuel_emissions


# Пример данных
distance = 150000   # Общее расстояние (км)

# Электромобили
electric_cars = [
    ElectricCar("Tesla Model 3", 79, 0.215, 145.1),  # расход 0.215 кВт·ч/км
    ElectricCar("Nissan Leaf", 40, 0.178, 145.1),      # расход 0.20 кВт·ч/км
]

# Бензиновые автомобили
petrol_cars = [
    PetrolCar("VW Tiguan Allspace 2.0 TDI (Diesel)", 0.168, 6.4, 0.43),  # выбросы 168 г CO2/км, расход 6.4 л/100 км, Pre-chain GHG для дизеля
    PetrolCar("Toyota Aygo X Air", 0.112, 4.9, 0.36),  # выбросы 112 г CO2/км, расход 4.9 л/100 км, Pre-chain GHG emissions для бензина
]

# Данные по выбросам CO2 при производстве электроэнергии (в кг/кВт·ч)
countries_co2 = {
    "Germany": 0.445,
    "China": 0.582,
    "France": 0.056,
    "World Average": 0.481
}

# Сравнение выбросов
print(f"\nComparison of CO2 emissions for {distance} km:\n")

# Электромобили
print("Electric cars:")
for e_car in electric_cars:
    production_emissions = e_car.calculate_co2_emissions(distance, countries_co2["Germany"])[1]
    print(f"\n{e_car.model} (Battery Production Emissions: {production_emissions:.2f} kg CO2):")
    for country, co2_per_kwh in countries_co2.items():
        emissions, _ = e_car.calculate_co2_emissions(distance, co2_per_kwh)
        print(f"  {country}: {emissions:.2f} kg CO2")

# Бензиновые автомобили
print("\nConventional cars:")
for p_car in petrol_cars:
    emissions = p_car.calculate_co2_emissions(distance)
    print(f"{p_car.model}: {emissions:.2f} kg CO2")
    