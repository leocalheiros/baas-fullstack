from flask import Blueprint, flash, session, request, redirect, url_for, render_template
import requests

transaction_controller = Blueprint("transaction_controller", __name__)
api_url = 'https://x0wiy4jqdf.execute-api.us-east-1.amazonaws.com/Prod/create-payment'


def get_response_data(response):
    api_response = response.json()
    response_data = api_response[0].get('response', {}).get('data', {})

    if 'status' in response_data:
        return response_data

    if 'errors' in api_response[0]:
        return api_response[0]

    return {}


@transaction_controller.route('/create-payment', methods=['GET'])
def create_payment_page():
    return render_template('criar-pagamento.html', titulo='Criar pagamento')


@transaction_controller.route('/create-transaction', methods=['POST'])
def create_transaction():
    if 'token' in session:
        email = session['email']
        amount = request.form.get("amount")

        data = {
            "email": email,
            "amount": int(amount)
        }

        token = session['token']
        headers = {
            'Authorization': f'Bearer {token}',
            'email': email
        }

        response = requests.post(api_url, json=data, headers=headers)
        response_data = get_response_data(response)
        print(response_data)
        status = response_data["status"]

        if status == 'success':
            flash("Transação realizada com sucesso!", "success")
            return redirect(url_for("perfil_controller.perfil"))
        elif status == 'fail':
            flash("Falha na transação. Verifique os detalhes.", "danger")
            return redirect(url_for("transaction_controller.create_payment_page"))
        else:
            flash("Erro ao processar a resposta da API externa.", "danger")
            return redirect(url_for("transaction_controller.create_payment_page"))

    flash("Você precisa fazer login para acessar esta página.", "warning")
    return redirect(url_for("auth_controller.login"))
