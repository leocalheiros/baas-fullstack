from flask import Blueprint, render_template, request, redirect, url_for, flash
import requests

cadastro_controller = Blueprint("cadastro_controller", __name__)
api_url = 'https://x0wiy4jqdf.execute-api.us-east-1.amazonaws.com/Prod/create-person'


@cadastro_controller.route("/cadastro", methods=["GET"])
def cadastro():
    return render_template("cadastro.html", titulo='Cadastro')


@cadastro_controller.route("/cadastrar", methods=["POST"])
def cadastrar():
    email = request.form.get("email")
    senha = request.form.get("senha")
    saldo = request.form.get("saldo")

    data = {
        "email": email,
        "senha": senha,
        "saldo": int(saldo)
    }

    response = requests.post(api_url, json=data)

    if response.status_code == 200:
        api_response = response.json()
        if "response" in api_response[0]:
            response_data = api_response[0]["response"]
            status = response_data.get('status')

            if status == 'success':
                flash("Cadastro realizado com sucesso!", "success")
                return redirect(url_for("cadastro_controller.cadastro"))

    flash("Erro na chamada da API externa", "danger")
    return redirect(url_for("cadastro_controller.cadastro"))
