from conexion import obtenerConexion
import json
import mysql


def crear(datos):
    con = obtenerConexion()
    query = "INSERT INTO paciente(nombre, apellido, nacimiento, género, dirección, telefono) VALUES(%s, %s, %s, %s, %s, %s);"
    values = (datos['nombre'], datos['apellido'], datos['nacimiento'],
              datos['género'], datos['dirección'], datos['telefono'])
    cursor = con.cursor()
    cursor.execute(query, values)
    con.commit()
    cursor.close()
    return True


def obtener():
    con = obtenerConexion()
    cursor = con.cursor()
    query = "SELECT * FROM paciente;"
    cursor.execute(query)
    resultado = cursor.fetchall()
    cursor.close()
    return resultado


def editar(id, cambiar):
    try:
        con = obtenerConexion()
        cursor = con.cursor()
        query = f"UPDATE paciente SET {list(cambiar.keys())[0]}=%s WHERE id=%s"
        values = (list(cambiar.values())[0], id)
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
        query = "DELETE FROM paciente WHERE id=%s"
        cursor.execute(query, (id,))
        con.commit()
        return True
    except mysql.connector.errors.IntegrityError as error:
        #print(error)
        return False


def citas(id_paciente):
    con = obtenerConexion()
    cursor = con.cursor()
    query = "SELECT * FROM cita INNER JOIN paciente ON paciente.id=cita.id_paciente WHERE paciente.id=%s;"
    cursor.execute(query, [(id_paciente)])
    resultado = cursor.fetchall()
    cursor.close()
    return resultado


def historias(id_paciente):
    con = obtenerConexion()
    cursor = con.cursor()
    query = "SELECT * FROM historia INNER JOIN paciente ON paciente.id=historia.id_paciente WHERE paciente.id=%s;"
    cursor.execute(query, [(id_paciente)])
    resultado = cursor.fetchall()
    cursor.close()
    return resultado


def guardar_resultado(resultado, N):
    nombre_archivo = f"paciente_{N}.json"
    guardar = [({'ID': fila[0],
                 'Nombre': fila[1],
                 'Apellido': fila[2],
                 'Nacimiento': fila[3],
                 'Género': fila[4],
                 'Dirección': fila[5],
                 'Telefono': fila[6]
                 }) for fila in resultado]
    archivo = open(f'./Queries/{nombre_archivo}', 'w', encoding='utf-8')
    json.dump(guardar, archivo, indent=2, ensure_ascii=False)
    archivo.close()
    return nombre_archivo


def guardar_resultado_cita(resultado, N):
    nombre_archivo = f"cita_{N}.json"
    guardar = [({'ID': fila[0], 'ID_Paciente': fila[1], 'ID_Médico': fila[2], 'paciente': {
        'ID': fila[6],
        'Nombre': fila[7],
        'Apellido': fila[8],
        'Nacimiento': fila[9],
        'Género': fila[10],
        'Dirección': fila[11],
        'Telefono': fila[12]
    },
        'Fecha_Cita': fila[3],
        'Hora_Cita': fila[4],
        'Razón_Cita': fila[5]
    }) for fila in resultado]
    archivo = open(f'./Queries/{nombre_archivo}', 'w', encoding='utf-8')
    json.dump(guardar, archivo, indent=2, ensure_ascii=False)
    archivo.close()
    return nombre_archivo


def guardar_resultado_historia(resultado, N):
    print(resultado)
    nombre_archivo = f"historia_{N}.json"
    guardar = [({'ID': fila[0], 'ID_Paciente': fila[1], 'paciente': {
        'ID': fila[6],
        'Nombre': fila[7],
        'Apellido': fila[8],
        'Nacimiento': fila[9],
        'Género': fila[10],
        'Dirección': fila[11],
        'Telefono': fila[12]
    },
        'Fecha_Visita': fila[2],
        'Diagnóstico': fila[3],
        'Tratamiento': fila[4],
        'Notas': fila[5]
    }) for fila in resultado]
    archivo = open(f'./Queries/{nombre_archivo}', 'w', encoding='utf-8')
    json.dump(guardar, archivo, indent=2, ensure_ascii=False)
    archivo.close()
    return nombre_archivo
