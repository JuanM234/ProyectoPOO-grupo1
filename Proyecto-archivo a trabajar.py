!/usr/bin/python3
# -*- coding: utf-8 -*-
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox as mssg
import sqlite3
<<<<<<< HEAD
from os import path
=======
#import re

#validar si la fecha es válida
def es_fecha_valida(fecha_texto):
   espacios = fecha_texto.split('/')
    
   if len(espacios) != 3:
      return False  # La fecha no tiene el formato correcto
    
   dia = int(espacios[0])
   mes = int(espacios[1])
   anio = int(espacios[2])
    
   # Validar el año
   if not (str(dia).isdigit() and str(mes).isdigit() and str(anio).isdigit()):
      return False  # Los componentes no son números
    
   if mes < 1 or mes > 12:
      return False  # Mes fuera de rango
    
   dias_por_mes = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    
   # Verificar si es año bisiesto
   if mes == 2 and ((anio % 4 == 0 and anio % 100 != 0) or (anio % 400 == 0)):
      dias_por_mes[1] = 29
    
   if dia < 1 or dia > dias_por_mes[mes - 1]:
      return False  # Día fuera de rango para el mes dado
    
   return True  # La fecha es válida
>>>>>>> 58e67181cca3adfb73ada828b7e7da011c02d0fb

