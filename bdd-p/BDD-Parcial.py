import pymysql
from tkinter import *
from tkinter import messagebox
from datetime import datetime, timedelta
import threading
import time

# Global variables
user_id = None
partida_id = 1  # Game ID or session ID
tiempo_voto = 20  # Voting duration in seconds
votacion_activa = False  # Voting flag
tiempo_inicio_votacion = None  # Voting start time

# MySQL Connection Function
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

# Get Command ID from the database (comandos_referencia table)
def obtener_id_comando(direccion):
    conexion = crear_conexion()
    if conexion:
        try:
            with conexion.cursor() as cursor:
                query = "SELECT ID_comando FROM comandos_referencia WHERE comando = %s"
                cursor.execute(query, (direccion,))
                resultado = cursor.fetchone()
                if resultado:
                    return resultado[0]
                else:
                    print(f"Error: No se encontró el ID para el comando: {direccion}")
                    return None
        except pymysql.MySQLError as e:
            print(f"Error al obtener ID del comando: {e}")
        finally:
            conexion.close()
    return None

# Register the vote using the stored procedure
def registrar_voto(direccion):
    if votacion_activa:
        conexion = crear_conexion()
        if conexion:
            try:
                with conexion.cursor() as cursor:
                    # Call stored procedure registrar_voto
                    cursor.callproc('registrar_voto', (user_id, direccion, partida_id))
                    conexion.commit()
                    print(f"Voto registrado: {direccion} por el usuario {user_id}")
            except pymysql.MySQLError as e:
                print(f"Error al registrar el voto: {e}")
            finally:
                conexion.close()
    else:
        messagebox.showerror("Error", "La votación no está activa en este momento. Espere el próximo ciclo.")

# Call the stored procedure to count votes and register the result
def contar_y_registrar_resultado():
    conexion = crear_conexion()
    if conexion:
        try:
            with conexion.cursor() as cursor:
                # Call stored procedure contar_y_registrar_resultado
                cursor.callproc('contar_y_registrar_resultado', (partida_id, tiempo_inicio_votacion))
                resultado = cursor.fetchone()

                # Check if the result is NULL
                if resultado and resultado[0]:
                    comando_ganador = resultado[0]
                else:
                    # If no result, assign "up" as the default command
                    comando_ganador = obtener_id_comando('up')
                    print("No hubo votos. Ejecutando comando 'up' por defecto.")
                
                print(f"Resultado registrado: {comando_ganador}")
        except pymysql.MySQLError as e:
            print(f"Error al contar los votos: {e}")
        finally:
            conexion.close()

# Call the stored procedure to clean up the old votes
def limpiar_votos():
    conexion = crear_conexion()
    if conexion:
        try:
            with conexion.cursor() as cursor:
                cursor.callproc('limpiar_votos', (partida_id,))
                conexion.commit()
                print("Votos antiguos eliminados.")
        except pymysql.MySQLError as e:
            print(f"Error al limpiar los votos: {e}")
        finally:
            conexion.close()

# Handle voting process
def votar(direction):
    registrar_voto(direction)

# Voting timer and reset mechanism
def iniciar_votacion():
    global votacion_activa, tiempo_inicio_votacion
    votacion_activa = True
    tiempo_inicio_votacion = datetime.now()
    print("Inicia la votación. Los usuarios tienen 20 segundos para votar.")
    
    time.sleep(tiempo_voto)
    votacion_activa = False
    print("Tiempo de votación finalizado. Contando votos...")
    lock_table_votos()
    contar_y_registrar_resultado()
    unlock_table_votos()
    limpiar_votos()
    reset_votacion()

def lock_table_votos():
    conexion = crear_conexion()
    if conexion:
        try:
            with conexion.cursor() as cursor:
                cursor.execute("LOCK TABLES votos WRITE;")
                conexion.commit()
                print("Table votos locked for writing.")
        except pymysql.MySQLError as e:
            print(f"Error al bloquear la tabla votos: {e}")
        finally:
            conexion.close()

def unlock_table_votos():
    conexion = crear_conexion()
    if conexion:
        try:
            with conexion.cursor() as cursor:
                cursor.execute("UNLOCK TABLES;")
                conexion.commit()
                print("Table votos unlocked.")
        except pymysql.MySQLError as e:
            print(f"Error al desbloquear la tabla votos: {e}")
        finally:
            conexion.close()


def reset_votacion():
    print("Preparando la próxima votación...")
    time.sleep(5)
    iniciar_votacion()

# GUI for voting using Tkinter
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

    threading.Thread(target=iniciar_votacion).start()

    ventana.mainloop()

# User login verification
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

# GUI for user registration
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

# GUI for login
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

# User registration
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

# Execute login window at start
if __name__ == "__main__":
    ventana_login()
