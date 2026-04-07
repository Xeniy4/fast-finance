import logging
import json
from httpx import Client

logger = logging.getLogger(__name__)

class LoggingClient:
    def __init__(self, client: Client):
        self.client = client

    def request(self, method: str, url: str, **kwargs):
        # Логируем запрос
        request_body = kwargs.get("json")
        headers = kwargs.get("headers", {})

        logger.info("%s %s", method.upper(), url)
        if request_body:
            logger.debug("Request body:\n%s",
                        json.dumps(request_body, indent=2, ensure_ascii=False, default=str))
        if headers:
            logger.debug("Headers:\n%s",
                        json.dumps({k: v for k, v in headers.items() if "Authorization" not in k},
                                  indent=2, ensure_ascii=False))

        # Выполняем запрос
        response = self.client.request(method, url, **kwargs)

        # Логируем ответ
        logger.info("Response: %s %s", response.status_code, response.reason_phrase)
        try:
            response_json = response.json()
            logger.debug("Response body:\n%s",
                    json.dumps(response_json, indent=2, ensure_ascii=False, default=str))
        except Exception:
            logger.debug("Raw response:\n%s", response.text)

        return response

    # Пробрасываем остальные методы
    def get(self, url, **kwargs):
        return self.request("GET", url, **kwargs)

    def post(self, url, **kwargs):
        return self.request("POST", url, **kwargs)

    def put(self, url, **kwargs):
        return self.request("PUT", url, **kwargs)

    def delete(self, url, **kwargs):
        return self.request("DELETE", url, **kwargs)
