import time
import json
import life
import sys


def loop(init_frame, timeout=0.2):
    # for frame in life.FrameGenerator(init_frame):
    for frame in life.frame_generator(init_frame, 1e4):
        life.render(frame)
        # time.sleep(timeout)


def main():
    images = json.load(open("../../patterns_examples.json"))
    example = images["Oscillators"]["Penta-decathlon"]
    # example = images["Oscillators"]["Pulsar"]
    # example = images["Spaceships"]["Glider"]
    # example = images["Spaceships"]["HWSS"]
    loop(example)


if __name__ == '__main__':
   main()