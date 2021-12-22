from flask import Flask
from flask_cors import CORS
from app.main.service.processos_service import ProcessoService
from apscheduler.schedulers.background import BackgroundScheduler
from app.main.bd.repository import init_bd, environment_config
from app import blueprint

app = Flask(__name__)
app.register_blueprint(blueprint)
CORS(app)

service = ProcessoService()

cfg = environment_config()

cron = BackgroundScheduler(daemon=True, timezone='America/Sao_Paulo')
cron.add_job(service.update_processos, 'cron', day_of_week=(
    'mon-fri'), minute='0-59/30', hour='8-18')

app.app_context().push()


def run():
    init_bd()
    cron.start()
    port = cfg["port"]
    app.run(host=cfg["host"], port=port, debug=cfg["debug"])


if __name__ == "__main__":
    run()