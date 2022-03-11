# -*- coding: utf-8 -*-
"""
Created on Fri Jan 21 09:58:52 2022

@author: Chantal
"""



import os
import pandas as pd
import statsmodels.api as sm
import numpy as np
import scipy.stats
from sklearn.metrics import (accuracy_score)

#Festsetzen des Pfads zum Odner, in dem sich das Scriptfile und der Datensatz befinden
os.chdir("C:/Users/Chantal/sciebo/Ewifo/WS2122/Übung_neu/Thema 8")

##############################################################################
############### Aufgabe 12.1 #################################################
##############################################################################

# Auslesen der Daten
data = pd.read_excel("affairs.xlsx","Sheet1")

# Erklärende Variablen
x = data[['yrsmarr','kids','male']]
x = pd.DataFrame(sm.add_constant(x.values, has_constant='add'), \
                    columns = ['const'] + x.columns.tolist())

# Abhängige Variable
y = data[['affair']]

##############################################################################
# a)

# Regression
model_affair1 = sm.OLS(y,x).fit() #LPM/OLS-Schätzung
model_affair2 = sm.Probit(y,x).fit() #Probit-Schätzung
model_affair3 = sm.Logit(y,x).fit() #Logit-Schätzung

#Ausgabe der drei Modelle
print('Regressionsoutput der LPM-Regression: \n', model_affair1.summary())
print('Regressionsoutput der Probit-Regression: \n',model_affair2.summary())
print('Regressionsoutput der Logit-Regression: \n', model_affair3.summary())

##############################################################################
# h)

#Berechnung von hat(y) für alle Beobachtungen im Datensatz und alle drei Modelle
yhat1=model_affair1.predict()
yhat2=model_affair2.predict()
yhat3=model_affair3.predict()

#Ersetze yhat durch 1, falls yhat>=0.5 und durch 0, falls yhat<0.5
pyhat1 = np.where(yhat1 >= 0.5, 1, yhat1)
pyhat1 = np.where(pyhat1 < 0.5, 0, pyhat1)
pyhat2 = np.where(yhat2 >= 0.5, 1, yhat2)
pyhat2 = np.where(pyhat2 < 0.5, 0, pyhat2)
pyhat3 = np.where(yhat3 >= 0.5, 1, yhat3)
pyhat3 = np.where(pyhat3 < 0.5, 0, pyhat3)

#Berechnung und Ausgabe des korrekt vorhergesagten Anteils der Beobchtungen y in den drei Modellen
print('Korrekt vorhergesagter Anteil der LPM-Schätzung= ', accuracy_score(y, pyhat1))
print('Korrekt vorhergesagter Anteil der Probit-Schätzung = ', accuracy_score(y, pyhat2))
print('Korrekt vorhergesagter Anteil der Logit-Schätzung = ', accuracy_score(y, pyhat3))


##############################################################################
# i)

#Ausgabe der AMEs (average marginal effect) der Probit-Schätzung
print('Geschätzte durchschnittliche marginale Effekte der Probit-Schätzung \n: '
      , model_affair2.get_margeff(dummy=True).summary())



##############################################################################
# j)

# Als erstes schätzen wir das Modell inklusive yrsmarr^2
data['yrsmarr_sq'] = data[['yrsmarr']]**2
x2 = data[['yrsmarr','yrsmarr_sq','kids','male']]
x2 = pd.DataFrame(sm.add_constant(x2.values, has_constant='add'), \
                    columns = ['const'] + x2.columns.tolist())

model_affair4 = sm.Probit(y,x2).fit()

# Likelihood Werte für beide Probit-Modelle ausgeben lassen
L_r = model_affair2.llf
L_ur = model_affair4.llf

# Signifikanzniveau
alphaLR = 0.05
# Teststatistik
LR = 2*(L_ur - L_r)
# Kritischer Wert
chi_krit = scipy.stats.chi2.ppf((1-alphaLR),1)

print('Teststatistik Likelihood Ratio Test: ', LR)
print('Dazugehöriger Kritischer Wert: ', chi_krit)
