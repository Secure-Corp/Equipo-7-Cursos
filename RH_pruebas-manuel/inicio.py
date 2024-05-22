from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/area')
def area():
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rh3' )
    cursor = conn.cursor()
    cursor.execute('select idArea, descripcion from area order by idArea')
    datos = cursor.fetchall()
    return render_template("area.html", comentarios = datos)

@app.route('/area_editar/<string:id>')
def area_editar(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rh3')
    cursor = conn.cursor()
    cursor.execute('select idArea, descripcion from area where idArea = %s', (id))
    dato  = cursor.fetchall()
    return render_template("area_edi.html", comentar=dato[0])

@app.route('/area_fedita/<string:id>',methods=['POST'])
def area_fedita(id):
    if request.method == 'POST':
        desc=request.form['descripcion']
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='rh3')
        cursor = conn.cursor()
        cursor.execute('update area set descripcion=%s where idArea=%s', (desc,id))
        conn.commit()
    return redirect(url_for('area'))

@app.route('/area_borrar/<string:id>')
def area_borrar(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rh3')
    cursor = conn.cursor()
    cursor.execute('delete from area where idArea = {0}'.format(id))
    conn.commit()
    return redirect(url_for('area'))

@app.route('/area_agregar')
def area_agregar():
    return render_template("area_agr.html")

@app.route('/area_fagrega', methods=['POST'])
def area_fagrega():
    if request.method == 'POST':
        desc = request.form['descripcion']
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='rh3' )
        cursor = conn.cursor()
        cursor.execute('insert into area (descripcion) values (%s)',(desc))
        conn.commit()
    return redirect(url_for('area'))



@app.route('/puesto')
def puesto():
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rh3' )
    cursor = conn.cursor()

    cursor.execute('select idPuesto, nomPuesto from puesto order by idPuesto')
    datos = cursor.fetchall()

    return render_template("puesto.html", pue = datos, dat='   ', catArea = '   ', catEdoCivil = '   ', catEscolaridad = '   ',
                           catGradoAvance = '    ', catCarrera = '    ', catIdioma = ' ', catHabilidad = ' ')


@app.route('/puesto_fdetalle/<string:idP>', methods=['GET'])
def puesto_fdetalle(idP):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rh3')
    cursor = conn.cursor()

    cursor.execute('select idPuesto, nomPuesto from puesto order by idPuesto')
    datos = cursor.fetchall()

    cursor.execute('select idPuesto,codPuesto,idArea,nomPuesto,puestoJefeSup,jornada,remunMensual,prestaciones,descripcionGeneral,'
            'funciones,edad,sexo,idEstadoCivil,idEscolaridad,idGradoAvance,idCarrera,experiencia,conocimientos,manejoEquipo,'
            'reqFisicos,reqPsicologicos,responsabilidades,condicionesTrabajo from puesto where idPuesto = %s', (idP))
    dato = cursor.fetchall()

    cursor.execute('select a.idArea, a.descripcion from area a, puesto b where a.idArea = b.idArea and b.idPuesto = %s', (idP))
    datos1 = cursor.fetchall()

    cursor.execute('select a.idEstadoCivil, a.descripcion from estado_civil a, puesto b where a.idEstadoCivil = b.idEstadoCivil and b.idPuesto = %s', (idP))
    datos2 = cursor.fetchall()

    cursor.execute('select a.idEscolaridad, a.descripcion from escolaridad a, puesto b where a.idEscolaridad = b.idEscolaridad and b.idPuesto = %s', (idP))
    datos3 = cursor.fetchall()

    cursor.execute('select a.idGradoAvance, a.descripcion from grado_avance a, puesto b where a.idGradoAvance = b.idGradoAvance and b.idPuesto = %s', (idP))
    datos4 = cursor.fetchall()

    cursor.execute('select a.idCarrera, a.descripcion from carrera a, puesto b where a.idCarrera = b.idCarrera and b.idPuesto = %s', (idP))
    datos5 = cursor.fetchall()

    cursor.execute('select a.idPuesto, b.idIdioma, b.descripcion from puesto a, idioma b, puesto_has_idioma c '
                   'where a.idPuesto = c.idPuesto and b.idIdioma = c.idIdioma and a.idPuesto = %s', (idP))
    datos6 = cursor.fetchall()

    cursor.execute('select a.idPuesto, b.idHabilidad, b.descripcion from puesto a, habilidad b, puesto_has_habilidad c '
                   'where a.idPuesto = c.idPuesto and b.idHabilidad = c.idHabilidad and a.idPuesto = %s', (idP))
    datos7 = cursor.fetchall()
    return render_template("puesto.html", pue = datos, dat=dato[0], catArea=datos1[0], catEdoCivil=datos2[0], catEscolaridad=datos3[0],
                           catGradoAvance=datos4[0], catCarrera=datos5[0], catIdioma=datos6, catHabilidad=datos7)

