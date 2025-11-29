# fuzzy_model.py
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# ==============================
# DEFINICIÓN DE LOS UNIVERSOS
# ==============================

# 1) Ingreso aproximado (límite de crédito) [0, 800 000]
ingreso = ctrl.Antecedent(np.linspace(0, 800000, 200), 'ingreso')
ingreso['bajo']  = fuzz.trapmf(ingreso.universe, [0,      0,      150000, 300000])
ingreso['medio'] = fuzz.trapmf(ingreso.universe, [150000, 300000, 300000, 500000])
ingreso['alto']  = fuzz.trapmf(ingreso.universe, [300000, 500000, 800000, 800000])

# 2) Nivel de deuda (ratio deuda / límite) [0, 2]
nivel_deuda = ctrl.Antecedent(np.linspace(0, 2.0, 200), 'nivel_deuda')
nivel_deuda['baja']  = fuzz.trapmf(nivel_deuda.universe, [0.0, 0.0, 0.3, 0.6])
nivel_deuda['media'] = fuzz.trapmf(nivel_deuda.universe, [0.3, 0.6, 0.6, 1.0])
nivel_deuda['alta']  = fuzz.trapmf(nivel_deuda.universe, [0.6, 1.0, 2.0, 2.0])

# 3) Historial de pago (máximo atraso) [-2, 8]
historial_pago = ctrl.Antecedent(np.linspace(-2, 8, 200), 'historial_pago')
historial_pago['bueno']   = fuzz.trapmf(historial_pago.universe, [-2, -2, 0, 1])
historial_pago['regular'] = fuzz.trapmf(historial_pago.universe, [0, 1, 1, 3])
historial_pago['malo']    = fuzz.trapmf(historial_pago.universe, [1, 3, 8, 8])

# 4) Edad [18, 75]
edad = ctrl.Antecedent(np.linspace(18, 75, 200), 'edad')
edad['joven']  = fuzz.trapmf(edad.universe, [18, 18, 25, 35])
edad['adulto'] = fuzz.trapmf(edad.universe, [25, 35, 45, 55])
edad['mayor']  = fuzz.trapmf(edad.universe, [45, 55, 75, 75])

# 5) Porcentaje de pago mensual (0% - 150%)
porcentaje_pago = ctrl.Antecedent(np.linspace(0, 150, 200), 'porcentaje_pago')
porcentaje_pago['bajo']  = fuzz.trapmf(porcentaje_pago.universe, [0,   0,   30,  60])
porcentaje_pago['medio'] = fuzz.trapmf(porcentaje_pago.universe, [30,  60,  60, 100])
porcentaje_pago['alto']  = fuzz.trapmf(porcentaje_pago.universe, [60, 100, 150, 150])

# Salida: riesgo crediticio [0,1]
riesgo_crediticio = ctrl.Consequent(np.linspace(0, 1, 201), 'riesgo_crediticio')
riesgo_crediticio['bajo']  = fuzz.trapmf(riesgo_crediticio.universe, [0.0, 0.0, 0.2, 0.4])
riesgo_crediticio['medio'] = fuzz.trapmf(riesgo_crediticio.universe, [0.2, 0.4, 0.6, 0.8])
riesgo_crediticio['alto']  = fuzz.trapmf(riesgo_crediticio.universe, [0.6, 0.8, 1.0, 1.0])

# ==============================
# REGLAS MANUALES
# ==============================

# Las reglas se definen explícitamente en base a lo que consideres como "riesgo bajo/medio/alto"

