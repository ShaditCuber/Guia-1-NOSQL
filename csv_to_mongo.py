import csv
from index import get_db

# Cargar datos CSV
data = open("solvesRubiks.csv", "r")


# Recorrer la data y guardarla en una lista de json
data = csv.DictReader(data)

data_list = []

for row in data:
    del row["#"]
    del row["Fastest Solve"]
    # Cambiar nombre a las columnas
    row["person"] = row.pop("Person")
    row["solve_1"] = row.pop("Solve 1")
    row["solve_2"] = row.pop("Solve 2")
    row["solve_3"] = row.pop("Solve 3")
    row["solve_4"] = row.pop("Solve 4")
    row["solve_5"] = row.pop("Solve 5")
    row["country"] = row.pop("Country")
    data_list.append(row)


# Conectar a la base de datos
db = get_db()

# Insertar los datos en la base de datos
db.solvesRubiks.insert_many(data_list)
