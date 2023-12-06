import pandas as pd

# Lee los datos del archivo Excel
df = pd.read_excel('lista.xlsx', skiprows=1, nrows=229)
df = df.rename(columns={df.columns[19]: 'T'})
nombre = df.rename(columns={df.columns[21]: 'V'})
nombre2 = df.rename(columns={df.columns[15]: 'P'})
nombre3 = df.rename(columns={df.columns[45]: 'AT'})
nombre4 = df.rename(columns={df.columns[47]: 'AV'})
nombre5 = df.rename(columns={df.columns[5]: 'F'})
nombre6 = df.rename(columns={df.columns[49]: 'AX'})
print(nombre6['AX'])

nombre_archivo = 'uwu.txt'
with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
    archivo.write("INSERT INTO `app_listas_plegables` (`id`, `codigos_grupo_investigacion`, `nombre_grupo_investigacion`, `redes_conocimiento`, `subareas_conocimiento`, `diciplina_subarea`,  `nombre_centro_formacion`, `actividades_economicas`) VALUES\n")
    contador = 0

    # Itera a través de los elementos de las columnas 'T' y 'V'
    for dato, dato1, dato2, dato3, dato4, dato5, dato6 in zip(df['T'], nombre['V'], nombre2['P'], nombre3['AT'], nombre4['AV'], nombre5['F'], nombre6['AX']):
        contador += 1
        # Reemplaza el valor 'NaN' por 'Null' en 'dato2' si es necesario
        if pd.isna(dato):
            dato = ''
        if pd.isna(dato1):
            dato1 = ''
        if pd.isna(dato2):
            dato2 = ''
        if pd.isna(dato3):
            dato3 = ''
        if pd.isna(dato5):
            dato5 = ''
        if pd.isna(dato6):
            dato6 = ''
        # Formatea cada par de elementos y escríbelos en el archivo
        dato_formateado = f"({contador}, '{dato}', '{dato1}', '{dato2}', '{dato3}', '{dato4}', '{dato5}', '{dato6}'),\n"
        archivo.write(dato_formateado)

print("Datos agregados al archivo uwu.txt con éxito.")