import collections


def new_cell(state, resources):
    match state, resources:
        case 1, 2 | 3:
            return 1
        case 0, 3:
            return 1
        case _:
            return 0


def new_frame(old_frame, resource_distribution):
    return [[
        new_cell(state, resource_distribution[y][x])
            for x, state in enumerate(row)] 
                for y, row in enumerate(old_frame)]


def calculate_resources(frame: list[list[int]]):
    resources_buffer = [[0 for _ in row] for row in frame]

    for y, row in enumerate(frame):
        for x, state in enumerate(row):
            if state:
                for dx, dy in [(dx, dy) for dx in [-1,0,1] for dy in [-1,0,1] if dx or dy]:
                    sx, sy = x+dx, y+dy
                    if sx == len(row): sx = 0
                    if sy == len(frame): sy = 0
                    resources_buffer[sy][sx] += 1

    return resources_buffer


def frame_generator(init_frame, count=float("inf"), buffered_frames_size=3):
    buffered_frames = collections.deque()
    frame = init_frame

    def loop_control(frame):
        if len(buffered_frames) > buffered_frames_size:
            buffered_frames.popleft()
        res = frame not in buffered_frames
        buffered_frames.append(frame)
        return res

    while (count := count-1) and loop_control(frame):
        yield frame
        resource_distribution = calculate_resources(frame)
        frame = new_frame(frame, resource_distribution)

    return frame


class FrameGenerator:
    buffered_frames: collections.deque
    buffered_frames_size: int
    frame: list[list[int]]
    resource_distribution: list[list[int]]
    count: float

    def __init__(self, init_frame, count=float('inf'), buffered_frames=3) -> None:
        self.buffered_frames = collections.deque()
        self.buffered_frames_size = buffered_frames
        self.frame = init_frame
        self.count = count

    def _loop_control(self):
        if len(self.buffered_frames) > self.buffered_frames_size:
            self.buffered_frames.popleft()
        res = self.frame not in self.buffered_frames
        self.buffered_frames.append(self.frame)
        return res
    
    def __iter__(self):
        while self.count and self._loop_control():
            yield self.frame
            self.resource_distribution = calculate_resources(self.frame)
            self.frame = new_frame(self.frame, self.resource_distribution)
            self.count-=1
        print("looped")
        return self.frame