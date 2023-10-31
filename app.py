from flask import Flask, render_template, Blueprint
from src.controllers.account.cadastro_controller import cadastro_controller
from src.controllers.account.login_controller import auth_controller
from src.controllers.account.perfil_controller import perfil_controller
from src.controllers.credit_card.register_card_controller import register_card_controller
from src.controllers.credit_card.delete_card_controller import delete_card_controller
from src.controllers.credit_card.create_payment_controller import transaction_controller
from src.controllers.pix.pix_controller import pix_controller

app = Flask(__name__)
app.secret_key = '123'
app.register_blueprint(cadastro_controller)
app.register_blueprint(auth_controller)
app.register_blueprint(perfil_controller)
app.register_blueprint(register_card_controller)
app.register_blueprint(delete_card_controller)
app.register_blueprint(transaction_controller)
app.register_blueprint(pix_controller)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', titulo='Página Inicial')


if __name__ == '__main__':
    app.run(debug=True)
