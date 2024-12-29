## Genshin Impact Themed Lottery Machine

这是一个以原神抽卡为模版设计的抽奖机。基于Python与Pygame构造。

**Features**
- 支持自定义权重
- 播放背景音乐（别问为什么是ZZZ的）
- 播放抽卡动画
- 没想好

**User Manuals**

1. 在程序运行目录新建一个文件`item.cvs`，格式如下：
```csv
item   ,weight ,image
王小一  ,     1 ,wx1.jpg
王小二  ,     1 ,
王小三  ,     1 ,wx3.jpg
```
2. 将图片置于`./assets/images/items`下。
3. Just Enjoy.

**注意事项**

1. 权重`weight`必须为整数；若需要将个别人禁用，可以将权重设置为`0`。
2. `image`图片地址不需保留路径，只需保留文件名和后缀。
3. 若使用图片，将`image`留空。

