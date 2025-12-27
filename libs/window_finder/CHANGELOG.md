## 2025年12月25日

要开始对这个项目做大改动，因为首先，一个窗口的长宽的数据分为两种。

一个是窗口外框区域（Window Rect / Window Bounds）。

另一个是客户区（Client Region / Client Rect）。

但是我目前的点击器应该是只返回第一种，但是做游戏自动化很显然需要的是第二种。

## 2025年12月26日

在models.py文件中， 把 rect_ltrb 替换成了 window_rect_ltrb， 并添加client_rect_ltrb。

dataclass中字段的顺序变换要遵守的规则：没有默认值的字段，必须写在有默认值的字段前面。

例子：比如之前的WindowInfo
```python
native_id: Optional[Union[int, str]]
title: str
rect_ltrb: Optional[RectLTRB] = None
pid: Optional[int] = None
app_name: Optional[str] = None
```
分析一下：
native_id → 无默认值
title → 无默认值
后面三个 → 都有默认值