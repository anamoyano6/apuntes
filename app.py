from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/persona'
db = SQLAlchemy(app)

class Persona(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(20), nullable=False)
    apellido = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    dni = db.Column(db.String(8), unique=True, nullable=False)
    
    def _init_(self, nombre, apellido, email, dni):
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.dni = dni
        
#Agregar una persona
@app.route('/personas', methods=['POST'])
def agregar_persona():
    data = request.get_json()
    nueva_persona = Persona(
        nombre=data['nombre'], 
        apellido=data['apellido'], 
        email=data['email'], 
        dni=data['dni']
        )
    db.session.add(nueva_persona)
    db.session.commit()
    return jsonify({'message': 'Se agrego una persona'}), 200
#Listar
@app.route('/personas', methods=['GET'])
def obtenerPersona():
    personas = Persona.query.all()
    personas_json = [{
        'nombre':persona.nombre,
        'apellido': persona.apellido,
        'email':persona.email,
        'dni': persona.dni}
        for persona in personas]
    return jsonify(personas_json), 200
 #buscar
@app.route('/personas/buscar', methods=['POST'])
def buscarPersona():
    data = request.get_json()
    dni = data.get('dni')
    if dni:
        persona = Persona.query.filter_by(dni=dni).first()
        if persona:
            persona_json = ({'nombre':persona.nombre,
                            'apellido': persona.apellido,
                            'email':persona.email,
                            'dni': persona.dni})
            return jsonify(persona_json), 200
        return jsonify({'message':'No se encontro la persona'}),404
#modificar
@app.route('/personas', methods=['PUT'])
def ModificarPersona():
    data = request.get_json()
    dni = data.get('dni')
    if dni:
        persona = Persona.query.filter_by(dni=dni).first()
        if persona:
            persona.nombre = data.get('nombre',persona.nombre)
            persona.appellido = data.get('apellido',persona.apellido)
            persona.email = data.get('email',persona.email)
            db.session.commit()
            return jsonify({'message':'Se modifico correctamente'}), 200
        return jsonify({'message':'No se encontro a la persona'}), 404
#eliminar
@app.route('/personas/<dni>', methods=['DELETE'])
def eliminarPersona(dni):
    persona = Persona.query.filter_by(dni=dni).first()
    if persona:
        db.session.delete(persona)
        db.session.commit()
        return jsonify({'message':'Se elimino correctamente'}), 200
    return jsonify({'message': 'No se encontro a la persona'}), 404


       
if __name__ == '__main__':
    with app.app_context(): 
        db.create_all()
    app.run(debug=True)