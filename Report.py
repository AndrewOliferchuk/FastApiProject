#  Завдання: Аналіз продажів у магазині
# У тебе є паркет-файл (sales.parquet), де містяться дані про продажі:
#
# order_id	customer_id	date	product	price	quantity
# 1	101	2024-02-01	Laptop	1200	1
# 2	102	2024-02-01	Phone	800	2
# 3	101	2024-02-02	Mouse	50	3
# 4	103	2024-02-02	Monitor	300	1
# 5	102	2024-02-03	Keyboard	100	2
# 6	104	2024-02-03	Phone	800	1
# 🎯 Твої задачі:
# Завантажити дані з sales.parquet за допомогою pl.scan_parquet().
# Обчислити загальний дохід (total_revenue = price * quantity).
# Знайти найпопулярніший товар (який купили найбільше разів).
# Знайти топ-3 клієнтів за витратами.
# Групувати дані по днях і знайти загальний денний дохід.
# Конвертувати результати у JSON.


import polars as pl
import os
import json

from _pytest.reports import BaseReport


# class SalesAnalysis:
#     def __init__(self, file_path:str):
#         self.file_path = file_path
#         self.df = None
#
#
#     def load_date(self):
#         # self.df = pl.scan_parquet(self.file_path)
#         data = {"a":[1,2,3], "b":["1","2", "3"], "c":[4,5,6]}
#         df = pl.DataFrame(data, schema=[("a", pl.Float32), ("b", pl.Utf8), ("c", pl.Int64)])
#         return df
#
#
#     def calculate_total_product(self):
#         self.df = self.df.with_colums(
#             pl.col("price") * pl.col("quantity")).alias("total_revenue")
#
#     def get_most_popular_product(self):
#         popular_product = (
#             self.df.group_by("product")
#             .agg(pl.sum("quantity").alias("total_sold"))
#             .sort("total_sold", descending=True)
#             .limit(1)
#             .collect()
#         )
#         return popular_product.to_dicts()


# Завдання: Аналіз продажів у мережі магазинів
# Уявімо, що ти працюєш з мережею магазинів, і тобі потрібно проаналізувати продажі по містах і категоріях товарів.
#
# 🔹 Вхідні дані (sales.parquet) – інформація про кожен продаж:
#
# order_id	customer_id	store_city	date	category	product	price	quantity	discount
# 1	101	Kyiv	2024-02-01	Electronics	Laptop	1200	1	0.05
# 2	102	Lviv	2024-02-01	Electronics	Phone	800	2	0.10
# 3	101	Kyiv	2024-02-02	Accessories	Mouse	50	3	0.00
# 4	103	Odesa	2024-02-02	Electronics	Monitor	300	1	0.07
# 5	102	Lviv	2024-02-03	Accessories	Keyboard	100	2	0.05
# 6	104	Dnipro	2024-02-03	Electronics	Phone	800	1	0.15
# 🎯 Що потрібно зробити:
# Завантажити дані (load_data()).
# Розрахувати підсумковий дохід (total_revenue = (price - discount) * quantity).
# Знайти найприбутковіше місто (де найбільший дохід).
# Знайти найпопулярнішу категорію товарів (за кількістю продажів).
# Топ-5 клієнтів за витратами.
# Розрахувати середню знижку по кожному місту.
# Групувати дані по днях та містах.
# Згенерувати JSON-звіт.
# Зберегти результати у CSV і Excel.


# class AnalysisProduct:
#     def __init__(self, file_path: str):
#         self.file_path = file_path
#         self.df = None
#
#     def load_date(self):
#         self.df = pl.scan_parquet(self.file_path)
#         return self
#
#     def calculate(self):
#         total_revenue = self.df.with_colums(
#             (pl.col("price") - pl.col("discount")) * pl.col("quantity"))
#
#
#     def most_profitable_city(self):
#         msf = self.df.group_by("store_city").


# if __name__ == "__main__":
#     data = SalesAnalysis("asd")
#     df = data.load_date()
#     ...