reglas = [
    # Escenarios de riesgo ALTO
    ctrl.Rule(ingreso['bajo'] & nivel_deuda['alta'] & historial_pago['malo'] & edad['mayor'] & porcentaje_pago['bajo'], riesgo_crediticio['alto']),
    ctrl.Rule(ingreso['bajo'] & nivel_deuda['alta'] & historial_pago['regular'] & edad['adulto'] & porcentaje_pago['bajo'], riesgo_crediticio['alto']),
    ctrl.Rule(ingreso['medio'] & nivel_deuda['alta'] & historial_pago['malo'] & edad['mayor'] & porcentaje_pago['bajo'], riesgo_crediticio['alto']),
    ctrl.Rule(ingreso['bajo'] & nivel_deuda['media'] & historial_pago['malo'] & edad['mayor'] & porcentaje_pago['bajo'], riesgo_crediticio['alto']),
    ctrl.Rule(ingreso['medio'] & nivel_deuda['alta'] & historial_pago['malo'] & edad['mayor'] & porcentaje_pago['medio'], riesgo_crediticio['alto']),
    ctrl.Rule(ingreso['alto'] & nivel_deuda['alta'] & historial_pago['malo'] & edad['mayor'] & porcentaje_pago['medio'], riesgo_crediticio['alto']),

    # Escenarios de riesgo MEDIO
    ctrl.Rule(ingreso['bajo'] & nivel_deuda['media'] & historial_pago['regular'] & edad['adulto'] & porcentaje_pago['medio'], riesgo_crediticio['medio']),
    ctrl.Rule(ingreso['medio'] & nivel_deuda['media'] & historial_pago['regular'] & edad['adulto'] & porcentaje_pago['medio'], riesgo_crediticio['medio']),
    ctrl.Rule(ingreso['medio'] & nivel_deuda['media'] & historial_pago['bueno'] & edad['adulto'] & porcentaje_pago['medio'], riesgo_crediticio['medio']),
    ctrl.Rule(ingreso['alto'] & nivel_deuda['baja'] & historial_pago['bueno'] & edad['adulto'] & porcentaje_pago['alto'], riesgo_crediticio['medio']),

    # Escenarios de riesgo BAJO
    ctrl.Rule(ingreso['alto'] & nivel_deuda['baja'] & historial_pago['bueno'] & edad['joven'] & porcentaje_pago['alto'], riesgo_crediticio['bajo']),
    ctrl.Rule(ingreso['alto'] & nivel_deuda['media'] & historial_pago['bueno'] & edad['joven'] & porcentaje_pago['alto'], riesgo_crediticio['bajo']),
    ctrl.Rule(ingreso['medio'] & nivel_deuda['baja'] & historial_pago['bueno'] & edad['joven'] & porcentaje_pago['alto'], riesgo_crediticio['bajo']),
    ctrl.Rule(ingreso['bajo'] & nivel_deuda['baja'] & historial_pago['bueno'] & edad['joven'] & porcentaje_pago['alto'], riesgo_crediticio['bajo']),
    ctrl.Rule(ingreso['bajo'] & nivel_deuda['baja'] & historial_pago['bueno'] & edad['adulto'] & porcentaje_pago['alto'], riesgo_crediticio['bajo']),
    ctrl.Rule(ingreso['alto'] & nivel_deuda['media'] & historial_pago['regular'] & edad['joven'] & porcentaje_pago['alto'], riesgo_crediticio['bajo']),
]

sistema_riesgo = ctrl.ControlSystem(reglas)

# ==============================
# FUNCIÓN DE EVALUACIÓN PÚBLICA
# ==============================

def evaluar_riesgo(limite_credito: float,
                   deuda_actual: float,
                   max_atraso_val: float,
                   edad_val: float,
                   porcentaje_pago_val: float):
    """
    Evalúa el riesgo crediticio difuso.
    """
    # Evitar división entre 0
    limite_seguro = max(limite_credito, 1.0)
    ratio = deuda_actual / limite_seguro

    sim = ctrl.ControlSystemSimulation(sistema_riesgo)

    sim.input['ingreso'] = limite_credito
    sim.input['nivel_deuda'] = ratio
    sim.input['historial_pago'] = max_atraso_val
    sim.input['edad'] = edad_val
    sim.input['porcentaje_pago'] = porcentaje_pago_val

    sim.compute()

    riesgo_crisp = sim.output['riesgo_crediticio']

    # Clasificar el valor crisp en bajo / medio / alto
    universo = riesgo_crediticio.universe
    mf_bajo  = riesgo_crediticio['bajo'].mf
    mf_medio = riesgo_crediticio['medio'].mf
    mf_alto  = riesgo_crediticio['alto'].mf

    grado_bajo  = fuzz.interp_membership(universo, mf_bajo,  riesgo_crisp)
    grado_medio = fuzz.interp_membership(universo, mf_medio, riesgo_crisp)
    grado_alto  = fuzz.interp_membership(universo, mf_alto,  riesgo_crisp)

    grados = {
        'bajo':  grado_bajo,
        'medio': grado_medio,
        'alto':  grado_alto
    }

    etiqueta_riesgo = max(grados, key=grados.get)

    return float(riesgo_crisp), etiqueta_riesgo
