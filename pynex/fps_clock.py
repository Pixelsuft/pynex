import time


class NFps:
    def __init__(
            self,
            fps: any,
            unlocked: bool = False,
            smooth_fix: bool = False,
            time_function: any = time.time
    ) -> None:
        super(NFps, self).__init__()
        self.fps = float(fps)
        self.frame_rate = 1 / fps
        self.delta = self.frame_rate
        self.unlocked = unlocked
        self.smooth_fix = smooth_fix
        self.speed_hack = 1.0
        self.time_func = time_function
        self.last_tick = self.time_func()

    def set(self, name: str, value: any) -> any:
        setattr(self, name, value)
        return self

    def tick(self) -> bool:
        now = self.time_func()
        if not self.unlocked and now < self.last_tick + self.frame_rate:
            return False
        if self.smooth_fix:
            self.delta = self.frame_rate * self.speed_hack
            self.last_tick += self.frame_rate
        else:
            self.delta = (now - self.last_tick) * self.speed_hack
            self.last_tick = now
        return True

    def get_fps_float(self) -> float:
        try:
            return self.speed_hack / self.delta
        except ZeroDivisionError:
            return self.fps

    def get_fps_int(self) -> int:
        return round(self.get_fps_float())
