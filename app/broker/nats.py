from typing import Dict, Optional

from config import Config, get_config
from nats.aio.client import Client

config: Config = get_config()


class NatsClient:
    def __init__(self):
        self.client = Client()

    async def connect(self) -> None:
        await self.client.connect(servers=[config.Broker.JetStream.DSN])

    async def pub(
        self,
        subject: str,
        payload: bytes = b"",
        reply: str = "",
        headers: Optional[Dict[str, str]] = None,
    ) -> None:
        await self.client.publish(
            subject=subject, payload=payload, reply=reply, headers=headers
        )

    async def close(self) -> None:
        await self.client.close()


nats_conn = NatsClient()


def get_nats_connection() -> NatsClient:
    return nats_conn
