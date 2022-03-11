# -*- coding: utf-8 -*-
"""
Created on Tue Sep 21 13:50:37 2021

@author: Chantal
"""
import os
import pandas as pd
import statsmodels.api as sm
from statsmodels.sandbox.regression.gmm import IV2SLS

#Festsetzen des Pfads zum Odner, in dem sich das Scriptfile und der Datensatz befinden
os.chdir("C:/Users/Chantal/sciebo/Ewifo/WS2122/Übung_neu/Thema 11")

##############################################################################
############# Exercise 11.3 ###################################################
##############################################################################

# Auslesen der Daten
data = pd.read_excel("cigarettes1.xlsx","Sheet1")
print('Variablen im Datensatz: \n', data.columns.values)

# Abhängige Variablen und Regressoren
y=data[['logQcig']]
x1=data[['logPcig']]
x = pd.DataFrame(sm.add_constant(x1.values, has_constant='add'), \
                    columns = ['constant'] + x1.columns.tolist())


# Schätzung ohne Berücksichtigung der Endogenität
cigreg = sm.OLS(y,x).fit()

##############################################################################
# a)

# Schätzung der ersten Stufe der TSLS-Regression. Annahme: ln(Pcig) ist die endogene Variable
# und Tcig das Instrument. In der 1. Stufe der TSLS-Schätzung ist die endogene Variable
# ln(Pcig) die abhängige Variable und das Instrument der Regressor.
x_IV = data[['Tcig']]
y_IV = x1
x_IV = pd.DataFrame(sm.add_constant(x_IV.values, has_constant='add'), columns = ['Konstante'] + x_IV.columns.tolist())
ivreg1 = sm.OLS(y_IV,x_IV).fit()
print('Koeffizienten der 1. Stufe der TSLS-Schätzung \n', ivreg1.params)


# Schätzung der zweiten Stufe der TSLS-Regression. In der 2. Stufe der TSLS-Schätzung ist
# ln(Qcig) die ahängige Variable und die geschätzte Variable hat(ln(Pcig)) der 1. Stufe
# ist der Regressor.
data['Pcighat']=ivreg1.predict(x_IV)
x_IV2= data[['Pcighat']]
x_IV2 = pd.DataFrame(sm.add_constant(x_IV2.values, has_constant='add'), columns = ['Konstante'] + x_IV2.columns.tolist())
y_IV2= y
ivreg2 = sm.OLS(y_IV2, x_IV2).fit()
print('Koeffizienten der 2. Stufe der TSLS-Schätzung \n', ivreg2.params)


##############################################################################
# c)

print('Steigungskoeffizient der 2.Stufe der TSLS-Schätzung: \n ', round(ivreg2.params['Pcighat'],4))


##############################################################################
# e)

resultIV = IV2SLS(y,x,x_IV).fit()
print('Koeffizienten der IV-Schätzung mit richtigen Standardfehlern \n', resultIV.params)

print('Standardfehler der 2. Stufe der TSLS-Schätzung \n', ivreg2.bse)
print('Standardfehler der IV-Schätzung mit richtigen Standardfehlern \n', resultIV.bse)
