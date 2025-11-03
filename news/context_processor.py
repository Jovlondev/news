from core.models import Category,New
import requests as rq


def valyuta():
    url = 'https://cbu.uz/uz/arkhiv-kursov-valyut/json/'
    response = rq.get(url).json()
    response = [
        {
            "Ccy" : "Usd",
            "Rate" : '12514.34',
            "Diff" : "-69.39",
        },
        {
            "Ccy": "RUB",
            "Rate": '156.41',
            "Diff": "0",
        },
        {
            "Ccy": "EUR",
            "Rate": '14600.48',
            "Diff": "67.39",
        },
    ]
    return response

def main(request):
    ctgs = Category.objects.filter(is_menu=True)
    svejiy_news = New.objects.filter().order_by('-id')
    return  {
        # 'valyuta' : valyuta(),
        'ctgs' : ctgs,
        'svejiy_news' : svejiy_news,
    }