@app.route('/puesto_borrar/<string:idP>')
def puesto_borrar(idP):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rh3')
    cursor = conn.cursor()
    cursor.execute('delete from puesto where idPuesto = %s',(idP))
    conn.commit()
    cursor.execute('delete from puesto_has_habilidad where idPuesto =%s ', (idP))
    conn.commit()
    cursor.execute('delete from puesto_has_idioma where idPuesto =%s ', (idP))
    conn.commit()
    return redirect(url_for('puesto'))


@app.route('/puesto_agrOp2')
def puesto_agrOp2():
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rh3')
    cursor = conn.cursor()
    cursor.execute('select idArea, descripcion from area ')
    datos1 = cursor.fetchall()

    cursor.execute('select idEstadoCivil, descripcion from estado_civil ')
    datos2 = cursor.fetchall()

    cursor.execute('select idEscolaridad, descripcion from escolaridad ')
    datos3 = cursor.fetchall()

    cursor.execute('select idGradoAvance, descripcion from grado_avance ')
    datos4 = cursor.fetchall()

    cursor.execute('select idCarrera, descripcion from carrera ')
    datos5 = cursor.fetchall()

    cursor.execute('select idIdioma, descripcion from idioma ')
    datos6 = cursor.fetchall()

    cursor.execute('select idHabilidad, descripcion from habilidad ')
    datos7 = cursor.fetchall()

    return render_template("puesto_agrOp2.html", catArea=datos1, catEdoCivil=datos2, catEscolaridad=datos3,
                           catGradoAvance=datos4, catCarrera=datos5, catIdioma=datos6, catHabilidad=datos7)


@app.route('/puesto_fagrega2', methods=['POST'])
def puesto_fagrega():
    if request.method == 'POST':

        if  'idArea' in request.form:
            idAr = request.form['idArea']
        else:
            idAr = '1'
        if 'idEstadoCivil' in request.form:
            idEC = request.form['idEstadoCivil']
        else:
            idEC = '1'
        if 'idEscolaridad' in request.form:
            idEs = request.form['idEscolaridad']
        else:
            idEs = '1'
        if 'idGradoAvance' in request.form:
            idGA = request.form['idGradoAvance']
        else:
            idGA = '1'
        if 'idCarrera' in request.form:
            idCa = request.form['idCarrera']
        else:
            idCa = '1'
        if 'sexo' in request.form:
            sex = request.form['sexo']
        else:
            sex = '1'
        codP = request.form['codPuesto']
        nomP = request.form['nomPuesto']
        pueJ = request.form['puestoJefeSup']
        jorn = request.form['jornada']
        remu = request.form['remunMensual']
        pres = request.form['prestaciones']
        desc = request.form['descripcionGeneral']
        func = request.form['funciones']
        eda = request.form['edad']
        expe = request.form['experiencia']
        cono = request.form['conocimientos']
        manE = request.form['manejoEquipo']
        reqF = request.form['reqFisicos']
        reqP = request.form['reqPsicologicos']
        resp = request.form['responsabilidades']
        conT = request.form['condicionesTrabajo']


    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rh3')
    cursor = conn.cursor()
    cursor.execute(
    'insert into puesto (codPuesto,idArea,nomPuesto,puestoJefeSup,jornada,remunMensual,prestaciones,descripcionGeneral,'
    'funciones,edad,sexo,idEstadoCivil,idEscolaridad,idGradoAvance,idCarrera,experiencia,conocimientos,manejoEquipo,'
    'reqFisicos,reqPsicologicos,responsabilidades,condicionesTrabajo) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
    (codP, idAr, nomP, pueJ, jorn, remu, pres, desc, func, eda, sex, idEC, idEs, idGA, idCa, expe, cono, manE, reqF,
     reqP, resp, conT))
    conn.commit()

    cursor.execute('select idPuesto from puesto where idPuesto=(select max(idPuesto) from puesto) ')
    dato = cursor.fetchall()
    idpue = dato[0]
    idP = idpue[0]

    cursor.execute('select count(*) from idioma ')
    dato = cursor.fetchall()
    nidio = dato[0]
    ni = nidio[0] + 1

    for i in range(1, ni):
        idio = 'i' + str(i)
        if idio in request.form:
            cursor.execute('insert into puesto_has_idioma(idPuesto,idIdioma) values (%s,%s)', (idP, i))
            conn.commit()

    cursor.execute('select count(*) from habilidad ')
    dato = cursor.fetchall()
    nhab = dato[0]
    nh =nhab[0]+1

    for i in range(1,nh):
        habi = 'h' + str(i)
        if habi in request.form:
            cursor.execute('insert into puesto_has_habilidad(idPuesto,idHabilidad) values (%s,%s)', (idP,i))
            conn.commit()

    return redirect(url_for('puesto'))



