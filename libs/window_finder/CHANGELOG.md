## 2025年12月25日  
  
要开始对这个项目做大改动，因为首先，一个窗口的长宽的数据分为两种。  

一个是窗口外框区域（Window Rect / Window Bounds）。  
另一个是客户区（Client Region / Client Rect）。  

但是我目前的点击器应该是只返回第一种，但是做游戏自动化很显然需要的是第二种。

现在的问题就抽象成，我需要改动我的`models.py`文件里的`WindowInfo`。这个是异常重要的dataclass。

GPT说可以：
- **新增字段**
- **改字段名**
- **加 property**
- **用 property 做 alias**
- **创建“新版 WindowInfo 实例”**
但是不建议再创建第二个ClientWindowInfo作为客户区的信息输出。
因为它们不是两个东西，而是同一个窗口的两种几何描述。
而且GPT还说下游 API 会变得恶心，具体可以看一眼`protocol.py`。

GPT告诉我：
```python
@dataclass
class WindowInfo:
    hwnd: int
    title: str

    window_rect_ltrb: RectLTRB
    client_rect_ltrb: RectLTRB | None = None

    @property
    def rect_ltrb(self) -> RectLTRB:
        """
        Legacy alias of window_rect_ltrb.
        """
        return self.window_rect_ltrb
```
然后在 **新代码** 里：一律用 `window_rect_ltrb`，老代码不动。等我下游项目都升级了或者准备 bump 版本再用 PyCharm 一把梭哈删掉 `rect_ltrb`。

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