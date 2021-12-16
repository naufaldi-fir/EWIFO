# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 14:30:08 2021

@author: Marvin Nöller
"""

# Importieren der benötigten Pakete
import os
import pandas as pd
import statsmodels.api as sm


# Pfad zum Ordner. Muss individuell angepasst werden
os.chdir("C:/Users/Chantal/sciebo/Ewifo/WS2122/Übung_neu/Thema 4")

##############################################################################
############### Aufgabe 4.2 ##################################################
##############################################################################

# Daten einlesen
data = pd.read_excel("houseprice.xlsx","Sheet1")

##############################################################################
# a)

# Wir erstellen zwei Blöcke an erklärenden Variablen, um die beiden Modelle zu
# schätzen.

# Erklärende Variablen Modell 1
x1 = data[['sqrft']]
x1 = pd.DataFrame(sm.add_constant(x1.values, has_constant='add'), \
                    columns = ['constant'] + x1.columns.tolist())

# Erklärende Variablen Modell 2
x2 = data[['sqrft', 'bdrms']]
x2 = pd.DataFrame(sm.add_constant(x2.values, has_constant='add'), \
                    columns = ['constant'] + x2.columns.tolist())

# Die abhängige Variable ist in beiden Modellen die selbe
y = data[['price']]

# Schätzung der Modelle
model_house_price1 = sm.OLS(y, x1).fit()
model_house_price2 = sm.OLS(y, x2).fit()

# Schätzergebnisse anzeigen, aus denen wir die Gleichungen aufschreiben können
print(model_house_price1.summary())
print(model_house_price2.summary())


##############################################################################
# c)

# Wir multiplizieren die geschätzen Koeffizienten mit den Angaben aus der
# Aufgabe

# Zunächst schreiben wir die Angaben in entsprechende Variablen
sqrft_exercise = 2438
bdrms_exercise = 4

# Danach können wir den erwarteten Preis berechnen
expected_price = model_house_price2.params['constant'] \
                 + model_house_price2.params['sqrft'] * sqrft_exercise \
                 + model_house_price2.params['bdrms'] * bdrms_exercise

print('Erwarteter Verkaufspreis: ', expected_price)

##############################################################################
# d)

# Hier lassen wir uns jeweils die R2 der jeweiligen Modelle ausgeben.
# Alternativ kann man die auch direkt aus den Outputs aus a) ablesen
print('R2 Modell 1: ', model_house_price1.rsquared)
print('R2 Modell 2: ', model_house_price2.rsquared)

##############################################################################
# e)

# Analog zu d)
print('Adjustiertes R2 Modell 1: ', model_house_price1.rsquared_adj)
print('Adjustiertes R2 Modell 2: ', model_house_price2.rsquared_adj)
