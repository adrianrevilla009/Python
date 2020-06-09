from tkinter import ttk #Importamos tkinter y todos sus componentes con * 
from tkinter import *   
import sqlite3  #Importamos el modulo de conexion a la base de datos

class Product:

    nombreBD = 'BaseDatos.db'       #Almacenamos el nombre de la BD creada

    #CONSTRUCTOR
    def __init__(self,window):      
        self.wind = window
        self.wind.title('Aplicacion inicial.')
        #FRAME
        frame = LabelFrame(self.wind, text='Registra un nuevo producto')    #Crea un frame dentro de la ventana para posicionar elementos
        frame.grid(row=0,column=0,columnspan=3,pady=20)        #La funcion grid posiciona el frame en la ventana
        #Row y Column es la posición donde se coloca el frame en la ventana
        #Columspan es la posicion desde donde los elementos se van a empezar a posicionar
        #Padding es el espaciado entre elementos
        #LABEL NOMBRE
        Label(frame,text='Nombre: ').grid(row=1,column=0) #Crea un label en el frame y lo posiciona con grid
        self.nombre = Entry(frame) #Crea una caja de texto en el frame y guarda el resultado en el atributo name
        self.nombre.focus() #Al ejecutar el cursor se posiciona en el input del nombre
        self.nombre.grid(row=1,column=1) #Posiciona la caja de texto

        #LABEL PRECIO
        Label(frame,text='Precio: ').grid(row=2,column=0) 
        self.precio = Entry(frame) 
        self.precio.grid(row=2,column=1) 

        #BOTON
        ttk.Button(frame, text='Guardar producto',command=self.añadirProducto).grid(row=3,columnspan=2,sticky=W+E)
        #Sticky para que el boton ocupe todo el frame (desde este a oeste)
        #Command sirve para ejecutar una funcion al hacer click en el boton

        #CONTROL DE MENSAJES
        self.mensajes = Label(text='',fg='red') #Se inicializa en null y su color es rojo
        self.mensajes.grid(row=3,column=0,columnspan=2,sticky=W+E)

        #CREAR TABLA
        self.tabla = ttk.Treeview(height=10,columns=2)  #Crea una tabla 10filas 2columnas
        self.tabla.grid(row=2,column=0,columnspan=2)
        self.tabla.heading('#0',text='Nombre', anchor=CENTER)   #Crea los titulos de la tabla
        self.tabla.heading('#1',text='Precio', anchor=CENTER)
        #Anchor es para centrar el texto y #0 para dar un indice a las columnas      

        #BOTONES DE ACTUALIZAR Y BORRAR
        ttk.Button(text = 'Borrar',command=self.borrarProducto).grid(row=5,column=0,sticky=W+E)
        ttk.Button(text = 'Actualizar',command=self.editarProducto).grid(row=5,column=1,sticky=W+E)
        #OBTENEMOS E INSERTAMOS LOS DATOS EN LA TABLA
        self.mostrarProductos()     

    #EJECUTA UNA CONSULTA A LA BD
    def ejecutarConsulta(self,query,parameters=()):   
        with sqlite3.connect(self.nombreBD) as conexion:    #Creamos una variable conexion
            cursor = conexion.cursor()                  #Obtiene la posicion de la conexion en la BD
            resultado = cursor.execute(query,parameters)            #Definimos la consulta a la base de datos (le pasa la query y los parametros)
            #En caso de un insert no devolvera nada, pero en caso de un select si
            conexion.commit()       #Ejecutamos la consulta
        return resultado

    #OBTIENE TODOS LOS PRODUCTOS
    def mostrarProductos(self):
        #BORRAMOS LOS DATOS DE LA TABLA
        datosTabla = self.tabla.get_children()      #Obtiene los datos de la tabla con get_children()
        for elemento in datosTabla:                 #Borramos todos los datos de la tabla
            self.tabla.delete(elemento)

        consulta = 'SELECT * FROM Producto ORDER BY nombre DESC'
        datos = self.ejecutarConsulta(consulta)     #llama a la función para la consulta
        #Indice 0 -> identificador / indice 1 -> nombre / indice 2 -> precio
        for fila in datos:
            self.tabla.insert('',0,text = fila[1],values = fila[2])
    
    #VALIDACION DE DATOS PARA EVITAR ERRORES DE INPUT
    def validarProducto(self):
        return len(self.nombre.get()) != 0 and len(self.precio.get()) != 0
        #Comprueba si los campos nombre y precio no son vacios
        #Para obtener el dato introducido se usa la funcion get()

    #AÑADE DATOS A LA BD
    def añadirProducto(self):
        if self.validarProducto():
            consulta = 'INSERT INTO Producto VALUES(NULL,?,?)'   #Los elementos ? indicarán cuando se ejecute la consulta donde meter los parametros que se pasan
            parametros = (self.nombre.get(),self.precio.get())
            self.ejecutarConsulta(consulta,parametros)  #Ejecuta la consulta
            self.mensajes['text'] = 'El producto {} ha sido insertado.'.format(self.nombre.get())
            #Añadimos un texto al Label mensajes en la propiedad text
            #Le pasamos por parametro un dato con la funcion format() y las llaves {}
            self.nombre.delete(0,END)   #Borra los campos en los input una vez añadido el producto
            self.precio.delete(0,END)
        else:
            self.mensajes['text'] = 'El nombre y precio es requerido.'
        self.mostrarProductos() #Una vez insertados los datos se refresca la tabla para que se muestren

    def borrarProducto(self):
        self.mensajes['text'] = ''
        #Comprueba si hay un registro seleccionado
        try:
            self.tabla.item(self.tabla.selection())['text'] #La funcion .selection devuelve true si el elemento item esta seleccionado en la tabla
        except IndexError as e:
            self.mensajes['text'] = 'Debes seleccionar un producto'
            return
        self.mensajes['text'] = ''
        #En caso de haberlo obtenemos el valor
        nombre = self.tabla.item(self.tabla.selection())['text']
        consulta = 'DELETE FROM Producto WHERE nombre = ?'
        #Ejecutamos la consulta y mostramos un mensaje de exito
        self.ejecutarConsulta(consulta,(nombre,))
        self.mensajes['text'] = 'El registro {} ha sido eliminado.'.format(nombre)
        #Actualizamos la tabla
        self.mostrarProductos()

    def editarProducto(self):
        #comprobación de elemento seleccionado
        self.mensajes['text'] = ''
        try:
            self.tabla.item(self.tabla.selection())['text'] 
        except IndexError as e:
            self.mensajes['text'] = 'Debes seleccionar un producto'
            return
        #obtenemos los datos del elemento seleccionado
        nombreAnterior = self.tabla.item(self.tabla.selection())['text']
        precioAnterior = self.tabla.item(self.tabla.selection())['values'][0]
        #creamos una ventana para modificar los datos
        self.ventanaEdicion = Toplevel()    #Crea una ventana
        self.ventanaEdicion.title = 'Edición del producto'

        #Ahora vamos a crear los elementos de la ventana de edición
        Label(self.ventanaEdicion, text = 'Nombre antiguo: ').grid(row=0,column=1)
        Entry(self.ventanaEdicion,textvariable=StringVar(self.ventanaEdicion,value = nombreAnterior),state = 'readonly').grid(row=0,column=2)
        #Propiedad textvariable sirve para mostrar dato por pantalla (en modo lectura)
        Label(self.ventanaEdicion, text = 'Nombre nuevo: ').grid(row=1,column=1)
        nuevoNombre = Entry(self.ventanaEdicion)
        nuevoNombre.grid(row=1,column=2)

        Label(self.ventanaEdicion, text = 'Precio antiguo: ').grid(row=2,column=1)
        Entry(self.ventanaEdicion,textvariable=StringVar(self.ventanaEdicion,value = precioAnterior),state = 'readonly').grid(row=2,column=2)
        Label(self.ventanaEdicion, text = 'Precio nuevo: ').grid(row=3,column=1)
        nuevoPrecio = Entry(self.ventanaEdicion)
        nuevoPrecio.grid(row=3,column=2)

        Button(self.ventanaEdicion,text='Actualizar',command=lambda:self.editarParametros(nuevoNombre.get(),nombreAnterior,nuevoPrecio.get(),precioAnterior)).grid(row=4,column=2,sticky=W)
        #no entiendo la funcion lambda

    def editarParametros(self,nuevoNombre,nombreAnterior,nuevoPrecio,precioAnterior):
        #ejecutamos la consulta de actualización
        consulta = 'UPDATE Producto SET nombre = ?, precio = ? WHERE nombre = ? AND precio = ?'
        parametros = (nuevoNombre,nuevoPrecio,nombreAnterior,precioAnterior)
        self.ejecutarConsulta(consulta,parametros)
        #cerramos la ventana de edición
        self.ventanaEdicion.destroy()
        self.mensajes['text'] = 'El registro {} ha sido actualizado correctamente'.format(nombreAnterior)
        self.mostrarProductos()



if __name__ == '__main__':      #Comprueba si el archivo es el main
    window = Tk()               #Crea una ventana 
    application = Product(window)   #Pasamos la ventana al constructor del producto para poder pasarle parametros
    window.mainloop()               #Ejecucion de la ventana