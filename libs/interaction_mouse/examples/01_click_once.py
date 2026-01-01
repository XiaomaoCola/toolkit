from interaction_mouse import Clicker, Point, Button

if __name__ == "__main__":
    c = Clicker()
    c.click(Point(200, 200), button=Button.LEFT)
