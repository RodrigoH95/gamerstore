from flask import Flask, jsonify, render_template, request, redirect
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
from datetime import datetime
import os
import cloudinary
import cloudinary.uploader
import cloudinary.api
from pathlib import Path
from flask_simplelogin import SimpleLogin, is_logged_in, login_required, Message

cloudinary.config( 
  cloud_name = "diwqcbv9y", 
  api_key = "169594223867694", 
  api_secret = "E_cSz0v2icml5B2QtRRNwmP3SwM" 
)

print(os.path.curdir)
app = Flask(__name__)

messages = {
    'login_success': Message('Iniciaste sesión!'),
    'login_failure': 'No se pudo iniciar sesión',
    'is_logged_in': Message('Ya iniciaste sesión', 'success'),
    'logout': None,
    'login_required': 'Debe iniciar sesión para continuar',
    'access_denied': 'Acceso denegado',
    'auth_error': 'Error de autenticación： {0}'
}

app.config['SECRET_KEY'] = 'clave-secreta'
app.config['SIMPLELOGIN_USERNAME'] = 'admin'
app.config['SIMPLELOGIN_PASSWORD'] = 'codoacodo22'

SimpleLogin(app, messages=messages)

mysql = MySQL(cursorclass=DictCursor)
app.config['MYSQL_DATABASE_HOST']='sql10.freesqldatabase.com'
app.config['MYSQL_DATABASE_USER']='sql10504583'
app.config['MYSQL_DATABASE_PASSWORD']='m1QjA2nK9H'
app.config['MYSQL_DATABASE_DB']='sql10504583'

mysql.init_app(app)

@app.route('/')
def index():
    filtro = request.args.get('filtrar')
    orden = request.args.get('orden')
    if filtro == None:
        filtro = "id"
    elif filtro == "precio":
        filtro = "precio * (1 - descuento / 100)"
    if orden == None:
        orden = "DESC"
    sql = f'SELECT * FROM `sql10504583`.`juegos` ORDER BY {filtro} {orden};'
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    juegos = cursor.fetchall()
    # Seleccion de los 4 juegos con mayor descuento (Colocar las ofertas en el return)
    # sql = f'SELECT * FROM `sql10504583`.`juegos` ORDER BY descuento DESC LIMIT 4;'
    # cursor.execute(sql)
    # ofertas = cursor.fetchall()
    conn.commit()
    return render_template('tienda/index.html', juegos=juegos, admin=is_logged_in('admin'))

@app.route('/lista')
@login_required(username='admin')
def lista():
    sql = "SELECT * FROM `sql10504583`.`juegos` ORDER BY id ASC;"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    juegos = cursor.fetchall()
    conn.commit()
    return render_template('admin/tabla.html', juegos = juegos)

@app.route('/eliminar/<int:id>')
@login_required(username='admin')
def eliminar(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT linkImg FROM `sql10504583`.`juegos` WHERE id=%s", id)
    fila = cursor.fetchall()
    print(fila)
    cloudinary.uploader.destroy(Path(fila[0]['linkImg']).stem)
    cursor.execute("DELETE FROM `sql10504583`.`juegos` WHERE id = %s;", (id))
    conn.commit()
    return redirect('/lista')

@app.route('/editar/<int:id>')
@login_required(username='admin')
def editar(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM `sql10504583`.`juegos` WHERE id = %s;", (id))
    juego = cursor.fetchall()
    conn.commit()

    return render_template('tienda/edit.html', juego=juego)

@app.route('/actualizar', methods=['POST'])
@login_required(username='admin')
def actualizar():
    _nombre = request.form['nombre']
    _desarrollador = request.form['desarrollador']
    _img = request.files['imagen']
    _precio = request.form['precio']
    _descuento = request.form['descuento']
    _calificacion = request.form['calificacion']
    id = request.form['id']

    now = datetime.now().strftime('%Y%H%M%S')
    
    sql = "UPDATE `sql10504583`.`juegos` SET `nombre`=%s, `desarrollador`=%s, `precio`=%s, `descuento`=%s, `calificacion`=%s WHERE id=%s;"
    
    if _descuento == None or _descuento == '':
        _descuento = "NULL"

    datos =(_nombre, _desarrollador, _precio, _descuento, _calificacion, id)
    conn = mysql.connect()
    cursor = conn.cursor()


    now = datetime.now().strftime('%Y%H%M%S')

    if _img.filename != '':
        nuevoNombreFoto = (now + Path(_img.filename).stem).replace(" ", "")
        cloudinary.uploader.upload(_img, 
        public_id = nuevoNombreFoto)
        nuevoNombreFoto = cloudinary.CloudinaryImage(nuevoNombreFoto).build_url()
        cursor.execute("SELECT linkImg FROM `sql10504583`.`juegos` WHERE id=%s", id)
        fila = cursor.fetchall()
        cloudinary.uploader.destroy(Path(fila[0]['linkImg']).stem)
        cursor.execute("UPDATE `sql10504583`.`juegos` SET linkImg=%s WHERE id=%s", (nuevoNombreFoto, id))
        conn.commit()
    
    cursor.execute(sql, datos)
    conn.commit()

    return redirect('/lista')

@app.route('/nuevo-juego')
@login_required(username='admin')
def agregar():
    return render_template('tienda/create.html')

@app.route('/guardar', methods=['POST'])
@login_required(username='admin')
def guardar():
    _nombre = request.form['nombre']
    _desarrollador = request.form['desarrollador']
    _img = request.files['imagen']
    _precio = request.form['precio']
    _descuento = request.form['descuento']
    _calificacion = request.form['calificacion']

    now = datetime.now().strftime('%Y%H%M%S')

    if _img.filename != '':
        nuevoNombreFoto = (now + Path(_img.filename).stem).replace(" ", "")
        cloudinary.uploader.upload(_img, 
        public_id = nuevoNombreFoto)
        nuevoNombreFoto = cloudinary.CloudinaryImage(nuevoNombreFoto).build_url()

    sql = "INSERT INTO `juegos` (`id`, `nombre`, `desarrollador`, `linkImg`, `precio`, `descuento`, `calificacion`) VALUES (NULL, %s, %s, %s, %s, %s, %s);"
    if _descuento == None or _descuento == '':
        _descuento = "NULL"
    datos =(_nombre, _desarrollador, nuevoNombreFoto, _precio, _descuento, _calificacion)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()
    
    return redirect('/lista')

if __name__ == '__main__':
    app.run(debug=True)