@app.route('/puesto_editar/<string:idP>')
def puesto_editar(idP):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rh3')
    cursor = conn.cursor()

    cursor.execute('select idPuesto,codPuesto,idArea,nomPuesto,puestoJefeSup,jornada,remunMensual,prestaciones,descripcionGeneral,'
        'funciones,edad,sexo,idEstadoCivil,idEscolaridad,idGradoAvance,idCarrera,experiencia,conocimientos,manejoEquipo,'
        'reqFisicos,reqPsicologicos,responsabilidades,condicionesTrabajo from puesto where idPuesto = %s', (idP))
    dato = cursor.fetchall()

    cursor.execute('select idArea, descripcion from area ')
    datos1 = cursor.fetchall()

    cursor.execute('select idEstadoCivil, descripcion from estado_civil ')
    datos2 = cursor.fetchall()

    cursor.execute('select idEscolaridad, descripcion from escolaridad ')
    datos3 = cursor.fetchall()

    cursor.execute('select idGradoAvance, descripcion from grado_avance ')
    datos4 = cursor.fetchall()

    cursor.execute('select idCarrera, descripcion from carrera ')
    datos5 = cursor.fetchall()

    cursor.execute('select idIdioma, descripcion from idioma ')
    datos6 = cursor.fetchall()

    cursor.execute('select idHabilidad, descripcion from habilidad ')
    datos7 = cursor.fetchall()

    cursor.execute('select a.idArea, a.descripcion from area a, puesto b where a.idArea = b.idArea and b.idPuesto = %s', (idP))
    datos11 = cursor.fetchall()

    cursor.execute('select a.idEstadoCivil, a.descripcion from estado_civil a, puesto b where a.idEstadoCivil = b.idEstadoCivil and b.idPuesto = %s',(idP))
    datos12 = cursor.fetchall()

    cursor.execute('select a.idEscolaridad, a.descripcion from escolaridad a, puesto b where a.idEscolaridad = b.idEscolaridad and b.idPuesto = %s',(idP))
    datos13 = cursor.fetchall()

    cursor.execute('select a.idGradoAvance, a.descripcion from grado_avance a, puesto b where a.idGradoAvance = b.idGradoAvance and b.idPuesto = %s',(idP))
    datos14 = cursor.fetchall()

    cursor.execute('select a.idCarrera, a.descripcion from carrera a, puesto b where a.idCarrera = b.idCarrera and b.idPuesto = %s', (idP))
    datos15 = cursor.fetchall()

    cursor.execute('select a.idPuesto, b.idIdioma, b.descripcion from puesto a, idioma b, puesto_has_idioma c '
                   'where a.idPuesto = c.idPuesto and b.idIdioma = c.idIdioma and a.idPuesto = %s', (idP))
    datos16 = cursor.fetchall()

    cursor.execute('select a.idPuesto, b.idHabilidad, b.descripcion from puesto a, habilidad b, puesto_has_habilidad c '
                   'where a.idPuesto = c.idPuesto and b.idHabilidad = c.idHabilidad and a.idPuesto = %s', (idP))
    datos17 = cursor.fetchall()


    return render_template("puesto_edi.html", dat=dato[0], catArea=datos1, catEdoCivil=datos2, catEscolaridad=datos3,
                           catGradoAvance=datos4, catCarrera=datos5, catIdioma=datos6, catHabilidad=datos7,
                           Area=datos11[0], EdoCivil=datos12[0], Escolaridad=datos13[0], GradoAvance=datos14[0],
                           Carrera=datos15[0], Idioma=datos16, Habilidad=datos17)


