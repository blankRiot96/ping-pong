import time


class Time:
    def __init__(self, seconds: float) -> None:
        self.seconds = seconds
        self.start = time.perf_counter()

    def reset(self):
        self.start = time.perf_counter()

    def tick(self) -> bool:
        end = time.perf_counter()
        if end - self.start > self.seconds:
            self.start = end
            return True
        return False
