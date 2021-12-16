# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 16:15:24 2021

@author: Marvin Nöller
"""

# Importieren der benötigten Pakete
import os
import pandas as pd
import statsmodels.api as sm
import scipy.stats


# Pfad zum Ordner. Muss individuell angepasst werden
os.chdir("C:/Users/Chantal/sciebo/Ewifo/WS2122/Übung_neu/Thema 5")

##############################################################################
############### Aufgabe 5.3 ##################################################
##############################################################################

# Einlesen der Daten
data = pd.read_excel("trmgpa.xlsx","Sheet1")

##############################################################################
# a)

# Erklärende Variable
x = data[['cumgpa']]
# Konstante hinzufügen
x = pd.DataFrame(sm.add_constant(x.values, has_constant='add'), \
                    columns = ['constant'] + x.columns.tolist())

# abhängige Variable
y = data[['trmgpa']]

# Schätzung des Modells
model_gpa = sm.OLS(y, x).fit()

# Ausgabe des fehlenden Parameters, gerundet auf 4 Nachkommastellen
print('Geschätzter Parameter: ', round(model_gpa.params['cumgpa'],4))

##############################################################################
# b)

# Wenn das Modell bereits geschätzt ist, lassen sich Tests in Python sehr
# leicht durchführen

# Wir testen ob der Koeffizient der Konstante unterschiedlich von 2 ist

# Erst führen wir den Test durch
t_test1 = model_gpa.t_test('constant = 2')
# Dann lassen wir uns den Wert der Teststatistik ausgeben
T_act = t_test1.tvalue.item() # .item() um kein array zu bekommen

# Als nächstes benötigen wir den kritischen Wert. Hierzu legen wir das
# Signifikanzniveau, sowie die Parameter n und k fest
sig_level = 0.01
n = model_gpa.nobs
k = model_gpa.df_model + model_gpa.k_constant
# Kritischer Wert
T_crit =scipy.stats.t.ppf((1-sig_level/2), n-k)

# Wir können uns die realisierte Teststatistik und den kritischen Wert
# anzeigen lassen und dann den Test händisch durchführen.
print('Realisierte Teststatistik, Aufgabenteil b): ', T_act)
print('Kritischer Wert,  Aufgabenteil b): ', T_crit)

# Wir können die Testentscheidung aber auch von Python fällen lassen
if abs(T_act) > T_crit :
    print('H0 von Aufgabenteil b) wird abgelehnt')
else:
    print('H0 von Aufgabenteil b) wird nicht abgelehnt')

# Alternativ können wir uns auch den p-Wert ausgeben lassen
p_value1 = t_test1.pvalue

# Auch hier können wir uns den p Wert anschauen und selbst mit dem Signifikanz
# Niveau vergleichen
print('p-Wert: ', p_value1)
# Oder wir lassen wieder Python die Entscheidung fällen
if p_value1 < sig_level :
    print('H0 von Aufgabenteil b) wird abgelehnt')
else:
    print('H0 von Aufgabenteil b) wird nicht abgelehnt')

##############################################################################
# c)

# Die Durchführung des Tests funktioniert analog zu Aufgabenteil b)
# Hier führen wir den Test nur mit Hilfe des p-Wertes durch

# Signifikanzniveau festlegen
sig_level_c = 0.1

# Test durchführen
t_test2 = model_gpa.t_test('cumgpa = 0.25')
# p-Wert ausgeben lassen
p_value2 = t_test2.pvalue
print('p-Wert, Aufgabenteil c): ', p_value2)
# Testentscheidung fällen
if p_value2 < sig_level_c :
    print('H0 von Aufgabenteil c) wird abgelehnt')
else:
    print('H0 Aufgabenteil c) wird nicht abgelehnt')
