from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Configuración de MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'tu_usuario'
app.config['MYSQL_PASSWORD'] = 'tu_contraseña'
app.config['MYSQL_DB'] = 'monitoreo_salud'

mysql = MySQL(app)

# Configuración de JWT
app.config['JWT_SECRET_KEY'] = 'tu_clave_secreta'
jwt = JWTManager(app)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    nombre = data['nombre']
    email = data['email']
    password = generate_password_hash(data['password'])

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)", (nombre, email, password))
    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "Usuario registrado exitosamente"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM usuarios WHERE email = %s", [email])
    user = cur.fetchone()
    cur.close()

    if user and check_password_hash(user[3], password):
        access_token = create_access_token(identity=user[0])
        return jsonify(access_token=access_token)
    else:
        return jsonify({"message": "Credenciales inválidas"}), 401

@app.route('/data', methods=['POST'])
@jwt_required()
def add_data():
    data = request.get_json()
    frecuencia_cardiaca = data['frecuencia_cardiaca']
    tension_arterial = data['tension_arterial']
    respiracion = data['respiracion']
    usuario_id = get_jwt_identity()

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO datos_salud (usuario_id, frecuencia_cardiaca, tension_arterial, respiracion) VALUES (%s, %s, %s, %s)",
                (usuario_id, frecuencia_cardiaca, tension_arterial, respiracion))
    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "Datos guardados exitosamente"}), 201

@app.route('/data', methods=['GET'])
@jwt_required()
def get_data():
    usuario_id = get_jwt_identity()

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM datos_salud WHERE usuario_id = %s", [usuario_id])
    data = cur.fetchall()
    cur.close()

    result = []
    for row in data:
        result.append({
            "id": row[0],
            "frecuencia_cardiaca": row[2],
            "tension_arterial": row[3],
            "respiracion": row[4],
            "timestamp": row[5]
        })

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
