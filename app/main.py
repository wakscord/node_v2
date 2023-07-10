import asyncio

from dependency_injector.wiring import Provide, inject
from redis.asyncio import Redis

from app.alarm.sender import AlarmSender
from app.alarm.task_parser import AlarmTaskParser
from app.common.di import AppContainer
from app.common.exceptions import async_exception_handler
from app.common.settings import settings
from app.node.manager import NodeManager


@inject
async def process_task(task: list[bytes], alarm_sender: AlarmSender = Provide[AppContainer.alarm_sender]) -> None:
    parser = AlarmTaskParser(task)
    await alarm_sender.send(parser.parse_subscribers(), parser.parse_message())


@async_exception_handler
async def listen(session: Redis = Provide[AppContainer.redis_session]) -> None:
    while True:
        task = await session.blpop(settings.NODE_ID)
        if task:
            asyncio.create_task(process_task(task))


@inject
async def run(
    node_manager: NodeManager = Provide[AppContainer.node_manager],
) -> None:
    await node_manager.join_server()
    await listen()


if __name__ == "__main__":
    container = AppContainer()
    container.wire(modules=[__name__])

    asyncio.run(run())
