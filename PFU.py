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
