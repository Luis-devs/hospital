from conexion import conectarYCrear, obtenerConexion
import medico
import paciente
import historia
import cita
import json
import mysql

N_cita = 1
N_historia = 1
N_medico = 1
N_paciente = 1


def subirDatosJSON(tabla, nombreArchivo):
    con = obtenerConexion()
    cursor = con.cursor()
    try:
        archivo = open(f'./datosIniciales/{nombreArchivo}')
        datos = json.load(archivo)
        if tabla == "medicos":
            query = "INSERT INTO medico VALUES(%s, %s, %s, %s, %s, %s);"
            values = [(fila['ID'], fila['Nombre'], fila['Apellido'],
                       fila['Especialidad'], fila['Telefono'], fila['correo']) for fila in datos]
        elif tabla == "pacientes":
            query = "INSERT INTO paciente VALUES(%s, %s, %s, %s, %s, %s, %s);"
            values = [(fila['ID'], fila['Nombre'], fila['Apellido'], fila['Nacimiento'],
                       fila['Género'], fila['Dirección'], fila['Telefono']) for fila in datos]
        elif tabla == "citas":
            query = "INSERT INTO cita VALUES(%s, %s, %s, %s, %s, %s);"
            values = [(fila['ID'], fila['ID_Paciente'], fila['ID_Médico'],
                       fila['Fecha_Cita'], fila['Hora_Cita'], fila['Razón_Cita']) for fila in datos]
        else:
            query = "INSERT INTO historia VALUES(%s, %s, %s, %s, %s, %s);"
            values = [(fila['ID'], fila['ID_Paciente'], fila['Fecha_Visita'],
                       fila['Diagnóstico'], fila['Tratamiento'], fila['Notas']) for fila in datos]

        cursor.executemany(query, values)
        con.commit()
        return len(values)
    except mysql.connector.errors.IntegrityError as error:
        print(error)
        return False


def iniciarSesion(usuario, contrasena):
    return (usuario == "admin_hospital" and contrasena == "test1234*")


print("--------Bienvenido al sistema del hospital--------")
while True:
    usuario=input("Ingrese usuario: ")
    contrasena=input("Ingrese contraseña: ")
    if(iniciarSesion(usuario, contrasena)):
        break
    else:
        print("Usuario o contraseña incorrecta",end="\n")
    
    print("\n")

conectarYCrear()  # Conecta a la BD y crea las tablas
opc = ''

