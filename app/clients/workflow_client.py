from pydantic import BaseModel
from logging import Logger
import requests
from typing import List, Set, Dict
from utils.logger import Logger
from app.configs.configs import WORKFLOW_BASE_URL, WORKFLOW_APPLICATION_NAME, WORKFLOW_APPLICATION_SECRET
from tqdm import tqdm

class WorflowClient:
    def __init__(self, logger: Logger):
        self.token = None
        self.logger = logger
        self._login()

    def _login(self):
        url = f"{WORKFLOW_BASE_URL}/auth/authenticate"
        
        payload = {
            "ApplicationName": WORKFLOW_APPLICATION_NAME,
            "ApplicationSecret": WORKFLOW_APPLICATION_SECRET
        }
        
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            self.token = response.json().get("token")
            self.logger.info("Login successful, token obtained.")
        else:
            self.logger.error(f"Login failed with status code {response.status_code}: {response.text}")
            self.token = None

    def _make_request(self, method: str, url: str, payload: dict = None, params: dict = None):
        if method not in ["POST", "GET"]:
            raise ValueError(f"Method {method} not supported")
        
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        response = requests.request(method, url, headers=headers, json=payload, params=params)
        if response.status_code == 200 or response.status_code == 201:
            return response.json()

        elif response.status_code == 204:
            return None
        elif response.status_code == 401:
            self.logger.info("Token expired, logging in again...")
            self._login()
            return self._make_request(method, url, payload, params)
        else:
            raise Exception(f"Request failed with status code {response.status_code}: {response.text}")
        
    def upload_part_video_url(
        self, 
        vehicle_stock_number: str,
        part_type_code: str,
        video_url: str,
    ) -> None:
        url = f"{WORKFLOW_BASE_URL}/vehicle-data/upload-vehicle-part-video"
        payload = {
            "vehicleStockNumber": vehicle_stock_number,
            "partTypeCode": part_type_code,
            "videoUrl": video_url,
        }
        self._make_request("POST", url, payload)