@app.route('/puesto_fedita/<string:idP>', methods=['POST'])
def puesto_fedita(idP):
    if request.method == 'POST':
        codP = request.form['codPuesto']
        idAr = request.form['idArea']
        nomP = request.form['nomPuesto']
        pueJ = request.form['puestoJefeSup']
        jorn = request.form['jornada']
        remu = request.form['remunMensual']
        pres = request.form['prestaciones']
        desc = request.form['descripcionGeneral']
        func = request.form['funciones']
        eda = request.form['edad']
        sex = request.form['sexo']
        idEC = request.form['idEstadoCivil']
        idEs = request.form['idEscolaridad']
        idGA = request.form['idGradoAvance']
        idCa = request.form['idCarrera']
        expe = request.form['experiencia']
        cono = request.form['conocimientos']
        manE = request.form['manejoEquipo']
        reqF = request.form['reqFisicos']
        reqP = request.form['reqPsicologicos']
        resp = request.form['responsabilidades']
        conT = request.form['condicionesTrabajo']

    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rh3')
    cursor = conn.cursor()

    cursor.execute('update puesto set codPuesto = %s, idArea = %s, nomPuesto = %s, puestoJefeSup = %s, jornada = %s, '
                   'remunMensual = %s, prestaciones = %s, descripcionGeneral = %s, funciones = %s, edad = %s, sexo = %s, '
                   'idEstadoCivil = %s, idEscolaridad = %s, idGradoAvance = %s, idCarrera = %s, experiencia = %s, '
                   'conocimientos = %s, manejoEquipo = %s, reqFisicos = %s, reqPsicologicos = %s, responsabilidades = %s, '
                   'condicionesTrabajo = %s where idPuesto = %s', (codP, idAr, nomP, pueJ, jorn, remu, pres, desc, func, eda,
                   sex, idEC, idEs, idGA, idCa, expe, cono, manE, reqF, reqP, resp, conT, idP))
    conn.commit()

    cursor.execute('delete from puesto_has_habilidad where idPuesto =%s ', (idP))
    conn.commit()
    cursor.execute('delete from puesto_has_idioma where idPuesto =%s ', (idP))
    conn.commit()

    cursor.execute('select count(*) from idioma ')
    dato = cursor.fetchall()
    nidio = dato[0]
    ni = nidio[0] + 1

    for i in range(1, ni):
        idio = 'i' + str(i)
        if idio in request.form:
            cursor.execute('insert into puesto_has_idioma(idPuesto,idIdioma) values (%s,%s)', (idP, i))
            conn.commit()

    cursor.execute('select count(*) from habilidad ')
    dato = cursor.fetchall()
    nhab = dato[0]
    nh = nhab[0] + 1

    for i in range(1, nh):
        habi = 'h' + str(i)
        if habi in request.form:
            cursor.execute('insert into puesto_has_habilidad(idPuesto,idHabilidad) values (%s,%s)', (idP, i))
            conn.commit()
    return redirect(url_for('puesto'))

@app.route('/carrera')
def carrera():
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rh3' )
    cursor = conn.cursor()
    cursor.execute('select idCarrera, descripcion from carrera order by idCarrera')
    datos = cursor.fetchall()
    return render_template("carrera.html", comentarios = datos)

