from flask import Flask, send_from_directory, render_template, request, session, redirect, url_for

app = Flask("proyecto-mate-financiera")
app.secret_key = 'supersecretkey'  # Necesario para usar sesiones

@app.route('/images/<path:filename>')
def images(filename):
    return send_from_directory('images', filename)

@app.route('/', methods=['GET', 'POST'])
def index():
    # Inicializar variables de resultado
    result_vf = None
    result_va = None
    result_tna = None
    years = None
    months = None
    days = None
    result_ci = None
    result_tea = None

    if 'mostrar_formulas' not in session:
        session['mostrar_formulas'] = False

    if request.method == 'POST' and 'toggle_formulas' in request.form:
        session['mostrar_formulas'] = not session['mostrar_formulas']
        return redirect(url_for('index') + '#info-boxes')

    return render_template('index.html', mostrar_formulas=session['mostrar_formulas'], 
    result_vf=result_vf, result_va=result_va, result_tna=result_tna,years=years, months=months,
    days=days, result_ci=result_ci, result_tea=result_tea)

# Rutas de cálculo (mantenerlas tal cual)
@app.route('/VF', methods=['POST'])
def VF():
    try:
        VA = float(request.form['VA']) 
        i = float(request.form['i'])     
        tiempo = int(request.form['tiempo']) 
        selectTiempo = request.form['selectTiempo']  

        if selectTiempo == 'opcion1':
            result_vf = VA * (1 + i * tiempo)
        elif selectTiempo == 'opcion2':
            result_vf = VA * (1 + (i / 12) * tiempo)
        elif selectTiempo == 'opcion3':
            result_vf = VA * (1 + (i / 365) * tiempo)
        else:
            return "Error: Unidad de tiempo no reconocida."

        return render_template('index.html', result_vf=result_vf, mostrar_formulas=session['mostrar_formulas'])
    except ValueError:
        return "Error: Asegúrate de que todos los campos sean válidos y numéricos."

@app.route('/VA', methods=['POST'])
def VA():
    try:
        VF = float(request.form['VF'])
        TNA = float(request.form['TNA'])
        tiempo = int(request.form['tiempo'])
        selectTiempo = request.form['selectTiempo']

        if selectTiempo == 'opcion1':
            result_va = VF / (1 + TNA * tiempo)
        elif selectTiempo == 'opcion2':
            result_va = VF / (1 + (TNA / 12) * tiempo)
        elif selectTiempo == 'opcion3':
            result_va = VF / (1 + (TNA / 365) * tiempo)
        else:
            return "Error: Unidad de tiempo no reconocida."

        return render_template('index.html', result_va=result_va, mostrar_formulas=session['mostrar_formulas'])
    except ValueError:
        return "Error: Asegúrate de que todos los campos sean válidos y numéricos."

@app.route('/TNA', methods=['POST'])
def TNA():
    try:
        i = float(request.form['i'])
        VA = float(request.form['VA'])
        tiempo = int(request.form['tiempo'])
        selectTiempo = request.form['selectTiempo']

        if selectTiempo == 'opcion1':
            result_tna = (i / (VA * tiempo))
        elif selectTiempo == 'opcion2':
            result_tna = (i / (VA * (tiempo / 12)))
        elif selectTiempo == 'opcion3':
            result_tna = (i / (VA * (tiempo / 365)))
        else:
            return "Error: Unidad de tiempo no reconocida."

        return render_template('index.html', result_tna=result_tna, mostrar_formulas=session['mostrar_formulas'])
    except ValueError:
        return "Error: Asegúrate de que todos los campos sean válidos y numéricos."

@app.route('/tiempo', methods=['POST'])
def calcular_tiempo():
    try:
        i = float(request.form['i'])
        VA = float(request.form['VA'])
        TNA = float(request.form['TNA'])

        years = int(i / 365)
        months = int((i % 365) / 30)
        days = int(i % 30)

        return render_template('index.html', years=years, months=months, days=days, mostrar_formulas=session['mostrar_formulas'])
    except ValueError:
        return "Error: Asegúrate de que todos los campos sean válidos y numéricos."

@app.route('/CI', methods=['POST'])
def CI():
    try:
        VA = float(request.form['VA'])
        TNA = float(request.form['TNA'])
        selectTiempo = request.form['selectTiempo']
        result_ci = 0  # Placeholder para tu lógica de CI

        return render_template('index.html', result_ci=result_ci, mostrar_formulas=session['mostrar_formulas'])
    except ValueError:
        return "Error: Asegúrate de que todos los campos sean válidos y numéricos."

@app.route('/TEA', methods=['POST'])
def TEA():
    try:
        TNA = float(request.form['TNA'])
        ISR = float(request.form['ISR'])
        result_tea = 0  # Placeholder para tu lógica de TEA

        return render_template('index.html', result_tea=result_tea, mostrar_formulas=session['mostrar_formulas'])
    except ValueError:
        return "Error: Asegúrate de que todos los campos sean válidos y numéricos."

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
