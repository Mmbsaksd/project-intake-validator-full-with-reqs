
import json, os
from openai import AzureOpenAI

class AzureOpenAILLM:
    def __init__(self):
        self.endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
        self.api_version = os.getenv("AZURE_OPENAI_API_VERSION")
        self.client = AzureOpenAI(api_key=self.api_key, azure_endpoint=self.endpoint, api_version=self.api_version)

    def complete_json(self, system_prompt: str, user_payload: str):
        msgs = []
        # Ensure system prompt mentions JSON for Azure OpenAI requirement
        if system_prompt:
            msgs.append({"role": "system", "content": system_prompt})
        else:
            msgs.append({"role": "system", "content": "You are a helpful assistant that responds with valid JSON."})
        msgs.append({"role": "user", "content": user_payload})

        resp = self.client.chat.completions.create(
            model=self.deployment,
            messages=msgs,
            temperature=0,
            response_format={"type": "json_object"},
        )
        txt = resp.choices[0].message.content
        return json.loads(txt)