@app.route('/carrera_editar/<string:id>')
def carrera_editar(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rh3')
    cursor = conn.cursor()
    cursor.execute('select idCarrera, descripcion from carrera where idCarrera = %s', (id))
    dato  = cursor.fetchall()
    return render_template("Carrera_edi.html", comentar=dato[0])

@app.route('/carrera_fedita/<string:id>',methods=['POST'])
def carrera_fedita(id):
    if request.method == 'POST':
        desc=request.form['descripcion']
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='rh3')
        cursor = conn.cursor()
        cursor.execute('update carrera set descripcion=%s where idCarrera=%s', (desc,id))
        conn.commit()
    return redirect(url_for('carrera'))

@app.route('/carrera_borrar/<string:id>')
def carrera_borrar(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rh3')
    cursor = conn.cursor()
    cursor.execute('delete from carrera where idCarrera = {0}'.format(id))
    conn.commit()
    return redirect(url_for('carrera'))

@app.route('/carrera_agregar')
def carrera_agregar():
    return render_template("Carrera_agr.html")

@app.route('/carrera_fagrega', methods=['POST'])
def carrera_fagrega():
    if request.method == 'POST':
        desc = request.form['descripcion']
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='rh3' )
        cursor = conn.cursor()
        cursor.execute('insert into estado_civil (descripcion) values (%s)',(desc))
        conn.commit()
    return redirect(url_for('carrera'))


@app.route('/ec')
def ec():
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rh3' )
    cursor = conn.cursor()
    cursor.execute('select idEstadoCivil, descripcion from estado_civil order by idEstadoCivil')
    datos = cursor.fetchall()
    return render_template("ec.html", comentarios = datos)

@app.route('/ec_editar/<string:id>')
def ec_editar(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rh3')
    cursor = conn.cursor()
    cursor.execute('select idEstadoCivil, descripcion from estado_civil where idEstadoCivil = %s', (id))
    dato  = cursor.fetchall()
    return render_template("ec_edi.html", comentar=dato[0])

@app.route('/ec_fedita/<string:id>',methods=['POST'])
def ec_fedita(id):
    if request.method == 'POST':
        desc=request.form['descripcion']
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='rh3')
        cursor = conn.cursor()
        cursor.execute('update estado_civil set descripcion=%s where idEstadoCivil=%s', (desc,id))
        conn.commit()
    return redirect(url_for('ec'))

@app.route('/ec_borrar/<string:id>')
def ec_borrar(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rh3')
    cursor = conn.cursor()
    cursor.execute('delete from estado_civil where idEstadoCivil = {0}'.format(id))
    conn.commit()
    return redirect(url_for('ec'))

@app.route('/ec_agregar')
def ec_agregar():
    return render_template("ec_agr.html")

@app.route('/ec_fagrega', methods=['POST'])
def ec_fagrega():
    if request.method == 'POST':
        desc = request.form['descripcion']
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='rh3' )
        cursor = conn.cursor()
        cursor.execute('insert into estado_civil (descripcion) values (%s)',(desc))
        conn.commit()
    return redirect(url_for('ec'))


@app.route('/es')
def es():
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rh3' )
    cursor = conn.cursor()
    cursor.execute('select idEscolaridad, descripcion from escolaridad order by idEscolaridad')
    datos = cursor.fetchall()
    return render_template("Escolaridad.html", comentarios = datos)

@app.route('/es_editar/<string:id>')
def es_editar(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rh3')
    cursor = conn.cursor()
    cursor.execute('select idEscolaridad, descripcion from escolaridad where idEscolaridad = %s', (id))
    dato  = cursor.fetchall()
    return render_template("Escolaridad_edi.html", comentar=dato[0])

@app.route('/es_fedita/<string:id>',methods=['POST'])
def es_fedita(id):
    if request.method == 'POST':
        desc=request.form['descripcion']
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='rh3')
        cursor = conn.cursor()
        cursor.execute('update escolaridad set descripcion=%s where idEscolaridad=%s', (desc,id))
        conn.commit()
    return redirect(url_for('es'))

