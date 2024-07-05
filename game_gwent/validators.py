# import requests
# from django.core.exceptions import ValidationError
# from django.conf import settings
#
#
def validate_and_clean_address(address_instance):
    pass
#     token = settings.DADATA_API_KEY
#     url = "https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/address"
#     headers = {
#         "Content-Type": "application/json",
#         "Accept": "application/json",
#         "Authorization": f"Token {token}",
#     }
#
#     full_address = (
#         f"{address_instance.street}, {address_instance.city},"
#         f"{address_instance.region}, {address_instance.postal_code}"
#     )
#     data = {"query": full_address}
#
#     response = requests.post(url, headers=headers, json=data)
#     result = response.json()
#
#     # Print debug information
#     print("Request Data:", data)
#     print("Full address:", full_address)
#     print("Response status code:", response.status_code)
#     print("Response JSON:", result)
#
#     if response.status_code != 200 or not result.get("suggestions"):
#         raise ValidationError(f"Invalid address. Full address: {full_address}")
#
#     cleaned_address = result["suggestions"][0]["data"]
#     address_instance.street = cleaned_address.get(
#         "street_with_type", address_instance.street
#     )
#     address_instance.city = cleaned_address.get(
#         "city", address_instance.city
#     )
#     address_instance.region = cleaned_address.get(
#         "region_with_type", address_instance.region
#     )
#     address_instance.postal_code = cleaned_address.get(
#         "postal_code", address_instance.postal_code
#     )
