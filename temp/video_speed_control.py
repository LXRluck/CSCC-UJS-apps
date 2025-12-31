import os
script_dir = os.path.dirname(os.path.abspath(__file__))
os.environ["PATH"] = script_dir + os.pathsep + os.environ["PATH"]
import mpv
import time
from pynput import keyboard

def video_speed_control(video_path):
    """
    使用 python-mpv 播放视频，支持动态调整播放速度
    快捷键：
    - 按 '+'/数字键'='：速度+0.25
    - 按 '-'：速度-0.25
    - 按 '0'：恢复1倍速
    - 按 'q'：退出播放
    """
    # 初始化 MPV 播放器
    player = mpv.MPV(
        # 按键绑定
        input_default_bindings=True,
        # 启用键盘输入
        input_vo_keyboard=True,
        # 进度条显示
        osc=True
    )

    # 初始播放速度
    current_speed = 1.0
    player.speed = current_speed  # 设置初始速度

    # 加载并播放视频
    player.play(video_path)
    print("视频开始播放！")
    print("操作说明：")
    print("  +/= → 提速（+0.25x） | - → 降速（-0.25x） | 0 → 恢复1x | q → 退出")

    # 实时调整速度
    def on_press(key):
        nonlocal current_speed
        try:
            if key.char == '=' or key.char == '+':
                current_speed = min(3.0, current_speed + 0.25)
                player.speed = current_speed
                print(f"播放速度调整为：{current_speed:.2f}x")
            elif key.char == '-':
                current_speed = max(0.5, current_speed - 0.25)
                player.speed = current_speed
                print(f"播放速度调整为：{current_speed:.2f}x")
            elif key.char == '0':
                current_speed = 1.0
                player.speed = current_speed
                print(f"播放速度恢复为：1.0x")
            elif key.char == '9' or key.char == 'q':
                print("退出播放")
                player.stop()
                return False
        except AttributeError:
            # 忽略非字符键（如方向键、功能键等）
            pass

    # 启动全局按键监听
    listener = keyboard.Listener(on_press=on_press)
    listener.start()    

    try:     
        while listener.is_alive():
            try:
                core_idle = player._get_property('core-idle')
                if core_idle:  # 视频播放完毕或暂停时，core-idle为True
                    time.sleep(0.1)
                    continue
            except Exception:
                break
            time.sleep(0.1)
    finally:
        # 停止监听并释放播放器资源
        listener.stop()
        player.terminate()

# 示例：播放视频并控制速度
if __name__ == "__main__":
    VIDEO_PATH = "D:\\计算机系统能力大赛\\测试\\一分钟.mp4"
    video_speed_control(VIDEO_PATH)