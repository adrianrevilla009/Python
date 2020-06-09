from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

#INICIALIZAR SERVIDOR WEB
aplicacion = Flask(__name__) #Objeto de conexion al modulo flask

#CONEXIÓN A LA BASE DE DATOS
aplicacion.config['MYSQL_HOST'] = 'localhost'
aplicacion.config['MYSQL_USER'] = 'root'
aplicacion.config['MYSQL_PASSWORD'] = ''
aplicacion.config['MYSQL_DB'] = 'pythoncontactos'
bd = MySQL(aplicacion)

#CONFIGURACIÓN DE SESIÓN
aplicacion.secret_key = 'adrian'

@aplicacion.route('/')  #ruta a la página principal que será manejada por la función index.
def index():
    conexion = bd.connection.cursor()
    conexion.execute('SELECT * FROM contactos')
    datos = conexion.fetchall() #obtiene los datos 
    return render_template('index.html', contactos = datos)

@aplicacion.route('/añadirContacto', methods=['POST'])  #Metodo post para la obtención de datos
def añadirContacto():
    if request.method == 'POST':
        nombre = request.form['nombre'] #Obtención de datos desde el formulario
        telefono = request.form['telefono']
        email = request.form['email']
        conexion = bd.connection.cursor()     #Obtiene la conexión mysql
        conexion.execute('INSERT INTO contactos (nombre,telefono,email) VALUES (%s,%s,%s)',(nombre,telefono,email))   #Creamos la consulta
        # %s significa que se le pasa un string como parametro
        bd.connection.commit()  #Ejecutamos la consulta y guarda cambios
        flash('Contacto añadido correctamente!')
    return redirect(url_for('index'))

@aplicacion.route('/editarContacto/<string:id>')
def editarContacto(id):
    conexion = bd.connection.cursor()
    conexion.execute('SELECT * FROM contactos WHERE id = %s',(id))
    dato = conexion.fetchall()  #obtiene el dato con el id que le pasamos
    return render_template('editar_contacto.html', contacto = dato[0])   #enviamos la tupla 0 a la plantilla editar_contacto

@aplicacion.route('/actualizarContacto/<string:id>', methods=['POST'])
def actualizarContacto(id):
    if request.method == 'POST':
        nombre = request.form['nombre'] #Obtención de datos desde el formulario
        telefono = request.form['telefono']
        email = request.form['email']
        conexion = bd.connection.cursor()
        conexion.execute('UPDATE contactos SET nombre=%s,telefono=%s,email=%s WHERE id=%s',(nombre,telefono,email,id))
        bd.connection.commit()
        flash('Contacto actualizado correctamente!')
        return redirect(url_for('index'))
    

@aplicacion.route('/borrarContacto/<string:id>')
def borrarContacto(id):
    conexion = bd.connection.cursor()
    conexion.execute('DELETE FROM contactos WHERE id={0}'.format(id))   #se puede usar format, tanto como pasarselos mediante %s
    bd.connection.commit()
    flash('Contacto borrado correctamete!')
    return redirect(url_for('index'))

#COMPROBAR ARCHIVO MAIN Y CORRER EL SERVIDOR
if __name__ == '__main__' :
    aplicacion.run(port=3000,debug=True)    #Ejecuta la conexión del servidor en el puerto 3000 , debug es para que cuando hagamos cambios en el servidor este se reinicie
