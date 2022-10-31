import asyncio
from asyncio.taskgroups import TaskGroup


async def sleep(s: int) -> None:
    await asyncio.sleep(s)
    print(f"sleeped for {s} seconds")


async def main_old():
    tasks = []
    for seconds in (3,1,2):
        tasks.append(asyncio.create_task(sleep(seconds)))
    await asyncio.gather(*tasks)


async def main_new():
    async with asyncio.TaskGroup() as tg:
        for seconds in (3,1,2):
            tg.create_task(sleep(seconds))


main = main_new
asyncio.run(main())