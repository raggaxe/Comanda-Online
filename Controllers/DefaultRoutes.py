from flask import render_template

def errorhandler(e):
    [cod, first, end] = str(e).split(':')[0].split(' ')
    return render_template("error.html", error=f'{first} {end}'), int(cod)