class Inventario:
  def __init__(self, master=None):
    self.path = str(path.dirname(__file__))
    self.db_name = self.path + r'/Inventario.db'
    self.ico=self.path + r'/f2.ico'
    ancho=830;alto=840 # Dimensione de la pantalla
    actualiza = None

    # Crea ventana principal
    self.win = tk.Tk() 
    self.win.geometry(f"{ancho}x{alto}")
    self.win.iconbitmap(self.ico) 
    self.win.resizable(True, True)
    self.win.title("Manejo de Proveedores") 

    #Centra la pantalla
    self.centra(self.win,ancho,alto)

    # Contenedor de widgets   
    self.win = tk.LabelFrame(master)
    self.win.configure(background="#e0e0e0",font="{Arial} 12 {bold}",
                       height=ancho,labelanchor="n",width=alto)
    self.tabs = ttk.Notebook(self.win)
    self.tabs.configure(height=800, width=799)

    #Frame de datos
    self.frm1 = ttk.Frame(self.tabs)
    self.frm1.configure(height=200, width=200)

    #Etiqueta IdNit del Proveedor
    self.lblIdNit = ttk.Label(self.frm1)
    self.lblIdNit.configure(text='Id/Nit', width=6)
    self.lblIdNit.place(anchor="nw", x=10, y=40)

    #Captura IdNit del Proveedor
    self.idNit = ttk.Entry(self.frm1)
    self.idNit.configure(takefocus=True)#, state = 'readonly')
    self.idNit.place(anchor="nw", x=50, y=40)
    self.idNit.bind("<KeyRelease>", self.validaIdNit)
    self.idNit.bind("<BackSpace>", lambda _:self.idNit.delete(len(self.idNit.get())),'end')
    self.idNit.focus_set()

    #Etiqueta razón social del Proveedor
    self.lblRazonSocial = ttk.Label(self.frm1)
    self.lblRazonSocial.configure(text='Razon social', width=12)
    self.lblRazonSocial.place(anchor="nw", x=210, y=40)

    #Captura razón social del Proveedor
    self.razonSocial = ttk.Entry(self.frm1)
    self.razonSocial.configure(width=36)
    self.razonSocial.place(anchor="nw", x=290, y=40)
    self.razonSocial.bind("<KeyRelease>", self.validaRazonSocial)
    self.razonSocial.bind("<BackSpace>", lambda _:self.razonSocial.delete(len(self.razonSocial.get())),'end')

    #Etiqueta ciudad del Proveedor
    self.lblCiudad = ttk.Label(self.frm1)
    self.lblCiudad.configure(text='Ciudad', width=7)
    self.lblCiudad.place(anchor="nw", x=540, y=40)

    #Captura ciudad del Proveedor
    self.ciudad = ttk.Entry(self.frm1)
    self.ciudad.configure(width=30)
    self.ciudad.place(anchor="nw", x=590, y=40)
    self.ciudad.bind("<KeyRelease>", self.validaCiudad)
    self.ciudad.bind("<BackSpace>", lambda _:self.ciudad.delete(len(self.ciudad.get())),'end')

    #Separador
    self.separador1 = ttk.Separator(self.frm1)
    self.separador1.configure(orient="horizontal")
    self.separador1.place(anchor="nw", width=800, x=0, y=79)

    #Etiqueta Código del Producto
    self.lblCodigo = ttk.Label(self.frm1)
    self.lblCodigo.configure(text='Código', width=7)
    self.lblCodigo.place(anchor="nw", x=10, y=120)

    #Captura el código del Producto
    self.codigo = ttk.Entry(self.frm1)
    self.codigo.configure(width=13)# state = 'readonly')
    self.codigo.place(anchor="nw", x=60, y=120)
    self.codigo.bind("<KeyRelease>", self.validaCodigo)
    self.codigo.bind("<BackSpace>", lambda _:self.codigo.delete(len(self.codigo.get())),'end')

    #Etiqueta descripción del Producto
    self.lblDescripcion = ttk.Label(self.frm1)
    self.lblDescripcion.configure(text='Descripción', width=11)
    self.lblDescripcion.place(anchor="nw", x=220, y=120)

    #Captura la descripción del Producto
    self.descripcion = ttk.Entry(self.frm1)
    self.descripcion.configure(width=36)
    self.descripcion.place(anchor="nw", x=290, y=120)
    self.descripcion.bind("<KeyRelease>", self.validaDescripcion)
    self.descripcion.bind("<BackSpace>", lambda _:self.descripcion.delete(len(self.descripcion.get())),'end')

    #Etiqueta unidad o medida del Producto
    self.lblUnd = ttk.Label(self.frm1)
    self.lblUnd.configure(text='Unidad', width=7)
    self.lblUnd.place(anchor="nw", x=540, y=120)

    #Captura la unidad o medida del Producto
    self.unidad = ttk.Entry(self.frm1)
    self.unidad.configure(width=10)
    self.unidad.place(anchor="nw", x=590, y=120)
    self.unidad.bind("<KeyRelease>", self.validaUnidad)
    self.unidad.bind("<BackSpace>", lambda _:self.unidad.delete(len(self.unidad.get())),'end')

    #Etiqueta cantidad del Producto
    self.lblCantidad = ttk.Label(self.frm1)
    self.lblCantidad.configure(text='Cantidad', width=8)
    self.lblCantidad.place(anchor="nw", x=10, y=170)

    #Captura la cantidad del Producto
    self.cantidad = ttk.Entry(self.frm1)
    self.cantidad.configure(width=12)
    self.cantidad.place(anchor="nw", x=70, y=170)
    self.cantidad.bind("<KeyRelease>", self.validaCantidad)
    self.cantidad.bind("<BackSpace>", lambda _:self.cantidad.delete(len(self.cantidad.get())),'end')

    #Etiqueta precio del Producto
    self.lblPrecio = ttk.Label(self.frm1)
    self.lblPrecio.configure(text='Precio $', width=8)
    self.lblPrecio.place(anchor="nw", x=170, y=170)

    #Captura el precio del Producto
    self.precio = ttk.Entry(self.frm1)
    self.precio.configure(width=15)
    self.precio.place(anchor="nw", x=220, y=170)
    self.precio.bind("<KeyRelease>", self.validaPrecio)
    self.precio.bind("<BackSpace>", lambda _:self.precio.delete(len(self.precio.get())),'end')

    #Etiqueta fecha de compra del Producto
    self.lblFecha = ttk.Label(self.frm1)
    self.lblFecha.configure(text='Fecha', width=6)
    self.lblFecha.place(anchor="nw", x=350, y=170)

    #Captura la fecha de compra del Producto
    self.fecha = ttk.Entry(self.frm1)
    self.fecha.configure(width=10)
    self.fecha.place(anchor="nw", x=390, y=170)
    self.fecha.bind("<FocusOut>", self.validaFecha)
    self.fecha.bind("<BackSpace>", lambda _:self.fecha.delete(len(self.fecha.get())),'end')    

    #Separador
    self.separador2 = ttk.Separator(self.frm1)
    self.separador2.configure(orient="horizontal")
    self.separador2.place(anchor="nw", width=800, x=0, y=220)


    #tablaTreeView
    self.style=ttk.Style()
    self.style.configure("estilo.Treeview", highlightthickness=0, bd=0, background="#e0e0e0", font=('Calibri Light',10))
    self.style.configure("estilo.Treeview.Heading", background='Azure', font=('Calibri Light', 10,'bold')) 
    self.style.layout("estilo.Treeview", [('estilo.Treeview.treearea', {'sticky': 'nswe'})])
    
    #Árbol para mosrtar los datos de la B.D.
    self.treeProductos = ttk.Treeview(self.frm1, style="estilo.Treeview")
    
    self.treeProductos.configure(selectmode="extended")

    # Etiquetas de las columnas para el TreeView
    self.treeProductos["columns"]=("Codigo","Descripcion","Und","Cantidad","Precio","Fecha")
    # Características de las columnas del árbol
    self.treeProductos.column ("#0",          anchor="w",stretch=True,width=3)
    self.treeProductos.column ("Codigo",      anchor="w",stretch=True,width=3)
    self.treeProductos.column ("Descripcion", anchor="w",stretch=True,width=150)
    self.treeProductos.column ("Und",         anchor="w",stretch=True,width=3)
    self.treeProductos.column ("Cantidad",    anchor="w",stretch=True,width=3)
    self.treeProductos.column ("Precio",      anchor="w",stretch=True,width=8)
    self.treeProductos.column ("Fecha",       anchor="w",stretch=True,width=3)

    # Etiquetas de columnas con los nombres que se mostrarán por cada columna
    self.treeProductos.heading("#0",          anchor="center", text='ID / Nit')
    self.treeProductos.heading("Codigo",      anchor="center", text='Código')
    self.treeProductos.heading("Descripcion", anchor="center", text='Descripción')
    self.treeProductos.heading("Und",         anchor="center", text='Unidad')
    self.treeProductos.heading("Cantidad",    anchor="center", text='Cantidad')
    self.treeProductos.heading("Precio",      anchor="center", text='Precio')
    self.treeProductos.heading("Fecha",       anchor="center", text='Fecha')

    #Carga los datos en treeProductos
    #self.lee_treeProductos() 
    self.treeProductos.place(anchor="nw", height=560, width=790, x=2, y=230)

    #Scrollbar en el eje Y de treeProductos
    self.scrollbary=ttk.Scrollbar(self.treeProductos, orient='vertical', command=self.treeProductos.yview)
    self.treeProductos.configure(yscroll=self.scrollbary.set)
    self.scrollbary.place(x=778, y=25, height=478)

    # Título de la pestaña Ingreso de Datos
    self.frm1.pack(side="top")
    self.tabs.add(self.frm1, compound="center", text='Ingreso de datos')
    self.tabs.pack(side="top")

    #Frame 2 para contener los botones
    self.frm2 = ttk.Frame(self.win)
    self.frm2.configure(height=100, width=800)

    #Botón para Buscar un Proveedor
    self.btnBuscar = ttk.Button(self.frm2)
    self.btnBuscar.configure(text='Buscar',command= self.button_buscar)
    self.btnBuscar.place(anchor="nw", width=70, x=200, y=10)

    #Botón para Guardar los datos
    self.btnGrabar = ttk.Button(self.frm2)
    self.btnGrabar.configure(text='Grabar')
    self.btnGrabar.place(anchor="nw", width=70, x=275, y=10)

    #Botón para Editar los datos
    self.btnEditar = ttk.Button(self.frm2)
    self.btnEditar.configure(text='Editar')
    self.btnEditar.place(anchor="nw", width=70, x=350, y=10)

    #Botón para Elimnar datos
    self.btnEliminar = ttk.Button(self.frm2)
    self.btnEliminar.configure(text='Eliminar')
    self.btnEliminar.place(anchor="nw", width=70, x=425, y=10)

    #Botón para cancelar una operación
    self.btnCancelar = ttk.Button(self.frm2)
    self.btnCancelar.configure(text='Cancelar', width=80, command = self.limpiaCampos)
    self.btnCancelar.place(anchor="nw", width=70, x=500, y=10)

    #Ubicación del Frame 2
    self.frm2.place(anchor="nw", height=60, relwidth=1, y=755)
    self.win.pack(anchor="center", side="top")

    # widget Principal del sistema
    self.mainwindow = self.win

  #Fución de manejo de eventos del sistema
  def run(self):
      self.mainwindow.mainloop()

  ''' ......... Métodos utilitarios del sistema .............'''
  #Rutina de centrado de pantalla
  def centra(self,win,ancho,alto): 
      """ centra las ventanas en la pantalla """ 
      x = win.winfo_screenwidth() // 2 - ancho // 2 
      y = win.winfo_screenheight() // 2 - alto // 2 
      win.geometry(f'{ancho}x{alto}+{x}+{y}') 
      win.deiconify() # Se usa para restaurar la ventana

 # Validaciones del sistema
  def validaIdNit(self, event):
    ''' Valida que la longitud no sea mayor a 15 caracteres'''
    if event.char:
      if ' ' in self.idNit.get():
            mssg.showerror("Error", "No se permiten espacios.")
            
            # Eliminar el espacio ingresado
            contenido_sin_espacio = self.idNit.get().replace(' ', '')
            # Establecer el contenido sin espacios en el Entry
            self.idNit.delete(0, tk.END)
            self.idNit.insert(0, contenido_sin_espacio)

      if len(self.idNit.get()) >= 15:
         self.idNit.delete(15,'end')
         mssg.showerror('Atención!!','.. ¡Máximo 15 caracteres! ..')
         
    else:
        self.idNit.delete(14)
    
  def validaRazonSocial(self, event):
     ''' Valida que la longitud no sea mayor a 25 caracteres'''
     if event.char:
        if len(self.razonSocial.get()) >= 25:
           self.razonSocial.delete(25,'end')
           mssg.showerror('Atención!!','.. ¡Máximo 25 caracteres! ..')
     else:
        self.razonSocial.delete(24)

  def validaCiudad(self, event):
     ''' Valida que la longitud no sea mayor a 15 caracteres'''
     if event.char:
        if len(self.ciudad.get()) >= 15:
           self.ciudad.delete(15,'end')
           mssg.showerror('Atención!!','.. ¡Máximo 15 caracteres! ..')
     else:
        self.ciudad.delete(14) 

  def validaCodigo(self, event):
     ''' Valida que la longitud no sea mayor a 15 caracteres'''
     if event.char:
        if ' ' in self.codigo.get():
            mssg.showerror("Error", "No se permiten espacios.")
            
            # Eliminar el espacio ingresado
            contenido_sin_espacio = self.codigo.get().replace(' ', '')
            # Establecer el contenido sin espacios en el Entry
            self.codigo.delete(0, tk.END)
            self.codigo.insert(0, contenido_sin_espacio)

        if len(self.codigo.get()) >= 15:
           self.codigo.delete(15,'end')
           mssg.showerror('Atención!!','.. ¡Máximo 15 caracteres! ..')
     else:
        self.codigo.delete(14)

  def validaDescripcion(self, event):
     ''' Valida que la longitud no sea mayor a 50 caracteres'''
     if event.char:
        if len(self.descripcion.get()) >= 50:
           self.descripcion.delete(50,'end')
           mssg.showerror('Atención!!','.. ¡Máximo 50 caracteres! ..')
     else:
        self.descripcion.delete(49) 
     
  def validaUnidad(self, event):
     ''' Valida que la longitud no sea mayor a 10 caracteres'''
     if event.char:
        if len(self.unidad.get()) >= 10:
           self.unidad.delete(10,'end')
           mssg.showerror('Atención!!','.. ¡Máximo 10 caracteres! ..')
     else:
        self.unidad.delete(9)  

  def validaCantidad(self, event):
     ''' Valida que la longitud no sea mayor a 6 caracteres y sea int'''
     if event.char:
        if len(self.cantidad.get()) >= 6:
            self.cantidad.delete(6,'end')
            mssg.showerror('Atención!!','.. ¡Máximo 6 caracteres! ..')
            
        else:
            self.cantidad.delete(5)
            
            if self.cantidad.get().isdecimal() == False:
                mssg.showerror('Atención!!','.. ¡Solo números! ..')
                self.cantidad.delete(0, 'end')
  
  def validaPrecio(self, event):
    ''' Valida que la longitud no sea mayor a 9 caracteres y sea int'''
    if event.char:
        if len(self.precio.get()) >= 9:
            self.precio.delete(9,'end')
            mssg.showerror('Atención!!','.. ¡Máximo 9 caracteres! ..')
            
        else:
            self.precio.delete(8)

    # Intentar convertir el contenido en un número
    try:
        float_numero = float(self.precio.get())
        pass
    except ValueError:
        mssg.showerror('Atención!!','.. ¡Precio inválido! ..')
        self.precio.delete(0, 'end')  # Limpiar el contenido del Entry en caso de error              
            
  def validaFecha(self, event):  
     ''' Valida que la fecha sea válida'''
     if event.char:
           ''' Valida que la longitud no sea mayor a 10 caracteres y sea int'''
     if event.char:
        #if re.match(r"^\d{2}/\d{2}/\d{4}$", self.fecha.get()):
      
         if es_fecha_valida(self.fecha.get()) == False:
            mssg.showerror('Atención!!','.. ¡Fecha Inválida! ..')
            self.fecha.delete(0, 'end')
        




        



  #Rutina de limpieza de datos
  def limpiaCampos(self):
      ''' Limpia todos los campos de captura'''
      Inventario.actualiza = None
      self.idNit.config(state = 'normal')
      self.idNit.delete(0,'end')
      self.razonSocial.delete(0,'end')
      self.ciudad.delete(0,'end')
      self.idNit.delete(0,'end')
      self.codigo.delete(0,'end')
      self.descripcion.delete(0,'end')
      self.unidad.delete(0,'end')
      self.cantidad.delete(0,'end')
      self.precio.delete(0,'end')
      self.fecha.delete(0,'end')
 
  #Rutina para cargar los datos en el árbol  
  def carga_Datos(self):
    self.idNit.insert(0,self.treeProductos.item(self.treeProductos.selection())['text'])
    self.idNit.configure(state = 'readonly')
    self.codigo.insert(0,self.treeProductos.item(self.treeProductos.selection())['values'][1])
    self.descripcion.insert(0,self.treeProductos.item(self.treeProductos.selection())['values'][2])
    self.unidad.insert(0,self.treeProductos.item(self.treeProductos.selection())['values'][3])
    self.cantidad.insert(0,self.treeProductos.item(self.treeProductos.selection())['values'][4])
    self.precio.insert(0,self.treeProductos.item(self.treeProductos.selection())['values'][5])
    self.fecha.insert(0,self.treeProductos.item(self.treeProductos.selection())['values'][6])
    

  # Operaciones con la base de datos
  def run_Query(self, query, parametros = ()):
    ''' Función para ejecutar los Querys a la base de datos '''
    with sqlite3.connect(self.db_name) as conn:
        cursor = conn.cursor()
        result = cursor.execute(query, parametros)
        conn.commit()
    return result

  def lee_treeProductos(self):
    ''' Carga los datos y Limpia la Tabla tablaTreeView '''
    tabla_TreeView = self.treeProductos.get_children()
    for linea in tabla_TreeView:
        self.treeProductos.delete(linea) # Limpia la filas del TreeView
    
    # Seleccionando los datos de la BD
    query = '''SELECT * from Proveedor INNER JOIN Inventario WHERE idNitProv = idNit ORDER BY idNitProv'''
    db_rows = self.run_Query(query).fetchall # db_rows contine la vista del query
    

    # Insertando los datos de la BD en treeProductos de la pantalla
    for row in db_rows:
      self.treeProductos.insert(0, text = row[0], values = [row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8]])

    ''' Al final del for row queda con la última tupla
        y se usan para cargar las variables de captura
    '''
    self.idNit.insert(0,row[0])
    self.razonSocial.insert(0,row[1])
    self.ciudad.insert(0,row[2])
