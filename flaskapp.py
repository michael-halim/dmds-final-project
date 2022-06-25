from flask import Flask, render_template, request
import sqlite3
import mongoconnect
import neo4jconnect as neo
import os

from flask_googlecharts import GoogleCharts
from flask_googlecharts import MaterialBarChart

from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)
charts = GoogleCharts(app)

mongo_client = mongoconnect.PyMongoClient('mongodb://localhost:27017/', 'proyek-dmds', 'products-final')
neo_client = neo.Neo4jConnector('bolt://localhost:7687', os.environ.get('USER_NEO4J'), os.environ.get('PASSWORD_NEO4J'))


@app.route('/get-transaction-details')
def func_name(foo):
    return render_template('expression')

@app.route('/get-member-relations/', methods=["GET", "POST"])
def memberrelations():
    return render_template('member_relations.html', membername = request.form['names'], memberchildren = neo_client.get_member_children(request.form["names"]), memberparent = neo_client.get_member_parent(request.form["names"]))

@app.route('/membersearch')
def members():
    return render_template('member_search.html', member_names = neo_client.get_member_names())

@app.route('/transactiondata/')
def transactiondata():
    sqlite_client = sqlite3.connect('session_database.db')
    cursor = sqlite_client.cursor()
    cursor.execute('SELECT * FROM transaction_details')
    raw_data = cursor.fetchall()
    
    # Get user name from Neo4J and product name from MongoDB
    data = []
    for obj in raw_data:
        product_name = mongo_client.getDetailByID(obj[3])['Nama']
        user_name = neo_client.get_member_names_by_id(obj[1])[0]
        data.append([obj[0],obj[1],user_name,obj[2], obj[3],product_name,obj[-1]])

    return render_template('transaction_data.html', tdata = data)

@app.route('/sessiondata/')
def sessiondata():
    sqlite_client = sqlite3.connect('session_database.db')
    cursor = sqlite_client.cursor()
    cursor.execute('SELECT * FROM session_data')
    _sessionlist = cursor.fetchall()
    return render_template('session_data.html', sessionlist = _sessionlist)

@app.route('/products/')
def products():
    return render_template('products.html', productlist = mongo_client.getAllShort())

@app.route('/products/<int:id_p>')
def product_detail(id_p):
    return render_template('product_detail.html',detail_product = mongo_client.getAllByID(id_p))

@app.route('/reporting/')
def reporting():
    return render_template('reporting.html')

@app.route('/reporting/contributor_vs_profit')
def contributor_vs_profit():

    # Get 10 contributor with the highest profit
    sqlite_client = sqlite3.connect('session_database.db')
    cursor = sqlite_client.cursor()
    cursor.execute('''SELECT contributor_id, SUM(profit_amount) as total
                        FROM profit_data
                        GROUP BY contributor_id
                        ORDER BY total DESC
                        LIMIT 10''')
    raw_data = cursor.fetchall()

    # Get user names in Neo4J and append it to a list
    data = []
    for obj in raw_data:
        data.append([neo_client.get_member_names_by_id(obj[0])[0],obj[1]])

    # Construct a Chart
    chart = MaterialBarChart('contributor_vs_profit', options={'title': 'Contributor VS Profit', 
                                                                'width': 1300, 
                                                                'height': 600})
    chart.add_column('string', 'Nama')
    chart.add_column('number', 'Komisi')

    # Added data to chart
    chart.add_rows(data)
    charts.register(chart)

    return render_template('contributor_vs_profit.html')

@app.route('/reporting/user_vs_profit')
def user_vs_profit():

    # Get 10 user with the highest profit
    sqlite_client = sqlite3.connect('session_database.db')
    cursor = sqlite_client.cursor()
    cursor.execute('''SELECT user_id, SUM(profit_amount) as total
                        FROM profit_data
                        GROUP BY user_id
                        ORDER BY total DESC
                        LIMIT 11''')
    raw_data = cursor.fetchall()

    # Get user names in Neo4J and append it to a list
    data = []
    for obj in raw_data:
        data.append([neo_client.get_member_names_by_id(obj[0])[0],obj[1]])

    # Construct a Chart
    chart = MaterialBarChart('user_vs_profit', options={'title': 'User VS Profit', 
                                                        'width': 1300, 
                                                        'height': 600})
    chart.add_column('string', 'Nama')
    chart.add_column('number', 'Komisi')

    # Added data to chart
    data.pop(0) # excluding company
    chart.add_rows(data)
    charts.register(chart)

    return render_template('user_vs_profit.html')

@app.route('/reporting/most_exp_tsc')
def most_exp_tsc():

    # Get user_id, product_id, qty from DB
    sqlite_client = sqlite3.connect('session_database.db')
    cursor = sqlite_client.cursor()
    cursor.execute('''SELECT user_id, product_id, qty
                        FROM transaction_details
                    ''')
    raw_data = cursor.fetchall()

    # Get name and price from MongoDB
    data = []
    for obj in raw_data:
        tmp = mongo_client.getDetailByID(obj[1])
        data.append([obj[0],tmp['Nama'], tmp['Harga'] * obj[-1]])

    # Count total transactions of every user_id
    from collections import Counter
    counter = Counter()
    for user_id, product_name, total_price in data:
        counter[user_id] += total_price

    data = list(counter.items())

    # Sort the user by the total price transaction
    data.sort(key=lambda u: u[1])
    
    # Take top 10 
    data = data[-10:]

    #for the products sold
    user_list = []
    for user in data:
        details_list = []
        for item in raw_data:
            if item[0] == user[0]:
                user_name = neo_client.get_member_names_by_id(item[0])[0]
                product_id = item[1]
                product_details = mongo_client.getDetailByID(product_id)
                product_name = product_details['Nama']
                product_brand = product_details['Brand']
                product_price = product_details['Harga']
                qty = item[2]
                details_list.append([user_name, product_id, product_name, product_brand, product_price, qty])
        user_list.append(details_list)
    
    # Get user names from Neo4J
    tmp = []
    for obj in data:
        tmp.append([neo_client.get_member_names_by_id(obj[0])[0],obj[1]])
    
    data = tmp

    # Construct a Chart
    chart = MaterialBarChart('most_exp_tsc', options={'title': 'Most Expensive Transaction', 
                                                        'width': 1300, 
                                                        'height': 600,
                                                        })
    chart.add_column('string', 'Nama')
    chart.add_column('number', 'Total Transaction')

    # Added data to chart
    chart.add_rows(data)
    charts.register(chart)

    return render_template('most_expensive_transaction.html', userlist = user_list)

@app.route('/reporting/most_clicked_product')
def most_clicked_product():
    sqlite_client = sqlite3.connect('session_database.db')
    cursor = sqlite_client.cursor()
    cursor.execute('SELECT * FROM session_data')
    _sessionlist = cursor.fetchall()

    data = {}
    for obj in _sessionlist:
        if obj[-1] == 'browse':
            if obj[-2] in data:
                data[obj[-2]] += 1
            else:
                data[obj[-2]] = 1

 
    data = [[k, v] for k, v in data.items()]
    data.sort(key=lambda u: u[1])
    data = data[-10:]
    # Construct a Chart
    chart = MaterialBarChart('most_clicked_product', options={'title': 'Most Clicked Product', 
                                                                'width': 1300, 
                                                                'height': 600})
    chart.add_column('string', 'Nama Produk')
    chart.add_column('number', 'Total Click')

    # Added data to chart
    chart.add_rows(data)
    charts.register(chart)

    return render_template('most_clicked_product.html')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=19067, debug=True)
 