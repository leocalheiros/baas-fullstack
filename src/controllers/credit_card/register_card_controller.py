from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, session
import requests

register_card_controller = Blueprint("cartao_controller", __name__)
api_url = 'https://x0wiy4jqdf.execute-api.us-east-1.amazonaws.com/Prod/register-credit-card'


@register_card_controller.route('/create-card', methods=['GET'])
def create_card_page():
    return render_template("cadastrar-cartao.html", titulo='Cadastro Cartão')


@register_card_controller.route("/cadastrar-cartao", methods=["POST"])
def cadastrar_cartao():
    if 'token' in session:
        email = session['email']
        card_number = request.form.get("card_number")
        expiration_month = request.form.get("expiration_month")
        expiration_year = request.form.get("expiration_year")
        security_code = request.form.get("security_code")
        holder_name = request.form.get("holder_name")

        data = {
            "email": email,
            "card_number": card_number,
            "expiration_month": int(expiration_month),
            "expiration_year": int(expiration_year),
            "security_code": security_code,
            "holder_name": holder_name
        }

        token = session['token']
        headers = {
            'Authorization': f'Bearer {token}',
            'email': email
        }

        response = requests.post(api_url, json=data, headers=headers)

        if response.status_code == 200:
            flash("Cartão de crédito cadastrado com sucesso!", "success")
            return redirect(url_for("perfil_controller.perfil"))

        flash("Erro no cadastro do cartão de crédito. Verifique os dados fornecidos.", "danger")

    flash("Você precisa fazer login para acessar esta página.", "warning")
    return redirect(url_for("perfil_controller.perfil"))
