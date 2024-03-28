# CRUD MONGO DB + PYTHON

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

