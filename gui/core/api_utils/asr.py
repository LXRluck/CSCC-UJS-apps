import requests
from typing import Optional
from pathlib import Path


class ASRClient:
    """语音识别 API 客户端"""

    def __init__(self, api_endpoint: str = None, api_key: str = None):
        """
        初始化 ASR 客户端

        Args:
            api_endpoint: API 端点 URL，例如 "https://api.siliconflow.cn/v1/audio/transcriptions"
            api_key: API 认证密钥
        """
        self.api_endpoint = api_endpoint
        self.api_key = api_key

    def set_credentials(self, api_endpoint: str, api_key: str):
        """
        设置 API 凭证

        Args:
            api_endpoint: API 端点 URL
            api_key: API 认证密钥
        """
        self.api_endpoint = api_endpoint
        self.api_key = api_key

    def transcribe(
        self,
        file_path: str,
        model: str = None
    ) -> Optional[str]:
        """
        调用语音转文本 API

        Args:
            file_path: 音频文件路径
            model: 使用的模型名称，由用户自行指定（例如："FunAudioLLM/SenseVoiceSmall"）

        Returns:
            识别的文本内容，失败时返回 None

        Raises:
            ValueError: 当 API 凭证未设置或参数无效时
            FileNotFoundError: 当音频文件不存在时
            requests.RequestException: 当网络请求失败时
        """
        # 验证 API 凭证
        if not self.api_endpoint:
            raise ValueError("API 端点未设置，请先调用 set_credentials() 设置")
        if not self.api_key:
            raise ValueError("API 密钥未设置，请先调用 set_credentials() 设置")

        # 验证模型名称
        if not model:
            raise ValueError("模型名称不能为空，请指定要使用的模型")

        # 验证文件存在
        file_path_obj = Path(file_path)
        if not file_path_obj.exists():
            raise FileNotFoundError(f"音频文件不存在: {file_path}")

        # 准备请求
        url = self.api_endpoint
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }

        # 准备 multipart/form-data
        with open(file_path, "rb") as audio_file:
            files = {
                "file": (file_path_obj.name, audio_file, "audio/mpeg")
            }
            data = {
                "model": model
            }

            # 发送请求
            try:
                response = requests.post(
                    url,
                    headers=headers,
                    files=files,
                    data=data,
                    timeout=300  # 5分钟超时
                )

                # 检查响应状态
                response.raise_for_status()

                # 解析响应
                result = response.json()

                # 返回识别的文本
                return result.get("text")

            except requests.exceptions.Timeout:
                raise requests.RequestException("请求超时，请检查网络连接或稍后重试")
            except requests.exceptions.HTTPError as e:
                error_msg = f"HTTP 错误: {e.response.status_code}"
                try:
                    error_detail = e.response.json()
                    error_msg += f" - {error_detail.get('message', error_detail)}"
                except:
                    error_msg += f" - {e.response.text}"
                raise requests.RequestException(error_msg)
            except requests.exceptions.RequestException as e:
                raise requests.RequestException(f"网络请求失败: {str(e)}")
            except Exception as e:
                raise Exception(f"处理响应时发生错误: {str(e)}")
