from conexion import obtenerConexion
import json
import mysql
 
def crear(datos):
    con= obtenerConexion()
    query="INSERT INTO historia(id_paciente, fecha_visita, diagnóstico, tratamiento, notas) VALUES(%s, %s, %s, %s, %s);"
    values=(datos['id_paciente'], datos['fecha_visita'], datos['diagnóstico'], datos['tratamiento'], datos['notas'])
    cursor= con.cursor()
    cursor.execute(query, values)
    con.commit()
    cursor.close()
    return True
    
def obtener():
    con = obtenerConexion()
    cursor = con.cursor()
    query = "SELECT * FROM historia;"
    cursor.execute(query)
    resultado = cursor.fetchall()
    cursor.close()
    return resultado

def editar(id, cambiar):
    try:
        con=obtenerConexion()
        cursor= con.cursor()
        query=f"UPDATE historia SET {list(cambiar.keys())[0]}=%s WHERE id=%s"
        values=(list(cambiar.values())[0], id)
        cursor.execute(query, values)
        con.commit()
        return True
    except mysql.connector.errors.IntegrityError as error:
        print(error)
        return False 

def eliminar(id):
    try:
        con = obtenerConexion()
        cursor = con.cursor()
        query = "DELETE FROM historia WHERE id=%s"
        cursor.execute(query, (id,))
        con.commit()
        return True
    except mysql.connector.errors.IntegrityError as error:
        #print(error)
        return False
    
def guardar_resultado(resultado, N):
    nombre_archivo = f"historia_{N}.json"
    guardar = [({
        'ID': fila[0],
        'ID_Paciente': fila[1],
        'Fecha_Visita': fila[2],
        'Diagnóstico': fila[3],
        'Tratamiento': fila[4],
        'Notas': fila[5]
    }) for fila in resultado]
    archivo = open(f'./Queries/{nombre_archivo}', 'w', encoding='utf-8')
    json.dump(guardar, archivo, indent=2, ensure_ascii=False)
    archivo.close()
    return nombre_archivo


    