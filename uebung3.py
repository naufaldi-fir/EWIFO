
"""
Created on Fri Sep 10 14:43:09 2021

@author: Marvin Nöller
"""

# Importieren der benötigten Pakete
import os
import pandas as pd
import statsmodels.api as sm

# Pfad zum Ordner. Muss individuell angepasst werden
os.chdir("C:/Users/Chantal/sciebo/Ewifo/WS2122/Übung_neu/Thema 3")

##############################################################################
############### Aufgabe 3.2  #################################################
##############################################################################

# Daten einlesen
data = pd.read_excel("houseprice.xlsx","Sheet1")

##############################################################################
# a)

# Abhängige Variable
YVar = data[['price']]

# Erklärende Variable
XVar = data[['sqrft']]
# Konstante hinzufügen
XVar = pd.DataFrame(sm.add_constant(XVar.values, has_constant='add'), \
                    columns = ['constant'] + XVar.columns.tolist())

# Schätzung
model_house_price = sm.OLS(YVar, XVar).fit()

# Koeffizienten der Schätzung anzeigen. \n startet eine neue Zeile
print('Geschätzte Koeffizienten: \n', model_house_price.params)

# Alternativ: den gesamten Schätzoutput anzeigen
print(model_house_price.summary())

##############################################################################
# b)

# Man kann sich auch nur den Parameter zu einer bestimmten Variablen anschauen
print('Parameter sqrft:', model_house_price.params['sqrft'])

# Gerundet
print('Parameter sqrft gerundet:', round(model_house_price.params['sqrft'],4))

##############################################################################
# c)

# Summe der quadrierten Residueen. Hier können wir auch die Ergebnisse der
# Modellschätzung zurückgreifen.
print('Summe der quadrierten Residueen:', model_house_price.ssr)

# Für die Stichprobenvarianz können wir nicht auf die Modellergebnisse zurück-
# greifen. Hier nehmen wir die Funktion pd.var(). Wichtig: bei neuen
# Funktionen immer die Dokumentation checken. Hier ist es zum Beispiel
# wichtig darauf zu achten, dass auch wirklich die Stichprobenvarianz
# berechnet wird, d.h. duch n-1 geteilt wird.
print('Stichprobenvarianz:', data.var()['price'])

##############################################################################
# d)

# R2. Auch hier können wir wieder auf die Modellschätzung zurückgreifen.
print('R2: ', model_house_price.rsquared)

##############################################################################
# f)

# Erstellung der Variablen price_euro und sqrmtr. Wir fügen die neuen
# Variablen direkt unserem Dataframe "data" hinzu.
data['price_euro'] = data['price'] * 0.88
data['sqrmtr'] = data['sqrft'] * 0.0929

# Erklärende Variable inklusive Konstante
XVar_f = data[['sqrmtr']]
XVar_f = pd.DataFrame(sm.add_constant(XVar_f.values, has_constant='add'), \
                      columns = ['constant'] + XVar_f.columns.tolist())

# Abhängige Variable
YVar_f = data[['price_euro']]

# Modellschätzung
model_house_price_f = sm.OLS(YVar_f, XVar_f).fit()

# Ausgabe der Parameter
print(model_house_price_f.params)
