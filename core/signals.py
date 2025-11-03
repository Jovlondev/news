from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from django.conf import settings
from .models import *
import requests
from django.core.mail import send_mail, EmailMessage




@receiver(post_save, sender=New)
def news_signals(sender, instance,created, **kwargs):
    """

    """
    if created:
        message = f"Saytdan Yangi Xabar\n" \
                  f"Title: {instance.title}\n" \
                  f"Qisqacha: {instance.short_desc}\n" \
                  f"Date: {instance.create.strftime('%D')}\n"

        email_royxat = [
            "jovlondev@gmail.com"
        ]

        send_mail(
            subject="Saytga Yangi Xabar qo'shildi ",
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=email_royxat,
        )
        print("\n\n", "Barcha gmailarga xabar yuborildi ", "\n\n")

        tg_id = [
            7509489027,
        ]
        for i in tg_id:
            url = f'https://api.telegram.org/bot{settings.TG_TOKEN}/sendMessage?chat_id={i}&text={message}&parse_mode=HTML'
            requests.get(url)

        message = "Xammaga xabar yuborildimi"
        url = f'https://api.telegram.org/bot{settings.TG_TOKEN}/sendMessage?chat_id={7509489027}&text={message}&parse_mode=HTML'
        requests.get(url)


# @receiver(post_save,)
# def new_create(sender,instance=None,created=None,*args,**kwargs):
#     print('\n\nYuboruvchi', sender)
#     print('\nObjects', instance)
#     print('\nYaraldimi', created)
#     print('\n',args,kwargs,'\n\n')
#
#
# @receiver(post_delete, sender=None)
# def delete_signal(sender,instance=None,*args,**kwargs):
#     print("\nYangi Signal\nYuboruvchi",sender)
#     print("\nObjects",instance)
#     print("\n", args, kwargs, "\n\n")


@receiver(post_save,sender=Comment)
def comment_signal(sender,instance,created,**kwargs):
    if created:
        message = f"Saytda Yangi Izoh qo'shildi\n" \
                  f"Yanglik: {instance.new.title}\n " \
                  f"User: {instance.user}\n" \
                  f"Message: {instance.message}\n" \
                  f"Sana: {instance.post.strftime('%H:%M / %d-%B %Y')}"
        url = f'https://api.telegram.org/bot{settings.TG_TOKEN}/sendMessage?chat_id={7509489027}&text={message}&parse_mode=HTML'
        requests.get(url)

#
# @receiver(post_delete, sender=Comment)
# def comment_delete_signal(sender, instance, **kwargs):
#     print("Keldi")
#     message = f"Saytdan Comment o'chirildi\n" f"Comment: <b>{instance.__str__()}</b>\n" \
#
#     url = f'https://api.telegram.org/bot{settings.TG_TOKEN}/sendMessage?chat_id={7509489027}&text={message}&parse_mode=HTML'
#     a = requests.get(url).text
#     print("Ishlayabti", f"\n\n\n{ a }\n\n\n")