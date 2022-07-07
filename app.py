from flask import Flask, render_template, request, redirect, send_from_directory, url_for
from flaskext.mysql import MySQL
from datetime import datetime
import os


app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']='yWApJA!J(7[rTMDL'
app.config['MYSQL_DATABASE_DB']='gamerstore'
mysql.init_app(app)

CARPETA = os.path.join('uploads')
app.config['CARPETA'] = CARPETA

@app.route('/uploads/<imagen>')
def uploads(imagen):
    return send_from_directory(app.config['CARPETA'], imagen)

@app.route('/')
def index():
    sql = "SELECT * FROM `gamerstore`.`juegos`;"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    juegos = cursor.fetchall()
    print(juegos)
    conn.commit()
    return render_template('tienda/index.html', juegos=juegos)

@app.route('/eliminar/<int:id>')
def eliminar(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT linkImg FROM `gamerstore`.`juegos` WHERE id=%s", id)
    fila = cursor.fetchall()
    os.remove(os.path.join(app.config['CARPETA'], fila[0][0]))
    cursor.execute("DELETE FROM `gamerstore`.`juegos` WHERE id = %s;", (id))
    conn.commit()
    return redirect('/')

@app.route('/editar/<int:id>')
def editar(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM `gamerstore`.`juegos` WHERE id = %s;", (id))
    juego = cursor.fetchall()
    conn.commit()

    return render_template('tienda/edit.html', juego=juego)

@app.route('/actualizar', methods=['POST'])
def actualizar():
    _nombre = request.form['nombre']
    _desarrollador = request.form['desarrollador']
    _img = request.files['imagen']
    _precio = request.form['precio']
    _descuento = request.form['descuento']
    _calificacion = request.form['calificacion']
    id = request.form['id']

    now = datetime.now().strftime('%Y%H%M%S')
    
    sql = "UPDATE `gamerstore`.`juegos` SET `nombre`=%s, `desarrollador`=%s, `precio`=%s, `descuento`=%s, `calificacion`=%s WHERE id=%s;"
    
    if _descuento == None or _descuento == '':
        _descuento = "NULL"

    datos =(_nombre, _desarrollador, _precio, _descuento, _calificacion, id)
    conn = mysql.connect()
    cursor = conn.cursor()

    now = datetime.now().strftime("%Y%H%M%S")
    if _img.filename != '':
        nuevoNombreFoto = now + _img.filename
        _img.save("uploads/" + nuevoNombreFoto)
        cursor.execute("SELECT linkImg FROM `gamerstore`.`juegos` WHERE id=%s", id)
        fila = cursor.fetchall()
        os.remove(os.path.join(app.config['CARPETA'], fila[0][3]))
        cursor.execute("UPDATE `gamerstore`.`juegos` SET linkImg=%s WHERE id=%s", (nuevoNombreFoto, id))
        conn.commit()
    
    cursor.execute(sql, datos)
    conn.commit()

    return redirect('/')

@app.route('/nuevo-juego')
def agregar():
    return render_template('tienda/create.html')

@app.route('/guardar', methods=['POST'])
def guardar():
    _nombre = request.form['nombre']
    _desarrollador = request.form['desarrollador']
    _img = request.files['imagen']
    _precio = request.form['precio']
    _descuento = request.form['descuento']
    _calificacion = request.form['calificacion']

    now = datetime.now().strftime('%Y%H%M%S')

    if _img.filename != '':
        nuevoNombreFoto = now + _img.filename
        _img.save("uploads/" + nuevoNombreFoto)

    sql = "INSERT INTO `juegos` (`id`, `nombre`, `desarrollador`, `linkImg`, `precio`, `descuento`, `calificacion`) VALUES (NULL, %s, %s, %s, %s, %s, %s);"
    if _descuento == None or _descuento == '':
        _descuento = "NULL"
    datos =(_nombre, _desarrollador, nuevoNombreFoto, _precio, _descuento, _calificacion)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()
    
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)