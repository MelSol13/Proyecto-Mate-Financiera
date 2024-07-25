from flask import Flask, render_template, request

app = Flask("proyecto-mate-financiera")

@app.route('/')
def index():
    return render_template('index.html', result=None)

@app.route('/sum', methods=['POST'])
def sum():
    num1 = request.form['num1']
    num2 = request.form['num2']
    result = int(num1) + int(num2)
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)