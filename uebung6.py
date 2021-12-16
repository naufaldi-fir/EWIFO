# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 09:05:26 2021

@author: Marvin Nöller
"""

# Importieren der benötigten Pakete
import os
import pandas as pd
import statsmodels.api as sm
import scipy.stats

# Pfad zum Ordner
os.chdir("C:/Users/Chantal/sciebo/Ewifo/WS2122/Übung_neu/Thema 6")

##############################################################################
############# Aufgabe 6.1  ###################################################
##############################################################################

# Daten einlesen
data = pd.read_excel("trmgpa.xlsx","Sheet1")

# Abhängige Variable für beide Modelle
y = data[['trmgpa']]

# Erklärende Variablen inkl Konstante, Modell 1
x1 = data[['cumgpa']]
x1 = pd.DataFrame(sm.add_constant(x1.values, has_constant='add'), \
                    columns = ['constant'] + x1.columns.tolist())

# Schätzung
model1 = sm.OLS(y,x1).fit()


##############################################################################
# a)

# Um das Konfidenzinvertall zu bestimmen, können wir unser geschätztes Modell
# verwenden. Wir müssen lediglich das Signifikanzniveau festlegen
sig_level_a = 0.05
ki = model1.conf_int(sig_level_a) #Konfidenzintervall für Konstante und cumgpa
ki_a = ki.iloc[1]  # Konfidenzintervall nur für cumgpa

print('Konfidenzintervall: [', ki_a[0], ',', ki_a[1], ']')

##############################################################################
# c)

# Wir führen einen einseitigen Test durch.

# Die Teststatistik erhalten wir mit dem gleichen Command wie für den
# zweiseitigen Test. Aber aufpassen, hier nehmen wir nicht den absolut Wert!
test_c = model1.t_test('cumgpa = 0.2')
T_real_c = test_c.tvalue.item()

# Signifikanzlevel
sig_level_c = 0.1
# Parameter n und k
n = model1.nobs
k = model1.df_model + model1.k_constant

# Kritischer Wert: Da wir einen einseitigen Test haben, teilen wir das
# Signifikanzlevel hier nicht durch zwei
T_crit_c = scipy.stats.t.ppf((1-sig_level_c), n-k)

print('Realisierter Wert, Aufgabenteil c)', T_real_c)
print('Kritischer Wert, Aufgabenteil c)', T_crit_c)

# Testentscheidung
if T_real_c > T_crit_c:
    print('H0 von Aufgabenteil c) wird abgelehnt')
else:
    print('H0 von Aufgabenteil c) wird nicht abgelehnt')

# Alternativ: Test über p-Wert
# Da wir einen einseitigen Test durchführen, können wir hier nicht den
# p-Wert von test_a nehmen (Vergleich uebung5.py)
# Stattdessen müssen wir den p-Wert "manuell" bestimmen
p_value_c = 1 - scipy.stats.t.cdf(T_real_c, n-k)
print('P-Wert, Aufgabenteil c): ', p_value_c)

# Testentscheidung
if p_value_c < sig_level_c:
    print('H0 von Aufgabenteil c) wird abgelehnt')
else:
    print('H0 von Aufgabenteil c) wird nicht abgelehnt')


##############################################################################
# d)

# Wieder ein einseitiger Test

# Teststatistik, Achtung nicht den absolut Wert benutzen
test_d = model1.t_test('constant = 1.8')
T_real_d = test_d.tvalue.item()

# Signifikanzlevel
sig_level_d = 0.05
# Die Parameter n und k sind gleich zu Aufgabe a)

# Kritischer Wert. Wieder aufpassen, Signifikanzniveau nicht durch 2 teilen
T_crit_d = scipy.stats.t.ppf((sig_level_d), n-k)

# Testentscheidung. Achtung hier ist die Testentscheidung umgekehrt!
print('Realisierter Wert, Aufgabenteil d)', T_real_d)
print('Kritischer Wert, Aufgabenteil d)', T_crit_d)

if T_real_d < T_crit_d:
    print('H0 von Aufgabenteil d) wird abgelehnt')
else:
    print('H0 von Aufgabenteil d) wird nicht abgelehnt')

# Alternativ wieder über den p-Wert. Aufpassen, hier nehmen wir nicht 1-cdf,
# dadurch können wir die Testentscheidung wie gewohnt fällen
p_value_d = scipy.stats.t.cdf(T_real_d, n-k)
print('P-Wert, Aufgabenteil d): ', p_value_d)


if p_value_d < sig_level_d:
    print('H0 von Aufgabenteil d) wird abgelehnt')
else:
    print('H0 von Aufgabenteil d) wird nicht abgelehnt')

##############################################################################
# e)

# Hier führen wir einen F-test durch

# Für die Durchführung des Tests können wir wieder auf unser geschätztes Modell
# zurückgreifen.
f_test_e = model1.f_test('(constant = cumgpa), (cumgpa = 0)')
# Realisierte Teststatistik
F_real_e = f_test_e.fvalue.item()

# Um den kritischen Wert zu bestimmen benötigen wir das Signifikanzlevel,
# sowie die Nenner und Zählerfreiheitsgrade. Letztere können wir manuell
# bestimmen oder wir nehmen den Output unseres Tests
sig_level_e = 0.05
df_denom = f_test_e.df_denom
df_num = f_test_e.df_num

# Nun können wir den kritischen Wert bestimmen
F_crit_e = scipy.stats.f.ppf(q = 1-sig_level_e, dfn = df_num, dfd = df_denom)

print('Realisierter Wert, Aufgabenteil e)', F_real_e)
print('Kritischer Wert, Aufgabenteil e)', F_crit_e)

# Testentscheidung
if F_real_e > F_crit_e:
    print('H0 von Aufgabenteil e) wird abgelehnt')
else:
    print('H0 von Aufgabenteil e) wird nicht abgelehnt')


##############################################################################
# f)
# Erklärende Variablen inkl Konstante, Modell 2
x2 = data[['cumgpa', 'hssize']]
x2 = pd.DataFrame(sm.add_constant(x2.values, has_constant='add'), \
                    columns = ['constant'] + x2.columns.tolist())

# Schätzung
model2 = sm.OLS(y,x2).fit()


##############################################################################
# g)

# Die entsprechende Teststatistik und der dazugehörige p-Wert werden direkt
# im Modelloutput gespeichert
print('F-Statistik, Aufgabenteil g): ', model2.fvalue)
print('p-Wert, Aufgabenteil g): ', model2.f_pvalue)
