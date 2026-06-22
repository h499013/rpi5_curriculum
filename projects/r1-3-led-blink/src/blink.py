#!/usr/bin/env python3
"""gpio17 led blink(1s) and count in system log"""
#shebang and docstring

#blink interval time.sleep()
import time
#timestamp
import datetime
#shell command
import subprocess
#file path
from pathlib import Path
#gpio control
from gpiozero import LED
#os signal
from signal import pause, signal, SIGTERM, SIGINT

LED_PIN = 17
PERIOD_SEC = 1.0
LOG_FILE = Path(__file__).parent.parent / "logs" / "blink.log"

#gpio17
led = LED(LED_PIN)
#running flag
running = True

#signal handler
def cleanup(signum, frame):
    global running
    running = False


#signal registration
signal(SIGTERM, cleanup)
signal(SIGINT, cleanup)


def get_temp():
    #temp capture
    out = subprocess.check_output(["vcgencmd", "measure_temp"], text=True)
    #parsing
    return float(out.split("=")[1].split("'")[0])


def main():
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    print(f"Blink started on GPIO{LED_PIN}. Logging to {LOG_FILE}")
    count = 0

    while running:
        led.on()
        time.sleep(PERIOD_SEC / 2)
        led.off()
        time.sleep(PERIOD_SEC / 2)
        count += 1

        if count % 10 == 0:
            ts = datetime.datetime.now().isoformat(timespec="seconds")
            temp = get_temp()
            line = f"{ts} | blinks={count} | temp={temp:.1f}°C\n"
            with LOG_FILE.open("a") as f:
                f.write(line)
            print(line, end="")

    led.off()
    print("\nStopped cleanly.")


if __name__ == "__main__":
    main()
