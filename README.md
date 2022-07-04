# Readme

Proyek menggunakan 3 database
data untuk transaksi tersimpan di root folder 'session_database.db' menggunakan SQLite (SQL)
data untuk produk tersimpan dalam 'data generator/products-with-price.json' (MongoDB)
data query user tersimpan dalam 'data generator/neo4j.query.txt' (Neo4J)

folder 'data generator' berisi data dan cara mengenerate data
folder 'static' berisi static files
folder 'templates' berisi HTML Templates
.env berisi credential untuk Neo4J

Cara memasukkan database
SQL tidak perlu dimasukkan karena otomatis
MongoDB
 - Masukkan 'data generator/products-with-price.json' ke dalam MongoDBCompass
 - nyalakan services MongoDB
Neo4J
 - Nyalakan services Neo4J
 - Masuk ke localhost:7474
 - masukkan query yang ada di 'data generator/neo4j.query.txt' satu persatu dipisahkan oleh enter 

Asal Data
Data transaksi dan log SQL di generate sendiri
Data produk dan detailnya di web-scraping pada website dekoruma.com
Data user dibuat sendiri menggunakan library faker dan yang dibuat adalah query neo4j nya bukan datanya secara langsung

Cara Menjalankan program
 - masuk ke root folder
 - buat ganti credential Neo4J di .env dengan credential sesuai dengan komputer masing - masing
 - jika error install python-dotenv (pip install python-dotenv)
 - di cli ketik 'python flaskapp.py'
 - enjoy...

