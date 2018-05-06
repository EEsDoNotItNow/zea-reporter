#!/usr/bin/env python


"""
    To keep our bot alive, we run a retry wrapper!
"""

import subprocess
import time

class EXPRetry:

    def __init__(self):
        self.retry_array = [
                0.1,0.2,0.5,
                  1,  2,  5,
                 10, 20, 50, 
                100,200,500]
        self.retries = -1
        self.t0 = 0
        self.t1 = 0

    def start(self):
        # Remember when we started
        self.t0 = time.time()

    def end(self):
        # Remembe when we ended
        self.t1 = time.time()
        pass

    def sleep(self):
        # Sleep according to our rules
        if self.t1 - self.t0 > 60:
            self.retries = -1

        self.retries += 1

        if self.retries == len(self.retry_array):
            self.retries -= 1
            print("Max retry length reached!")

        t_sleep = self.retry_array[self.retries]

        print(f"Sleep for {t_sleep}")

        time.sleep(t_sleep)

RT = EXPRetry()
while 1:
    RT.start()

    try:
        subprocess.run("./ZeaReporter.py")
    except KeyboardInterrupt:
        break
    except Exception as e:
        print(e)
        pass

    RT.end()
    RT.sleep()



