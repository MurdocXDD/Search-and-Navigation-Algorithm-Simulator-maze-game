import random
import tkinter as tk
from tkinter import messagebox
import time

def crear_laberinto(filas, columnas):
    laberinto = [[1] * columnas for _ in range(filas)]  # Inicializar con paredes
    laberinto[0][0] = 0  # Entrada
    # Determinar una salida en una posición aleatoria
    salida_fila = random.randint(1, filas - 2)
    salida_columna = random.randint(1, columnas - 2)
    laberinto[salida_fila][salida_columna] = 2  # Salida
    # Crear espacios abiertos aleatorios
    for i in range(filas):
        for j in range(columnas):
            if (i, j) != (salida_fila, salida_columna) and random.random() < 0.6:
                laberinto[i][j] = 0
    # Agregar casilla morada con trivia
    casilla_morada_fila = random.randint(0, filas - 1)
    casilla_morada_columna = random.randint(0, columnas - 1)
    while laberinto[casilla_morada_fila][casilla_morada_columna] != 0:  # Asegurar que la casilla sea camino
        casilla_morada_fila = random.randint(0, filas - 1)
        casilla_morada_columna = random.randint(0, columnas - 1)
    laberinto[casilla_morada_fila][casilla_morada_columna] = '?'  # Casilla morada
    # Agregar casilla dorada para teletransportar
    casilla_dorada_fila = random.randint(0, filas - 1)
    casilla_dorada_columna = random.randint(0, columnas - 1)
    while laberinto[casilla_dorada_fila][casilla_dorada_columna] != 0:  # Asegurar que la casilla sea camino
        casilla_dorada_fila = random.randint(0, filas - 1)
        casilla_dorada_columna = random.randint(0, columnas - 1)
    laberinto[casilla_dorada_fila][casilla_dorada_columna] = 'D'  # Casilla dorada
    return laberinto

def resolver_laberinto():
    global laberinto, filas, columnas

    def resolver(fil, col):
        nonlocal solved
        if 0 <= fil < filas and 0 <= col < columnas and not solved:
            if laberinto[fil][col] == 2:
                solved = True
                messagebox.showinfo("Laberinto", "¡Laberinto resuelto!")
                return

            if laberinto[fil][col] == '?':
                trivia_correcta = False
                while not trivia_correcta:
                    trivia_resuelta = messagebox.askyesno("Trivia", "¿Es 2 + 2 igual a 4?")
                    if trivia_resuelta:
                        trivia_correcta = True
                    else:
                        messagebox.showinfo("Trivia", "Respuesta incorrecta. Intenta de nuevo.")

                laberinto[fil][col] = 0
                mostrar_laberinto(laberinto)
                time.sleep(1.0)  # Retraso de 1 segundo
                resolver(fil + 1, col)
                resolver(fil, col + 1)
                resolver(fil - 1, col)
                resolver(fil, col - 1)
                laberinto[fil][col] = '?'  # Deshacer el movimiento

            if laberinto[fil][col] == 'D':
                messagebox.showinfo("Teletransporte", "¡Te has teletransportado!")
                fil, col = teletransportar_mas_cerca_de_salida(fil, col)
                mostrar_laberinto(laberinto)
                time.sleep(1.0)  # Retraso de 1 segundo
                resolver(fil, col)

            if laberinto[fil][col] == 0:
                laberinto[fil][col] = '.'
                mostrar_laberinto(laberinto)
                time.sleep(1.0)  # Retraso de 1 segundo
                resolver(fil + 1, col)
                resolver(fil, col + 1)
                resolver(fil - 1, col)
                resolver(fil, col - 1)
                laberinto[fil][col] = 0  # Deshacer el movimiento

    solved = False
    resolver(0, 0)
    if not solved:
        messagebox.showinfo("Laberinto", "No se encontró una solución.")

def teletransportar_mas_cerca_de_salida(fil, col):
    salida_fila, salida_columna = encontrar_salida()
    distancia_actual = abs(fil - salida_fila) + abs(col - salida_columna)
    mejor_fila, mejor_col = fil, col

    for i in range(filas):
        for j in range(columnas):
            if laberinto[i][j] == 0:
                distancia = abs(i - salida_fila) + abs(j - salida_columna)
                if distancia < distancia_actual:
                    mejor_fila, mejor_col = i, j
                    distancia_actual = distancia

    return mejor_fila, mejor_col

def encontrar_salida():
    for i in range(filas):
        for j in range(columnas):
            if laberinto[i][j] == 2:
                return i, j

def generar_laberinto(entry_filas, entry_columnas):
    global laberinto, filas, columnas
    filas = int(entry_filas.get())
    columnas = int(entry_columnas.get())
    if filas < 6 or columnas < 6:
        messagebox.showerror("Error", "El tamaño mínimo del laberinto es 6x6.")
        return
    elif filas != columnas:
        messagebox.showerror("Error", "El tamaño debe ser cuadrado.")
        return

    laberinto = crear_laberinto(filas, columnas)
    mostrar_laberinto(laberinto)

def mostrar_laberinto(laberinto):
    global canvas
    canvas.delete("all")  # Eliminar todos los elementos del lienzo antes de redibujar

    colores = {0: "white", 1: "black", 2: "red", '?': "purple", '.': "green", 'entrada': "blue", 'D': "gold"}

    # Calcular el tamaño del laberinto
    num_filas = len(laberinto)
    num_columnas = len(laberinto[0])

    # Calcular el tamaño de una celda en el lienzo
    ancho_celda = canvas.winfo_width() / num_columnas
    alto_celda = canvas.winfo_height() / num_filas

    for i, fila in enumerate(laberinto):
        for j, valor in enumerate(fila):
            color = colores[valor]
            if (i, j) == (0, 0):
                color = colores['entrada']

            # Calcular las coordenadas para dibujar la celda en el lienzo
            x0 = j * ancho_celda
            y0 = i * alto_celda
            x1 = x0 + ancho_celda
            y1 = y0 + alto_celda

            canvas.create_rectangle(x0, y0, x1, y1, fill=color)

    canvas.update()

