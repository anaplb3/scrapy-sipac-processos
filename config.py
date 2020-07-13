import os

DEV_CFG = {
    "debug": True,
    "database_url": "postgresql://postgres:starwars@localhost/processos_sipac",
    "sslmode": "disable",
    "port": 5000,
    "host": "127.0.0.1",
    "chave": os.environ.get("chave_populando", None)
}

PROD_CFG = {
    "debug": False,
    "database_url": os.environ['DATABASE_URL'],
    "sslmode": "require",
    "port": int(os.environ.get("PORT", 5000)),
    "host": "0.0.0.0",
    "chave": os.environ.get("chave_populando", None)
}
