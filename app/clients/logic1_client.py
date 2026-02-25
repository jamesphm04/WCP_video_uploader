import requests
from logging import Logger
import os
from app.configs.configs import LOGIC1_BASE_URL
import re

class Logic1Client:
    def __init__(self, logger: Logger):
        self.logger = logger

    def make_request(self, method: str, url: str, payload: dict = None, params: dict = None):
        if method not in ["POST", "GET"]:
            raise ValueError(f"Method {method} not supported")
        
        response = requests.request(method, url, json=payload, params=params)
        if response.json()["status"] == "success":
            return response.json()["data"]
        else:
            raise Exception(f"Request failed with status code {response.status_code}: {response.text}")

    def get_mvr_video_urls(self, after_date: str):
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', after_date):
            raise ValueError("Invalid date format. Please use YYYY-MM-DD format.")
        
        url = f"{LOGIC1_BASE_URL}/api/MVRMedia/GetMVRMedia?afterDate={after_date}"
        return self._make_request("GET", url)

    
    