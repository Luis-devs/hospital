from conexion import obtenerConexion
import json
import mysql

def crear(datos):
    con = obtenerConexion()
    query = "INSERT INTO medico(nombre, apellido, especialidad, telefono, correo) VALUES(%s, %s, %s, %s, %s);"
    values = (datos['nombre'], datos['apellido'],
              datos['especialidad'], datos['telefono'], datos['correo'])
    cursor = con.cursor()
    cursor.execute(query, values)
    con.commit()
    cursor.close()
    return True


def obtener():
    con = obtenerConexion()
    cursor = con.cursor()
    query = "SELECT * FROM medico;"
    cursor.execute(query)
    resultado = cursor.fetchall()
    cursor.close()
    return resultado

def editar(id, cambiar):
    try:
        con=obtenerConexion()
        cursor= con.cursor()
        query=f"UPDATE medico SET {list(cambiar.keys())[0]}=%s WHERE id=%s"
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
        query = "DELETE FROM medico WHERE id=%s"
        cursor.execute(query, (id,))
        con.commit()
        return True
    except mysql.connector.errors.IntegrityError as error:
        #print(error)
        return False
    
def citas(id_medico):
    con = obtenerConexion()
    cursor = con.cursor()
    query = "SELECT * FROM cita INNER JOIN medico ON medico.id=cita.id_médico WHERE medico.id=%s;"
    cursor.execute(query, [(id_medico)])
    resultado = cursor.fetchall()
    cursor.close()
    return resultado


def guardar_resultado(resultado, N):
    nombre_archivo = f"medico_{N}.json"
    guardar = [({
        'ID': fila[0],
        'Nombre': fila[1],
        'Apellido': fila[2],
        'Especialidad': fila[3],
        'Telefono': fila[4],
        'correo': fila[5]
    }) for fila in resultado]
    archivo = open(f'./Queries/{nombre_archivo}', 'w', encoding='utf-8')
    json.dump(guardar, archivo, indent=2, ensure_ascii=False)
    archivo.close()
    return nombre_archivo


def guardar_resultado_cita(resultado, N):
    nombre_archivo = f"cita_{N}.json"
    guardar = [({'ID': fila[0], 'ID_Paciente': fila[1], 'medico': {
        'ID': fila[6],
        'Nombre': fila[7],
        'Apellido': fila[8],
        'Especialidad': fila[9],
        'Telefono': fila[10],
        'correo': fila[11]
    },
        'Fecha_Cita': fila[3],
        'Hora_Cita': fila[4],
        'Razón_Cita': fila[5]
    }) for fila in resultado]
    archivo = open(f'./Queries/{nombre_archivo}', 'w', encoding='utf-8')
    json.dump(guardar, archivo, indent=2, ensure_ascii=False)
    archivo.close()
    return nombre_archivo
