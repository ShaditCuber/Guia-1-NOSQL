from pymongo import MongoClient
import math


def get_db():
    client = MongoClient("localhost:27017")
    db = client.rubiks
    return db


# CRUD
def create_solve(document):
    db = get_db()
    db.solvesRubiks.insert_one(document)


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
        db.solvesRubiks.update_many(document, new_document)
    else:
        db.solvesRubiks.update_one(document, new_document)


def delete_solve(document: dict, many: bool = False):
    db = get_db()
    if many:
        db.solvesRubiks.delete_many(document)
    else:
        db.solvesRubiks.delete_one(document)


def transform_cetiseconds_to_seconds(cetiseconds):
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

    # # Insertar un documento
    create_solve(document)

    # # Leer un documento
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

    # # Actualizar un documento
    update_solve(
        {"person": "Felipe Ignacio Bastidas López"},
        {"$set": {"solve_1": "947"}},
    )

    # Eliminar un documento
    delete_solve({"person": "Felipe Ignacio Bastidas López", "solve_1": "DNF"})
