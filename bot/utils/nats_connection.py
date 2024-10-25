import nats
from nats.aio.client import Client
from nats.js import JetStreamContext


async def connect_to_nats(
        servers: list[str],
        user: str,
        password: str,
        token: str,
) -> tuple[Client, JetStreamContext]:
    nc: Client = await nats.connect(servers, user=user, password=password)
    js: JetStreamContext = nc.jetstream()

    return nc, js
