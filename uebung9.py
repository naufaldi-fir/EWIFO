# -*- coding: utf-8 -*-
"""
Created on Tue Sep 21 13:50:37 2021

@author: Chantal
"""
import os
import pandas as pd
import statsmodels.api as sm
import scipy.stats

# Pfad zum Ordner. Muss individuell angepasst werden
os.chdir("C:/Users/Chantal/sciebo/Ewifo/WS2122/Übung_neu/Thema 9")

##############################################################################
############# Aufgabe 9.1 ###################################################
##############################################################################

# Auslesen der Daten
data = pd.read_excel("weeksworked.xlsx","Sheet1")

# Abhängige Variablen und Regressoren
y = data[['weeks']]
x = data[['morekids', 'educ']]
x = pd.DataFrame(sm.add_constant(x.values, has_constant='add'), \
                    columns = ['Konstante'] + x.columns.tolist())

# Schätzung
weeksreg = sm.OLS(y,x).fit()

# Berechnung der Residuen des geschätzten Modells und Quadrierung der Residuen
resid=weeksreg.resid
residsq=resid*resid

# Quadrierung der unabhängigen Variablen educ von Modell 1 (morekids als Dummy-Variable
#wird nicht quadriert)
data['educsq'] = data['educ']*data['educ']

# Definiere die Interaktion der beiden unabhängigen Variablen von Modell 1
data['educ_morekids'] = data['educ']*data['morekids']

# Festsetzen der unabhängigen Variablen der White-Hilfsregression. Die Hilfsregression
# enthält immer die beiden Regressoren des ursprünglichen Modells, die beiden quadrierten
# Regressoren des ursprünglichen Modells und die Interaktion der beiden Regressoren
XVarWhite = data[['educ','morekids','educsq','educ_morekids']]
XVarWhite = pd.DataFrame(sm.add_constant(XVarWhite.values, has_constant='add'), columns = ['Konstante'] + XVarWhite.columns.tolist())

# Festsetzen der abhängigen Variable der Hilfsregression, hier also die quadrierten
# Residuen von weeksreg
YVarWhite=residsq

# Schätzung der White-Hilfsregession
weeks_White = sm.OLS(YVarWhite,XVarWhite).fit()

##############################################################################
# b)

# Berechnung des realisierten Wertes des White-Testes anhand der Anzahl der Beobachtungen
# der Hilfsregression und des Bestimmtheitsmaßes der Hilfsregression
R2_White=weeks_White.rsquared
k_White= weeks_White.df_model+weeks_White.k_constant
n_White=int(weeks_White.df_resid +k_White )
White_act=n_White*R2_White
print('Realisierter Wert zum White-Test', White_act)

##############################################################################
# c)

# Berechnung des kritischen Wertes anhand der Chi-Verteilung zum Signifikanzniveau 5%
#und der Anzahl der Freiheitsgrade k_White-1, wobei k_White für die Anzahl der geschätzten
#Koeffizienten der Hilfsregression steht.
alphaWhite=0.01
chi_krit=scipy.stats.chi2.ppf((1-alphaWhite),k_White-1)
print('Kritischer Wert zum White-Test', chi_krit)


##############################################################################
############# Aufgabe 9.3 ###################################################
##############################################################################


# Auslesen der Daten
data = pd.read_excel("trmgpa.xlsx","Sheet1")

# Abhängige Variablen und Regressoren
y = data[['trmgpa']]
x = data[['female', 'frstsem']]
x = pd.DataFrame(sm.add_constant(x.values, has_constant='add'), \
                    columns = ['const'] + x.columns.tolist())

# Schätzung
trmgpa = sm.OLS(y,x).fit()
print('Geschätzte Koeffizienten zu trmgpa \n', trmgpa.params)
print('Standardfehler zu trmgpa \n', trmgpa.bse)
print('Robuste Standardfehler zu trmgpa \n', trmgpa.HC0_se)
