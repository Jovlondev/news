import random
import uuid
from django.conf import settings
from django.shortcuts import render , redirect
from core.models import User,Otp
from methodism import code_decoder,generate_key
import requests

def send_sms(code):
    url = "https://notify.eskiz.uz/api/message/sms/send"
    payload = {"mobile_phone" : "998994920435",
               "message" : f"Bu Eskiz dan test",
               "from" : "4546",
               "callback_url" : "http://0000.uz/test.php"
               }
    files = [

    ]
    headers = {
        "AUTHORIZATION" : f"Bearer {settings.ESKIZ_TOKEN}"
    }
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    print(response)
    print(response.text)

def auth(request):
    if request.POST:
        key = request.POST.get("login", None)
        data = request.POST
        if key:
            phone = data.get("login_phone", None)
            pas = data.get("login_pass", None)

            user = User.objects.filter(phone=phone).first()
            if not user:
                return render(request, "auth/login.html", {"error": "Phone Yoki Parol Xato"})

            if not user.check_password(str(pas)):
                return render(request,"auth/login.html", {"error":"Phone Yoki Parol Xato"})
            #OTP yharatishimiz kerak

        # login qilish kerak
        else:
            phone = data.get("regis_phone", None)


        code = random.randint(100_000, 999_999)
        send_sms(code)
        message = f"Sizning OTP kodingiz: {code}"
        url = f'https://api.telegram.org/bot{settings.TG_TOKEN}/sendMessage?chat_id={7509489027}&text={message}&parse_mode=HTML'
        requests.get(url)
        unical = uuid.uuid4()
        gen_code = generate_key(15)

        natija = f"{unical}${code}${gen_code}"
        shifr = code_decoder(natija, l=2)
        otp = Otp.objects.create(mobile=phone,key=shifr)
        request.session['key'] = otp.key
        return redirect("otp")

    ctx = {

    }
    return render(request, 'auth/login.html',ctx)

def logout(request):
    return redirect("login")