import signal
import sys


def handler(sig_num, frame):
     # Gertaera kudeatu
     print('\nSignal handler called with signal ' + str(sig_num))
     print('Check signal number on '
     'https://en.wikipedia.org/wiki/Signal_%28IPC%29#Default_action')
     print('\nExiting gracefully')
     sys.exit(0)

if __name__ == "__main__":
      # SIGINT jasotzen denean, "handler" metodoa exekutatuko da
     signal.signal(signal.SIGINT, handler)
     print('Running. Press CTRL-C to exit.')
     while True:
        pass # Ezer ez egin