# PolyContacts
> Orane Braillon, Romain Brocheton et Valentin Point  
> Cours de Sécurité des SI, 2022


## Description
Un annuaire en Flask.  


## Installation
### Base de données
Nous utilisons un serveur MySQL pour l'application. Docker nous permet de lancer ce service via la commande suivante :  
```
docker-compose up
```

### Flask
PolyContacts a été créée en Flask. Pour pouvoir lancer l'application, il est nécessaire d'installer certains packages Python :  
```
pip install flask
pip install flask_sqlalchemy
pip install mysql-python
pip install mysqlclient
```

## Lancement
PolyContacts peut être lancé via la commande suivante :
```
python run.py
```

## Utilisation
### Base de données
| Paramètre 	| Valeur            	|
|-----------	|-------------------	|
| Host      	| `localhost:27017` 	|
| Database  	| `db`              	|
| User      	| `user`            	|
| Password  	| `password`        	|

Nous avons pris la liberté d'installer également le service PhpMyAdmin grâce à Docker. Vous pouvez donc visualiser facilement notre base de données à l'adresse [http://localhost:8081](http://localhost:8081).

### Application
L'application est accessible à l'adresse [http://localhost:5000](http://localhost:5000).

### Dockerfile
#### Build
Pour construire le container, exécutez cette commande :
```
docker build --tag annuaire-docker .
docker tag annuaire-docker:latest annuaire-docker:v1.0.0
```

#### Lancement
Pour lancer le container, exécuter cette commande :
```
docker run --publish 5000:5000 annuaire-docker
```

Le site sera accessible à l'adresse [http://localhost:5000](http://localhost:5000).