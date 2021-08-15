from flask import Flask, render_template
from flask.globals import request
from flask.helpers import flash
import math

app = Flask(__name__)
app.testing = True
app.secret_key = '123'

@app.route("/", methods = ["POST", "GET"])

def zadatak_1():
    if request.method == "POST":
        return render_template('zadatak1.html', recenica=izracunaj(request))
    return render_template('zadatak1.html')

def izracunaj(request):
    try:
        error = None
        neto_placa = float(request.form["neto_placa"])
        radni_dani = float(request.form["radni_dani"])
        iznos = float(request.form["iznos"])
        if not neto_placa or not radni_dani or not iznos or neto_placa < 0 or radni_dani < 0 or iznos < 0:
            error = "Molimo unesite sve podatke"
        
        if error is None:
            return izracun(neto_placa, radni_dani, iznos)

        flash(error)
    except:
        return ("Nesto je krivo sa podacima, pokusajte ponovo")

def izracun(neto_placa, radni_dani, iznos):
    satnica = math.floor(neto_placa / radni_dani / 8)
    broj_sati = iznos / satnica
    broj_dana = math.floor(broj_sati / 8)
    ostatak_sati = zaokruzi((broj_sati / 8 - broj_dana) * 8, 0)
    recenica_dan = recenica_sat = recenica = ""

    if broj_dana == 1: 
        recenica_dan = str(broj_dana) + " dan"
    elif broj_dana > 1: 
        recenica_dan = str(broj_dana) + " dana"

    if ostatak_sati > 0 and ostatak_sati <= 1:
        recenica_sat = str(ostatak_sati) + " sat"
    elif ostatak_sati > 1  and ostatak_sati <= 4:
        recenica_sat = str(ostatak_sati) + " sata"
    elif ostatak_sati > 4 and ostatak_sati < 8:
        recenica_sat = str(ostatak_sati) + " sati"
    elif ostatak_sati == 8:
        broj_dana += 1
        recenica_dan = str(broj_dana) + " dana"

    if recenica_dan and recenica_sat:
        recenica = str(recenica_dan) + " i " + recenica_sat
    elif recenica_dan:
        recenica = str(recenica_dan)
    elif recenica_sat:
        recenica = str(recenica_sat)
    else:
        recenica = "Nesto je krivo sa podacima, pokusajte ponovo"
    return recenica

def zaokruzi(n, decimals=2): 
    multiplier = 10 ** decimals 
    b = math.ceil(n * multiplier) / multiplier
    return int(b)
