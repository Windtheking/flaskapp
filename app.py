import pymysql
from flask import Flask, request, jsonify, render_template, url_for, redirect
from markupsafe import escape


app = Flask(__name__)

def get_connection():                     #conectar a base de datos                      
    return pymysql.connect(
        host= 'localhost',
        user= 'root',
        password= '',
        db= 'usuarios_flask'
    )





@app.route("/")                                                      #con este codigo el root de este mensaje es en la pagina principal 
def indo():

    conexion = get_connection()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SET @num := 0;")
            cursor.execute("UPDATE usuarios SET id = @num := (@num+1);")
            cursor.execute("ALTER TABLE usuarios AUTO_INCREMENT = 1;")
            coneion.commit()
    except Exception as e:
        return "error interno de servidor"
    finally:
            conexion.close()
            return redirect(url_for("index"))                           #esto es para que aparezca la pagina creada con html en el servidor en vivo
    
    # with open('pruebadatabase.txt', 'a') as f:
    #     f.write(f'{nombre},{contrasena}\n')

    # return render_template("respuestas.html" , nombre = nombre)         #de esta manera hacemos que otra pagina aparte sea la que reciba (return) el valor para mostrarlo
                                                                        #dentro del if - post puedes qué debe retornar cuando ocurra un post - puedes hacer que retorne (esscriba) varios valoress pero debes ponerlos en la misma linea
                                                                        #puedes meter una tupla,el segundo valor sera uno de los tantosss codigoss http (consultar informacion)


@app.route("/guardoconexito", methods = ["GET", "POST"])
def pag_guardado():
    if request.method == "POST":
        return render_template('cambios guardados.html')


@app.route("/pagina_principal", methods = ["GET", "POST"])                                                
def index():
    return render_template('formulario.html')


@app.route("/recibir", methods = ["GET","POST"])                          #jamas olvides poner que metodos quieres
def CR():
    if request.method == "POST":
        action = request.form.get('action')

        if action == "create":
            return crear()
        elif action == "read":
            return leer()
        elif action == "update":
            return redirect(url_for("U"))
        elif action == "delete":
            return redirect(url_for("D"))
        else:
            return "Acción no válida"
    return render_template("actualizardatos.html")
        
def crear():                                    # Flask lo atrapa por el name del input - #cuando ocurra el metodo post aparece el mensaje dentro del if
    nombre = request.form['nombre'].strip()                               
    contrasena = request.form['contrasen'].strip()
    
    if not nombre or not contrasena:
        return "Error: Ambos campos son requeridos."

    conexion = get_connection()

    

    try:
        with conexion.cursor() as cursor:
            sql = "INSERT INTO usuarios (nombre, contrasena) VALUES (%s, %s)"
            cursor.execute(sql, (nombre, contrasena))
            conexion.commit()
        return render_template("guardado exitosamente.html")
    except Exception as e:
        return "porfavor llenar todos los campos"
    finally:
            conexion.close()

def leer():
    conexion = get_connection()
    try:
        with conexion.cursor() as cursor:
            sql = "SELECT * FROM usuarios"
            cursor.execute(sql)
            usuarios = cursor.fetchall()
        return render_template('verdatos.html', usuarios=usuarios)
    except Exception as e:
        return f"Error al leer los datos: {str(e)}"
    finally:
        conexion.close()

@app.route("/recibir/actua", methods = ["GET", "POST"])
def U():
    return render_template("actualizardatos.html")

@app.route("/datoactualizado", methods = ["GET", "POST"])

def actualizar(): 
    ident = request.form('identificacion').strip()
    nombre = request.form('nombre').strip()
    contrasena = request.form('contrasen').strip()
    conteo = 0

    # if not nombre or not contrasena:
    #     return "Error: Ambos campos son requeridos."

    conexion = get_connection()
    try:
        with conexion.cursor() as cursor:
            sql = f"UPDATE usuarios SET nombre=%s, contrasena=%s WHERE id=%s"
            cursor.execute(sql, (nombre, contrasena, ident))
            conexion.commit()
            conteo += 1
        print(f"Usuario con ID {id} actualizado correctamente")
    except Exception as e:
        return f"Error al actualizar el usuario: {str(e)}"
    finally:
        conexion.close()

    if conteo < 1:
        return eliminar()


@app.route("/recibir/get", methods = ["GET", "POST"])
def D():
    return render_template("Borrar datos.html")


@app.route("/datoborrado", methods = ["GET", "POST"])

def eliminar():
    identif = int(request.form['identificacion'])
    conteo = 0
   
    if not identif:
        return "Error: Id requerida para eliminar datos"
    

    conexion = get_connection()
    try:
        with conexion.cursor() as cursor:
            sql = "DELETE FROM usuarios WHERE id=%s"
            cursor.execute(sql, (identif))
            conexion.commit()
            conteo += 1
        print(f"Usuario con ID {identif} actualizado correctamente")
    except Exception as e:
        return f"Error al actualizar el usuario: {str(e)}"
    finally:
        conexion.close()
    
    if conteo < 1:
        return eliminar()
    return redirect(url_for("index"))




@app.route("/prueba/<nombre>")
def mostrar_perfil_personal(nombre):
    # nombre = request.form['nombre'].strip()
    return f"perfil de {escape(nombre)}"




@app.route("/api/info")
def api_info():
    data = {
            "nombre": "Notes app",
            "version": "1.1.1"
        }
    return jsonify(data), 200


if __name__ == "__main__":
    app.run()