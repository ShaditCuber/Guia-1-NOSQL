# CRUD MONGO DB + PYTHON

## Modelo de Datos 
#,Person,Solve 1,Solve 2,Solve 3,Solve 4,Solve 5,Fastest Solve,Country

Mi dataset es parte de los resultados de la [WCA](www.worldcubeassociation.org), que es un  organismo sin fines de lucro dedicado a la competencia de Cubos de Rubiks.

Cada json tiene un nombre del competidor , 5 tiempos de sus soluciones en el cubo de Rubik 3x3, tiene la solución mas rápida y su País.


## Instrucciones de Uso

Primero instalar pipenv en caso de no tenerlo

```
sudo apt install pipenv
```

Encender la shell de mongoDB en caso de no tenerla iniciada

```
sudo service mongod start
```


Ejecutar dentro de esta misma carpeta

```
pipenv install
pipenv shell
```

Ejecutar csv_to_mongo para cargar el csv como json a mongodb

```
python csv_to_mongo.py
```



Ejecutar index.py y ver el CRUD dentro de ese archivo, por consola se muestran valores de las consultas 


```
python index.py
```

