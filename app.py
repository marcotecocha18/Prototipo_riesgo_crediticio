# app.py
from flask import Flask, request, jsonify, render_template
from fuzzy_model import evaluar_riesgo

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/riesgo', methods=['POST'])
def api_riesgo():
    datos = request.get_json()

    try:
        limite_credito = float(datos.get('limite_credito', 0))
        deuda_actual   = float(datos.get('deuda_actual', 0))
        max_atraso     = float(datos.get('max_atraso', 0))
        edad           = float(datos.get('edad', 0))
        porcentaje_pago = float(datos.get('porcentaje_pago', 0))
    except (TypeError, ValueError):
        return jsonify({"error": "Parámetros inválidos"}), 400

    riesgo_crisp, etiqueta = evaluar_riesgo(
        limite_credito=limite_credito,
        deuda_actual=deuda_actual,
        max_atraso_val=max_atraso,
        edad_val=edad,
        porcentaje_pago_val=porcentaje_pago
    )

    return jsonify({
        "limite_credito": limite_credito,
        "deuda_actual": deuda_actual,
        "max_atraso": max_atraso,
        "edad": edad,
        "porcentaje_pago": porcentaje_pago,
        "riesgo_crisp": riesgo_crisp,
        "riesgo_etiqueta": etiqueta
    })

if __name__ == "__main__":
    app.run(debug=True)
