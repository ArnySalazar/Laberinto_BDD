import pymysql
from tkinter import *
from tkinter import messagebox
from datetime import datetime, timedelta

user_id = None
partida_id = 1
tiempo_voto = 20
votacion_activa = False
tiempo_inicio_votacion = None

def crear_conexion():
    try:
        connection = pymysql.connect(
            host='autorack.proxy.rlwy.net',
            user='root',
            password='lDWLBIxYCbLnYZXYqQFYLkNrTJVgQnDM',
            database='railway',
            port=36047
        )
        return connection
    except pymysql.MySQLError as e:
        print(f"Error al conectar: {e}")
        return None

def registrar_voto(direccion):
    if votacion_activa:
        conexion = crear_conexion()
        if conexion:
            try:
                with conexion.cursor() as cursor:
                    cursor.callproc('registrar_voto', (user_id, direccion, partida_id))
                    conexion.commit()
                    print(f"Voto registrado: {direccion} por el usuario {user_id}")
            except pymysql.MySQLError as e:
                print(f"Error al registrar el voto: {e}")
            finally:
                conexion.close()
    else:
        messagebox.showerror("Error", "La votación no está activa en este momento. Espere el próximo ciclo.")


def votar(direction):
    registrar_voto(direction)

def tkinter_controls():
    ventana = Tk()
    ventana.title("Votación del Juego")
    ventana.geometry("300x200")

    btn_up = Button(ventana, text="↑", command=lambda: votar('up'), width=5, height=2)
    btn_up.pack(side=TOP, pady=5)

    btn_down = Button(ventana, text="↓", command=lambda: votar('down'), width=5, height=2)
    btn_down.pack(side=BOTTOM, pady=5)

    btn_left = Button(ventana, text="←", command=lambda: votar('left'), width=5, height=2)
    btn_left.pack(side=LEFT, padx=5)

    btn_right = Button(ventana, text="→", command=lambda: votar('right'), width=5, height=2)
    btn_right.pack(side=RIGHT, padx=5)

    ventana.mainloop()

def verificar_login(nombre_usuario, ventana_login):
    global user_id
    conexion = crear_conexion()
    if conexion:
        try:
            with conexion.cursor() as cursor:
                query = "SELECT ID_usuario FROM usuarios WHERE nombre_usuario = %s"
                cursor.execute(query, (nombre_usuario,))
                resultado = cursor.fetchone()
                if resultado:
                    user_id = resultado[0]
                    messagebox.showinfo("Login", f"Bienvenido, {nombre_usuario}!")
                    ventana_login.destroy()
                    tkinter_controls()
                else:
                    messagebox.showerror("Error", "Usuario no encontrado.")
        except pymysql.MySQLError as e:
            messagebox.showerror("Error", f"Error en el login: {e}")
        finally:
            conexion.close()

def ventana_registro():
    def registrar():
        nombre_usuario = entry_nombre.get()
        if nombre_usuario:
            registrar_usuario(nombre_usuario)
            ventana_registro.destroy()

    ventana_registro = Toplevel()
    ventana_registro.title("Registro de Usuario")
    ventana_registro.geometry("300x200")

    label_nombre = Label(ventana_registro, text="Nombre de Usuario:")
    label_nombre.pack(pady=5)

    entry_nombre = Entry(ventana_registro)
    entry_nombre.pack(pady=5)

    btn_registrar = Button(ventana_registro, text="Registrar", command=registrar)
    btn_registrar.pack(pady=10)

def ventana_login():
    def login():
        nombre_usuario = entry_nombre.get()
        if nombre_usuario:
            verificar_login(nombre_usuario, ventana_login)

    ventana_login = Tk()
    ventana_login.title("Login")
    ventana_login.geometry("300x200")

    label_nombre = Label(ventana_login, text="Nombre de Usuario:")
    label_nombre.pack(pady=5)

    entry_nombre = Entry(ventana_login)
    entry_nombre.pack(pady=5)

    btn_login = Button(ventana_login, text="Login", command=login)
    btn_login.pack(pady=10)

    btn_registro = Button(ventana_login, text="Registrar", command=ventana_registro)
    btn_registro.pack(pady=5)

    ventana_login.mainloop()

def registrar_usuario(nombre_usuario):
    conexion = crear_conexion()
    if conexion:
        try:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT * FROM usuarios WHERE nombre_usuario = %s", (nombre_usuario,))
                resultado = cursor.fetchone()
                if resultado:
                    messagebox.showerror("Error", "El usuario ya existe.")
                else:
                    query = "INSERT INTO usuarios (nombre_usuario) VALUES (%s)"
                    cursor.execute(query, (nombre_usuario,))
                    conexion.commit()
                    messagebox.showinfo("Registro", f"Usuario '{nombre_usuario}' registrado correctamente.")
        except pymysql.MySQLError as e:
            messagebox.showerror("Error", f"Error al registrar el usuario: {e}")
        finally:
            conexion.close()

if __name__ == "__main__":
    ventana_login()