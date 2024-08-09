from flask import Flask, jsonify, request, session, redirect, url_for, render_template, send_from_directory

app = Flask("proyecto-mate-financiera")
app.secret_key = 'supersecretkey'

@app.route('/images/<path:filename>')
def images(filename):
    return send_from_directory('images', filename)

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'mostrar_formulas' not in session:
        session['mostrar_formulas'] = False

    if request.method == 'POST' and 'toggle_formulas' in request.form:
        session['mostrar_formulas'] = not session['mostrar_formulas']
        return redirect(url_for('index') + '#info-boxes')

    return render_template('index.html', mostrar_formulas=session['mostrar_formulas'])

@app.route('/VF', methods=['POST'])
def VF():
    try:
        VA = float(request.form['VA'])
        i = float(request.form['i']) / 100
        tiempo = float(request.form['tiempo'])
        selectTiempo = request.form['selectTiempo']

        if selectTiempo == 'opcion1':
            result_vf = VA * (1 + i * tiempo)
        elif selectTiempo == 'opcion2':
            result_vf = VA * (1 + (i / 12) * tiempo)
        elif selectTiempo == 'opcion3':
            result_vf = VA * (1 + (i / 360) * tiempo)
        else:
            return jsonify({"error": "Unidad de tiempo no reconocida."})

        result_vf_formatted = "{:,.2f}".format(result_vf)
        return jsonify({"result_vf": result_vf_formatted})
    except ValueError:
        return jsonify({"error": "Asegúrate de que todos los campos sean válidos y numéricos."})

@app.route('/VA', methods=['POST'])
def VA():
    try:
        VF = float(request.form['VF'])
        I = float(request.form['I'])
        TNA = float(request.form['TNA']) / 100
        tiempo = float(request.form['tiempo'])
        selectTiempo = request.form['selectTiempo']

        if selectTiempo == 'opcion1':
            result_va = VF / (1 + TNA * tiempo)
        elif selectTiempo == 'opcion2':
            result_va = VF / (1 + (TNA / 12) * tiempo)
        elif selectTiempo == 'opcion3':
            result_va = VF / (1 + (TNA / 360) * tiempo)
        else:
            return jsonify({"error": "Unidad de tiempo no reconocida."})

        result_va_formatted = "{:,.2f}".format(result_va)
        return jsonify({"result_va": result_va_formatted})
    except ValueError:
        return jsonify({"error": "Asegúrate de que todos los campos sean válidos y numéricos."})

@app.route('/TNA', methods=['POST'])
def TNA():
    try:
        I = float(request.form['I'])
        VA = float(request.form['VA'])
        tiempo = float(request.form['tiempo'])
        selectTiempo = request.form['selectTiempo']

        if selectTiempo == 'opcion1':
            result_tna = (I / (VA * tiempo)) * 100
        elif selectTiempo == 'opcion2':
            result_tna = (I / (VA * (tiempo / 12))) * 100
        elif selectTiempo == 'opcion3':
            result_tna = (I / (VA * (tiempo / 360))) * 100
        else:
            return jsonify({"error": "Unidad de tiempo no reconocida."})

        result_tna_formatted = "{:,.2f}".format(result_tna)
        return jsonify({"result_tna": result_tna_formatted})
    except ValueError:
        return jsonify({"error": "Asegúrate de que todos los campos sean válidos y numéricos."})

@app.route('/tiempo', methods=['POST'])
def calcular_tiempo():
    try:
        i = float(request.form['i'])
        VA = float(request.form['VA'])
        TNA = float(request.form['TNA']) / 100
        result = i / (VA * TNA)
        
        years = int(result)
        months = int((result - years) * 12)
        days = int((result - years - (months / 12)) * 365)

        return jsonify({"years": years, "months": months, "days": days})
    except ValueError:
        return jsonify({"error": "Asegúrate de que todos los campos sean válidos y numéricos."})

@app.route('/CI', methods=['POST'])
def CI():
    try:
        VA = float(request.form['VA'])
        i = float(request.form['i']) / 100
        tiempo = float(request.form['tiempo'])
        selectTiempo = request.form['selectTiempo']

        if selectTiempo == 'opcion1':
            result_ci = ( VA * i * tiempo )
        elif selectTiempo == 'opcion2':
            result_ci = VA * i * tiempo
        elif selectTiempo == 'opcion3':
            result_ci = VA * i * tiempo
        else:
            return jsonify({"error": "Unidad de tiempo no reconocida."})

        result_ci_formatted = "{:,.2f}".format(result_ci)
        return jsonify({"result_ci": result_ci_formatted})
    except ValueError:
        return jsonify({"error": "Asegúrate de que todos los campos sean válidos y numéricos."})

@app.route('/TEA', methods=['POST'])
def TEA():
    try:
        TNA = float(request.form['TNA']) / 100
        ISR = float(request.form['ISR']) / 100
        result_tea = TNA * (1 - ISR) * 100

        return jsonify({"result_tea": result_tea})
    except ValueError:
        return jsonify({"error": "Asegúrate de que todos los campos sean válidos y numéricos."})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)