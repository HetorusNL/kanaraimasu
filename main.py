import asyncio

from kanaraimasu import Kanaraimasu


async def main():
    print("starting kanaraimasu")
    game_instance = Kanaraimasu(run_async=True)
    i = 0
    while True:
        i += 1
        game_instance.game_loop()
        await asyncio.sleep(0)


asyncio.run(main())
