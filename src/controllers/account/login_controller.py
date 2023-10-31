from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import requests

auth_controller = Blueprint("auth_controller", __name__)
api_url = 'https://x0wiy4jqdf.execute-api.us-east-1.amazonaws.com/Prod/login'


def get_response_data(response):
    api_response = response.json()
    response_data = api_response[0].get('response', {}).get('data', {})

    if 'status' in response_data:
        return response_data

    if 'errors' in api_response[0]:
        return api_response[0]

    return {}


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

    if response_data:
        status = response_data.get('status')

        if status == 'success':
            token = response_data.get('token')
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
