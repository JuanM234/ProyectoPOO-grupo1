#!/usr/bin/python3
# -*- coding: utf-8 -*-
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox as mssg
import sqlite3
from os import path

#import re

#validar si la fecha es válida
def es_Fecha_Valida(fecha_texto):
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


class Inventario:
  def __init__(self, master=None):
    self.path = str(path.dirname(__file__))
    self.db_name = self.path + r'/Inventario.db'
    self.ico=self.path + r'/f2.ico'
    ancho=830;alto=690 # Dimensione de la pantalla
    self.actualiza = None

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
    self.tabs.configure(height=650, width=799)

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
    self.idNit.bind("<KeyRelease>", self.valida_Id_Nit)
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
    self.razonSocial.bind("<KeyRelease>", self.valida_Razon_Social)
    self.razonSocial.bind("<BackSpace>", lambda _:self.razonSocial.delete(len(self.razonSocial.get())),'end')

    #Etiqueta ciudad del Proveedor
    self.lblCiudad = ttk.Label(self.frm1)
    self.lblCiudad.configure(text='Ciudad', width=7)
    self.lblCiudad.place(anchor="nw", x=540, y=40)

    #Captura ciudad del Proveedor
    self.ciudad = ttk.Entry(self.frm1)
    self.ciudad.configure(width=30)
    self.ciudad.place(anchor="nw", x=590, y=40)
    self.ciudad.bind("<KeyRelease>", self.valida_Ciudad)
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
    self.codigo.bind("<KeyRelease>", self.valida_Codigo)
    self.codigo.bind("<BackSpace>", lambda _:self.codigo.delete(len(self.codigo.get())),'end')

    #Etiqueta descripción del Producto
    self.lblDescripcion = ttk.Label(self.frm1)
    self.lblDescripcion.configure(text='Descripción', width=11)
    self.lblDescripcion.place(anchor="nw", x=220, y=120)

    #Captura la descripción del Producto
    self.descripcion = ttk.Entry(self.frm1)
    self.descripcion.configure(width=36)
    self.descripcion.place(anchor="nw", x=290, y=120)
    self.descripcion.bind("<KeyRelease>", self.valida_Descripcion)
    self.descripcion.bind("<BackSpace>", lambda _:self.descripcion.delete(len(self.descripcion.get())),'end')

    #Etiqueta unidad o medida del Producto
    self.lblUnd = ttk.Label(self.frm1)
    self.lblUnd.configure(text='Unidad', width=7)
    self.lblUnd.place(anchor="nw", x=540, y=120)

    #Captura la unidad o medida del Producto
    self.unidad = ttk.Entry(self.frm1)
    self.unidad.configure(width=10)
    self.unidad.place(anchor="nw", x=590, y=120)
    self.unidad.bind("<KeyRelease>", self.valida_Unidad)
    self.unidad.bind("<BackSpace>", lambda _:self.unidad.delete(len(self.unidad.get())),'end')

    #Etiqueta cantidad del Producto
    self.lblCantidad = ttk.Label(self.frm1)
    self.lblCantidad.configure(text='Cantidad', width=8)
    self.lblCantidad.place(anchor="nw", x=10, y=170)

    #Captura la cantidad del Producto
    self.cantidad = ttk.Entry(self.frm1)
    self.cantidad.configure(width=12)
    self.cantidad.place(anchor="nw", x=70, y=170)
    self.cantidad.bind("<KeyRelease>", self.valida_Cantidad)
    self.cantidad.bind("<BackSpace>", lambda _:self.cantidad.delete(len(self.cantidad.get())),'end')

    #Etiqueta precio del Producto
    self.lblPrecio = ttk.Label(self.frm1)
    self.lblPrecio.configure(text='Precio $', width=8)
    self.lblPrecio.place(anchor="nw", x=170, y=170)

    #Captura el precio del Producto
    self.precio = ttk.Entry(self.frm1)
    self.precio.configure(width=15)
    self.precio.place(anchor="nw", x=220, y=170)
    self.precio.bind("<KeyRelease>", self.valida_Precio)
    self.precio.bind("<BackSpace>", lambda _:self.precio.delete(len(self.precio.get())),'end')

    #Etiqueta fecha de compra del Producto
    self.lblFecha = ttk.Label(self.frm1)
    self.lblFecha.configure(text='Fecha', width=6)
    self.lblFecha.place(anchor="nw", x=350, y=170)

    #Captura la fecha de compra del Producto
    self.fecha = ttk.Entry(self.frm1)
    self.fecha.configure(width=10)
    self.fecha.place(anchor="nw", x=390, y=170)
    self.fecha.bind("<FocusOut>", self.valida_Fecha)
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
    self.treeProductos.bind('<Double-Button-1>',lambda _: self.carga_Datos())

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
    self.treeProductos.place(anchor="nw", height=400, width=790, x=2, y=230)

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
    self.frm2.configure(height=50, width=800)

    #Botón para Buscar un Proveedor
    self.btnBuscar = ttk.Button(self.frm2)
    self.btnBuscar.configure(text='Busca',command= self.search_Button)
    self.btnBuscar.place(anchor="nw", width=70, x=200, y=20)

    #Botón para Guardar los datos
    self.btnGrabar = ttk.Button(self.frm2)
    self.btnGrabar.configure(text='Grabar', command= self.record_Button)
    self.btnGrabar.place(anchor="nw", width=70, x=275, y=20)

    #Botón para Editar los datos
    self.btnEditar = ttk.Button(self.frm2)
    self.btnEditar.configure(text='Editar', command=self.edit_Button)
    self.btnEditar.place(anchor="nw", width=70, x=350, y=20)

    #Botón para Elimnar datos
    self.btnEliminar = ttk.Button(self.frm2)
    self.btnEliminar.configure(text='Eliminar', command= self.eliminar_Button)
    self.btnEliminar.place(anchor="nw", width=70, x=425, y=20)

    #Botón para cancelar una operación
    self.btnCancelar = ttk.Button(self.frm2)
    self.btnCancelar.configure(text='Cancelar', width=80, command = self.cancel_Button)
    self.btnCancelar.place(anchor="nw", width=70, x=500, y=20)

    #Ubicación del Frame 2
    self.frm2.place(anchor="nw", height=60, relwidth=1, y=605)
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
      
  def estado_Buttons(self, estado):
     if estado==True:
        self.btnBuscar.configure(state='normal')
        self.btnEditar.configure(state='normal')
        self.btnEliminar.configure(state='normal')
     elif estado==False:
        self.btnBuscar.configure(state='disabled')
        self.btnEditar.configure(state='disabled')
        self.btnEliminar.configure(state='disabled')
      
  def abrir_Ventana_Eliminar(self):
     # Crear una ventana secundaria usando toplevel
     self.ventana_eliminar = tk.Toplevel(self.win)
     self.ventana_eliminar.configure(
            background="#afafaf",
            padx=10,
            pady=30)
     self.ventana_eliminar.geometry("350x350")
     self.ventana_eliminar.iconbitmap(self.ico)
     self.ventana_eliminar.resizable(False, False)
     self.ventana_eliminar.title("Eliminar")

     self.frame_eliminar_1 = ttk.Frame(self.ventana_eliminar)
     self.frame_eliminar_1.place(
            anchor="center",
            height=200,
            width=250,
            x=165,
            y=100)

     self.obj_eliminar = tk.StringVar()

     self.radiobutton1 = ttk.Radiobutton(self.frame_eliminar_1)
     self.radiobutton1.configure(
            text='Eliminar eL Producto \nseleccionado',
            value="Producto",
            variable=self.obj_eliminar)
     self.radiobutton1.place(anchor="w", height=50, x=10, y=50)
     
     self.radiobutton2 = ttk.Radiobutton(self.frame_eliminar_1)
     self.radiobutton2.configure(
            text='Eliminar Proveedor y todos sus \nproductos',
            value="Proveedor",
            variable=self.obj_eliminar)
     self.radiobutton2.place(anchor="w", x=10, y=95)

     self.radiobutton3 = ttk.Radiobutton(self.frame_eliminar_1)
     self.radiobutton3.configure(
            text='Eliminar todos los productos \ncon el codigo seleccionado',
            value="Todos los productos",
            variable=self.obj_eliminar)
     self.radiobutton3.place(anchor="w", x=10, y=145)
    
     self.btn_cancelar= ttk.Button(self.ventana_eliminar)
     self.btn_cancelar.configure(text='Cancelar', command= self.ventana_eliminar.destroy)
     self.btn_cancelar.pack(side="bottom")

     self.btn_continuar = ttk.Button(self.ventana_eliminar)
     self.btn_continuar.configure(text='Continuar', command= self.continuar_Button)
     self.btn_continuar.pack(side="bottom")

     # Centrar la ventana emergente en la pantalla
     self.centra(self.ventana_eliminar, 350, 350)

  def continuar_Button(self):
     item=self.treeProductos.item(self.treeProductos.selection())
     text_warning=''
     if self.obj_eliminar.get()=='Producto':
        text_warning= f'Eliminar el registro del producto {item["values"][0]}, \ncorrespondiente al proveedor {item["text"]} '
     elif self.obj_eliminar.get()=='Proveedor':
        text_warning=f'Eliminar el proveedor {item["text"]} y todos \nlos registros relacionados a él '
     elif self.obj_eliminar.get()== 'Todos los productos':
        text_warning=f'Eliminar todos los registros relacionados \nal producto {item["values"][0]} '

     self.warning= self.path + r'\warning.png'

     self.ventana_confirmacion = tk.Toplevel(self.ventana_eliminar)
     self.ventana_confirmacion.configure(
            background="#ffffff",
            height=200,
            padx=10,
            pady=10,
            width=500)
     self.ventana_confirmacion.iconbitmap(self.ico)
     self.ventana_confirmacion.resizable(False, False)
     self.ventana_confirmacion.title("Warning")

     self.img_warning = tk.PhotoImage(file=self.warning)

     self.lebel1_warning = ttk.Label(self.ventana_confirmacion)
     self.lebel1_warning.configure(image=self.img_warning)
     self.lebel1_warning.place(anchor="w", x=20, y=90)

     self.label2_warning = ttk.Label(self.ventana_confirmacion)
     self.label2_warning.configure(
            background="#ffffff",
            font="{Arial} 12 {bold}",
            text=f'Esta seguro que quiere realizar \nla siquiente acción: \n\n{text_warning}')
     self.label2_warning.place(anchor="w", x=130, y=60)

     self.btn_yes = ttk.Button(self.ventana_confirmacion)
     self.btn_yes.configure(text='Si')
     self.btn_yes.place(anchor="w", width=70, x=243, y=150)
     self.btn_yes.bind('<Button-1>', lambda _: (self.elimina_Registro(item),self.ventana_eliminar.destroy()))

     self.btn_no = ttk.Button(self.ventana_confirmacion)
     self.btn_no.configure(text='No', command= self.ventana_eliminar.destroy)
     self.btn_no.place(anchor="w", x=317, y=150)
     self.centra(self.ventana_confirmacion,500,200)
     
 # Validaciones del sistema
  def valida_Id_Nit(self, event):
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
    
  def valida_Razon_Social(self, event):
     ''' Valida que la longitud no sea mayor a 25 caracteres'''
     if event.char:
        if len(self.razonSocial.get()) >= 25:
           self.razonSocial.delete(25,'end')
           mssg.showerror('Atención!!','.. ¡Máximo 25 caracteres! ..')
     else:
        self.razonSocial.delete(24)

  def valida_Ciudad(self, event):
     ''' Valida que la longitud no sea mayor a 15 caracteres'''
     if event.char:
        if len(self.ciudad.get()) >= 15:
           self.ciudad.delete(15,'end')
           mssg.showerror('Atención!!','.. ¡Máximo 15 caracteres! ..')
     else:
        self.ciudad.delete(14) 

  def valida_Codigo(self, event):
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

  def valida_Descripcion(self, event):
     ''' Valida que la longitud no sea mayor a 50 caracteres'''
     if event.char:
        if len(self.descripcion.get()) >= 50:
           self.descripcion.delete(50,'end')
           mssg.showerror('Atención!!','.. ¡Máximo 50 caracteres! ..')
     else:
        self.descripcion.delete(49) 
     
  def valida_Unidad(self, event):
     ''' Valida que la longitud no sea mayor a 10 caracteres'''
     if event.char:
        if len(self.unidad.get()) >= 10:
           self.unidad.delete(10,'end')
           mssg.showerror('Atención!!','.. ¡Máximo 10 caracteres! ..')
     else:
        self.unidad.delete(9)  

  def valida_Cantidad(self, event):
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
  
  def valida_Precio(self, event):
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
            
  def valida_Fecha(self, event):  
     ''' Valida que la fecha sea válida'''
     if event.char:
           ''' Valida que la longitud no sea mayor a 10 caracteres y sea int'''
     if event.char:
        #if re.match(r"^\d{2}/\d{2}/\d{4}$", self.fecha.get()):
      
         if es_Fecha_Valida(self.fecha.get()) == False:
            mssg.showerror('Atención!!','.. ¡Fecha Inválida! ..')
            self.fecha.delete(0, 'end')
   
  def validar_ID(self):
     id=self.idNit.get()
     search_id=self.accion_Buscar('*','Proveedor','idNitProv= ? ', (id,)).fetchone()
     if search_id==None :
        prov_Exist=False
     else:
        prov_Exist=True
     return prov_Exist
  
  def validar_Cod(self):
     codigo=self.codigo.get()
     search_id=self.accion_Buscar('*','Producto','Codigo= ? ', (codigo,)).fetchone()
     if search_id==None :
        cod_Exist=False
     else:
        cod_Exist=True
     return cod_Exist
        
  #Rutina de limpieza de datos
  def limpia_Campos(self):
      ''' Limpia todos los campos de captura'''
      self.idNit.configure(state = 'normal')
      self.idNit.delete(0,'end')
      self.razonSocial.delete(0,'end')
      self.ciudad.delete(0,'end')
      self.idNit.delete(0,'end')
      self.codigo.configure(state = 'normal')
      self.codigo.delete(0,'end')
      self.descripcion.delete(0,'end')
      self.unidad.delete(0,'end')
      self.cantidad.delete(0,'end')
      self.precio.delete(0,'end')
      self.fecha.delete(0,'end')
      
 
  #Rutina para cargar los datos en el árbol  
  def carga_Datos(self):
    seleccion=self.treeProductos.selection()
    if seleccion != ():
       self.estado_Buttons(False)
       self.limpia_Campos()
       item=self.treeProductos.item(seleccion)
       self.cargar_Proveedor(item ['text'])
       self.idNit.configure(state = 'readonly')
       self.codigo.insert(0,item['values'][0])
       self.codigo.configure(state='readonly')
       self.descripcion.insert(0,item['values'][1])
       self.unidad.insert(0,item['values'][2])
       self.cantidad.insert(0,item['values'][3])
       self.precio.insert(0,item['values'][4])
       self.fecha.insert(0,item['values'][5])
       self.actualiza=True
       dato_cargado=[[item['text'],item['values'][0],item['values'][1],item['values'][2],item['values'][3],item['values'][4],item['values'][5]]]
       self.cargar_Datos_Buscados(dato_cargado)
       mssg.showinfo('Confirmación',
                     '''.. Se ha activado el modo Editar, puede modificar la información del producto y provvedor seleccionado ..''')
    elif seleccion== ():
       mssg.showerror('Atención!!','.. ¡No se ha seleccionado nada! ..')

  def actualizar_datos(self):
     id_nit = self.idNit.get()
     razon_social = self.razonSocial.get()
     ciudad = self.ciudad.get()
     codigo = self.codigo.get()
     descripcion = self.descripcion.get()
     unidad = self.unidad.get()
     cantidad = float(self.cantidad.get())
     precio = float(self.precio.get())
     fecha = self.fecha.get()
     proveedor=self.accion_Buscar('*', 'Proveedor', ' idNitProv = ? ', (id_nit,)).fetchone()
     producto=self.accion_Buscar('*', 'Producto', ' IdNit = ? AND Codigo = ? ', (id_nit, codigo,)).fetchone()
     proveedor_update=(id_nit,razon_social,ciudad)
     producto_update=(id_nit,codigo,descripcion,unidad,cantidad,precio,fecha)
     if proveedor == proveedor_update:
        if producto==producto_update:
           mssg.showinfo('.. Confirmación ..', '.. No se realizo ningun cambio, saliendo del modo Editar ..')
        elif producto!=producto_update:
           self.actualizar_Producto((descripcion,unidad,cantidad,precio,fecha,id_nit,codigo,))
           self.cargar_Datos_Buscados([[id_nit,codigo,descripcion,unidad,cantidad,precio,fecha]])
           mssg.showinfo('.. Confirmación ..', '.. Producto actualizado ..')
     elif proveedor!=proveedor_update:
        self.actualizar_Proveedor((razon_social,ciudad,id_nit,))
        mssg.showinfo('.. Confirmación ..', '.. Proveedor actualizado ..')   
        if producto!=producto_update:
           self.actualizar_Producto((descripcion,unidad,cantidad,precio,fecha,id_nit,codigo,))
           self.cargar_Datos_Buscados([[id_nit,codigo,descripcion,unidad,cantidad,precio,fecha]])
           mssg.showinfo('.. Confirmación ..', '.. Producto actualizado ..')
     self.actualiza=None
     self.limpia_Campos()
           
  # Operaciones con la base de datos
  def run_Query(self, query, parametros = ()):
    ''' Función para ejecutar los Querys a la base de datos '''
    with sqlite3.connect(self.db_name) as conn:
        cursor = conn.cursor()
        result = cursor.execute(query, parametros)
        conn.commit()
    return result

  def lee_Tree_Productos(self):
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
    self.codigo.insert(0,row[4])
    self.descripcion.insert(0,row[5])
    self.unidad.insert(0,row[6])
    self.cantidad.insert(0,row[7])
    self.precio.insert(0,row[8])
    self.fecha.insert(0,row[9])  
    
  def limpiar_Treeview(self):
    tabla_TreeView = self.treeProductos.get_children()
    for linea in tabla_TreeView:
        self.treeProductos.delete(linea)

  def cargar_Datos_Treeview(self,db_rows):
      for row in db_rows:
         self.treeProductos.insert('',0, text = row[0], values = [row[1],row[2],row[3],row[4],row[5],row[6]])

  def cargar_Datos_Buscados(self,search):
      self.limpiar_Treeview()
      self.cargar_Datos_Treeview(search)
          
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
    relacion=self.accion_Buscar('*','Producto','IdNit = ? AND Codigo = ?',(id_nit, codigo,)).fetchone()

    if id_nit=="" and codigo=="":
       mssg.showerror('Atención!!','.. ¡No se han especificado ningun dato para guardar! ..')

    elif id_nit=="" and codigo!="":
       mssg.showerror('Atención!!','.. ¡No se especifico ningun proveedor para el producto! ..')

    elif codigo=="" and id_nit!= "":
       
       if self.validar_ID()==False:
          self.insertar_Proveedor(id_nit, razon_social,ciudad)
          mssg.showinfo('Confirmación','.. El proveedor a sido registrado correctamente ..')

       elif self.validar_ID()==True:
          mssg.showerror('Atención!!','.. ¡El proveedor ya existe no puede ser insertado otra vez! ..')

    elif id_nit!="" and codigo!="":
       if fecha!="":
          if (self.validar_ID()==False and self.validar_Cod()==False) or (self.validar_Cod()==True and self.validar_ID()==False):
             self.insertar_Proveedor(id_nit,razon_social,ciudad)
             mssg.showinfo('Confirmación','.. El proveedor a sido registrado correctamente ..')
             self.insertar_Producto(id_nit,codigo,descripcion,unidad,cantidad, precio, fecha)
             mssg.showinfo('Confirmación','.. El producto a sido registrado correctamente ..')
             datos=self.accion_Buscar("*","Producto"," IdNit = ? AND Codigo = ?",(id_nit,codigo,)).fetchall()
             self.cargar_Datos_Buscados(datos)

          elif (self.validar_ID()==True and self.validar_Cod()==False) or (relacion == None):
          
             self.insertar_Producto(id_nit,codigo,descripcion,unidad,cantidad, precio, fecha)
             mssg.showinfo('Confirmación','.. El producto a sido registrado correctamente ..')
             datos=self.accion_Buscar("*","Producto"," IdNit = ? AND Codigo = ?",(id_nit,codigo,)).fetchall()
             self.cargar_Datos_Buscados(datos)

          elif relacion!= None:  
             mssg.showerror('Atención!!','.. ¡El producto ya esta relacionado con el proveedor indicado! ..')
       elif fecha=="":
            mssg.showerror('Atención!!','.. ¡Digite una fecha para registrar! ..')
          
  def edita_Tree_Proveedores(self, event=None):
    ''' Edita una tupla del TreeView'''
    pass
      
  def elimina_Registro(self, obj):
    '''Elimina un Registro en la BD'''
    id=obj["text"]
    codigo=obj["values"][0]
    if self.obj_eliminar.get()=='Producto':
       try:
          self.accion_Eliminar('Producto','IdNit = ? AND Codigo = ? ',(id, codigo,))
       except:
          mssg.showerror('.. Error! ..', f'Se ha producido un error al tratar de eliminar el registro del producto {codigo}, correspondiente al proveedor {id}')
       else:
          mssg.showinfo(' .. Confirmación .. ', f'Se ha eliminado el registro del producto {codigo}, correspondiente al proveedor {id} correctamente')
    elif self.obj_eliminar.get()=='Proveedor':
       try:
          self.accion_Eliminar('Producto','IdNit = ? ',(id,))
          self.accion_Eliminar('Proveedor','idNitProv = ? ', (id,))
       except:
          mssg.showerror('.. Error! ..', f'Se ha producido un error al tratar de eliminar el proveedor {id} y todos los registros relacionados a él')
       else:
          mssg.showinfo(' .. Confirmación .. ', f'Se ha eliminado el proveedor {id} y todos los registros relacionados a él correctamente')
    elif self.obj_eliminar.get()=='Todos los productos':
       try:
          self.accion_Eliminar('Producto','Codigo = ? ',(codigo,))
       except:
          mssg.showerror('.. Error! ..', f'Se ha producido un error al tratar de eliminar todos los registros relacionados con el producto {codigo}')
       else:
          mssg.showinfo(' .. Confirmación .. ', f'Se ha eliminado todos los registros relacionados al producto {codigo}')      
        
  
  def accion_Buscar(self,seleccion,tabla,condicion, valoresdecodicion =()):
    search=f'''SELECT {seleccion} FROM {tabla} WHERE {condicion}'''
    resultado=self.run_Query(search,valoresdecodicion)
    return resultado
  
  def accion_Eliminar(self, tabla, condicion, valores_de_la_condicion):
     delete=f''' DELETE FROM {tabla} WHERE {condicion} '''
     self.run_Query(delete, valores_de_la_condicion)
  
  def insertar_Proveedor(self, id , razon_social, ciudad):
    insert=f''' INSERT INTO Proveedor VALUES (?,?,?)'''
    self.run_Query(insert, (id, razon_social, ciudad,))
   
  def insertar_Producto(self, IdNit, Codigo, descripcion, und, cantidad, precio, fecha):
    insert=f''' INSERT INTO Producto VALUES (?,?,?,?,?,?,?)'''
    self.run_Query(insert, (IdNit, Codigo, descripcion, und, cantidad, precio, fecha,))

  def actualizar_Proveedor(self, values):
     update=''' UPDATE Proveedor 
                SET Razon_Social = ? , Ciudad = ? WHERE 
                idNitProv = ? '''
     self.run_Query(update,values)

  def actualizar_Producto(self,values):
     update=''' UPDATE Producto 
             SET Descripcion = ? , Und = ? , Cantidad = ? , Precio = ? , Fecha = ? 
             WHERE IdNit = ? AND Codigo = ? '''
     self.run_Query(update,values)
  
  def cargar_Proveedor(self, id):
     proveedor=self.accion_Buscar("*","Proveedor","idNitProv= ? " , (id,)).fetchone()
     self.idNit.insert(0,proveedor[0])
     self.razonSocial.insert(0,proveedor[1])
     self.ciudad.insert(0, proveedor[2])
  
  def cargar_Producto(self,producto):
     self.codigo.insert(0,producto[1])
     self.descripcion.insert(0,producto[2])
     self.unidad.insert(0,producto[3])
     self.cantidad.insert(0,producto[4])
     self.precio.insert(0,producto[5])
     self.fecha.insert(0,producto[6])

     
  def search_Button (self):
     id= self.idNit.get()
     cod= self.codigo.get()
     if id != "" and cod =="":
        if self.validar_ID()==True:
          search=self.accion_Buscar("*","Producto", "IdNit= ? ", (id,)).fetchall()
          self.limpia_Campos()
          self.cargar_Datos_Buscados(search)
          self.cargar_Proveedor(id)
        else:
           mssg.showerror('Atención!!','.. ¡El proveedor no existe! ..')
     elif id == "" and cod !="":
        if self.validar_Cod()==True:
           search=self.accion_Buscar("*","Producto", "Codigo= ? ",(cod,)).fetchall()
           self.cargar_Datos_Buscados(search)
           self.limpia_Campos()
           if len(search)>1:
              self.codigo.insert(0,cod)
           else:
              self.cargar_Producto(search[0])
              self.cargar_Proveedor(id)
        else:
           mssg.showerror('Atención!!','.. ¡El producto no existe! ..')
     elif id != "" and cod !="":
        if self.validar_ID()==True and self.validar_Cod()==True:
           search=self.accion_Buscar("*","Producto", "Codigo= ? AND IdNit= ? ", (cod , id,)).fetchall()
           if search == None:
              mssg.showerror('Atención!!','.. ¡El producto no corresponde al proveedor indicado! ..')
           else: 
              self.limpia_Campos()
              self.cargar_Datos_Buscados(search)
              self.cargar_Proveedor(id)
              self.cargar_Producto(search[0])
        elif self.validar_ID()==True and self.validar_Cod()==False:
           mssg.showerror('Atención!!','.. ¡El producto no existe! ..')
        elif self.validar_ID()==False and self.validar_Cod()==True:
           mssg.showerror('Atención!!','.. ¡El proveedor no existe! ..')
        elif self.validar_ID()==False and self.validar_Cod()==False:
           mssg.showerror('Atención!!','.. ¡Ni el producto, ni el proveedor existen! ..')

  def cancel_Button(self):
     self.limpiar_Treeview()
     self.limpia_Campos()
     if self.actualiza== True:
         self.actualiza = None
         mssg.showinfo(".. Confirmación ..", '.. Ha salido del modo Editar ..')
     self.estado_Buttons(True)
   
  def record_Button(self):
     if self.actualiza==None:
        self.adiciona_Registro()
     elif self.actualiza== True:
        self.actualizar_datos()
        self.estado_Buttons(True)
        
  def edit_Button(self):
     self.carga_Datos()

  def eliminar_Button(self):
     if self.treeProductos.selection() != ():
        self.abrir_Ventana_Eliminar()
     elif self.treeProductos.selection()==():
        mssg.showerror('.. Error!..', ' .. No se ha seleccionado ningun registro a eliminar! .. ')
     
if __name__ == "__main__":
    app = Inventario()
    app.run()
