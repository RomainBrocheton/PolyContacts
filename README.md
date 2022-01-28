# PolyContacts
> Orane Braillon, Romain Brocheton et Valentin Point  
> Cours de Sécurité des SI, 2022


## Description
Un annuaire en Flask.  

## Lancement
PolyContacts peut être lancé via la commande suivante :
```
docker compose up --build
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