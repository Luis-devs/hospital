from conexion import obtenerConexion
import json
import mysql

def crear(datos):
    con= obtenerConexion()
    query="INSERT INTO cita(id_paciente, id_médico, fecha_cita, hora_cita, razón_cita) VALUES(%s, %s, %s, %s, %s);"
    values=(datos['id_paciente'], datos['id_médico'], datos['fecha_cita'], datos['hora_cita'], datos['razón_cita'])
    cursor= con.cursor()
    cursor.execute(query, values)
    con.commit()
    cursor.close()
    return True
    
def editar(id, cambiar):
    try:
        con=obtenerConexion()
        cursor= con.cursor()
        query=f"UPDATE cita SET {list(cambiar.keys())[0]}=%s WHERE id=%s"
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
        query = "DELETE FROM cita WHERE id=%s"
        cursor.execute(query, (id,))
        con.commit()
        return True
    except mysql.connector.errors.IntegrityError as error:
        #print(error)
        return False
    
def obtener():
    con = obtenerConexion()
    cursor = con.cursor()
    query = "SELECT * FROM cita;"
    cursor.execute(query)
    resultado = cursor.fetchall()
    cursor.close()
    return resultado


def guardar_resultado(resultado, N):
    nombre_archivo = f"cita_{N}.json"
    guardar = [({
        'ID': fila[0],
        'ID_Paciente': fila[1],
        'ID_Médico': fila[2],
        'Fecha_Cita': fila[3],
        'Hora_Cita': fila[4],
        'Razón_Cita': fila[5]
    }) for fila in resultado]
    archivo = open(f'./Queries/{nombre_archivo}', 'w', encoding='utf-8')
    json.dump(guardar, archivo, indent=2, ensure_ascii=False)
    archivo.close()
    return nombre_archivo