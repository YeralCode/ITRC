import csv
import os
def txt_to_csv(filenames, base_path, input_separator="|", output_separator="|"):
    """
    Convierte múltiples archivos TXT a CSV, usando pipe "|" como separador en ambos.
    
    Args:
        filenames (list): Lista de nombres de archivos a convertir
        base_path (str): Ruta base donde se encuentran los archivos
        input_separator (str): Separador en los archivos TXT (por defecto "|")
        output_separator (str): Separador para el CSV resultante (por defecto "|")
    """
    
    for filename in filenames:
        # Construir rutas completas
        input_path = os.path.join(base_path, filename)
        output_filename = filename.replace('.txt', '_CONVERTIDO.csv')
        output_path = os.path.join(base_path, output_filename)
        
        try:
            with open(input_path, 'r', encoding='utf-8') as txt_file:
                lines = txt_file.readlines()
                
                if not lines:
                    print(f"Archivo vacío: {filename}")
                    continue
                
                with open(output_path, 'w', newline='', encoding='utf-8') as csv_file:
                    # Configurar escritor CSV con pipe como delimitador
                    writer = csv.writer(csv_file, delimiter=output_separator)
                    
                    for line in lines:
                        line = line.strip()
                        if not line:
                            continue
                        
                        # Dividir usando el separador de entrada
                        row = [field.strip() for field in line.split(input_separator)]
                        writer.writerow(row)
            
            print(f"Conversión completada: {filename} -> {output_filename}")
        
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo {input_path}")
        except Exception as e:
            print(f"Error en {filename}: {str(e)}")

# Lista de archivos a procesar
filenames = [
    'ARCHIVO_DIAN_DISC_I20240101_F20240131.txt',
    'ARCHIVO_DIAN_DISC_I20240201_F20240229.txt',
    'ARCHIVO_DIAN_DISC_I20240301_F20240331.txt',
    'ARCHIVO_DIAN_DISC_I20240401_F20240430.txt',
    'ARCHIVO_DIAN_DISC_I20240501_20240531.txt',
    'ARCHIVO_DIAN_DISC_I20240601_F20240630.txt',
    'ARCHIVO_DIAN_DISC_I20240701_F20240731.txt',
    'ARCHIVO_DIAN_DISC_I20240801_F20240831.txt',
    'ARCHIVO_DIAN_DISC_I20240901_F20240930.txt',
    'ARCHIVO_DIAN_DISC_I20241001_F20241031.txt',
    'ARCHIVO_DIAN_DISC_I20241101_F20241130.txt',
    'ARCHIVO_DIAN_DISC_I20241201_20241231.txt',
]

# Ruta base donde están los archivos
base_path = os.path.expanduser("~/Documentos/ITRC/DOCUMENTOS_LIMPIAR/copia_DIAN_DISC/2024/")

# Verificar si la ruta existe
if not os.path.exists(base_path):
    print(f"Error: La ruta {base_path} no existe")
else:
    # Ejecutar conversión con el separador correcto
    txt_to_csv(filenames, base_path, input_separator="|", output_separator="|")