@app.route('/es_borrar/<string:id>')
def es_borrar(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rh3')
    cursor = conn.cursor()
    cursor.execute('delete from escolaridad where idEscolaridad = {0}'.format(id))
    conn.commit()
    return redirect(url_for('es'))

@app.route('/Escolaridad_agregar')
def Escolaridad_agregar():
    return render_template("Escolaridad_agr.html")

@app.route('/es_fagrega', methods=['POST'])
def es_fagrega():
    if request.method == 'POST':
        desc = request.form['descripcion']
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='rh3' )
        cursor = conn.cursor()
        cursor.execute('insert into escolaridad (descripcion) values (%s)',(desc))
        conn.commit()
    return redirect(url_for('es'))


@app.route('/GA')
def GA():
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rh3' )
    cursor = conn.cursor()
    cursor.execute('select idGradoAvance, descripcion from grado_avance order by idGradoAvance')
    datos = cursor.fetchall()
    return render_template("GA.html", comentarios = datos)

@app.route('/GA_editar/<string:id>')
def GA_editar(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rh3')
    cursor = conn.cursor()
    cursor.execute('select idGradoAvance, descripcion from grado_avance where idGradoAvance = %s', (id))
    dato  = cursor.fetchall()
    return render_template("GA_edi.html", comentar=dato[0])

@app.route('/GA_fedita/<string:id>',methods=['POST'])
def GA_fedita(id):
    if request.method == 'POST':
        desc=request.form['descripcion']
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='rh3')
        cursor = conn.cursor()
        cursor.execute('update grado_avance set descripcion=%s where idGradoAvance=%s', (desc,id))
        conn.commit()
    return redirect(url_for('GA'))

@app.route('/GA_borrar/<string:id>')
def GA_borrar(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rh3')
    cursor = conn.cursor()
    cursor.execute('delete from grado_avance where idGradoAvance = {0}'.format(id))
    conn.commit()
    return redirect(url_for('GA'))

@app.route('/GA_agregar')
def GA_agregar():
    return render_template("GA_agr.html")

@app.route('/Ga_fagrega', methods=['POST'])
def Ga_fagrega():
    if request.method == 'POST':
        desc = request.form['descripcion']
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='rh3' )
        cursor = conn.cursor()
        cursor.execute('insert into grado_avance (descripcion) values (%s)',(desc))
        conn.commit()
    return redirect(url_for('GA'))


@app.route('/HA')
def HA():
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rh3' )
    cursor = conn.cursor()
    cursor.execute('select idHabilidad, descripcion from habilidad order by idHabilidad')
    datos = cursor.fetchall()
    return render_template("HA.html", comentarios = datos)

@app.route('/HA_editar/<string:id>')
def HA_editar(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rh3')
    cursor = conn.cursor()
    cursor.execute('select idHabilidad, descripcion from habilidad where idHabilidad = %s', (id))
    dato  = cursor.fetchall()
    return render_template("HA_edi.html", comentar=dato[0])

@app.route('/HA_fedita/<string:id>',methods=['POST'])
def HA_fedita(id):
    if request.method == 'POST':
        desc=request.form['descripcion']
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='rh3')
        cursor = conn.cursor()
        cursor.execute('update habilidad set descripcion=%s where idHabilidad=%s', (desc,id))
        conn.commit()
    return redirect(url_for('HA'))

@app.route('/HA_borrar/<string:id>')
def HA_borrar(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rh3')
    cursor = conn.cursor()
    cursor.execute('delete from habilidad where idHabilidad = {0}'.format(id))
    conn.commit()
    return redirect(url_for('HA'))

@app.route('/HA_agregar')
def HA_agregar():
    return render_template("HA_agr.html")

@app.route('/Ha_fagrega', methods=['POST'])
def Ha_fagrega():
    if request.method == 'POST':
        desc = request.form['descripcion']
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='rh3' )
        cursor = conn.cursor()
        cursor.execute('insert into habilidad (descripcion) values (%s)',(desc))
        conn.commit()
    return redirect(url_for('HA'))


@app.route('/id')
def id():
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rh3' )
    cursor = conn.cursor()
    cursor.execute('select idIdioma, descripcion from idioma order by idIdioma')
    datos = cursor.fetchall()
    return render_template("id.html", comentarios = datos)

