# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 14:22:37 2021

@author: Marvin Nöller
"""

# Importieren der benötigten Pakete
import os
import pandas as pd
import statsmodels.api as sm
import numpy as np
import matplotlib.pyplot as plt


# Pfad zum Ordner. Muss individuell angepasst werden
os.chdir("C:/Users/Chantal/sciebo/Ewifo/WS2122/Übung_neu/Thema 7")

##############################################################################
############# Exercise 7.1 ###################################################
##############################################################################

# Einlesen der Daten
data = pd.read_excel("wage.xlsx","Sheet1")

# Erstellen der Variablen log(wage) und exper^2. Hierzu benötigen wir das
# package numpy, welches wir oben als np geladen haben
data['lwage'] = np.log(data['wage'])
data['expersq'] = np.square(data['exper'])

# Abhängige Variable
y = data[['lwage']]
# Erklärende Variablen inkl. Konstante
x = data[['educ', 'exper', 'expersq']]
x = pd.DataFrame(sm.add_constant(x.values, has_constant='add'), \
                    columns = ['constant'] + x.columns.tolist())

# Schätzung des Modells
mincer = sm.OLS(y,x).fit()

##############################################################################
# b)

# Das R2 wird im Schätzoutput gespeichert
print('R2: ', mincer.rsquared)

##############################################################################
# c)

# p-Wert aus Schätzoutput nehmen
p_value_expersq = mincer.pvalues['expersq']
# Signifikanzlevel festlegen
sig_level_c = 0.01

# Test Entscheidung
if p_value_expersq < sig_level_c:
    print('beta_3 ist signifikant verschieden von Null')
elif p_value_expersq >= sig_level_c:
    print('beta_3 ist nicht signifikant verschieden von Null')

##############################################################################
# d)

# Die beiden Level an experience festlegen
exper_level_1 = 4
exper_level_2 = 19

# Marginalen Effekt mit Hilfe der Schätzergebnisse ausrechnen
marg_effect_1 = mincer.params['exper'] \
                + 2 * mincer.params['expersq'] * exper_level_1

marg_effect_2 = mincer.params['exper'] \
                + 2 * mincer.params['expersq'] * exper_level_2

print('Marginaler Effekt für experience von ',exper_level_1 ,': ', marg_effect_1)
print('Marginaler Effekt für experience von ',exper_level_2 ,': ', marg_effect_2)

##############################################################################
######### Den restlichen Code müssen Sie nicht können ########################
##############################################################################

##############################################################################
# e)

# Grid für mögliche Werte an Erfahrung
grid_exper = np.linspace(0,45,100)
# Damit einhergehender Lohn laut Schätzung
grid_log_wage = mincer.params['exper'] * grid_exper \
              + mincer.params['expersq'] * grid_exper**2

# Plot
plt.plot(grid_exper, grid_log_wage)
plt.xlabel('Arbeitserfahrung')
plt.ylabel('log-Lohn')
