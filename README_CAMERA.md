# 驾驶员监控系统摄像头使用说明

## 查找可用摄像头

要列出系统中所有可用的摄像头，请运行：

```bash
python3 camera_list.py
```

该命令将检查系统中的摄像头并列出所有可用的摄像头ID。

## 使用指定摄像头运行面部追踪

运行面部追踪功能并指定摄像头ID：

```bash
python3 facial.py --webcam <摄像头ID>
```

例如，使用ID为1的摄像头：

```bash
python3 facial.py --webcam 1
```

如果不指定摄像头ID，系统将使用配置文件(conf.py)中设置的默认摄像头(默认为0)。

## 使用指定摄像头运行完整的驾驶员监控系统

运行完整的驾驶员监控系统并指定摄像头ID：

```bash
python3 dms.py --checkpoint models/model_split.h5 --webcam <摄像头ID>
```

例如，使用ID为1的摄像头：

```bash
python3 dms.py --checkpoint models/model_split.h5 --webcam 1
```

## 常见问题解决

1. 如果您看到"错误: 无法打开摄像头"消息，请确保您指定的摄像头ID是有效的。使用`camera_list.py`检查可用摄像头。

2. 如果摄像头能打开但画面不正确，您可能需要调整配置文件中的分辨率设置。可以在`facial_tracking/conf.py`文件中修改`FRAME_W`和`FRAME_H`值。

3. 要退出任何运行中的程序，请按键盘上的'q'键。 