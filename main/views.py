from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from common.utils import Scrapper, PriceGetter


@api_view(['GET'])
def scrapper(request):
    scrapper = Scrapper()
    scrapped_data = scrapper.scrapper_for_theblockcrypto()
    if scrapped_data is not False:
        data = {"response": scrapped_data}
        return Response(data, status=status.HTTP_200_OK)
    else:
        data = {
            'response': "An error has occured. Check the logs",
        }
        return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_eth_price(request):
    price_getter = PriceGetter()
    scrapped_data = price_getter.get_price("ethereum", "usd")
    print(scrapped_data)
    data = {"response": scrapped_data}
    return Response(data, status=status.HTTP_200_OK)
