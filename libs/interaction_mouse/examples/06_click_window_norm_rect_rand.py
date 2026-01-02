from interaction_mouse import Clicker, Button
from interaction_mouse.models import WindowNormalizedRect

if __name__ == "__main__":
    # 创建 Clicker，鼠标移动时间带随机
    c = Clicker(move_duration=(0.2, 0.5))

    target = WindowNormalizedRect(
        keyword="BlueStacks",   # 窗口标题关键字
        left=0,
        top=0,
        right=1,
        bottom=1,
        button=Button.LEFT,
    )

    c.click_window_norm_rect_rand(
        target,
        count=100,            # 总点击次数
        interval=(0.1, 0.3),  # 每次点击之间的间隔
        avoid_edges_px=5,   # 避开区域边缘 5 像素
    )
