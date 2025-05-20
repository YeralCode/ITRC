import csv
import os
import re
import unicodedata
from datetime import datetime
from valores_choice.direccion_seccional_dian import VALORES_DIRECCION_SECCIONAL, VALORES_REEMPLAZO_DIRECCION_SECCIONAL
from valores_choice.departamento import VALORES_DEPARTAMENTO, VALORES_REEMPLAZO_DEPARTAMENTO
from valores_choice.ciudad import VALORES_CIUDAD, VALORES_REEMPLAZO_CIUDAD


def limpiar_nit(valor):
    """
    Limpia un NIT eliminando caracteres no numéricos y ajustando la longitud.

    Args:
        valor: El NIT a limpiar.

    Returns:
        El NIT limpiado, o None si no es válido.
    """
    if valor is None:
        return None
    valor = str(valor).strip()
    valor = valor.replace(".000000", "")
    valor = valor.split("-")[0]  # quitar parte después del guion
    valor = re.sub(r"[^\w]", "", valor)    # Elimina no numéricos
    return valor

def validar_entero(valor):
    """Valida si un valor es un entero."""
    if valor is None:
        return False
    valor = str(valor).strip()
    return re.fullmatch(r"^-?\d+$", valor) is not None

def validar_flotante(valor):
    """Valida si un valor es un flotante."""
    if valor is None:
        return False
    valor = str(valor).strip()
    return re.fullmatch(r"^-?\d+(\.\d+)?$", valor) is not None

