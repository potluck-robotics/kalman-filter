import select
import sys
import termios
import tty

class Key:
    def __init__(self):
        self.old_settings = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin.fileno())

    def stop(self):
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)

    def read(self):
        c = None
        if self.is_data():
            c = sys.stdin.read(1)
        return c

    def is_data(self):
        return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])