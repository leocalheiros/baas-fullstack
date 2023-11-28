from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import requests

auth_controller = Blueprint("auth_controller", __name__)
api_url = 'https://x0wiy4jqdf.execute-api.us-east-1.amazonaws.com/Prod/login'


def get_response_data(response):
    api_response = response.json()
    return api_response


@auth_controller.route("/login", methods=["GET"])
def login():
    return render_template("login.html", titulo='Login')


@auth_controller.route("/autenticar", methods=["POST"])
def autenticar():
    email = request.form.get("email")
    senha = request.form.get("senha")

    data = {
        "email": email,
        "senha": senha
    }

    response = requests.post(api_url, json=data)
    response_data = get_response_data(response)

    if response.status_code == 200:
        info_data = response_data['response']['data']
        token = info_data.get('token')
        session['token'] = token
        session['email'] = email

        flash("Login realizado com sucesso!", "success")
        return redirect(url_for("perfil_controller.perfil"))

    flash("Erro no login. Verifique suas credenciais.", "danger")
    return redirect(url_for("auth_controller.login"))


@auth_controller.route("/logout", methods=["GET"])
def logout():
    session.clear()
    flash("Logout realizado com sucesso!", "success")
    return redirect(url_for("auth_controller.login"))
