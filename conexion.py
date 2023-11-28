import mysql.connector as mysql
config={
    'host':'localhost',
    'user':'admin',
    'password':'bio4100',
    'database':'general_hospital'
}
query=""" 
        CREATE TABLE IF NOT EXISTS medico(id INT(11) PRIMARY KEY AUTO_INCREMENT,
        nombre VARCHAR(60) NOT NULL, 
        apellido VARCHAR(60) NOT NULL,
        especialidad VARCHAR(45) NOT NULL,
        telefono VARCHAR(20) NOT NULL,
        correo VARCHAR(50) NOT NULL
        );

        CREATE TABLE IF NOT EXISTS paciente(id INT(11) PRIMARY KEY AUTO_INCREMENT,
            nombre VARCHAR(60) NOT NULL,
            apellido VARCHAR(60) NOT NULL,
            nacimiento VARCHAR(12) NOT NULL,
            género VARCHAR(2) NOT NULL,
            dirección VARCHAR(80) NOT NULL,
            telefono VARCHAR(20) NOT NULL
        );
        
        CREATE TABLE IF NOT EXISTS historia(id INT(11) PRIMARY KEY AUTO_INCREMENT,
            id_paciente INT(11) NOT NULL,
            fecha_visita VARCHAR(12) NOT NULL,
            diagnóstico TEXT NOT NULL,
            tratamiento TEXT NOT NULL,
            notas TEXT NOT NULL,
            FOREIGN KEY(id_paciente) REFERENCES paciente(id)
        );
        
        CREATE TABLE IF NOT EXISTS cita(id INT(11) PRIMARY KEY AUTO_INCREMENT,
            id_paciente INT(11) NOT NULL,
            id_médico INT(11) NOT NULL,
            fecha_cita VARCHAR(12) NOT NULL,
            hora_cita VARCHAR(10) NOT NULL,
            razón_cita TEXT NOT NULL,
            FOREIGN KEY(id_paciente) REFERENCES paciente(id),
            FOREIGN KEY(id_médico) REFERENCES medico(id)
        );
    """
    
def conectarYCrear():
    try:
        connection=  mysql.connect(**config)
        if connection.is_connected():
            cursor= connection.cursor()
            cursor.execute(query)
    except mysql.Error as e:
        print(f"Error: {e}")
        
def obtenerConexion():
    return mysql.connect(**config)