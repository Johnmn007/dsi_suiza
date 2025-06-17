from flask import Flask, render_template, request, redirect
import os
from werkzeug.security import generate_password_hash, check_password_hash
from config import DevelopmentConfig, TestingConfig, ProductionConfig
from extensions import db  # Importa la instancia
from models import LoginNot  # Importa tu modelo

app = Flask(__name__)

# Cargar configuración según entorno
env = os.getenv('FLASK_ENV')

if env == 'production':
    app.config.from_object(ProductionConfig)
elif env == 'testing':
    app.config.from_object(TestingConfig)
else:
    app.config.from_object(DevelopmentConfig)

# Inicializar extensiones
db.init_app(app)

# Si usarás create_all, añade esto opcionalmente:
with app.app_context():
    db.create_all()


# Lista de preguntas
preguntas = [
    {"pregunta": "¿Te entusiasma aprender sobre nuevas tecnologías?", "opciones": [1, 2, 3, 4, 5]},
    {"pregunta": "¿Disfrutas resolver problemas complejos?", "opciones": [1, 2, 3, 4, 5]},
    {"pregunta": "¿Te sientes cómodo trabajando con computadoras durante largas horas?", "opciones": [1, 2, 3, 4, 5]},
    {"pregunta": "¿Te gustaría tener un trabajo que implique la creación y diseño de software?", "opciones": [1, 2, 3, 4, 5]},
    {"pregunta": "¿Eres una persona que disfruta organizando datos y buscando patrones?", "opciones": [1, 2, 3, 4, 5]},
    {"pregunta": "¿Te resulta interesante la idea de mejorar sistemas y procesos a través de la tecnología?", "opciones": [1, 2, 3, 4, 5]},
    {"pregunta": "¿Te interesa conocer el funcionamiento interno de las computadoras y dispositivos tecnológicos?", "opciones": [1, 2, 3, 4, 5]},
    {"pregunta": "¿Te gustaría tener una carrera donde puedas combinar creatividad y lógica?", "opciones": [1, 2, 3, 4, 5]},
    {"pregunta": "¿Disfrutas enfrentar retos matemáticos y encontrar soluciones para ellos??", "opciones": [1, 2, 3, 4, 5]},
    {"pregunta": "¿Te interesa la programación y te gustaría crear aplicaciones desde cero?", "opciones": [1, 2, 3, 4, 5]},
    {"pregunta": "¿Te sientes cómodo trabajando con algoritmos y estructuras de datos?", "opciones": [1, 2, 3, 4, 5]},
    {"pregunta": "¿Te motiva el trabajar con bases de datos y la gestión de grandes volúmenes de información?", "opciones": [1, 2, 3, 4, 5]},
    # {"pregunta": "¿Te gusta investigar nuevas tecnologías y métodos para mejorar sistemas existentes?", "opciones": [1, 2, 3, 4, 5]},
    # {"pregunta": "¿Te atrae la idea de trabajar con lenguajes de programación y entender cómo funcionan?", "opciones": [1, 2, 3, 4, 5]},
    # {"pregunta": "¿Disfrutas de los trabajos que implican analizar información para resolver problemas?", "opciones": [1, 2, 3, 4, 5]},
    # {"pregunta": "¿Te interesa el diseño de interfaces de usuario (UI) y la experiencia de usuario (UX)?", "opciones": [1, 2, 3, 4, 5]},
    # {"pregunta": "¿Te gustaría crear soluciones tecnológicas que mejoren la vida de las personas?", "opciones": [1, 2, 3, 4, 5]},
    # {"pregunta": "¿Prefieres trabajar en proyectos que requieren concentración y atención al detalle?", "opciones": [1, 2, 3, 4, 5]},
    # {"pregunta": "¿Te resulta fácil aprender nuevos conceptos técnicos?", "opciones": [1, 2, 3, 4, 5]},
    # {"pregunta": "¿Te atrae la idea de colaborar en equipos multidisciplinarios para resolver problemas?", "opciones": [1, 2, 3, 4, 5]},
    # {"pregunta": "¿Te sientes cómodo utilizando software especializado para crear y modificar programas?", "opciones": [1, 2, 3, 4, 5]},
    # {"pregunta": "¿Te interesa la seguridad informática y proteger los sistemas y datos?", "opciones": [1, 2, 3, 4, 5]},
    # {"pregunta": "¿Te gustaría trabajar en una empresa que desarrolle software para diferentes industrias?", "opciones": [1, 2, 3, 4, 5]},
    # {"pregunta": "¿Te apasiona la idea de ser responsable de crear y mantener sistemas informáticos?", "opciones": [1, 2, 3, 4, 5]},
    # {"pregunta": "¿Te gustaría crear aplicaciones móviles o sitios web que sean utilizados por millones de personas?", "opciones": [1, 2, 3, 4, 5]},
    # {"pregunta": "¿Eres detallista y meticuloso cuando trabajas en proyectos de programación?", "opciones": [1, 2, 3, 4, 5]},
    # {"pregunta": "¿Te gusta hacer pruebas para asegurarte de que un sistema funcione correctamente?", "opciones": [1, 2, 3, 4, 5]},
    # {"pregunta": "¿Disfrutas del proceso de depuración de código para encontrar y corregir errores?", "opciones": [1, 2, 3, 4, 5]},
    # {"pregunta": "¿Te interesa entender cómo los sistemas operativos gestionan los recursos de una computadora?", "opciones": [1, 2, 3, 4, 5]},
    # {"pregunta": "¿Te gustaría especializarte en el desarrollo de software para dispositivos móviles?", "opciones": [1, 2, 3, 4, 5]},
    # {"pregunta": "¿Te resulta interesante la idea de crear videojuegos o aplicaciones interactivas?", "opciones": [1, 2, 3, 4, 5]},
    # {"pregunta": "¿Te gustaría desarrollar sistemas que ayuden a empresas a gestionar sus recursos eficientemente?", "opciones": [1, 2, 3, 4, 5]},
    # {"pregunta": "¿Te atrae la idea de aprender constantemente debido a la rapidez de los avances tecnológicos?", "opciones": [1, 2, 3, 4, 5]},
    # {"pregunta": "¿Te gustaría trabajar en un entorno donde la innovación y la mejora continua sean esenciales?", "opciones": [1, 2, 3, 4, 5]},
    # {"pregunta": "¿Te sientes cómodo resolviendo problemas utilizando herramientas y lenguajes de programación?", "opciones": [1, 2, 3, 4, 5]},
    # {"pregunta": "¿Disfrutas investigando nuevas tecnologías para aplicar en proyectos futuros?", "opciones": [1, 2, 3, 4, 5]},
    # {"pregunta": "¿Te gustaría ser parte de un equipo que trabaja en soluciones tecnológicas para diferentes sectores?", "opciones": [1, 2, 3, 4, 5]},
    # {"pregunta": "¿Te interesa la integración de sistemas y cómo se comunican entre sí?", "opciones": [1, 2, 3, 4, 5]},
    # {"pregunta": "¿Te gusta investigar sobre nuevas tendencias en desarrollo de software, como inteligencia artificial o blockchain?", "opciones": [1, 2, 3, 4, 5]},
    # {"pregunta": "¿Te atrae la idea de optimizar el rendimiento de los sistemas y aplicaciones?", "opciones": [1, 2, 3, 4, 5]},
    # {"pregunta": "¿Te interesa trabajar en proyectos que impliquen la automatización de procesos mediante software?", "opciones": [1, 2, 3, 4, 5]},
    # {"pregunta": "¿Te gustaría trabajar en una empresa que se enfoque en la transformación digital y la innovación tecnológica?", "opciones": [1, 2, 3, 4, 5]},
    # {"pregunta": "¿Te resulta interesante desarrollar aplicaciones que puedan analizar datos en tiempo real?", "opciones": [1, 2, 3, 4, 5]},
    # {"pregunta": "¿Te atrae la idea de trabajar en un entorno que promueva el trabajo en equipo y la colaboración?", "opciones": [1, 2, 3, 4, 5]},
    # {"pregunta": "¿Te gustaría encargarte de la administración de sistemas y redes dentro de una organización?", "opciones": [1, 2, 3, 4, 5]},
    # {"pregunta": "¿Te gustaría liderar proyectos de desarrollo de software y coordinar equipos de trabajo?", "opciones": [1, 2, 3, 4, 5]},
    # {"pregunta": "¿Te interesa investigar sobre las nuevas metodologías de desarrollo ágil (agile) y cómo implementarlas?", "opciones": [1, 2, 3, 4, 5]},
    # {"pregunta": "¿Te gustaría realizar un trabajo que implique tanto habilidades técnicas como de gestión de proyectos?", "opciones": [1, 2, 3, 4, 5]},
    # {"pregunta": "¿Te motiva la idea de ayudar a las empresas a resolver problemas tecnológicos mediante soluciones de software?", "opciones": [1, 2, 3, 4, 5]},
    # {"pregunta": "¿Te atrae la idea de diseñar interfaces visuales atractivas para aplicaciones y sitios web?", "opciones": [1, 2, 3, 4, 5]},

]