@app.route('/id_editar/<string:id>')
def id_editar(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rh3')
    cursor = conn.cursor()
    cursor.execute('select idIdioma, descripcion from idioma where idIdioma = %s', (id))
    dato  = cursor.fetchall()
    return render_template("id_edi.html", comentar=dato[0])

@app.route('/id_fedita/<string:id>',methods=['POST'])
def id_fedita(id):
    if request.method == 'POST':
        desc=request.form['descripcion']
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='rh3')
        cursor = conn.cursor()
        cursor.execute('update idioma set descripcion=%s where idIdioma=%s', (desc,id))
        conn.commit()
    return redirect(url_for('id'))

@app.route('/id_borrar/<string:id>')
def id_borrar(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rh3')
    cursor = conn.cursor()
    cursor.execute('delete from idioma where idIdioma = {0}'.format(id))
    conn.commit()
    return redirect(url_for('id'))

@app.route('/id_agregar')
def id_agregar():
    return render_template("id_agr.html")

@app.route('/id_fagrega', methods=['POST'])
def id_fagrega():
    if request.method == 'POST':
        desc = request.form['descripcion']
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='rh3' )
        cursor = conn.cursor()
        cursor.execute('insert into idioma (descripcion) values (%s)',(desc))
        conn.commit()
    return redirect(url_for('id'))

@app.route("/tabla_con")
def tabla_con():
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rh3' )
    cursor = conn.cursor()
    cursor.execute("select * from usuario order by idusuario")
    datos  = cursor.fetchall()
    return render_template("tabla_can.html", comentarios = datos)

@app.route("/clubvist/<string:id>")
def clubvist(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rh3' )
    cursor = conn.cursor()
    cursor.execute("select * from cursos order by idcursos")
    datos = cursor.fetchall()
    return render_template("clubs.html", comentarios = datos , pot=id)

@app.route("/cursoagr/<string:nombre>/<string:decripcion>/<string:id>")
def cursoagr(nombre,decripcion,id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rh3' )
    cursor = conn.cursor()
    cursor.execute("insert into agcuso (nombre,descripcion,idusuario,completado) values (%s,%s,%s,%s)",(nombre,decripcion,id,2))
    conn.commit()
    return redirect(url_for('tabla_con'))

@app.route("/arg_curso")
def agr_curso():
    return render_template('agr_cur.html')

@app.route("/arg_cur", methods=['POST'])
def agr_cur():
    if request.method == 'POST':
        nombre=request.form['nombre']
        descripcion=request.form['descripcion']
        conn = pymysql.connect(host="localhost", user="root", passwd="",db="rh3")
        cursor = conn.cursor()
        cursor.execute("insert into cursos (nombre,descripcion) values (%s,%s)",(nombre,descripcion))
        conn.commit()
    return redirect(url_for('tabla_con'))

@app.route("/clubstu/<string:id>")
def clubstu(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rh3' )
    cursor = conn.cursor()
    cursor.execute("select b.idusuario,a.nombre,a.descripcion,c.descripcion,a.idagcu  from agcuso as a inner join usuario as b inner join completadas as c on a.idusuario=b.idusuario where c.id=a.completado and a.idusuario = {0}".format(id))
    datos = cursor.fetchall()
    return render_template("cali.html", comentarios = datos)
    
@app.route("/clubvist2/<string:id>",methods=['POST'])
def clubvist2(id):
    if request.method == 'POST':
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='rh3' )
        cursor = conn.cursor()
        cursor.execute("update agcuso set completado=%s where idagcu=%s",( 1 ,id) )
        conn.commit()
        return redirect(url_for('tabla_con'))

@app.route("/curriculum/<string:id>")
def curiculim(id):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rh3' )
    cursor = conn.cursor()
    cursor.execute("select b.*,a.nombre,a.descripcion,c.descripcion,a.idagcu from agcuso as a inner join usuario as b inner join completadas as c on a.idusuario=b.idusuario where c.id=a.completado and a.idusuario = {0}".format(id))
    datos  = cursor.fetchall()
    return render_template("curiculum.html", comentarios = datos)


if __name__ == "__main__":
    app.run(debug=True)
