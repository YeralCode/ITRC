import os
import csv
import re

base_path_original = os.path.expanduser("~/Documentos/ITRC/DOCUMENTOS_LIMPIAR/copia_DIAN_DISC/2024/CSV_CONVERTIDOS")
base_path_limpio = os.path.expanduser("~/Documentos/ITRC/DOCUMENTOS_LIMPIAR/copia_DIAN_DISC/2024/CSV_LIMPIO/")

lista_archivos_csv_at = [
    'ARCHIVO_DIAN_DISC_I20240101_F20240131_CONVERTIDO.csv',
    'ARCHIVO_DIAN_DISC_I20240201_F20240229_CONVERTIDO.csv',
    'ARCHIVO_DIAN_DISC_I20240301_F20240331_CONVERTIDO.csv',
    'ARCHIVO_DIAN_DISC_I20240401_F20240430_CONVERTIDO.csv',
    'ARCHIVO_DIAN_DISC_I20240501_F20240531_CONVERTIDO.csv',
    'ARCHIVO_DIAN_DISC_I20240601_F20240630_CONVERTIDO.csv',
    'ARCHIVO_DIAN_DISC_I20240701_F20240731_CONVERTIDO.csv',
    'ARCHIVO_DIAN_DISC_I20240801_F20240831_CONVERTIDO.csv',
    'ARCHIVO_DIAN_DISC_I20240901_F20240930_CONVERTIDO.csv',
    'ARCHIVO_DIAN_DISC_I20241001_F20241031_CONVERTIDO.csv',
    'ARCHIVO_DIAN_DISC_I20241101_F20241130_CONVERTIDO.csv',
    'ARCHIVO_DIAN_DISC_I20241201_F20241231_CONVERTIDO.csv',
]

# Asegurarse de que el directorio de salida exista
os.makedirs(base_path_limpio, exist_ok=True)

for nombre_archivo_csv_at in lista_archivos_csv_at:
    archivo_entrada = os.path.join(base_path_original, nombre_archivo_csv_at)
    nombre_archivo_base, _ = os.path.splitext(nombre_archivo_csv_at)
    nombre_archivo_csv_pipe = nombre_archivo_base + ".csv"
    archivo_salida = os.path.join(base_path_limpio, nombre_archivo_csv_pipe)


    if os.path.exists(archivo_entrada):
        print(f"Procesando archivo: {archivo_entrada}")
        try:
            with open(archivo_entrada, 'r', newline='', encoding='utf-8') as infile, \
                 open(archivo_salida, 'w', newline='', encoding='utf-8') as outfile:
                # Escribir la cabecera con las nuevas columnas al principio
                coincidencia_fecha = re.search(r"I(\d{8})", nombre_archivo_csv_at)

                mes_reporte = "Desconocido"
                if coincidencia_fecha:
                    fecha_str = coincidencia_fecha.group(1)
                    anio = fecha_str[:4]
                    mes = fecha_str[4:6]
                    mes_reporte = f"{mes}_{anio}"
                primera_linea = infile.readline().strip()
                cabecera = primera_linea.split('@|')
                nueva_cabecera = ['nombre_archivo', 'mes_reporte'] + cabecera
                outfile.write('|'.join(nueva_cabecera) + '\n')

                # Escribir los datos con las columnas adicionales vacías al principio
                for line in infile:
                    campos = line.strip().split('@|')
                    nueva_linea = [nombre_archivo_csv_at, mes_reporte] + campos
                    outfile.write('|'.join(nueva_linea) + '\n')
            print(f'Archivo convertido y guardado en: {archivo_salida}')
        except UnicodeDecodeError:
            print(f"Error de codificación UTF-8. Intentando con latin-1 para: {nombre_archivo_csv_at}")
            try:
                with open(archivo_entrada, 'r', newline='', encoding='latin-1') as infile_latin, \
                     open(archivo_salida, 'w', newline='', encoding='utf-8') as outfile:
                    # Escribir la cabecera con las nuevas columnas al principio
                    coincidencia_fecha = re.search(r"I(\d{8})", nombre_archivo_csv_at)

                    mes_reporte = "Desconocido"
                    if coincidencia_fecha:
                        fecha_str = coincidencia_fecha.group(1)
                        anio = fecha_str[:4]
                        mes = fecha_str[4:6]
                        mes_reporte = f"{mes}_{anio}"
                    primera_linea = infile_latin.readline().strip()
                    cabecera = primera_linea.split('@|')
                    nueva_cabecera = ['nombre_archivo', 'mes_reporte'] + cabecera
                    outfile.write('|'.join(nueva_cabecera) + '\n')

                    # Escribir los datos con las columnas adicionales vacías al principio
                    for line in infile_latin:
                        campos = line.strip().split('@|')
                        nueva_linea = [os.path.splitext(nombre_archivo_csv_at)[0], mes_reporte] + campos
                        outfile.write('|'.join(nueva_linea) + '\n')
                print(f'Archivo convertido y guardado (con latin-1) en: {archivo_salida}')
            except Exception as e_latin:
                print(f"Error al leer o convertir el archivo {nombre_archivo_csv_at} con latin-1: {e_latin}")
        except FileNotFoundError:
            print(f"Error: El archivo {nombre_archivo_csv_at} no se encontró en: {base_path_original}")
        except Exception as e:
            print(f"Error al leer o convertir el archivo {nombre_archivo_csv_at}: {e}")
    else:
        print(f"El archivo {nombre_archivo_csv_at} no existe en: {base_path_original}")

print("Proceso de conversión de archivos CSV completado.")