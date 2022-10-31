import time
import asyncio

import sys
sys.path.append("./spectrometer")
from spectrometer.device.core import Spectrometer


async def test_read_data_fps(device: Spectrometer, count=100) -> (float, int, float):
	ts = time.time()
	for i in range(count):
		await device.read_data()
	elapsed_time = time.time() - ts
	return elapsed_time, count, count / elapsed_time


async def async_run():
	device = Spectrometer()
	
	print('Check version:', device.fpga.get_version())
	print('Check gpio_status:', device.gpio.get_pin())
	
	device.fpga.set_counter(125000000)
	data = await device.read_data()
	print('Check read_data:', len(data), data[:10])
	
	elapsed_time, count, fps = await test_read_data_fps(device)
	print(f'Check performance: FPS={fps}, time={elapsed_time}, count={count}')


def run():
	asyncio.run(async_run())
