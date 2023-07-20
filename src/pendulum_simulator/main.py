from .pendulum import Pendulum

from pygame import event

def main():
    pendulum = Pendulum()

    pendulum.set_window_properties()
    pendulum.print_info()

    while 1:
        pendulum.tick()

        for e in event.get():
            pendulum.handle_event(e)

        pendulum.draw_frame()
        pendulum.update_frame()

if __name__ == "__main__":
    main()