def reglas():
    root_regla = tk.Tk()
    root_regla.configure(background="#0E2954")
    root_regla.title("Reglas")
    root_regla.geometry("650x350")
    label_reglas = tk.Label(root_regla, text="REGLAS: \n", font=("Berlin Sans FB Demi", 14),bg="#0E2954" ,fg="#A4CE95")
    label_reglas1 = tk.Label(root_regla, text="1. La casilla azul es la posicion inicial\n", bg="#0E2954" ,fg="Blue" ,font=("Berlin Sans FB Demi", 12))
    label_reglas2 = tk.Label(root_regla, text="2. Las casillas verdes es el camino que recorre el jugador\n",bg="#0E2954" ,fg="Green" ,font=("Berlin Sans FB Demi", 12))
    label_reglas3 = tk.Label(root_regla, text="3. La casilla roja es la salida\n",bg="#0E2954" ,fg="Red" ,font=("Berlin Sans FB Demi", 12))
    label_reglas4 = tk.Label(root_regla, text="4. La casilla morada es una trivia\n"
                                              "(No se podra avanzar hasta responder bien)\n",bg="#0E2954" ,fg="Purple" ,font=("Berlin Sans FB Demi", 12))
    label_reglas5 = tk.Label(root_regla, text="5. La casilla amarilla es un teletransporte\n"
                                              "(Te enviara a una posicion al azar del laberinto)\n",bg="#0E2954" ,fg="Yellow" ,font=("Berlin Sans FB Demi", 12))

    label_reglas.pack()
    label_reglas1.pack()
    label_reglas2.pack()
    label_reglas3.pack()
    label_reglas4.pack()
    label_reglas5.pack()
    button_ocultar = tk.Button(root_regla, text="Ocultar", font=("Berlin Sans FB Demi", 9),command=root_regla.destroy, bg="#6196A6", fg="#F4EDCC")
    button_ocultar.pack()

def creditos():

    credits = tk.Tk()
    credits.title("Creditos")

    label_credits = tk.Label(credits, text="DESARROLLADO POR:\n", font=("Berlin Sans FB Demi",12), fg="#A4CE95")
    label_credits.pack()
    label_credits1 = tk.Label(credits, text="Omar Alejandro Brizuela Esqueda (Administrador)\n"
                                            "Javier Solorzano Razo (Backend)\n"
                                            "Angel Sebastian Garnica Carbajal (Frontend)", font=("Berlin Sans FB Demi",12), fg="#5F5D9C")
    label_credits1.pack()

    button_ocultar = tk.Button(credits, text="Ocultar", font=("Berlin Sans FB Demi", 9),command=credits.destroy, bg="#6196A6", fg="#F4EDCC")
    button_ocultar.pack(pady=5)

def opc_maze():
    root.destroy()
    global canvas  # Importar la variable global canvas

    opc = tk.Tk()
    opc.title("Medidas")
    label_filas = tk.Label(opc, text="Filas:", font=("Berlin Sans FB Demi", 14), fg="#A4CE95")
    label_filas.pack()
    entry_filas = tk.Entry(opc)
    entry_filas.pack()

    label_columnas = tk.Label(opc, text="Columnas:", font=("Berlin Sans FB Demi", 14),fg="#A4CE95")
    label_columnas.pack()
    entry_columnas = tk.Entry(opc)
    entry_columnas.pack()

    button_generar = tk.Button(opc, text="Generar Laberinto", font=("Berlin Sans FB Demi", 9), bg="#6196A6", fg="#F4EDCC",command=lambda: generar_laberinto(entry_filas, entry_columnas))
    button_generar.pack(pady=3)

    button_resolver = tk.Button(opc, text="Resolver Laberinto",font=("Berlin Sans FB Demi", 9),command=resolver_laberinto, bg="#6196A6", fg="#F4EDCC")
    button_resolver.pack(pady=3)

    button_reglas = tk.Button(opc, text="Reglas", font=("Berlin Sans FB Demi", 9),command=reglas, bg="#6196A6", fg="#F4EDCC")
    button_reglas.pack(pady=3)
    # Crear lienzo para mostrar el laberinto
    canvas = tk.Canvas(opc, width=300, height=300)
    canvas.pack()

root = tk.Tk()
root.title("Laberinto")
icono = tk.PhotoImage(file="mazeicon.png")
root.iconphoto(True, icono)

label_bienvenida = tk.Label(root, text="¡Bienvenido al juego del laberinto!", fg="#A4CE95",font=("Berlin Sans FB Demi", 14))
label_bienvenida.pack()

label_creditos = tk.Label(root, text="Desarrollado por el equipo 2", fg="#5F5D9C",font=("Berlin Sans FB Demi", 10))
label_creditos.pack()

start_button = tk.Button(root, text="Empezar", font=("Berlin Sans FB Demi", 9),bg="#6196A6", fg="#F4EDCC",command=opc_maze)
start_button.pack(pady=10)

credits_button = tk.Button(root, text="Creditos", command=creditos, font=("Berlin Sans FB Demi", 9), bg="#6196A6", fg="#F4EDCC")
credits_button.pack(pady=5)

root.mainloop()