from interaction_mouse import Clicker, Rect, Button

if __name__ == "__main__":
    c = Clicker(click_delay=(0.008, 0.015), move_duration=(0.0, 0.02))

    # Random click in rectangle
    c.rand_click(
        Rect(100, 200, 200, 260),
        count=8,
        interval=(0.09, 0.16),
        avoid_edges_px=4,
        button=Button.LEFT,
    )
