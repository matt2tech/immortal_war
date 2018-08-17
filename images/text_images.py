from time import sleep
import sys

# text_images will deal with artwork made with unicode or ascii characters


# this works will loading to create a loading bar "Do not touch!"
# however, if needed, delete loading from shell
def report_progress(ratio, width=50):
    filled = '█' * int(ratio * width)
    rest = '-' * (width - int(ratio * width))
    sys.stderr.write('\r|' + filled + rest + '|')
    sys.stderr.flush()


# creates a loading bar "Do not touch!"
def loading():
    for i in range(101):
        report_progress(i / 100.0, 50)
        sleep(0.05)
    print('\n')


# creates the title screen artwork
def title():
    sleep(0.1)
    print('\n')
    sleep(0.1)
    print(
        '    ▄█ █▀▄▀█ █▀▄▀█ ████▄ █▄▄▄▄    ▄▄▄▄▀ ██   █          ▄ ▄   ██   █▄▄▄▄ '
    )
    sleep(0.1)
    print(
        '    ██ █ █ █ █ █ █ █   █ █  ▄▀ ▀▀▀ █    █ █  █         █   █  █ █  █  ▄▀ '
    )
    sleep(0.1)
    print(
        '    ██ █ ▄ █ █ ▄ █ █   █ █▀▀▌      █    █▄▄█ █        █ ▄   █ █▄▄█ █▀▀▌  '
    )
    sleep(0.1)
    print(
        '    ▐█ █   █ █   █ ▀████ █  █     █     █  █ ███▄     █  █  █ █  █ █  █  '
    )
    sleep(0.1)
    print(
        '     ▐    █     █          █     ▀         █     ▀     █ █ █     █   █   '
    )
    sleep(0.1)
    print(
        '         ▀     ▀          ▀               █             ▀ ▀     █   ▀    '
    )
    sleep(0.1)
    print(
        '                                         ▀                     ▀         '
    )
    sleep(0.1)
    print('\n')
    sleep(0.1)
