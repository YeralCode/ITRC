import pandas as pd
import os

# Lista de archivos CSV a combinar
filenames = [
    'cconsolidado_final_defensoria_Ene_Dic_2023_procesado.csv',
    'consolidado_final_defensoria_Ene_Dic_2021_procesado.csv',
    'consolidado_final_defensoria_Ene_Dic_2024_procesado.csv',
    'consolidado_final_defensoria_Ene-Feb_2025_procesado.csv',
    'consolidado_final_defensoria_Feb_Nov_2022_procesado.csv',

]

# Ruta base donde están los archivos
base_path = os.path.expanduser("~/Documentos/ITRC/DOCUMENTOS_LIMPIAR/copia_DIAN_DEFENSORIA/")

# Función para limpiar valores tipo '123.0' -> '123'
def clean_value(val):
    if isinstance(val, str) and val.endswith('.0'):
        return val[:-2]
    return val

# Inicializar lista de DataFrames
dataframes = []

# Procesar cada archivo
for filename in filenames:
    file_path = os.path.join(base_path, filename)
    if not os.path.isfile(file_path):
        print(f"⚠️ Archivo no encontrado: {file_path}")
        continue
    try:
        df = pd.read_csv(file_path, delimiter='|', dtype=str)
        df = df.applymap(clean_value)
        dataframes.append(df)
        print(f"📥 Cargado: {filename} ({df.shape[0]} filas)")
    except Exception as e:
        print(f"❌ Error al leer {filename}: {e}")

# Verificar si hay data para concatenar
if not dataframes:
    print("❗ No se cargó ningún archivo válido. Proceso cancelado.")
else:
    combined_df = pd.concat(dataframes, ignore_index=True)
    output_file = os.path.join(base_path, "consolidado_final_disciplinario_2021_2025_Feb.csv")
    combined_df.to_csv(output_file, sep='|', index=False)
    print(f"✅ Consolidado generado con éxito en: {output_file} ({combined_df.shape[0]} filas)")

