import numpy as np
import skfuzzy as fuzz
import skfuzzy.control as ctrl

# Variables difusas
temperatura = ctrl.Antecedent(np.arange(15, 31, 1), 'temperatura')
potencia = ctrl.Consequent(np.arange(0, 101, 1), 'potencia')

# Definir funciones de pertenencia
temperatura['baja'] = fuzz.trimf(temperatura.universe, [15, 15, 22])
temperatura['media'] = fuzz.trimf(temperatura.universe, [20, 23, 26])
temperatura['alta'] = fuzz.trimf(temperatura.universe, [24, 30, 30])

potencia['baja'] = fuzz.trimf(potencia.universe, [0, 0, 50])
potencia['media'] = fuzz.trimf(potencia.universe, [30, 50, 70])
potencia['alta'] = fuzz.trimf(potencia.universe, [60, 100, 100])

# Reglas difusas
rule1 = ctrl.Rule(temperatura['baja'], potencia['baja'])
rule2 = ctrl.Rule(temperatura['media'], potencia['media'])
rule3 = ctrl.Rule(temperatura['alta'], potencia['alta'])

# Controlador difuso
ac_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
ac = ctrl.ControlSystemSimulation(ac_ctrl)

# Simulación
temp = 23
ac.input['temperatura'] = temp
ac.compute()


print(f"Temperatura: {temp} - Potencia del aire acondicionado: {ac.output['potencia']:.2f}%")