#  seccion---------llamo a la pagina principal--------------------------------   
@app.route("/", methods=["GET", "POST"])
def index():
    return render_template('index.html') #----/final de la seccion llamado-----

@app.route("/prueba", methods=["GET", "POST"])
def prueba():
    return render_template('prueba.html')
    
    
@app.route("/test", methods=["GET", "POST"])
def test():
    if request.method == "POST":
        # Procesar respuestas del formulario
        respuestas = []
        for idx in range(len(preguntas)):
            respuesta = request.form.get(f"pregunta_{idx}")
            if respuesta is not None:
                respuestas.append(int(respuesta))
        
        # Calcular el porcentaje de compatibilidad
        max_puntaje = len(preguntas) * 5  # Cada pregunta tiene un máximo de 5
        puntaje_obtenido = sum(respuestas)
        resultado = (puntaje_obtenido / max_puntaje) * 100

        # Renderizar la página de resultados
        return render_template("test_res.html", resultado=int(resultado))

    # Agregar índices a las preguntas
    preguntas_con_indices = [{"idx": idx, **pregunta} for idx, pregunta in enumerate(preguntas)]

    # Renderizar la página principal
    return render_template("test.html", preguntas=preguntas_con_indices)

# ------------------------------------------------------------------------------login-
@app.route('/login')
def login():
    
    return render_template('login.html')

@app.route('/ing', methods=['GET', 'POST'])
def ing():
    if request.method == 'POST':
        nombre_usuario = request.form['usuario']
        contraseña = request.form['contraseña']

        user = LoginNot.query.filter_by(usuario=nombre_usuario).first()

        if user and user.check_password(contraseña):
            return redirect('/sis')
        else:
            error = 'Usuario o contraseña incorrectos'
            return render_template('login.html', error=error)



# -----------------------------------------------------empieza registr_user-----------
@app.route('/reg', methods=['POST'])
def registro():
    usuario = request.form['usuario']
    contraseña = request.form['contraseña']

    # Encriptar la contraseña
    encriptada = generate_password_hash(contraseña)

    # Crear nuevo usuario
    nuevo_usuario = usuario(usuario=usuario, contraseña=encriptada)

    # Guardar en la base de datos
    db.session.add(nuevo_usuario)
    db.session.commit()

    return redirect('/login')


# ----------------------------------------------------------sis_notas-----------
@app.route('/sis')  
def sis():
    
    return render_template('sis_notas.html')

@app.route('/boleta')  
def boleta():
    
    return render_template('boleta_notas.html')



if __name__ == "__main__":
    app.run(debug=True)
    
 