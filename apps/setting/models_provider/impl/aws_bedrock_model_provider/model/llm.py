from typing import List, Dict

from botocore.config import Config
from langchain_community.chat_models import BedrockChat
from setting.models_provider.base_model_provider import MaxKBBaseModel


def get_max_tokens_keyword(model_name):
    """
    根据模型名称返回正确的 max_tokens 关键字。

    :param model_name: 模型名称字符串
    :return: 对应的 max_tokens 关键字字符串
    """
    maxTokens = ["ai21.j2-ultra-v1", "ai21.j2-mid-v1"]
    # max_tokens_to_sample = ["anthropic.claude-v2:1", "anthropic.claude-v2", "anthropic.claude-instant-v1"]
    maxTokenCount = ["amazon.titan-text-lite-v1", "amazon.titan-text-express-v1"]
    max_new_tokens = [
        "us.meta.llama3-2-1b-instruct-v1:0", "us.meta.llama3-2-3b-instruct-v1:0", "us.meta.llama3-2-11b-instruct-v1:0",
        "us.meta.llama3-2-90b-instruct-v1:0"]
    if model_name in maxTokens:
        return 'maxTokens'
    elif model_name in maxTokenCount:
        return 'maxTokenCount'
    elif model_name in max_new_tokens:
        return 'max_new_tokens'
    else:
        return 'max_tokens'


class BedrockModel(MaxKBBaseModel, BedrockChat):

    @staticmethod
    def is_cache_model():
        return False

    def __init__(self, model_id: str, region_name: str, credentials_profile_name: str,
                 streaming: bool = False, config: Config = None, **kwargs):
        super().__init__(model_id=model_id, region_name=region_name,
                         credentials_profile_name=credentials_profile_name, streaming=streaming, config=config,
                         **kwargs)

    @classmethod
    def new_instance(cls, model_type: str, model_name: str, model_credential: Dict[str, str],
                     **model_kwargs) -> 'BedrockModel':
        optional_params = MaxKBBaseModel.filter_optional_params(model_kwargs)

        config = {}
        # 判断model_kwargs是否包含 base_url 且不为空
        if 'base_url' in model_credential and model_credential['base_url']:
            proxy_url = model_credential['base_url']
            config = Config(
                proxies={
                    'http': proxy_url,
                    'https': proxy_url
                },
                connect_timeout=60,
                read_timeout=60
            )

        return cls(
            model_id=model_name,
            region_name=model_credential['region_name'],
            credentials_profile_name=model_credential['credentials_profile_name'],
            streaming=model_kwargs.pop('streaming', True),
            model_kwargs=optional_params,
            config=config
        )
