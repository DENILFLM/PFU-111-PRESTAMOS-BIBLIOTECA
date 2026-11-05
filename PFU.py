import csv

ARCHIVO_CSV = "prestamos.csv"
CAMPOS = ["codigo", "nombre", "titulo", "dias"]

#para el codigo de estudiante
PREFIJO_CODIGO = "SIS-"
DIGITOS_CODIGO = 6
DIGITOS = "0123456789"

DIAS_MIN = 1
DIAS_MAX = 30
LARGO_NOMBRE_MIN = 3
LARGO_NOMBRE_MAX = 60
LARGO_TITULO_MAX = 80

# UTILIDADES
def limpiar_texto(texto):
    return " ".join(texto.split())


def enmascarar_codigo(codigo):

    return codigo[:4] + "***" + codigo[-3:]


# VALIDACIONES
def tiene_formato_codigo(codigo):
    """Comprueba el formato SIS-123456 sin usar expresiones regulares."""
    if len(codigo) != len(PREFIJO_CODIGO) + DIGITOS_CODIGO:
        return False
    if not codigo.startswith(PREFIJO_CODIGO):
        return False
    for caracter in codigo[len(PREFIJO_CODIGO):]:
        if caracter not in DIGITOS:
            return False
    return True


def validar_codigo(codigo):
    if codigo == "":
        return False, "El código del estudiante no puede estar vacío."
    if not tiene_formato_codigo(codigo):
        return False, "Formato inválido. Use el formato SIS-123456 (SIS- y 6 dígitos)."
    return True, ""


def validar_nombre(nombre):
    if nombre == "":
        return False, "El nombre del estudiante no puede estar vacío."
    if len(nombre) < LARGO_NOMBRE_MIN or len(nombre) > LARGO_NOMBRE_MAX:
        return False, (f"El nombre debe tener entre {LARGO_NOMBRE_MIN} "
                       f"y {LARGO_NOMBRE_MAX} caracteres.")
    for caracter in nombre:
        if not (caracter.isalpha() or caracter == " "):
            return False, "El nombre solo puede contener letras y espacios."
    return True, ""


def validar_titulo(titulo):
    if titulo == "":
        return False, "El título del material no puede estar vacío."
    if len(titulo) > LARGO_TITULO_MAX:
        return False, f"El título no puede superar los {LARGO_TITULO_MAX} caracteres."
    if titulo[0] in "=+-@":
        return False, "El título no puede comenzar con los caracteres = + - @."
    return True, ""


def validar_dias(texto_dias):
    """Valida que sea un entero entre 1 y 30. Devuelve (valido, dias|mensaje)."""
    try:
        dias = int(texto_dias)
    except ValueError:
        return False, "La cantidad de días debe ser un número entero."
    if dias < DIAS_MIN or dias > DIAS_MAX:
        return False, f"La cantidad de días debe estar entre {DIAS_MIN} y {DIAS_MAX}."
    return True, dias


def es_duplicado(prestamos, codigo, titulo):
    """Un préstamo está duplicado si el mismo estudiante ya tiene el mismo material."""
    for p in prestamos:
        if p["codigo"] == codigo and p["titulo"].lower() == titulo.lower():
            return True
    return False