<<<<<<< HEAD
    self.codigo.insert(0,row[4])
    self.descripcion.insert(0,row[5])
    self.unidad.insert(0,row[6])
    self.cantidad.insert(0,row[7])
    self.precio.insert(0,row[8])
    self.fecha.insert(0,row[9])  
    
  def limpiar_treeview(self):
    tabla_TreeView = self.treeProductos.get_children()
    for linea in tabla_TreeView:
        self.treeProductos.delete(linea)
  def cargar_datos_treeview(self,db_rows):
      for row in db_rows:
         self.treeProductos.insert('',0, text = row[0], values = [row[1],row[2],row[3],row[4],row[5],row[6]])
  def cargar_datos_buscados(self,search):
      self.limpiar_treeview()
      self.cargar_datos_treeview(search)
      
=======
    self.codigo.insert(0,row[3])
    self.descripcion.insert(0,row[4])
    self.unidad.insert(0,row[5])
    self.cantidad.insert(0,row[6])
    self.precio.insert(0,row[7])
    self.fecha.insert(0,row[8])  
>>>>>>> 58e67181cca3adfb73ada828b7e7da011c02d0fb
          
  def adiciona_Registro(self, event=None):
    '''Adiciona un producto a la BD si la validación es True'''
    # Obtener los valores de los campos de entrada
    id_nit = self.idNit.get()
    razon_social = self.razonSocial.get()
    ciudad = self.ciudad.get()
    codigo = self.codigo.get()
    descripcion = self.descripcion.get()
    unidad = self.unidad.get()
    cantidad = self.cantidad.get()
    precio = self.precio.get()
    fecha = self.fecha.get()
    pass
   
  def editaTreeProveedores(self, event=None):
    ''' Edita una tupla del TreeView'''
    pass
      
  def eliminaRegistro(self, event=None):
    '''Elimina un Registro en la BD'''
    pass
  def accion_Buscar(self,seleccion,tabla,condicion):
    search=f'''SELECT {seleccion} FROM {tabla} WHERE {condicion}'''
    resultado=self.run_Query(search)
    return resultado
  def validar_ID(self):
    id=self.idNit.get()
    search_id=self.accion_Buscar('*','Proveedor',f'idNitProv={id}').fetchone()
    if search_id==None :
      prov_Exist=False
    else:
       prov_Exist=True
    return prov_Exist
  def validar_Codigo(self):
     codigo=self.codigo.get()
     search_id=self.accion_Buscar('*','Producto',f'Codigo={codigo}').fetchone()
     if search_id==None :
        cod_Exist=False
     else:
        cod_Exist=True
     return cod_Exist
  
  def cargar_proveedor(self, id):
     proveedor=self.accion_Buscar("*","Proveedor",f"idNitProv={id}").fetchone()
     self.idNit.insert(0,proveedor[0])
     self.razonSocial.insert(0,proveedor[1])
     self.ciudad.insert(0, proveedor[2])
  
  def cargar_producto(self,producto):
     self.codigo.insert(0,producto[1])
     self.descripcion.insert(0,producto[2])
     self.unidad.insert(0,producto[3])
     self.cantidad.insert(0,producto[4])
     self.precio.insert(0,producto[5])
     self.fecha.insert(0,producto[6])

     
  def button_buscar(self):
     if self.idNit.get()!= "" and self.codigo.get()=="":
        if self.validar_ID()==True:
          search=self.accion_Buscar("*","Producto", f"IdNit={self.idNit.get() } ").fetchall()
          self.cargar_datos_buscados(search)
          self.limpiaCampos()
          self.cargar_proveedor(search[0][0])
        else:
           mssg.showerror('Atención!!','.. ¡El proveedor no existe! ..')
     elif self.idNit.get()== "" and self.codigo.get()!="":
        if self.validar_Codigo()==True:
           search=self.accion_Buscar("*","Producto", f"Codigo={self.codigo.get() } ").fetchall()
           self.cargar_datos_buscados(search)
           self.limpiaCampos()
           self.cargar_proveedor(search[0][0])
           self.cargar_producto(search[0])
        else:
           mssg.showerror('Atención!!','.. ¡El producto no existe! ..')
     elif self.idNit.get()!= "" and self.codigo.get()!="":
        if self.validar_ID()==True and self.validar_Codigo()==True:
           search=self.accion_Buscar("*","Producto", f"Codigo={self.codigo.get() } AND IdNit= {self.idNit.get()} ").fetchall()
           if search == None:
              mssg.showerror('Atención!!','.. ¡El producto no corresponde al proveedor indicado! ..')
           else: 
              self.cargar_datos_buscados(search)
              self.limpiaCampos()
              self.cargar_proveedor(search[0][0])
              self.cargar_producto(search[0])
        elif self.validar_ID()==True and self.validar_Codigo()==False:
           mssg.showerror('Atención!!','.. ¡El producto no existe! ..')
        elif self.validar_ID()==False and self.validar_Codigo()==True:
           mssg.showerror('Atención!!','.. ¡El proveedor no existe! ..')
        elif self.validar_ID()==False and self.validar_Codigo()==False:
           mssg.showerror('Atención!!','.. ¡Ni el producto, ni el proveedor existen! ..')
           


if __name__ == "__main__":
    app = Inventario()
    app.run()
