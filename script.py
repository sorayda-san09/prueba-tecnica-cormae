import pandas as pd
import re

#archivo de entrada
df = pd.read_excel('Datos de entrada simple.xlsx', dtype={'CLABE': str})

estados = []
motivos = []

for index, row in df.iterrows():
    beneficiario = row.get('Beneficiario')
    clabe = row.get('CLABE')
    importe = row.get('Importe')
    
    error = None
    
    #beneficiario no vacío
    if pd.isna(beneficiario) or str(beneficiario).strip() == '':
        error = 'El beneficiario está vacío'
    
    #clabe
    elif pd.isna(clabe):
        error = 'La CLABE está vacía'
    else:
        # quitar espacios
        clabe_limpia = str(clabe).replace(' ', '').strip()
        if not clabe_limpia.isdigit():
            error = 'CLABE inválida: contiene caracteres no numéricos'
        elif len(clabe_limpia) != 18:
            error = f'CLABE inválida: tiene {len(clabe_limpia)} dígitos (debe tener 18)'
            
    #importe 
    if error is None:
        try:
            importe_num = float(importe)
            if importe_num <= 0:
                error = 'El importe debe ser un número positivo mayor a 0'
            else:
                partes = str(importe).split('.')
                if len(partes) > 1 and len(partes[1]) > 2:
                    error = 'El importe tiene más de 2 decimales'
        except (ValueError, TypeError):
            error = 'El importe no es un valor numérico válido'
            
    #estado
    if error:
        estados.append('inválido')
        motivos.append(error)
    else:
        estados.append('válido')
        motivos.append('')

#columnas de resultados
df['estado'] = estados
df['motivo_error'] = motivos

#archivo resultado
df.to_excel('resultado.xlsx', index=False)
print("Proceso terminado, archivo: 'resultado.xlsx' actualizado con éxito.")