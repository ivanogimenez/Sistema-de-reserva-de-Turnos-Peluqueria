import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
from datetime import date
import json
import os
import re

# Archivos donde se almacenan los datos:
archivo_json_turnos = "./Proyecto_Final/turnos.json"
archivo_json_clientes = "./Proyecto_Final/clientes.json"
archivo_json_usuarios = "./Proyecto_Final/usuarios.json"
# Rango horario permitido para los turnos (9am a 19pm)
HORARIO_INICIO = 9
HORARIO_FIN = 19

# Funciones CRUD para turnos y clientes:
#  Leer Archivo (que puede ser turnos.json o clientes.json)
# si todo esta bien ---> retorna un json que es: texto formateado a json
def cargar_datos(archivo_json):
    if os.path.exists(archivo_json):
        with open(archivo_json, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []

# Guardar Archivo
def guardar_datos(archivo_json , datos):
    with open(archivo_json, 'w') as file:
        json.dump(datos, file, indent=4)

def crear_cliente(nombre, email):
    datos = cargar_datos(archivo_json_clientes)
    if not existe_cliente(nombre):
        datos.append({'nombre': nombre, 'email': email})
        guardar_datos(archivo_json_clientes, datos)
        listar_clientes()
    else:
        messagebox.showwarning("Error", "El cliente ya existe")

def eliminar_cliente(index):
    clientes = cargar_datos(archivo_json_clientes)
    cliente = clientes[index]['nombre']
    eliminar_turnos_cliente(cliente)
    del clientes[index]
    guardar_datos(archivo_json_clientes, clientes)
    listar_clientes()

def eliminar_turnos_cliente(nombre):
    turnos = cargar_datos(archivo_json_turnos)
    resultados = [turno for turno in turnos if nombre != turno['cliente']]
    guardar_datos(archivo_json_turnos, resultados)
    listar_turnos()

def existe_cliente(nombre):
    clientes = cargar_datos(archivo_json_clientes)
    for cliente in clientes:
        if cliente["nombre"].lower() == nombre.lower():
            return True
    return False

def listar_clientes():
    clientes_list.delete(0, tk.END)
    datos = cargar_datos(archivo_json_clientes)
    for cliente in datos:
        clientes_list.insert(tk.END, f"{cliente['nombre']} - {cliente['email']}")

# Funciones CRUD
def crear_turno(cliente, fecha, hora):
    if verificar_horario(hora) and not verificar_turno_existente(fecha, hora):
        datos = cargar_datos(archivo_json_turnos)
        datos.append({'cliente': cliente, 'fecha': fecha,'hora': hora})
        guardar_datos(archivo_json_turnos, datos)
        listar_turnos()
    else:
        messagebox.showwarning("Turno Invalido","El horario debe estar entre las 9.00 y las 19:00 y solo puede haber un turno por hora")

def listar_turnos():
    turnos_list.delete(0, tk.END)
    datos = cargar_datos(archivo_json_turnos)

    for turno in datos:
        turnos_list.insert(tk.END, f"{turno['cliente']} - {turno['fecha']} - {turno['hora']}hs.")

def actualizar_turno(index, fecha, hora):
    if verificar_horario(hora) and not verificar_turno_existente(fecha, hora):
        datos = cargar_datos(archivo_json_turnos)
        datos[index]['fecha'] = fecha
        datos[index]['hora'] = hora
        guardar_datos(archivo_json_turnos, datos)
        listar_turnos()
    else:
        messagebox.showwarning("Turno Invalido","El horario debe estar entre las 9.00 y las 19:00 y solo puede haber un turno por hora")

def eliminar_turno(index):
    datos = cargar_datos(archivo_json_turnos)
    del datos[index]
    guardar_datos(archivo_json_turnos, datos)
    listar_turnos()

def verificar_horario(hora):
    try:
        if HORARIO_INICIO <= int(hora) < HORARIO_FIN:
            return True
        else:
            return False
    except ValueError:
        return False

def verificar_turno_existente(fecha, hora):
    datos = cargar_datos(archivo_json_turnos)
    for turno in datos:
        if turno["fecha"] == fecha and turno["hora"] == hora:
            return True
    return False

def verificar_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None
    
def on_crear_cliente():
    nombre = entry_cliente.get()
    email = entry_email.get()
    if nombre and email:
        if (verificar_email(email)):
            crear_cliente(nombre, email)
            entry_cliente.delete(0, tk.END)
            entry_email.delete(0, tk.END)
        else:
            messagebox.showwarning("Error", "El email no es válido...")
    else:
        messagebox.showwarning("Error", "El cliente y email no puede estar vacío...")

def on_eliminar_cliente():
    try:
        index= clientes_list.curselection()[0]
        eliminar_cliente(index)
    except IndexError:
        messagebox.showwarning("Error", "Seleccione un cliente para eliminar")

def on_crear_turno():
    try:
        clientes = cargar_datos(archivo_json_clientes)
        index = clientes_list.curselection()[0]
        cliente = clientes[index]['nombre']
        fecha = entry_fecha.get_date()
        hora = entry_hora.get()
        if cliente and fecha and hora:
            crear_turno(cliente,fecha, hora)
            entry_hora.delete(0, tk.END)
        else:
            messagebox.showwarning("Error", "Todos los campos son requeridos")
    except (tk.TclError,IndexError):
        messagebox.showwarning("Error", "Seleccione un cliente para asignar el turno")

def on_actualizar_turno():
    try:
        index = turnos_list.curselection()[0]
        fecha = entry_fecha.get_date()
        hora = entry_hora.get()
        if fecha and hora:
            actualizar_turno(index, fecha, hora)
            entry_hora.delete(0,tk.END)
        else:
            messagebox.showwarning("Error", "Todos los campor son requeridos")
    except(tk.TclError, IndexError):
        messagebox.showwarning("Error", "Seleccione un turno para actualizar")

def on_eliminar_turno():
    try:
        index= turnos_list.curselection()[0]
        eliminar_turno(index)
    except IndexError:
        messagebox.showwarning("Error", "Seleccione un turno para eliminar")

def verificar_usuario(usuario, contrasena):
    usuarios = cargar_datos(archivo_json_usuarios)
    for u in usuarios:
        if u["usuario"] == usuario and u["contrasena"] == contrasena:
            return True
    return False

# Interfaz gráfica login
def mostrar_login():
    def login():
        usuario = entry_usuario.get()
        contrasena = entry_contrasena.get()
        if verificar_usuario(usuario, contrasena):
            login_window.destroy()
            mostrar_crud()
        else:
            messagebox.showerror("Error de login", "Credenciales incorrectas")
    
    login_window = tk.Toplevel(root)
    login_window.title("Login")
    login_window.geometry("300x300")

    tk.Label(login_window, text="Usuario:", font=("Arial", 12)).pack(pady=10)
    entry_usuario = tk.Entry(login_window, font=("Arial", 12))
    entry_usuario.pack(pady=5)

    tk.Label(login_window, text="Contraseña:", font=("Arial", 12)).pack(pady=10)
    entry_contrasena = tk.Entry(login_window, font=("Arial", 12), show="*")
    entry_contrasena.pack(pady=5)

    tk.Button(login_window, text="Acceder", command=login, font=("Arial", 12)).pack(pady=20)

# Interfaz gráfica CRUD
def mostrar_crud():
    global entry_cliente, entry_email, clientes_list, entry_hora, entry_fecha, turnos_list

    frame_clientes = tk.Frame(root)
    frame_clientes.pack(pady=10)

    tk.Label(frame_clientes, text="Clientes").pack()
    tk.Label(frame_clientes, text="Nombre").pack(side=tk.LEFT, padx=5)
    entry_cliente = tk.Entry(frame_clientes)
    entry_cliente.pack(side=tk.LEFT, padx=5)
    tk.Label(frame_clientes, text="Email").pack(side=tk.LEFT, padx=5)
    entry_email = tk.Entry(frame_clientes)
    entry_email.pack(side=tk.LEFT, padx=5)
    tk.Button(frame_clientes, text="Crear cliente", command=on_crear_cliente).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_clientes, text="Eliminar cliente", command=on_eliminar_cliente).pack(side=tk.LEFT, padx=5)


    frame_lista_clientes = tk.Frame(root)
    frame_lista_clientes.pack(pady=2)
    clientes_list = tk.Listbox(frame_lista_clientes,width=50)
    clientes_list.pack(pady=10)

    frame_turnos = tk.Frame(root)
    frame_turnos.pack(pady=10)

    tk.Label(frame_turnos, text="Fecha").grid(row=0, column=0)
    tk.Label(frame_turnos, text="Hora (hh)").grid(row=1, column=0)

    hoy = date.today()
    entry_hora = tk.Entry(frame_turnos)
    entry_fecha = Calendar(frame_turnos,font="Arial 7", selectmode='day', locale='es_ES',date_pattern="dd-mm-y", year=hoy.year, month=hoy.month, day=hoy.day)

    entry_fecha.grid(row=0, column=1)
    entry_hora.grid(row=1, column=1)

    tk.Button(frame_turnos, text="Crear Turno", command=on_crear_turno).grid(row=2, column=0, pady=10)
    tk.Button(frame_turnos, text="Actualizar Turno", command=on_actualizar_turno).grid(row=2, column=1, pady=10)
    tk.Button(frame_turnos, text="Eliminar Turno", command=on_eliminar_turno).grid(row=2, column=2, columnspan=2, pady=10)

    turnos_list = tk.Listbox(root,width=50)
    turnos_list.pack(pady=10)

    root.wm_deiconify()
    listar_clientes()
    listar_turnos()

# Inicio programa
root = tk.Tk()
root.title("Reserva de Turnos - Salón")
root.withdraw()

mostrar_login()

root.mainloop()