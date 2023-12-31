from flask import Blueprint, render_template, flash, session, redirect, url_for
import requests

delete_card_controller = Blueprint("delete_card_controller", __name__)
api_url = ' https://x0wiy4jqdf.execute-api.us-east-1.amazonaws.com/Prod/delete-card'


def get_response_data(response):
    api_response = response.json()
    response_data = api_response[0].get('response', {}).get('data', {})

    if 'status' in response_data:
        return response_data

    if 'errors' in api_response[0]:
        return api_response[0]

    return {}


@delete_card_controller.route('/delete-card', methods=['GET'])
def delete_card():
    if 'token' in session:
        email = session['email']

        data = {
            "email": email
        }

        token = session['token']
        headers = {
            'Authorization': f'Bearer {token}',
            'email': email
        }

        response = requests.post(api_url, json=data, headers=headers)

        if response.status_code == 200:
            flash("Cartão de crédito deletado com sucesso!", "success")
            return redirect(url_for("perfil_controller.perfil"))
        elif response.status_code == 404:
            flash("Você não possui cartão de crédito cadastrado!.", "danger")
            return redirect(url_for("perfil_controller.perfil"))
        else:
            flash("Falha ao deletar cartão de crédito.", "danger")
            return redirect(url_for("perfil_controller.perfil"))

    flash("Você precisa fazer login para acessar esta página.", "warning")
    return redirect(url_for("auth_controller.login"))

