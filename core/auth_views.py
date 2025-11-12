import random
import uuid
import datetime
from django.conf import settings
from django.contrib.auth import login , authenticate
from django.shortcuts import render , redirect
from core.models import User,Otp
from methodism.helper import code_decoder,generate_key
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
            print('keldi')
            phone = data.get("login_phone", None)
            pas = data.get("login_pass", None)
            print(data, '>>>>>>>>>>>')
            print(phone, '>>>>><<<<<<<<<<<')
            user = User.objects.filter(phone=phone).first()
            print(user, 'mmmmmmmmmmmmmmmmmmmmmmmmmmm')
            if not user or not user.check_password(pas):
                print(user, '22222222222222222')
                return render(request, "auth/login.html", {"error": "Phone yoki parol xato!"})
            if not user.is_active:
                return render(request, "auth/login.html", {"error": "Ushbu user blocklangan"})

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
        otp = Otp.objects.create(mobile=phone,key=shifr, by = 'login' if key else 'regis')
        request.session['key'] = otp.key
        return redirect("otp")

    ctx = {

    }
    return render(request, 'auth/login.html',ctx)

# auth two -> otp

def otp(request):
   token = request.session.get("key")
   if token:
       redirect("auth")
   if request.POST:
       data = request.POST
       code = "".join(data.get(f"otp{x}") for x in range(1,7))
       otp = Otp.objects.filter(key=token).first()
       if not otp:
           return render(request, "auth/otp.html",{"error":"Token Aniqlanmadi"})
       if otp.is_expired:
           return render(request,"auth/otp.html",{"error":"Token Eskirgan"})
       if otp.is_confirmed:
           return render(request, "auth/otp.html", {"error": "Token Eskirgan"})
       if not otp.check_date():
           otp.is_expired = True
           otp.save()
           return render(request,'auth/otp.html',{'error':'Tokeni vaqti tugadi'})

       natija_code = code_decoder(token,l=2,decode=True).split("$")[1]
       if str(natija_code) != str(code):
           otp.tries +=1
           otp.save()
           return render(request,'auth/otp.html',{'error': f'Kod Xato: {3-otp.tries} urunish qoldi'})
       if otp.by == 'login':
           user = User.objects.filter(phone = otp.mobile).first()
           login(request,user)
       else:
           user = User.objects.create_user(phone=otp.mobile, **otp.extra)
           login(request,user)
           authenticate(request)
           return redirect('home')



   return render(request,'auth/otp.html', ctx)

ctx = {

}
def logout(request):
    return redirect("auth")