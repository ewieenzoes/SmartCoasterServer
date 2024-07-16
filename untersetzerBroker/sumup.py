import requests
from django.conf import settings

class SumupAPI:
    def __init__(self):
        self.base_url = settings.SUMUUP_API_URL
        self.api_token = settings.SUMUPAPI_TOKEN
        self.receipt_url = settings.SUMUP_RECEIPT_URL
        self.headers = {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json'
        }

    def get(self, endpoint, params=None):
        url = f'{self.base_url}/{endpoint}'
        response = requests.get(url, headers=self.headers, params=params)
        # response.raise_for_status()
        return response.json()

    def post(self, endpoint, data=None):
        url = f'{self.base_url}/{endpoint}'
        response = requests.post(url, headers=self.headers, json=data)
        # response.raise_for_status()
        return response.json()
    
    def get_reciept_url(self, id):
        return f'{self.receipt_url}MC3P7RKD/receipt/sale:{id}'
    
    def get_merchant_code(self):
        response = SumupAPI.get(self, "me")
        return response["merchant_profile"]["merchant_code"]