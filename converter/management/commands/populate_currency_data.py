import requests
from unicodedata import normalize
from django.core.management.base import BaseCommand
from converter.models import Currency


class Command(BaseCommand):
    help = 'Add symbols and their names to the database'

    def handle(self, *args, **options):
        #this is used to normalize the json data in symbol names
        def normalize_unicode_in_json(data):
            if isinstance(data, str):
                return normalize('NFC', data)
            elif isinstance(data, list):
                return [normalize_unicode_in_json(item) for item in data]
            elif isinstance(data, dict):
                return {key: normalize_unicode_in_json(value) for key, value in data.items()}
            else:
                return data

        def get_exchange_rate(): #this is used to get the exchange rate data as a dictionary
            base_url = 'http://data.fixer.io/api/latest'
            params = {
                'access_key': 'f136c31426b44b704672fc731e7bcb99'
            }
            response = requests.get(base_url, params=params)
            data = response.json()['rates']

            rounded_data = {currency: round(value, 2) for currency, value in data.items()}

            return rounded_data

        def get_symbol_data(): #this is used to get the symbol data as a list with dictionaries
            base_url = 'http://data.fixer.io/api/symbols'
            params = {
                'access_key': 'f136c31426b44b704672fc731e7bcb99'
            }
            response = requests.get(base_url, params=params)
            data = response.json()

            normalized_data = normalize_unicode_in_json(data)

            for_model_data = [] #creating a list of dictionaries to store the data for the model
            for code, name in normalized_data['symbols'].items():
                for_model_dict = {'code': code, 'name': name}
                for_model_data.append(for_model_dict)

            return for_model_data

        exchange_data = get_exchange_rate()
        model_data = get_symbol_data()

        model_data = [
            {
                'code': currency['code'],
                'name': currency['name'],
                'exchange_rate': exchange_data[currency['code']]
            }
            for currency in model_data
            if currency['code'] in exchange_data
        ]

        exeptions_list = ['XAU', 'XAG', 'BTC']
        #finally populating the database
        for item in model_data:
            if item['code'] in exeptions_list:
                continue
            Currency.objects.update_or_create(
                code=item['code'],
                defaults={
                    'name': item['name'],
                    'base': 'EUR',
                    'exchange_rate': item['exchange_rate']
                }
            )

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
