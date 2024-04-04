from pymongo import MongoClient
import math


def get_db():
    client = MongoClient("localhost:27017")
    db = client.rubiks
    return db


# CRUD
def create_solve(document):
    db = get_db()
    result = db.solvesRubiks.insert_one(document)

    return result.inserted_id


def read_solve(document):
    db = get_db()
    return db.solvesRubiks.find_one(document)


def read_all_solves(sorted_by=None):
    db = get_db()

    if sorted_by:
        return db.solvesRubiks.find().sort(sorted_by)

    return db.solvesRubiks.find()


def update_solve(document, new_document, many: bool = False):
    db = get_db()
    if many:
        result = db.solvesRubiks.update_many(document, new_document)
    else:
        result = db.solvesRubiks.update_one(document, new_document)

    return result.modified_count


def delete_solve(document: dict, many: bool = False):
    db = get_db()
    if many:
        result = db.solvesRubiks.delete_many(document)
    else:
        result = db.solvesRubiks.delete_one(document)

    return result.deleted_count


def execute_query(query):
    db = get_db()
    result = db.solvesRubiks.aggregate(query)
    return list(result)


def transform_cetiseconds_to_seconds(cetiseconds):
    if cetiseconds == None:
        return cetiseconds
    if cetiseconds == "DNF":
        return cetiseconds
    cetiseconds = int(cetiseconds)
    seconds = cetiseconds // 100
    cetiseconds = cetiseconds % 100
    total_seconds = seconds + cetiseconds / 100
    return round(total_seconds, 2)


def calculate_average(solves: list):

    print("Tiempos:", solves)
    if solves.count("DNF") >= 2:
        return "DNF"

    # Quitar la mejor y la peor si es DNF cuenta como peor
    solves_average = list(filter(lambda solve: solve != "DNF", solves))

    if len(solves_average) == 5:
        solves_average.remove(min(solves_average))

    if len(solves_average) >= 2:
        solves_average.remove(max(solves_average))

    if solves_average:
        average = sum(solves_average) / 3
        return round(average, 2)


# Ejemplo de uso
if __name__ == "__main__":
    # Crear un documento
    document = {
        "person": "Felipe Ignacio Bastidas López",
        "solve_1": "DNF",
        "solve_2": "1321",
        "solve_3": "1402",
        "solve_4": "DNF",
        "solve_5": "1541",
        "country": "Chile",
    }

    # Insertar un documento
    create_solve(document)

    # Leer un documento
    print(read_solve({"person": "Felipe Ignacio Bastidas López"}))

    # Leer todos los documentos
    for solve in read_all_solves():
        solves = [
            solve["solve_1"],
            solve["solve_2"],
            solve["solve_3"],
            solve["solve_4"],
            solve["solve_5"],
        ]
        solves = list(map(transform_cetiseconds_to_seconds, solves))
        print(
            "El competidor",
            solve["person"],
            "de",
            solve["country"],
            "tiene los siguientes tiempos:",
            solves,
            "su promedio es",
            calculate_average(solves),
            "su mejor tiempo es",
            min(filter(lambda solve: solve != "DNF", solves)),
        )

    # Actualizar un documento
    print(
        "Se actualizaron",
        update_solve(
            {"person": "Felipe Ignacio Bastidas López"},
            {"$set": {"country": "China"}},
            False,
        ),
        "documentos",
    )

    # Eliminar un documento
    print(
        "Se eliminaron",
        delete_solve({"person": "Felipe Ignacio Bastidas López"}),
        "documentos",
    )

    # Mostrar el pais y la cantidad de competidores de cada pais
    query = [
        {
            "$group": {
                "_id": "$country",
                "count": {"$sum": 1},
            }
        }
    ]

    for result in execute_query(query):
        print(
            "El pais",
            result["_id"],
            "tiene",
            result["count"],
            "competidores",
        )

    # Promedio de los mejores tiempos de cada pais
    query = [
        {"$match": {"fastest_solve": {"$ne": "DNF"}}},
        {
            "$group": {
                "_id": "$country",
                "average_fastest_solve": {"$avg": "$fastest_solve"},
            }
        },
    ]

    result = execute_query(query)
    for country in result:
        print(
            "El pais",
            country["_id"],
            "tiene el mejor tiempo de",
            transform_cetiseconds_to_seconds(country["average_fastest_solve"]),
            "segundos",
        )
