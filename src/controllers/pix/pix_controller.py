from flask import Blueprint, flash, session, request, redirect, render_template, url_for
import requests

pix_controller = Blueprint("generate_pix_code_controller", __name__)
api_url = ' https://x0wiy4jqdf.execute-api.us-east-1.amazonaws.com/Prod/gerar-pix'


def get_response_data(response):
    api_response = response.json()
    return api_response


@pix_controller.route('/generate-pix-code', methods=['GET'])
def generate_pix_code_page():
    return render_template('gerar-pix.html', titulo='Gerar Código Pix')


@pix_controller.route('/generate-pix', methods=['POST'])
def generate_pix_code():
    if 'token' in session:
        email = session['email']
        nome = request.form.get("nome")
        chavepix = request.form.get("chavepix")
        valor = request.form.get("valor")
        cidade = request.form.get("cidade")

        data = {
            "nome": nome,
            "chavepix": chavepix,
            "valor": valor,
            "cidade": cidade
        }

        token = session['token']
        headers = {
            'Authorization': f'Bearer {token}',
            'email': email
        }

        response = requests.post(api_url, json=data, headers=headers)
        response_data = get_response_data(response)

        if response.status_code == 200:
            info_data = response_data['response']['data']
            payload = info_data.get("payload")
            flash(f"Código Pix gerado com sucesso! Código: {payload}", "success")
        elif response.status_code == 422:
            flash("Dados inválidos para gerar código pix", "danger")
        else:
            flash("Erro ao criar o código pix", "danger")

        return redirect(url_for("generate_pix_code_controller.generate_pix_code_page"))

    flash("Você precisa fazer login para acessar esta página.", "warning")
    return redirect(url_for("auth_controller.login"))
