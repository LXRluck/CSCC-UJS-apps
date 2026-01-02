import os
import re
script_dir = os.path.dirname(os.path.abspath(__file__))
os.environ["PATH"] = script_dir + os.pathsep + os.environ["PATH"]
import mpv
import time
from pynput import keyboard

class MPVPlayerCore:
    def __init__(self):
        self.mpv_player = mpv.MPV(
            vo='gpu',  
            input_default_bindings=True,
            input_vo_keyboard=True,
            osc=True, 
            # SUBTITLE OPTIONS
            sid='no',
            sub_auto='no',
            sub_font_size=24,
            sub_color='#FFFFFF',
            sub_border_color='#000000',
            sub_border_size=2
        )

        self.is_playing = False
        self.current_file = None

        self.set_volume(80)

        self.injected_subtitle_ids = []
        self.temp_sub_track_id=None

        self.temp_sub_file=None
        self.subtitle_counter = 0

        self.duration_loaded = False

        self.current_speed = 1.0
        self.mpv_player.speed = self.current_speed
        self.keylistener = None

        @self.mpv_player.event_callback('file-loaded')
        def on_file_loaded(event):
            self.duration_loaded = True

        self.progress_update_callback=None

        @self.mpv_player.property_observer('time-pos')
        def time_pos_observer(_name, value):
            #进度监听回调
            if self.progress_update_callback and value is not None:
                self.progress_update_callback(value, self.get_duration())


    def bind_to_window(self, win_id):
        #将MPV绑定到指定窗口
        self.mpv_player.wid = str(int(win_id))

    def load_video(self, file_path):
        #加载并播放指定视频文件
        self.stop()
        self.current_file = file_path
        self.duration_loaded= False
        self.mpv_player.play(file_path)
        self.is_playing = True
        #重置播放速度
        self.current_speed = 1.0
        self.mpv_player.speed = self.current_speed


    def toggle_play_pause(self):
        #切换播放/暂停状态
        if not self.current_file:
            raise ValueError("未加载视频文件")
        
        if self.is_playing:
            self.mpv_player.pause=True
            self.is_playing = False
        else:
            self.mpv_player.pause=False
            self.is_playing = True


    def stop(self):
        #停止播放并重置状态
        if self.current_file:
            self.mpv_player.stop()
            self.is_playing = False
            self.current_file = None
            if self.keylistener and self.keylistener.is_alive():
                self.keylistener.stop()
            if self.temp_sub_track_id is not None:
                self.mpv_player.command('sub-remove', self.temp_sub_track_id)
                self.temp_sub_track_id = None

    def set_volume(self, value):
        if 0 <= value <= 100:
            self.mpv_player.volume = value

    def get_volume(self):
        return self.mpv_player.volume

    def get_duration(self, timeout=5.0, interval=0.1):
        #获取总时长
        start = time.time()
        while time.time() - start < timeout:
            if self.duration_loaded:
                try:
                    return self.mpv_player.duration or 0
                except AttributeError:
                    return 0
            time.sleep(interval)
        return 0
    
    def set_position(self, seconds):
        if 0 <= seconds <= self.get_duration():
            self.mpv_player.seek(seconds, reference='absolute')

    def get_position(self):
        try:
            return self.mpv_player.time_pos or 0
        except:
            return 0

    def set_progress_callback(self, callback):
        #进度更新回调
        self.progress_update_callback = callback

    def set_subtitle_file(self, subtitle_path):
        subtitle_path = os.path.abspath(subtitle_path)
        if not os.path.exists(subtitle_path):
            raise FileNotFoundError(f"字幕文件不存在：{subtitle_path}")
    
        #清除所有旧字幕轨道
        self._cleanup_all_subtitles()
    
        try:
            self.mpv_player.sid = "no"  # 禁用内置字幕
            self.mpv_player.sub_auto = "no"  # 关闭自动匹配
            self.mpv_player.sub_codepage = "utf-8"  # 强制指定编码（兼容绝大多数字幕）
        
            self.mpv_player.command("sub-add", subtitle_path)
        
            #强制启用新添加的外部字幕轨道
            self.mpv_player.sub = "1" 
            self.mpv_player.sub_visibility = True  
        
            print(f"字幕切换成功：{subtitle_path}")
            print(f"当前启用的字幕轨道：{self.mpv_player.sub}")  
        
        except Exception as e:
            # 捕获MPV命令执行异常（如字幕文件损坏）
            raise RuntimeError(f"切换字幕失败：{str(e)} | 字幕路径：{subtitle_path}")


    def _cleanup_all_subtitles(self):
        # 清除所有注入的字幕轨道
        for sub_id in self.injected_subtitle_ids:
            try:
                self.mpv_player.command("sub-remove", sub_id)
            except Exception as e:
                print(f"清除旧轨道{sub_id}失败：{e}")
        self.injected_subtitle_ids.clear()
    
        for temp_file in self.temp_subtitle_files:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            except Exception as e:
                print(f"删除临时文件{temp_file}失败：{e}")
        self.temp_subtitle_files.clear()
    
        # 清除MPV当前的字幕配置
        self.mpv_player.sub_file = "" 
        self.mpv_player.sub = "0" 
        self.mpv_player.sub_visibility = False 
        
