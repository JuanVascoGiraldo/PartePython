from flask import Flask, render_template, make_response
from flask_mysqldb import MySQL
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model
import io

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'us-cdbr-east-04.cleardb.com'
app.config['MYSQL_USER'] = 'b00626f5b867f4'
app.config['MYSQL_PASSWORD'] = '11819e67'
app.config['MYSQL_DB'] = 'heroku_d3addcd55daeffa'
mysql = MySQL(app)
plt.style.use('fivethirtyeight')

@app.route("/")
def index():
    return "Hola"


@app.route('/simple.png/<id>', methods=['GET'])
def simple_image(id=None):
    cursor = mysql.connection.cursor()
    cursor.execute("Select dia, cantidad from cantidadcaloria where id_usu = %s", (id,))
    data = cursor.fetchall()
    lista1 = []
    lista2 = []
    for i in data:
        lista1.append(((i[0]).split("/"))[0])
        lista2.append(i[1])
    plt.rcParams['figure.figsize'] = (10, 5)
    tamanios = [30, 31]
    plt.scatter(lista1, lista2, s=tamanios[0])
    df = pd.DataFrame()
    df["dia"] = lista1
    df["cantidad"] = lista2
    dataX = df[["dia"]]
    X_train = np.array(dataX)
    y_train = df['cantidad'].values
    regr = linear_model.LinearRegression()
    regr.fit(X_train, y_train)
    x = range(0, 31)
    lista3 = []
    for i in x:
        lista3.append(regr.coef_ * i + regr.intercept_)
    plt.plot(x, lista3)
    plt.axhline(0, color="black")
    plt.axvline(0, color="black")
    plt.xlim(0, 31)
    plt.xlabel("Dias")
    plt.ylabel("Cantidad de Calorias")

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    response = make_response(buffer.getvalue())
    response.mimetype = 'image/png'
    cursor.close()
    return response

@app.route('/verProgreso/<id>', methods=['GET'])
def hola(id=None):
    cursor = mysql.connection.cursor()
    cursor.execute("Select dia, cantidad from cantidadcaloria where id_usu = %s", (id,))
    data = cursor.fetchall()
    uwu = len(data)
    if len(data) >= 10:
        lista1 = []
        lista2 = []
        for i in data:
            lista1.append(((i[0]).split("/"))[0])
            lista2.append(i[1])
        df = pd.DataFrame()
        df["dia"] = lista1
        df["cantidad"] = lista2
        dataX = df[["dia"]]
        X_train = np.array(dataX)
        y_train = df['cantidad'].values
        regr = linear_model.LinearRegression()
        regr.fit(X_train, y_train)
        y_t = regr.predict([[30]])
        mensaje = "Si sigues con este ritmo en 30 dias quemaras ", y_t[0], " Calorias"
        cursor.close()
    else:
        mensaje ="Necesita a ver registrado la rutina almenos de 10 veces"
    return render_template('verProgreso.html', mensaje=mensaje, id=id, cantidad=uwu )

if __name__ == '__main__':
    import sys
    app.run(debug='d' in sys.argv[-1])