# PERSISTENCIA (archivo CSV)
def cargar_prestamos():
    """Lee los préstamos desde el CSV. Ignora filas dañadas o inválidas
    (el sistema legado tenía datos inconsistentes)."""
    prestamos = []
    ignoradas = 0

    try:
        with open(ARCHIVO_CSV, mode="r", newline="", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                try:
                    codigo = limpiar_texto(fila.get("codigo") or "").upper()
                    nombre = limpiar_texto(fila.get("nombre") or "")
                    titulo = limpiar_texto(fila.get("titulo") or "")
                    ok_dias, dias = validar_dias(fila.get("dias") or "")

                    if (validar_codigo(codigo)[0] and validar_nombre(nombre)[0]
                            and validar_titulo(titulo)[0] and ok_dias
                            and not es_duplicado(prestamos, codigo, titulo)):
                        prestamos.append({"codigo": codigo, "nombre": nombre,
                                          "titulo": titulo, "dias": dias})
                    else:
                        ignoradas += 1
                except (AttributeError, TypeError):
                    ignoradas += 1
    except FileNotFoundError:
        return prestamos  # primera ejecución: aún no existe el archivo
    except (OSError, csv.Error, UnicodeDecodeError) as error:
        print(f"[!] No se pudo leer el archivo '{ARCHIVO_CSV}': {error}")
        return prestamos

    if ignoradas > 0:
        print(f"[!] Se ignoraron {ignoradas} registro(s) inválidos o duplicados del archivo.")
    return prestamos


def guardar_prestamos(prestamos):
    try:
        with open(ARCHIVO_CSV, mode="w", newline="", encoding="utf-8") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=CAMPOS)
            escritor.writeheader()
            escritor.writerows(prestamos)
        return True
    except OSError as error:
        print(f"[!] No se pudo guardar el archivo: {error}")
        return False

# ENTRADA DE DATOS (repite hasta que el dato sea válido)
def pedir_codigo():
    while True:
        codigo = limpiar_texto(input("Código del estudiante (ej. SIS-123456): ")).upper()
        valido, mensaje = validar_codigo(codigo)
        if valido:
            return codigo
        print(f"  [x] {mensaje}")


def pedir_nombre():
    while True:
        nombre = limpiar_texto(input("Nombre del estudiante: "))
        valido, mensaje = validar_nombre(nombre)
        if valido:
            return nombre
        print(f"  [x] {mensaje}")


def pedir_titulo():
    while True:
        titulo = limpiar_texto(input("Título del material solicitado: "))
        valido, mensaje = validar_titulo(titulo)
        if valido:
            return titulo
        print(f"  [x] {mensaje}")


def pedir_dias():
    while True:
        texto = input(f"Cantidad de días del préstamo ({DIAS_MIN}-{DIAS_MAX}): ").strip()
        valido, resultado = validar_dias(texto)
        if valido:
            return resultado
        print(f"  [x] {resultado}")

# OPERACIONES DEL MENÚ
def registrar_prestamo(prestamos):
    print("\n--- REGISTRAR NUEVO PRÉSTAMO ---")
    try:
        codigo = pedir_codigo()
        nombre = pedir_nombre()
        titulo = pedir_titulo()

        if es_duplicado(prestamos, codigo, titulo):
            print("[x] Préstamo duplicado: ese estudiante ya tiene registrado ese material.")
            return

        dias = pedir_dias()
    except (KeyboardInterrupt, EOFError):
        print("\n[!] Registro cancelado.")
        return

    nuevo = {"codigo": codigo, "nombre": nombre, "titulo": titulo, "dias": dias}
    prestamos.append(nuevo)

    if guardar_prestamos(prestamos):
        print("[✓] Préstamo registrado y guardado correctamente.")
    else:
        prestamos.pop()  # se revierte para mantener consistencia con el archivo
        print("[x] El préstamo no se registró porque no se pudo guardar.")


def mostrar_tabla(lista):
    """Imprime los préstamos en formato tabla (con el código enmascarado)."""
    print(f"\n{'N°':<4}{'Código':<12}{'Estudiante':<28}{'Material':<32}{'Días':<5}")
    print("-" * 81)
    for i, p in enumerate(lista, start=1):
        print(f"{i:<4}{enmascarar_codigo(p['codigo']):<12}"
              f"{p['nombre'][:26]:<28}{p['titulo'][:30]:<32}{p['dias']:<5}")
    print(f"\nTotal: {len(lista)} préstamo(s).")


