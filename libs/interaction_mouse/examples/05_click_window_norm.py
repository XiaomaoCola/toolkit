from interaction_mouse import Clicker, Button
from interaction_mouse.models import WindowNormalizedPoint

if __name__ == "__main__":
    c = Clicker()

    # 点击BlueStacks，Builder Base的村庄场景的左下角的Attack按钮。
    target = WindowNormalizedPoint(
        keyword="BlueStacks",   # 窗口标题关键字
        x=0.075,
        y=0.875,
        button=Button.LEFT,
    )

    c.click_window_norm(target)