while opc != "s":
    opc = input(""" 
    a. Crear
    b. Consultar
    c. Editar
    d. Eliminar
    e. Subir datos por JSON
    s. SALIR
Ingrese una opción: """).lower()

    if opc == "a":
        opc = input(""" 
            a. Crear Médico
            b. Crear Paciente
            c. Crear Historia médica
            d. Crear Cita
        Ingrese una opción: """).lower()
        print('\n')
        if opc == "a":
            datos = {'nombre': None, 'apellido': None,
                     'especialidad': None, 'telefono': None, 'correo': None}
            datos["nombre"] = input("Ingrese nombre del médico: ")
            datos["apellido"] = input("Ingrese apellido del médico: ")
            datos["especialidad"] = input("Ingrese especialidad: ")
            datos["telefono"] = input("Ingrese teléfono: ")
            datos["correo"] = input("Ingrese correo: ")
            if medico.crear(datos):
                print("Médico creado correctamente\n")
            else:
                print("No se pudo crear el médico\n")
        elif opc == "b":
            datos = {'nombre': None, 'apellido': None, 'nacimiento': None,
                     'género': None, 'dirección': None, 'telefono': None}
            datos["nombre"] = input("Ingrese nombre del paciente: ")
            datos["apellido"] = input("Ingrese apellido del paciente: ")
            datos["nacimiento"] = input(
                "Ingrese fecha de nacimiento, YYYY-mm-dd: ")
            datos["género"] = input("Ingrese género, F o M: ").upper()
            datos["dirección"] = input("Ingrese dirección: ")
            datos["telefono"] = input("Ingrese teléfono: ")

            if paciente.crear(datos):
                print("Paciente creado correctamente\n")
            else:
                print("No se pudo crear el paciente\n")
        elif opc == "c":
            pacientes = paciente.obtener()
            if len(pacientes) > 0:
                datos = {
                    'id_paciente': 1,
                    'fecha_visita': None,
                    'diagnóstico': None,
                    'tratamiento': None,
                    'notas': None
                }
                print("Pacientes\n")
                for fila in pacientes:
                    print(f"ID: {fila[0]}, Nombre: {fila[1]} {fila[2]}")
                print("\n")
                datos["id_paciente"] = int(input("Ingrese ID del paciente: "))
                datos["fecha_visita"] = input(
                    "Ingrese fecha de visita, YYYY-mm-dd: ")
                datos["diagnóstico"] = input("Ingrese diagnóstico: ")
                datos["tratamiento"] = input("Ingrese tratamiento: ")
                datos["notas"] = input("Ingrese nota: ")
                if historia.crear(datos):
                    print("Historia creada correctamente\n")
                else:
                    print("No se pudo crear la historia")
            else:
                print("No hay pacientes, no se puede crear la historia médica")
        elif opc == "d":
            pacientes = paciente.obtener()
            medicos = medico.obtener()
            if (len(pacientes) > 0 and len(medicos) > 0):
                datos = {
                    'id_paciente': 1,
                    'id_médico': 1,
                    'fecha_cita': None,
                    'hora_cita': None,
                    'razón_cita': None
                }
                print("Pacientes")
                for fila in pacientes:
                    print(f"ID: {fila[0]}, Nombre: {fila[1]} {fila[2]}")
                datos['id_paciente'] = int(
                    input("Ingrese el ID del paciente: "))

                print("\nMédicos")
                for fila in medicos:
                    print(
                        f"ID: {fila[0]}, Nombre: {fila[1]} {fila[2]}, Especialidad: {fila[3]}")
                datos['id_médico'] = int(input("Ingrese el ID del médico: "))
                datos['fecha_cita'] = input(
                    "Ingrese fecha de la cita, YYYY-mm-dd: ")
                datos["hora_cita"] = input(
                    "Ingrese hora de la cita, HH:mm AM-PM: ")
                datos["razón_cita"] = input("Ingrese la razón de la cita: ")
                if cita.crear(datos):
                    print("Cita creada correctamente")
                else:
                    print("No se pudo crear la cita")
            else:
                print("No hay pacientes o médicos, no se puede crear la cita")
    elif opc == "b":
        print("\nConsultar")
        opc = input(""" 
            a. Citas por médico
            b. Citas por paciente
            c. Historias por paciente      
            d. Todos los pacientes
            e. Todos los médicos
            f. Todas las citas
            g. Todas las historias médicas
Ingrese una opción: """).lower()

        if opc == "a":
            medicos = medico.obtener()
            if len(medicos) > 0:
                print("\nMédicos")
                for fila in medicos:
                    print(
                        f"ID: {fila[0]}, Nombre: {fila[1]} {fila[2]}, Especialidad: {fila[3]}")

                id_medico = int(
                    input("Ingrese el ID del médico a consultar citas: "))
                resultado = medico.citas(id_medico)
                if len(resultado) > 0:
                    ruta = medico.guardar_resultado_cita(resultado, N_cita)
                    print(f"Resultados guardados en la ruta: Queries/{ruta}")
                    N_cita += 1
                else:
                    print("El médico no tiene citas, no se creó el archivo")
            else:
                print("No hay médicos para consultar citas")
        elif opc == "b":
            pacientes = paciente.obtener()
            if (len(pacientes) > 0):
                print("Pacientes")
                for fila in pacientes:
                    print(f"ID: {fila[0]}, Nombre: {fila[1]} {fila[2]}")

                id_paciente = int(
                    input("Ingrese ID del paciente a consultar citas: "))
                resultado = paciente.citas(id_paciente)
                if len(resultado) > 0:
                    ruta = paciente.guardar_resultado_cita(resultado, N_cita)
                    print(f"Resultados guardados en la ruta: Queries/{ruta}")
                    N_cita += 1
                else:
                    print("El paciente no tiene citas, no se creó el archivo")
            else:
                print("No hay pacientes para consultar citas")
        elif opc == "c":
            pacientes = paciente.obtener()
            if (len(pacientes) > 0):
                print("Pacientes")
                for fila in pacientes:
                    print(f"ID: {fila[0]}, Nombre: {fila[1]} {fila[2]}")

                id_paciente = int(
                    input("Ingrese ID del paciente a consultar historias médicas: "))
                resultado = paciente.historias(id_paciente)
                if len(resultado) > 0:
                    ruta = paciente.guardar_resultado_historia(
                        resultado, N_historia)
                    print(f"Resultados guardados en la ruta: Queries/{ruta}")
                    N_historia += 1
                else:
                    print(
                        "El paciente no tiene historias médicas, no se creó el archivo")
            else:
                print("No hay pacientes para consultar historias médicas")
        elif opc == "d":
            pacientes = paciente.obtener()
            if (len(pacientes) > 0):
                ruta = paciente.guardar_resultado(pacientes, N_paciente)
                print(f"Resultados guardados en la ruta: Queries/{ruta}")
                N_paciente += 1
            else:
                print("No hay pacientes registrados, no se creó el archivo")
        elif opc == "e":
            medicos = medico.obtener()
            if len(medicos) > 0:
                ruta = medico.guardar_resultado(medicos, N_medico)
                print(f"Resultados guardados en la ruta: Queries/{ruta}")
                N_medico += 1
            else:
                print("No hay médicos registrados, no se creó el archivo")
        elif opc == "f":
            citas = cita.obtener()
            if len(citas) > 0:
                ruta = cita.guardar_resultado(citas, N_cita)
                print(f"Resultados guardados en la ruta: Queries/{ruta}")
                N_cita += 1
            else:
                print("No hay citas registradas, no se creó el archivo")
        elif opc == "g":
            historias = historia.obtener()
            if len(historias) > 0:
                ruta = historia.guardar_resultado(historias, N_historia)
                print(f"Resultados guardados en la ruta: Queries/{ruta}")
                N_historia += 1
            else:
                print("No hay historias médicas registradas, no se creó el archivo")

    elif opc == "c":
        opc = input(""" 
            a. Paciente
            b. Médico
            c. Cita
            d. Historia médica
        Ingrese opción: """).lower()

        if opc == "a":
            pacientes = paciente.obtener()
            if (len(pacientes) > 0):
                print("Pacientes")
                for fila in pacientes:
                    print(f"ID: {fila[0]}, Nombre: {fila[1]} {fila[2]}")

                id_paciente = int(
                    input("Ingrese ID del paciente a editar: "))
                print(
                    "CAMPOS: nombre, apellido, nacimiento, género, dirección o telefono")
                campo = input("Ingrese nombre del campo a editar: ").lower()
                valor = input("Ingrese nuevo valor para el campo: ")
                resultado = paciente.editar(id_paciente, {campo: valor})
                if resultado:
                    print("Paciente editado correctamente")
                else:
                    print("No se pudo editar el paciente")
            else:
                print("No hay pacientes registrados")
        elif opc == "b":
            medicos = medico.obtener()
            if (len(medicos) > 0):
                print("Médicos")
                for fila in medicos:
                    print(
                        f"ID: {fila[0]}, Nombre: {fila[1]} {fila[2]}, Especialidad: {fila[3]}")

                id_medico = int(
                    input("Ingrese ID del médico a editar: "))
                print("CAMPOS: nombre, apellido, especialidad, telefono, correo")
                campo = input("Ingrese nombre del campo a editar: ").lower()
                valor = input("Ingrese nuevo valor para el campo: ")
                resultado = medico.editar(id_medico, {campo: valor})
                if resultado:
                    print("Médico editado correctamente")
                else:
                    print("No se pudo editar el médico")
            else:
                print("No hay médicos registrados")
        elif opc == "c":
            citas = cita.obtener()
            if (len(citas) > 0):
                print("Citas")
                for fila in citas:
                    print(
                        f"ID: {fila[0]}, ID_Paciente: {fila[1]}, ID_Médico: {fila[2]}")

                id_cita = int(
                    input("Ingrese ID de la cita a editar: "))
                print(
                    "CAMPOS: id_paciente, id_médico, fecha_cita, hora_cita, razón_cita")
                campo = input("Ingrese nombre del campo a editar: ").lower()
                valor = input("Ingrese nuevo valor para el campo: ")
                resultado = cita.editar(id_paciente, {campo: valor})
                if resultado:
                    print("Cita editada correctamente")
                else:
                    print("No se pudo editar la cita")
            else:
                print("No hay citas registradas")
        elif opc == "d":
            historias = historia.obtener()
            if (len(historias) > 0):
                print("Historias médicas")
                for fila in historias:
                    print(
                        f"ID: {fila[0]}, ID_Paciente: {fila[1]}, Fecha_Visita: {fila[2]}")

                id_historia = int(
                    input("Ingrese ID de la historia a editar: "))
                print(
                    "CAMPOS: id_paciente, fecha_visita, diagnóstico, tratamiento, notas")
                campo = input("Ingrese nombre del campo a editar: ").lower()
                valor = input("Ingrese nuevo valor para el campo: ")
                resultado = historia.editar(id_paciente, {campo: valor})
                if resultado:
                    print("Historia médica editada correctamente")
                else:
                    print("No se pudo editar la historia médica")
            else:
                print("No hay historias médicas registradas")
    elif opc == "d":
        opc = input(""" 
            a. Paciente
            b. Médico
            c. Cita
            d. Historia médica 
        Ingrese una opción: """).lower()

        if opc == "a":
            pacientes = paciente.obtener()
            if (len(pacientes) > 0):
                print("Pacientes")
                for fila in pacientes:
                    print(f"ID: {fila[0]}, Nombre: {fila[1]} {fila[2]}")

                id_paciente = int(
                    input("Ingrese ID del paciente a eliminar: "))
                resultado = paciente.eliminar(id_paciente)
                if resultado:
                    print("Paciente eliminado correctamente")
                else:
                    print("No se pudo eliminar el paciente")
            else:
                print("No hay pacientes registrados")
        elif opc == "b":
            medicos = medico.obtener()
            if len(medicos) > 0:
                if len(medicos) > 0:
                    print("\nMédicos")
                    for fila in medicos:
                        print(
                            f"ID: {fila[0]}, Nombre: {fila[1]} {fila[2]}, Especialidad: {fila[3]}")

                    id_medico = int(
                        input("Ingrese el ID del médico a eliminar: "))
                    resultado = medico.eliminar(id_medico)
                    if resultado:
                        print("Médico eliminado correctamente")
                    else:
                        print("No se pudo eliminar el médico")
            else:
                print("No hay médicos registrados")
        
        elif opc=="c":
            citas = cita.obtener()
            if len(citas) > 0:
                print("Citas")
                for fila in citas:
                    print(f"ID: {fila[0]}, ID_Paciente: {fila[1]}, ID_Médico: {fila[2]}, Fecha_Cita: {fila[3]}")
                
                id_cita=int(input("Ingrese ID de la cita a eliminar: "))
                resultado= cita.eliminar(id_cita)
                if resultado:
                    print("Cita eliminada correctamente")
                else:
                    print("No se pudo eliminar la cita")
            else:
                print("No hay citas registradas")        
        
        elif opc=="d":
            historias= historia.obtener()
            if len(historias)>0:
                print("Historias médicas")
                for fila in historias:
                    print(f"ID: {fila[0]}, ID_Paciente: {fila[1]}, Fecha_Visita: {fila[2]}")

                id_historia=int(input("Ingrese ID de la historia médica a eliminar: "))
                resultado= historia.eliminar(id_historia)
                if resultado:
                    print("Historia médica eliminada correctamente")
                else:
                    print("No se pudo eliminar la historia médica")
            else:
                print("No hay historias médicas registradas")
        
    elif opc == "e":
        nombreArchivo = input(
            "Ingrese nombre del archivo JSON a subir datos: ")
        tabla = nombreArchivo.split('.')
        sub = subirDatosJSON(tabla[0].lower(), nombreArchivo)
        if sub:
            print(f"{sub} registros insertados en la tabla {tabla[0]}")
        else:
            print(
                "No pudieron insertar los registros, verifique los id que no estén duplicados")