# 实时字幕注入
# ///////////////////////////////////////////////////////////////
    def inject_mpv_subtitle(self, start_time, end_time, subtitle_text, custom_track_id=None):
        """
        实时注入字幕（复用同一轨道+同一文件，多次调用不覆盖）
        
        Args:
            start_time: 字幕开始时间（秒）
            end_time: 字幕结束时间（秒）
            subtitle_text: 字幕文本
            custom_track_id: 显式指定轨道ID（如2）
        """
        # 1. 基础状态校验（保持原逻辑）
        if not self.current_file or not self.is_playing:
            print("注入失败：未加载视频或未播放")
            return
        if not isinstance(subtitle_text, str) or not subtitle_text.strip():
            print("注入失败：字幕文本为空或格式错误")
            return
        if not isinstance(start_time, (int, float)) or not isinstance(end_time, (int, float)):
            print("注入失败：时间格式错误")
            return

        try:
            # 2. 追加字幕到临时文件（核心：不新建，只追加）
            self._append_sub_to_temp_file(start_time, end_time, subtitle_text)

            # 3. 轨道处理：首次调用创建，后续调用刷新
            if not self.injected_subtitle_ids:
                # 3.1 首次注入：创建轨道并绑定临时文件
                try:
                    if custom_track_id is not None:
                        # 显式指定ID（如2）
                        self.mpv_player.command(
                            "sub-add", self.temp_sub_file, "select", f"track-id={custom_track_id}"
                        )
                        sub_id = custom_track_id
                    else:
                        # 自动分配ID
                        sub_id = self.mpv_player.command("sub-add", self.temp_sub_file, "select")

                    # 记录轨道ID（后续复用）
                    self.injected_subtitle_ids.append(sub_id)
                    # 激活轨道并显示
                    self.mpv_player.sid = "no"  # 禁用内置字幕
                    self.mpv_player.sub = sub_id  # 激活当前轨道
                    self.mpv_player.sub_visibility = True
                    self.mpv_player.sub_auto = "no"
                    print(f"首次注入：轨道ID={sub_id}，内容={subtitle_text[:20]}...")

                except Exception as cmd_err:
                    print(f"创建轨道失败：{cmd_err}")
                    return
            else:
                # 3.2 后续注入：刷新轨道（MPV自动重读临时文件）
                sub_id = self.injected_subtitle_ids[0]
                self.mpv_player.command("sub-reload", sub_id)  # 关键：刷新轨道
                print(f"追加注入：轨道ID={sub_id}，内容={subtitle_text[:20]}...")

        except Exception as e:
            print(f"注入总失败：{type(e).__name__} - {e}")

    def _cleanup_all_subtitles(self):
        # 1. 清理轨道
        for sub_id in self.injected_subtitle_ids:
            try:
                self.mpv_player.command("sub-remove", sub_id)
                print(f"清理轨道：{sub_id}")
            except Exception as e:
                print(f"清理轨道{sub_id}失败：{e}")
        self.injected_subtitle_ids.clear()

        # 2. 清理临时文件（仅1个）
        if self.temp_sub_file and os.path.exists(self.temp_sub_file):
            try:
                os.remove(self.temp_sub_file)
                print(f"清理临时文件：{self.temp_sub_file}")
            except Exception as e:
                print(f"清理文件{self.temp_sub_file}失败：{e}")
        self.temp_sub_file = None  # 重置

        # 3. 重置字幕序号（下次注入从1开始）
        self.subtitle_counter = 0

        # 4. 重置MPV字幕配置
        self.mpv_player.sub_file = ""
        self.mpv_player.sub = "0"
        self.mpv_player.sub_visibility = False

    def _seconds_to_srt_time(self, seconds):
        """修复：支持超过1天的秒数转SRT时间格式 (HH:MM:SS,mmm)"""
        total_seconds = int(seconds)
        milliseconds = int((seconds - total_seconds) * 1000)
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        secs = total_seconds % 60
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{milliseconds:03d}"


    def _append_sub_to_temp_file(self, start_time, end_time, subtitle_text):
        """追加字幕条目到复用的临时SRT文件"""
        # 1. 首次调用：创建临时文件（delete=False表示不自动删除）
        if not self.temp_sub_file:
            temp_file_obj = tempfile.NamedTemporaryFile(
                mode='w', 
                suffix='.srt', 
                delete=False, 
                encoding='utf-8',
                newline='\n'  # 强制LF换行，兼容MPV解析
            )
            self.temp_sub_file = temp_file_obj.name
            temp_file_obj.close()  # 先关闭，后续用追加模式打开

        # 2. 递增字幕序号（SRT格式要求：每个条目序号唯一且递增）
        self.subtitle_counter += 1
        # 3. 转换时间格式（保持原逻辑）
        start_str = self._seconds_to_srt_time(start_time)
        end_str = self._seconds_to_srt_time(end_time)
        # 4. 构造SRT条目（标准格式：序号+时间轴+文本+空行）
        srt_entry = f"{self.subtitle_counter}\n{start_str} --> {end_str}\n{subtitle_text}\n\n"

        # 5. 追加写入文件（关键：用'a'模式而非'w'模式，避免覆盖）
        with open(self.temp_sub_file, 'a', encoding='utf-8', newline='\n') as f:
            f.write(srt_entry)
            f.flush()  # 强制刷新缓冲区
            os.fsync(f.fileno())  # 确保内容写入磁盘（MPV能读取到）


    def fast_forward(self):
        if not self.current_file:
            raise ValueError("未加载视频文件，无法快进")
    
        total_duration = self.get_duration()
        current_pos = self.get_position()
    
        increment = total_duration * 0.01
        
        if increment <= 0: 
            return

        new_pos = min(current_pos + increment, total_duration)
    
        if increment<5: self.set_position(new_pos+5)
        else: self.set_position(new_pos)

    def fast_rewind(self):
        if not self.current_file:
            raise ValueError("未加载视频文件，无法快退")
    
        total_duration = self.get_duration()
        current_pos = self.get_position()
    
        increment = total_duration * 0.01
        if increment <= 0:
            return

        new_pos = max(current_pos - increment, 0)
        self.set_position(new_pos)

    def adjust_playback_speed(self, delta):
        """
        adjust_playback_speed 的 Docstring
        
        :param delta: 速度调整量
        return: 视频调整后的速度
        """
        if not self.current_file:
            raise ValueError("未加载视频文件，无法调整速度")
        
        self.current_speed = max(0.5, min(3.0, self.current_speed + delta))
        self.mpv_player.speed = self.current_speed
        return self.current_speed
    
    def reset_playback_speed(self):
        """重置播放速度"""
        self.current_speed = 1.0
        self.mpv_player.speed = self.current_speed
        return self.current_speed
    
    def start_playback_speed(self):
        """启动速度控制循环（监听按键调整速度）"""
        if not self.current_file:
            raise ValueError("请先调用load_video加载视频文件")
        
        #    ===== 视频播放速度控制 =====
        #操作说明：
        # = → 提速（+0.25x） | - → 降速（-0.25x）
        # 0 → 恢复1x | q → 退出播放

        def on_press(key):
            try:
                if key.char == '=' or key.char == '+':
                    new_speed = self.adjust_playback_speed(0.25)
                    print(f"播放速度调整为：{new_speed:.2f}倍速")
                elif key.char == '-':
                    new_speed = self.adjust_playback_speed(-0.25)
                    print(f"播放速度调整为：{new_speed:.2f}倍速")
                elif key.char == '0':
                    new_speed = self.reset_playback_speed()
                    print(f"播放速度恢复为：{new_speed:.2f}倍速")
                elif key.char == 'q' or key.char == '9':
                    print("退出播放...")
                    self.stop()
                    return False
            except AttributeError:
                pass
        
        self.key_listener = keyboard.Listener(on_press=on_press)
        self.key_listener.start()

        try:
            while self.key_listener.is_alive() and self.current_file:
                try:
                    core_idle = self.mpv_player._get_property('core-idle')
                    if core_idle:
                        time.sleep(0.1)
                        continue
                except Exception:
                    break
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("用户手动中断操作")
            self.stop()

    def cleanup(self):
        if self.key_listener and self.key_listener.is_alive():
            self.key_listener.stop()

        self.stop()
        self.mpv_player.terminate()

    def __del__(self):
        self.cleanup()