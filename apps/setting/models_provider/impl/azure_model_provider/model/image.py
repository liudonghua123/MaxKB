from typing import Dict

from langchain_openai import AzureChatOpenAI
from langchain_openai.chat_models import ChatOpenAI

from common.config.tokenizer_manage_config import TokenizerManage
from setting.models_provider.base_model_provider import MaxKBBaseModel


def custom_get_token_ids(text: str):
    tokenizer = TokenizerManage.get_tokenizer()
    return tokenizer.encode(text)


class AzureOpenAIImage(MaxKBBaseModel, AzureChatOpenAI):

    @staticmethod
    def new_instance(model_type, model_name, model_credential: Dict[str, object], **model_kwargs):
        optional_params = MaxKBBaseModel.filter_optional_params(model_kwargs)
        return AzureOpenAIImage(
            model_name=model_name,
            openai_api_key=model_credential.get('api_key'),
            azure_endpoint=model_credential.get('api_base'),
            openai_api_version=model_credential.get('api_version'),
            openai_api_type="azure",
            streaming=True,
            **optional_params,
        )
