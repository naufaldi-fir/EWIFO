# -*- coding: utf-8 -*-
"""
Created on Tue Sep 21 10:15:45 2021

@author: Chantal
"""

import os
import pandas as pd
import statsmodels.api as sm
import numpy as np

# Pfad zum Ordner. Muss individuell angepasst werden
os.chdir("C:/Users/Chantal/sciebo/Ewifo/WS2122/Übung_neu/Thema 8")

##############################################################################
############### Aufgabe 8.1 #################################################
##############################################################################

# Auslesen der Daten
data = pd.read_excel("affairs.xlsx","Sheet1")

# Um das Regressionsmodell zu schätzen, muss der Interaktionsterm zwischen male und
#yrsmarr definiert werden und die  Matrix x aller Regressoren (inklusive Konstante)
#gebildet werden
data['male_yrsmarr'] = data['male']*data['yrsmarr']
x1 = data[['yrsmarr','kids','male','male_yrsmarr']]
x = pd.DataFrame(sm.add_constant(x1.values, has_constant='add'), \
                    columns = ['const'] + x1.columns.tolist())

# Abhängige Variable
y = data[['affair']]

# Regression und Ausgabe des Modells
model_affair1 = sm.OLS(y, x).fit()


##############################################################################
# a)

print('Geschätzter Effekt von kids auf affair: ', model_affair1.params['kids'])

##############################################################################
# b)

# Berechnnung der geschätzten Wahrscheinlichkeit einer außerehelichen Affäre anhand der
#Charakteristika der interviewten Person und der geschätzten Koeffizienten.
expected_affair = model_affair1.params['const'] \
                 + model_affair1.params['yrsmarr'] * 25 \
                 + model_affair1.params['kids'] * 1 \
                 + model_affair1.params['male'] * 0 \
                 + model_affair1.params['male_yrsmarr'] * 0 *25

print('Geschätzte Wahrscheinlichkeit einer außerehelichen Affäre: ', expected_affair)

##############################################################################
# c)

# Berechnung des Stichprobenmittels von yrsmarr
meanyrs=round(np.mean(data['yrsmarr']),0)

# Geschätzter Effekt von male auf affairs am Durschnitt von yrsmarr (MEA)

expected_effect = model_affair1.params['male'] * 1 \
                 + model_affair1.params['male_yrsmarr'] * 1 *meanyrs

print('Geschätzter marginaler Effekt von male auf affair am Durschnitt der Ehedauer:', expected_effect)
