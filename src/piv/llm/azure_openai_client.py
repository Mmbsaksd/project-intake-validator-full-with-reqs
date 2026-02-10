
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

import json, os
from openai import AzureOpenAI
from logger import CustomLogger
from exception import ValidationException

# Initialize logger
_logger_instance = CustomLogger()
logger = _logger_instance.get_logger(__name__)


class AzureOpenAILLM:
    def __init__(self):
        try:
            self.endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
            self.api_key = os.getenv("AZURE_OPENAI_API_KEY")
            self.deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
            self.api_version = os.getenv("AZURE_OPENAI_API_VERSION")

            if not all([self.endpoint, self.api_key, self.deployment]):
                raise ValidationException("Missing Azure OpenAI configuration: please set AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY and AZURE_OPENAI_DEPLOYMENT_NAME")

            self.client = AzureOpenAI(api_key=self.api_key, azure_endpoint=self.endpoint, api_version=self.api_version)
        except ValidationException:
            raise
        except Exception as e:
            logger.exception("Failed to initialize AzureOpenAI client")
            raise ValidationException("AzureOpenAILLM init failed", e) from e

    def complete_json(self, system_prompt: str, user_payload: str):
        msgs = []
        # Ensure system prompt mentions JSON for Azure OpenAI requirement
        if system_prompt:
            msgs.append({"role": "system", "content": system_prompt})
        else:
            msgs.append({"role": "system", "content": "You are a helpful assistant that responds with valid JSON."})
        msgs.append({"role": "user", "content": user_payload})

        try:
            resp = self.client.chat.completions.create(
                model=self.deployment,
                messages=msgs,
                temperature=0,
                response_format={"type": "json_object"},
            )
            txt = resp.choices[0].message.content
            return json.loads(txt)
        except Exception as e:
            logger.exception("AzureOpenAI completion failed")
            raise ValidationException("AzureOpenAILLM.complete_json failed", e) from e
