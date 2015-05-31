import time
import random
class Mover(object):
    def __init__(self, scout, config, api=None):
        if api is None:
            import wordamentbot.winapi as api
        self.api = api
        self.scout = scout
        self.config = config
    def move(self, path, delay=0.01, delay_variance=0.05):
        up = True
        for coords in path:
            pos = self.scout.coords_to_pos(coords)
            self.api.set_mouse(pos)
            if delay is not None:
                if delay_variance is not None:
                    # TODO: Allow pos/neg delay variance centered around delay
                    delay += (random.random() * delay_variance)
                time.sleep(delay)
            if up:
                self.api.left_down()
                up = False
        self.api.left_up()
        if delay: time.sleep(delay)
