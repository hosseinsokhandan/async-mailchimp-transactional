import json
from typing import List

from aiohttp import ClientResponse, ClientSession, request


class TransactionalAPIClient:
    def __init__(self, api_key: str):
        self.host: str = "https://mandrillapp.com/api/1.0"
        self.user_agent: str = "Swagger-Codegen/1.0.47/python"
        self.format_list: List[str] = ["json", "xml", "yaml"]
        self.content_type: str = "application/json"
        self.default_output_format: str = "json"
        self.accepts: List[str] = [
            "application/json",
            "application/xml",
            "application/x-php",
            "application/x-yaml; charset=utf-8",
        ]
        self.timeout: int = 300
        self.api_key: str = api_key

    async def _handle_response(self, res: ClientResponse):
        data = None

        if res.ok:
            data = await res.json()
        else:
            # TODO: log res.status
            if "application/json" in res.headers.get("content-type"):
                data = await res.json()
            else:
                data = await res.text()

        return data

    async def _request(self, *, path: str, body: dict, headers={}):
        # header parameters
        headers["User-Agent"] = self.user_agent
        headers["Content-Type"] = self.content_type

        # request url
        url = f"{self.host}{path}.{self.default_output_format}"

        # API Key
        body["key"] = self.api_key
        async with ClientSession() as session:
            async with session.post(url, data=json.dumps(body), headers=headers, timeout=self.timeout) as response:
                return await self._handle_response(response)

    async def send_message(self, *, body={}):
        """
        Send a new transactional message through the Transactional API.
        """
        return await self._request(path="/messages/send", body=body)
