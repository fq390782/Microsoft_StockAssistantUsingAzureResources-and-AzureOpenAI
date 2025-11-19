from openai import AzureOpenAI
from ..settings import api_settings


def get_azure_open_ai_instance():
    """Azure OpenAI 인스턴스를 전역으로 관리하여 반환."""
    if not api_settings.AZURE_OPENAI_ENDPOINT:
        raise EnvironmentError("Endpoint is not provided.")
    if not hasattr(get_azure_open_ai_instance, '_instance'):
        instance = AzureOpenAI(
            azure_deployment=api_settings.AZURE_OPENAI_DEPLOYMENT,
            api_key=api_settings.AZURE_OPENAI_KEY,
            api_version=api_settings.AZURE_OPENAI_API_VERSION,
            azure_endpoint=api_settings.AZURE_OPENAI_ENDPOINT,
        )
        get_azure_open_ai_instance._instance = instance     # type: ignore
    return get_azure_open_ai_instance._instance             # type: ignore


def send_conversation_to_openai(
        az_openai: AzureOpenAI,
        model: str,
        system_context: str,
        user_context: str,
        response_json_format: bool=True
):
    kwargs = {}
    if response_json_format:
        kwargs['response_format'] = {'type': 'json_object'}
    response = az_openai.chat.completions.create(
        model=model,
        messages=[
            {   
                "role": "system", 
                "content": system_context
            },
            {   
                "role": "user",
                # "content": user_context 
                "content": f"```json\n{user_context}```" if response_json_format else user_context
            }
        ],
        **kwargs
    )

    return response.choices[0].message.content

