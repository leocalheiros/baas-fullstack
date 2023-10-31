from flask import Blueprint, render_template, flash, session, redirect, url_for
import requests
import base64

perfil_controller = Blueprint("perfil_controller", __name__)

api_url = 'https://x0wiy4jqdf.execute-api.us-east-1.amazonaws.com/Prod/get-person'


def get_response_data(response):
    if response.status_code == 200:
        api_response = response.json()[0]
        return api_response.get('response', {}).get('data', {})


def __decode_and_format_card_number(card_number):
    card_number_decoded = base64.b64decode(card_number.encode()).decode()
    visible_digits = card_number_decoded[-4:]
    masked_digits = '*' * (len(card_number_decoded) - 4)
    formatted_card_number = f'{masked_digits}{visible_digits}'
    return formatted_card_number


@perfil_controller.route('/perfil', methods=['GET'])
def perfil():
    if 'token' in session:
        token = session['token']
        email = session['email']

        data = {
            "email": email
        }

        headers = {
            'Authorization': f'Bearer {token}',
            'email': email
        }

        response = requests.post(api_url, json=data, headers=headers)
        response_data = get_response_data(response)

        if response_data:
            email = response_data.get('email')
            saldo = response_data.get('saldo')
            if response_data.get('credit_card', {}):
                holder_name = response_data.get('credit_card', {}).get('holder_name')
                card_number = response_data.get('credit_card', {}).get('card_number')
                card_number_decoded = __decode_and_format_card_number(card_number)
            else:
                holder_name = 'Sem registro de cartão'
                card_number_decoded = 'Sem registro de cartão'
            return render_template("perfil.html", titulo='Perfil', email=email, saldo=saldo,
                                   holder_name=holder_name, card_number=card_number_decoded)
        else:
            flash("Erro ao obter informações do perfil.", "danger")

    flash("Você precisa fazer login para acessar esta página.", "warning")
    return redirect(url_for("auth_controller.login"))