def consultar_prestamos(prestamos):
    print("\n--- CONSULTAR PRÉSTAMOS ---")
    if len(prestamos) == 0:
        print("No hay préstamos registrados.")
        return

    print("1. Ver todos los préstamos")
    print("2. Buscar por código de estudiante")
    opcion = input("Elija una opción: ").strip()

    if opcion == "1":
        mostrar_tabla(prestamos)
    elif opcion == "2":
        codigo = limpiar_texto(input("Código del estudiante: ")).upper()
        valido, mensaje = validar_codigo(codigo)
        if not valido:
            print(f"[x] {mensaje}")
            return
        encontrados = [p for p in prestamos if p["codigo"] == codigo]
        if len(encontrados) == 0:
            print("No se encontraron préstamos para ese código.")
        else:
            mostrar_tabla(encontrados)
    else:
        print("[x] Opción inválida.")

# OPERACIONES DEL MENÚ
def registrar_prestamo(prestamos):
    print("\n--- REGISTRAR NUEVO PRÉSTAMO ---")
    try:
        codigo = pedir_codigo()
        nombre = pedir_nombre()
        titulo = pedir_titulo()

        if es_duplicado(prestamos, codigo, titulo):
            print("[x] Préstamo duplicado: ese estudiante ya tiene registrado ese material.")
            return

        dias = pedir_dias()
    except (KeyboardInterrupt, EOFError):
        print("\n[!] Registro cancelado.")
        return

    nuevo = {"codigo": codigo, "nombre": nombre, "titulo": titulo, "dias": dias}
    prestamos.append(nuevo)

    if guardar_prestamos(prestamos):
        print("[✓] Préstamo registrado y guardado correctamente.")
    else:
        prestamos.pop()  # se revierte para mantener consistencia con el archivo
        print("[x] El préstamo no se registró porque no se pudo guardar.")


def mostrar_tabla(lista):
    """Imprime los préstamos en formato tabla (con el código enmascarado)."""
    print(f"\n{'N°':<4}{'Código':<12}{'Estudiante':<28}{'Material':<32}{'Días':<5}")
    print("-" * 81)
    for i, p in enumerate(lista, start=1):
        print(f"{i:<4}{enmascarar_codigo(p['codigo']):<12}"
              f"{p['nombre'][:26]:<28}{p['titulo'][:30]:<32}{p['dias']:<5}")
    print(f"\nTotal: {len(lista)} préstamo(s).")


def consultar_prestamos(prestamos):
    print("\n--- CONSULTAR PRÉSTAMOS")
    if len(prestamos) == 0:
        print("No hay préstamos registrados.")
        return

    print("1. Ver todos los préstamos")
    print("2. Buscar por código de estudiante")
    opcion = input("Elija una opción: ").strip()

    if opcion == "1":
        mostrar_tabla(prestamos)
    elif opcion == "2":
        codigo = limpiar_texto(input("Código del estudiante: ")).upper()
        valido, mensaje = validar_codigo(codigo)
        if not valido:
            print(f"[x] {mensaje}")
            return
        encontrados = [p for p in prestamos if p["codigo"] == codigo]
        if len(encontrados) == 0:
            print("No se encontraron préstamos para ese código.")
        else:
            mostrar_tabla(encontrados)
    else:
        print("[x] Opción inválida.")


# MENÚ PRINCIPAL
def mostrar_menu():
    print("   SISTEMA DE PRÉSTAMOS - BIBLIOTECA")
    print(f"\n\n 1. Registrar un nuevo préstamo")
    print("2. Consultar los préstamos registrados")
    print("3. Salir del programa")


def main():
    prestamos = cargar_prestamos()
    print(f"Se cargaron {len(prestamos)} préstamo(s) desde '{ARCHIVO_CSV}'.")

    while True:
        mostrar_menu()
        try:
            opcion = input("Seleccione una opción (1-3): ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n[!] Programa interrumpido. ¡Hasta luego!")
            break

        if opcion == "1":
            registrar_prestamo(prestamos)
        elif opcion == "2":
            consultar_prestamos(prestamos)
        elif opcion == "3":
            print("Saliendo del programa. ¡Hasta luego!")
            break
        else:
            print("[x] Opción inválida. Ingrese 1, 2 o 3.")


if __name__ == "__main__":
    main()



