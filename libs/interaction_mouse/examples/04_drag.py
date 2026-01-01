from interaction_mouse import Clicker, Point, Button

if __name__ == "__main__":
    c = Clicker(click_delay=0.01, move_duration=0.0)

    # Drag from start to end
    c.drag(
        start=Point(400, 400),
        end=Point(700, 420),
        duration=0.6,
        steps=30,
        button=Button.LEFT,
    )
