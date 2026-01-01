"""
adapter的定义：把“别人给我的复杂对象”，转换成“我自己包里需要的最小对象”。

具体的例子就是：
把 window_finder 的“一堆数据”，适配成 interaction_mouse 能用的 Rect。
只有 adapter 知道 window_finder 的返回结构。
clicker 完全不知道 window_finder 存在。
"""