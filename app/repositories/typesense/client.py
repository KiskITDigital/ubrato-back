import typesense
from config import Config, get_config

config: Config = get_config()

client = typesense.Client(
    {
        "api_key": config.Database.Typesense.API_KEY,
        "nodes": [
            {
                "host": config.Database.Typesense.HOST,
                "port": config.Database.Typesense.PORT,
                "protocol": config.Database.Typesense.PROTOCOL,
            },
        ],
        "connection_timeout_seconds": 10,
    }
)


def get_db_connection() -> typesense.Client:
    return client
