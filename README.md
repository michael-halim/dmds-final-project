# Data Modelling for Data Science Project

## The main task in this project is to uses 3 different databases and make analysis from the data

## This Project Uses 3 Databases
- [SQLite3] - SQLite for Transactional and Log Data
- [MongoDB] - MongoDB for dealing with unstructured data
- [Neo4J] - Neo4J for handling user data that has child-parent relationship

## Installation
- SQLite3 is automatic
- MongoDB
 - put 'data generator/products-with-price.json' to MongoDBCompass
 - start MongoDB services
- Neo4J
 - Start Neo4J services
 - go to localhost:7474
 - Put 'data generator/neo4j query.txt' query block by block separated by enter
- Main Program
 - Change the Neo4J credential in .env
 - Install python-dotenv ```pip install python-dotenv ```
 - In CLI  ```python flaskapp.py ```
 - Enjoy

## Data Origin
- SQLite3 Data is generated by code
- Product data and its detail is scraped from [https:dekoruma.com][PlDb]
- User data is queries generated by code with faker library

## Data Location
- SQLite3 data in 'session_database.db'
- MongoDB data in 'data generator/products-with-price.json'
- Neo4J data in 'data generator/neo4j query.txt'

## Details
- 'data generator' folder contains data and how to generate them
- 'static' folder contains static files
- 'templates' contains HTML Templates
- .env contains credential for Neo4J

