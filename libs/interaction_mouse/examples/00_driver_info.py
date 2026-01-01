import platform
from interaction_mouse import Clicker
from interaction_mouse.drivers import get_default_driver

if __name__ == "__main__":
    d = get_default_driver()
    print("OS:", platform.system())
    print("Selected driver:", type(d).__name__)

    c = Clicker(driver=d)
    print("Clicker ready:", c)
