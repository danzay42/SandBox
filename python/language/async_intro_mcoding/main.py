import time
import asyncio


async def do_work(s: str, delay_s: float = 1.):
    print(f"{s} started")
    await asyncio.sleep(delay_s)
    print(f"{s} done")


async def main():
    start = time.perf_counter()
    todo = ['foo', 'bar', 'baz']

    # tasks = [asyncio.create_task(do_work(work)) for work in todo]
    # done, pending = await asyncio.wait(tasks)
    # for task in done:
    #     result = task.result()
    
    coros = [do_work(work) for work in todo]
    results = await asyncio.gather(*coros, return_exceptions=True)

    # async with asyncio.TaskGroup() as tg: # Python 3.11+
    #     tasks = [tg.create_task(do_work(work)) for work in todo]

    end = time.perf_counter()
    print(f"time: {end-start:.2f}s")

if __name__ == "__main__":
    asyncio.run(main())
