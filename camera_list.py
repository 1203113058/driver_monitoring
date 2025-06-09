import cv2

def list_cameras(max_cameras=10):
    """
    列出系统中可用的摄像头
    参数 max_cameras: 要检查的最大摄像头数量
    """
    available_cameras = []
    for i in range(max_cameras):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                available_cameras.append(i)
                print(f"摄像头 {i} 可用")
            cap.release()
        else:
            print(f"摄像头 {i} 不可用")
    
    if len(available_cameras) == 0:
        print("未找到可用摄像头")
    else:
        print(f"\n总共找到 {len(available_cameras)} 个可用摄像头")
    
    return available_cameras

if __name__ == "__main__":
    print("正在检查系统中可用的摄像头...")
    available_cameras = list_cameras()
    
    if available_cameras:
        print("\n使用方法:")
        print("1. 使用完整驾驶员监控系统:")
        print(f"   python3 dms.py --checkpoint models/model_split.h5 --webcam {available_cameras[0]}")
        print("\n2. 仅使用面部追踪功能:")
        print("   python3 facial.py")
        print(f"\n当前在conf.py中设置的摄像头ID为: {0}") 