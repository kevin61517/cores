from src.database import Mixin, db
from src.models import Test
from src.service import Service, AsyncService
import asyncio


class TestService(Service):
    __model__ = Test


test_service = TestService()


async def run():
    db.create_engine()
    result = test_service.get(1)
    print('result===>', result)
    await db.close_engine()


if __name__ == '__main__':
    asyncio.run(run())
    print(Mixin)
    print(Service)
    print(AsyncService)