def validar_fecha(valor):
    """
    Valida si un valor es una fecha en formato YYYY-MM-DD o DD/MM/YYYY y la convierte a objeto date.
    """
    if valor is None:
        return None  # Retornar None en lugar de False para manejar valores nulos explícitamente
    valor = str(valor).strip()
    match_yyyy_mm_dd_hh_mm = re.fullmatch(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$", valor)
    if match_yyyy_mm_dd_hh_mm:
        try:
            dt = datetime.strptime(valor, "%Y-%m-%d %H:%M:%S")
            if dt.time().hour == 0 and dt.time().minute == 0 and dt.time().second == 0:
                valor = dt.strftime("%Y-%m-%d")  # convertir a solo fecha
        except ValueError:
            valor = str(valor).strip()
            return re.fullmatch(r"^\d{4}-\d{2}-\d{2}$", valor) is not None
    # Intenta con formato YYYY-MM-DD
    match_yyyy_mm_dd = re.fullmatch(r"^\d{4}-\d{2}-\d{2}$", valor)
    if match_yyyy_mm_dd:
        try:
            fecha_obj = datetime.strptime(valor, "%Y-%m-%d").date()
            return fecha_obj.strftime("%Y-%m-%d")
        except ValueError:
            return False  # No es una fecha válida en este formato, probar el siguiente

    # Intenta con formato DD/MM/YYYY
    match_dd_mm_yyyy = re.fullmatch(r"^\d{1,2}/\d{2}/\d{4}$", valor)
    if match_dd_mm_yyyy:
        try:
            fecha_obj =  datetime.strptime(valor, "%d/%m/%Y").date()
            return fecha_obj.strftime("%Y-%m-%d")
        except ValueError:
            return False  # No es una fecha válida en este formato
    match_dd_mm_yyyy_dos = re.match(r"^(\d{1,2}/\d{2}/\d{4})(?: - \d{1,2}/\d{2}/\d{4})?$", valor)
    if match_dd_mm_yyyy_dos:
        try:
            fecha_obj =  datetime.strptime(match_dd_mm_yyyy_dos.group(1), "%d/%m/%Y").date()
            return fecha_obj.strftime("%Y-%m-%d")
        except ValueError:
            return False  # No es una fecha válida en este formato
    match_dd_mm_yyyy_dos = re.match(r"^(\d{1,2}/\d{2}/\d{4})(?: - \d{1,2}/\d{2}/\d{4})?$", valor)
    if match_dd_mm_yyyy_dos:
        try:
            fecha_obj =  datetime.strptime(match_dd_mm_yyyy_dos.group(1), "%d/%m/%Y").date()
            return fecha_obj.strftime("%Y-%m-%d")
        except ValueError:
            return False
    match_yyyy_mm_dd_dos = re.match(r"^(\d{4}-\d{2}-\d{2})(?: - \d{4}-\d{2}-\d{2})?$", valor)
    if match_yyyy_mm_dd_dos:
        try:
            fecha_obj = datetime.strptime(match_yyyy_mm_dd_dos.group(1), "%Y-%m-%d").date()
            return fecha_obj.strftime("%Y-%m-%d")  # Retornar en formato %Y-%m-%d
        except ValueError:
            return False
    return False # Retorna False si no coincide con ninguno de los formatos

def validar_fecha_dd_mm_yyyy(valor):
    """Valida si un valor es una fecha en formato YYYY-MM-DD."""
    if valor is None:
        return False
    valor = str(valor).strip()
    return re.fullmatch(r"^\d{2}/\d{2}/\d{4}$", valor) is not None

def validar_fecha_hora(valor):
    """Valida si un valor es una fecha y hora en formato YYYY-MM-DD HH:MM."""
    if valor is None:
        return False

    valor = str(valor).strip()

    # Intenta parsear el valor como datetime
    try:
        dt = datetime.strptime(valor, "%Y-%m-%d %H:%M:%S")
        if dt.time().hour == 0 and dt.time().minute == 0 and dt.time().second == 0:
            valor = dt.strftime("%Y-%m-%d")  # convertir a solo fecha
    except ValueError:
        valor = str(valor).strip()
        return re.fullmatch(r"^\d{4}-\d{2}-\d{2}$", valor) is not None


    return valor

def validar_cadena(valor):
    """Valida si un valor es una cadena (siempre es verdadero, pero limpia espacios)."""
    if valor is None:
        return True #consideramos nulo como cadena vacia
    return True
def validar_cadena_caracteres_especiales(valor):
    """
    Valida si un valor es una cadena.
    - Si es None, retorna True.
    - Si es cadena, remueve espacios y normaliza caracteres especiales (acentos, tildes, etc.).
    """
    if valor is None:
        return True  # Consideramos nulo como cadena vacía

    # Eliminar espacios al inicio y final
    valor = valor.strip()

    # Normalizar la cadena para eliminar acentos y caracteres especiales
    valor = unicodedata.normalize('NFKD', valor).encode('ASCII', 'ignore').decode('ASCII')
    valor = valor.replace('.', '').replace(',', '')

    # Puedes retornar el valor limpio si necesitas procesarlo más adelante
    return valor

def validar_direccion_seccional(valor):
    """
    Valida si un valor corresponde a una dirección seccional válida.
    Retorna True si es válido, False en caso contrario.
    """
    if valor is None:
        return True  # Se permite None aquí
    if '-' in valor:
        valor = valor.split('-', 1)[1]
    valor_normalizado = validar_cadena_caracteres_especiales(valor).lower()
    if "direccion seccional de impuestos  y aduanas de " in valor_normalizado:
        valor_normalizado = valor_normalizado.replace("direccion seccional de impuestos  y aduanas de", "direccion seccional de impuestos y aduanas de")
    if "direccion seccional de impuestos  de " in valor_normalizado:
        valor_normalizado = valor_normalizado.replace("direccion seccional de impuestos  de ", "direccion seccional de impuestos de ")
    if "direccion seccionalde aduanas de" in valor_normalizado:
        valor_normalizado = valor_normalizado.replace("direccion seccionalde aduanas de", "direccion seccional de aduanas de")
    if "direccion seccional de impuests y aduanas de" in valor_normalizado:
        valor_normalizado = valor_normalizado.replace("direccion seccional de impuests y aduanas de", "direccion seccional de impuestos y aduanas de")
    valor_normalizado = VALORES_REEMPLAZO_DIRECCION_SECCIONAL.get(valor_normalizado, valor_normalizado)
    if not valor_normalizado in VALORES_DIRECCION_SECCIONAL:
        # breakpoint()
        return False
    else:
        return valor_normalizado

def validar_departamento(valor):
    """
    Valida si un valor corresponde a una dirección seccional válida.
    Retorna True si es válido, False en caso contrario.
    """
    if valor is None:
        return True  # Se permite None aquí

    valor_normalizado = validar_cadena_caracteres_especiales(valor).upper()
    valor_normalizado = VALORES_REEMPLAZO_DEPARTAMENTO.get(valor_normalizado, valor_normalizado)
    if not valor_normalizado in VALORES_DEPARTAMENTO:
        return False
    else:
        return valor_normalizado
def validar_ciudad(valor):
    """
    Valida si un valor corresponde a una dirección seccional válida.
    Retorna True si es válido, False en caso contrario.
    """
    if valor is None:
        return True  # Se permite None aquí

    valor_normalizado = validar_cadena_caracteres_especiales(valor).upper()
    valor_normalizado = VALORES_REEMPLAZO_CIUDAD.get(valor_normalizado, valor_normalizado)
    if not valor_normalizado in VALORES_CIUDAD:
        return False
    else:
        return valor_normalizado

def validar_expediente(valor):
    patron = r'^\d{3}-\d{3}-\d{4}-\d+$'
    return bool(re.match(patron, valor))



def procesar_csv(archivo_entrada, archivo_salida, archivo_errores, tipos_por_posicion):
    """
    Procesa un archivo CSV, valida los tipos de datos y guarda los datos limpios y los errores.

    Args:
        archivo_entrada: Ruta del archivo CSV de entrada.
        archivo_salida: Ruta del archivo CSV de salida para los datos limpios.
        archivo_errores: Ruta del archivo CSV para guardar los errores.
        tipos_por_posicion: Diccionario que mapea las posiciones de las columnas a los tipos de datos.
    """
    errores = []
    filas_procesadas = []
    nombre_archivo = os.path.splitext(os.path.basename(archivo_entrada))[0]

    # Extraer "mes año" del nombre del archivo


    with open(archivo_entrada, 'r', encoding='utf-8') as archivo_csv:
        lector_csv = csv.reader(archivo_csv, delimiter='|')
        encabezado = next(lector_csv)# Leer el encabezado
        print(f"Archivo leído exitosamente. Número de columnas: {len(encabezado)}")
        print(f"Primeras columnas: {encabezado[:5]} ...")

        for num_fila, fila in enumerate(lector_csv, start=1):  # Iterar sobre las filas
            fila_procesada = []
            if len(fila) != len(encabezado):
                errores.append({
                    "fila": num_fila,
                    "error": "Número de columnas en la fila no coincide con el encabezado",
                    "valor": fila
                })
                continue  # Saltar la fila si el número de columnas no coincide
            for num_col, valor in enumerate(fila):
                col_name = encabezado[num_col]
                tipo_esperado = None
                for tipo, posiciones in tipos_por_posicion.items():
                    if num_col in posiciones:
                        tipo_esperado = tipo
                        break
                if tipo_esperado is None:
                    tipo_esperado = "str" #si no esta en la lista se trata como str
                valor_original = valor
                valor = valor.replace("$null$", "").replace("nan", "").replace(
                    "NULL", "").replace("N.A", "").replace("N.A.", "")
                if tipo_esperado == "int" and valor != "":
                    valor = str(valor).replace(".0", "")
                    if validar_entero(valor):
                        valor_procesado = int(valor)
                    else:
                        errores.append({
                            "columna": col_name,
                            "numero_columna":num_col,
                            "tipo": "int",
                            "valor": valor_original,
                            "fila": num_fila,
                            "error": "No es un entero válido"
                        })
                        valor_procesado = 0
                        break
                elif tipo_esperado == "float" and valor != "":
                    if "." not in valor and validar_entero(valor):
                        valor = str(valor) + ".0"
                    if validar_flotante(valor):
                        valor_procesado = float(valor)
                    else:
                        errores.append({
                            "columna": col_name,
                            "numero_columna":num_col,
                            "tipo": "float",
                            "valor": valor_original,
                            "fila": num_fila,
                            "error": "No es un flotante válido"
                        })
                        valor_procesado = 0.0
                        break
                elif tipo_esperado == "date" and valor != "":
                    if validar_fecha(valor):
                        valor_procesado = valor  # Ya está en formato YYYY-MM-DD
                    else:
                        errores.append({
                            "columna": col_name,
                            "numero_columna":num_col,
                            "tipo": "date",
                            "valor": valor_original,
                            "fila": num_fila,
                            "error": "No es una fecha válida (YYYY-MM-DD)"
                        })
                        valor_procesado = True
                        break
                elif tipo_esperado == "date-dd-mm-yyyy" and valor != "":
                    if validar_fecha_dd_mm_yyyy(valor):
                        valor_procesado = valor  # Ya está en formato YYYY-MM-DD
                    else:
                        errores.append({
                            "columna": col_name,
                            "numero_columna":num_col,
                            "tipo": "date",
                            "valor": valor_original,
                            "fila": num_fila,
                            "error": "No es una fecha válida (YYYY-MM-DD)"
                        })
                        valor_procesado = True
                        break
                elif tipo_esperado == "datetime" and valor != "":
                    valor = validar_fecha_hora(valor)
                    if valor is False:
                        errores.append({
                            "columna": col_name,
                            "numero_columna":num_col,
                            "tipo": "datetime",
                            "valor": valor_original,
                            "fila": num_fila,
                            "error": "No es una fecha y hora válida (YYYY-MM-DD HH:MM)"
                        })
                        valor_procesado = True
                        break
                    else:
                        valor_procesado = valor #ya esta en el formato
                        
                elif tipo_esperado == "nit":
                    valor_procesado = limpiar_nit(valor)
                    if valor_procesado is None:
                            errores.append({
                            "columna": col_name,
                            "numero_columna":num_col,
                            "tipo": "nit",
                            "valor": valor_original,
                            "fila": num_fila,
                    
                            "error": "No es un NIT válido"
                        })
                            valor_procesado = True
                            break
                elif tipo_esperado == "choice_direccion_seccional" and valor != "":
                    valor = validar_direccion_seccional(valor)
                    if valor is False:
                        errores.append({
                            "columna": col_name,
                            "numero_columna":num_col,
                            "tipo": "choice",
                            "valor": valor_original,
                            "fila": num_fila,
                            "error": "No se encuentra en direccion seccional"
                        })
                        valor_procesado = True
                        break
                    else:
                        valor_procesado = valor #ya esta en el formato
                elif tipo_esperado == "choice_departamento" and valor != "":
                    valor = validar_departamento(valor)
                    if valor is False:
                        errores.append({
                            "columna": col_name,
                            "numero_columna":num_col,
                            "tipo": "choice",
                            "valor": valor_original,
                            "fila": num_fila,
                            "error": "No se encuentra en Departamento"
                        })
                        valor_procesado = True
                        break
                    else:
                        valor_procesado = valor #ya esta en el formato
                        
                elif tipo_esperado == "choice_ciudad" and valor != "":
                    valor = validar_ciudad(valor)
                    if valor is False:
                        errores.append({
                            "columna": col_name,
                            "numero_columna":num_col,
                            "tipo": "choice",
                            "valor": valor_original,
                            "fila": num_fila,
                            "error": "No se encuentra en macroproceso"
                        })
                        valor_procesado = True
                        break
                    else:
                        valor_procesado = valor #ya esta en el formato
                elif tipo_esperado == "expediente" and valor != "":
                    valor = validar_expediente(valor)
                    if valor is False:
                        errores.append({
                            "columna": col_name,
                            "numero_columna":num_col,
                            "tipo": "choice",
                            "valor": valor_original,
                            "fila": num_fila,
                            "error": "no cumple como un expediente "
                        })
                        valor_procesado = True
                        break
                    else:
                        valor_procesado = valor_original
                elif tipo_esperado == "str":
                    valor_procesado = str(valor).strip()
                elif tipo_esperado == "str-sin-caracteres-especiales":
                    valor_procesado = validar_cadena_caracteres_especiales(valor)
                else:
                    valor_procesado = str(valor).strip()

                fila_procesada.append(valor_procesado)
            filas_procesadas.append(fila_procesada)

        # Guardar archivo limpio
        # if not errores: # Solo guardar si no hay errores
        print(f"Guardando archivo limpio como '{archivo_salida}'...")
        try:
            with open(archivo_salida, 'w', newline='', encoding='utf-8') as archivo_csv_limpio:
                escritor_csv = csv.writer(archivo_csv_limpio, delimiter='|')
                escritor_csv.writerow(encabezado)
                escritor_csv.writerows(filas_procesadas)
            print("✅ Archivo limpio guardado.")
        except Exception as e:
            print(f"❌ Error al guardar el archivo limpio: {e}")
            errores.append({"archivo": archivo_salida, "error": str(e), "tipo": "escritura"})
        # else:
        #     print("No se guardó el archivo limpio debido a errores.")

        # Guardar errores
        if errores:
            print(f"⚠️ Se encontraron {len(errores)} errores. Guardando en '{archivo_errores}'...")
            try:
                with open(archivo_errores, 'w', newline='', encoding='utf-8') as archivo_csv_errores:
                    escritor_csv_errores = csv.DictWriter(archivo_csv_errores, fieldnames=errores[0].keys())
                    escritor_csv_errores.writeheader()
                    escritor_csv_errores.writerows(errores)
                print("📝 Archivo de errores guardado.")
            except Exception as e:
                print(f"❌ Error al guardar el archivo de errores: {e}")
                print("  Errores encontrados:")
                for error in errores:
                    print(f"    - {error}")
        else:
            print("🎉 No se encontraron errores durante el procesamiento.")

if __name__ == "__main__":
    # Rutas de los archivos
    archivo_entrada = "consolidado_final_disciplinario_Ene_Dic_2022.csv"  # Reemplaza con tu archivo de entrada
    base_path = os.path.expanduser("~/Documentos/ITRC/DOCUMENTOS_LIMPIAR/copia_DIAN_DISC/2022/CSV_LIMPIO/")
    archivo_entrada = os.path.join(base_path, archivo_entrada)
    archivo_salida = os.path.join(base_path, "consolidado_final_disciplinario_Ene_Dic_2022_procesado.csv")
    archivo_errores = os.path.join(base_path, "errores_procesamiento.csv")

    # Mapeo de tipos de datos por posición de columna
    tipos_por_posicion = {
    "int": [],
    "float": [],
    "date": [3, 4, 5, 6,32, 33, 34, 35],
    "datetime": [],
    "str": [0, 1, 7, 12, 13, 15, 16, 17, 18, 21, 22, 23, 24, 25, 26, 27,
            28, 29, 30, 31, 35, 36, 37, 38, 39, 40, 41],
    "str-sin-caracteres-especiales": [
        14
    ],
    "nit": [
        8
    ],
    "choice_departamento": [
        9,
    ],
    "choice_ciudad": [
        10,
    ],
    "choice_direccion_seccional": [
        11,
    ],
    "expediente": [
        2,
    ]
}

    procesar_csv(archivo_entrada, archivo_salida, archivo_errores, tipos_por_posicion)



