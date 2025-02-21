import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy.orm import DeclarativeBase

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
app = Flask(__name__)

# Configuração
app.secret_key = os.environ.get("SESSION_SECRET", "your-secret-key")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///clinica.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True
}
app.config["ENV"] = "development"

# Inicialização do LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor, faça login para acessar esta página.'

db.init_app(app)

with app.app_context():
    # Importar modelos e rotas após a inicialização do app
    from models import User
    from routes import *

    db.create_all()
    # Criar usuário admin se não existir
    try:
        admin_user = User.query.filter_by(email='adm@prime.com').first()
        if not admin_user:
            logger.info("Criando usuário admin...")
            admin_user = User(
                username='admin',
                email='adm@prime.com',
                is_admin=True
            )
            admin_user.set_password('@Admin123')
            db.session.add(admin_user)
            db.session.commit()
            logger.info("Usuário admin criado com sucesso!")
        else:
            logger.info("Usuário admin já existe")
    except Exception as e:
        logger.error(f"Erro ao criar usuário admin: {str(e)}")
        db.session.rollback()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)