import os

import toml
import argparse
import socket
import json
import base64
import logging

from sms_platform.models.request_sms_platform import HTTPRequest
from sms_platform.models.response_sms_platform import HTTPResponse


class Process:

    def __init__(self) -> None:
        self.setup_logging()
        self.logger = logging.getLogger(__name__)

    def load_config(self):
        with open('config.toml', 'r') as file:
            config = toml.load(file)
        return config['sms_service']

    def setup_logging(self):
        """Настраивает логирование в файл"""
        log_dir = "logs"
        log_file = os.path.join(log_dir, "sms_service.log")

        # Создаем папку для логов, если её нет
        os.makedirs(log_dir, exist_ok=True)

        logging.basicConfig(
            level=logging.INFO,  # Можно сменить на DEBUG
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler(log_file, encoding="utf-8"),  # Лог в файл
                logging.StreamHandler()  # Лог в консоль
            ]
        )

    def load_config(self):
        with open('config.toml', 'r') as file:
            config = toml.load(file)
        return config['sms_service']

    def parse_arguments(self):
        parser = argparse.ArgumentParser(description="SMS Sender CLI")
        parser.add_argument('--sender', required=True, help="Номер отправителя")
        parser.add_argument('--recipient', required=True, help="Номер получателя")
        parser.add_argument('--message', required=True, help="Текст сообщения")
        return parser.parse_args()

    def send_http_request(self, config, sender, recipient, message):
        try:
            url = "/send_sms"
            body = json.dumps({
                "sender": sender,
                "recipient": recipient,
                "message": message
            })
            headers = {
                "Host": config['server_address'],
                "Content-Type": "application/json",
                "Content-Length": str(len(body)),
                "Authorization": "Basic " + base64.b64encode(
                    f"{config['username']}:{config['password']}".encode()
                ).decode()
            }

            request = HTTPRequest("POST", url, headers, body)

            server_address, server_port = config['server_address'].split(":")
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((server_address, int(server_port)))
                s.sendall(request.to_bytes())

                response_data = b""
                while True:
                    chunk = s.recv(4096)
                    if not chunk:
                        break
                    response_data += chunk

            response = HTTPResponse.from_bytes(response_data)
            return response

        except socket.error as e:
            self.logger.error(f"Ошибка подключения к серверу: {e}")
            return HTTPResponse(500, {}, json.dumps({"error": "Connection error"}))
        except Exception as e:
            self.logger.error(f"Произошла ошибка: {e}")
            return HTTPResponse(500, {}, json.dumps({"error": "Internal error"}))
