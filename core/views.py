from django.core.paginator import Paginator
from django.shortcuts import render, redirect
# Create your views here.
from .models import Category,Contact,New,Comment,Subscribe
import random
from django.db.models import Q

from django.core.mail import send_mail
from django.conf import settings




def index(request):
    qabul_qiluvchilar = ["jovlondev@gmail.com",]
    send_mail(
        subject = 'Prosta test',
        message = 'Bu news projectdidan dars uchun test sifatidan yuborilayotgan xabar,',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list = qabul_qiluvchilar,
    )
    print("\n\n", "Hammaga xabar yuborildi" ,"\n\n")


    news = New.objects.all().order_by('-create')
    random_news = [news[random.randint(0, len(news)-1)], news[random.randint(0, len(news)-1)]]
    print("\n\n",random_news)
    aktual = New.objects.all().order_by('-create')[:4]
    pop_news = New.objects.all().order_by('-create')
    t_random_news = [news[random.randint(0, len(news)-1)],]
    tasodif_news = New.objects.all().order_by('-create')[:4]
    siyosiy_news = [news[random.randint(0, len(news) - 1)], news[random.randint(0, len(news) - 1)]]
    r_siyosiy_news = New.objects.all().order_by('-create')[:4]
    svejiy_news = New.objects.filter(Q(title__icontains = 'tramp') | Q(short_desc__icontains = "tramp"))[:3]
    jamiyat_news = New.objects.all().order_by('-create')[:2]
    jamiyat2_news = New.objects.all().order_by('-create')[:5]
    dunyo_news = New.objects.all().order_by('-create')[:2]
    dunyo_news2 = New.objects.all().order_by('-create')[:5]
    texnologiya_new = New.objects.filter(Q(title__icontains = 'tramp') | Q(short_desc__icontains = "tramp"))[:1]
    ekonomika_new = New.objects.all().order_by('-create')[:4]
    rasmi_news = New.objects.filter(Q(title__icontains = 'tramp') | Q(short_desc__icontains = "tramp"))[:1]
    ctx = {
        'news':news,
        "random_news":random_news,
        'aktual':aktual,
        'pop_news': pop_news,
        't_random_news' : t_random_news,
        'tasodif_news' : tasodif_news,
        'siyosiy_news' : siyosiy_news,
        'r_siyosiy_news' : r_siyosiy_news,
        'svejiy_news' : svejiy_news,
        'jamiyat_news' : jamiyat_news,
        'jamiyat2_news' : jamiyat2_news,
        'dunyo_news' : dunyo_news,
        'dunyo_news2' : dunyo_news2,
        'texnologiya_new' : texnologiya_new,
        'ekonomika_new' : ekonomika_new,
        'rasmi_news' : rasmi_news

    }

    return render(request,'index.html',ctx)


def ctg(request, slug):
    one_ctg = Category.objects.filter(slug=slug).first()
    if not one_ctg:
        return render(request,'category.html',{"error":404})
    news = New.objects.filter(ctg=one_ctg).order_by('-id')
    if not news:
        return  render(request, 'category.html',{"error": 404})

    paginator = Paginator(news, 2)
    page = request.GET.get('page', 1)
    result = paginator.get_page(page)
    ctx = {
        'one_ctg':one_ctg,
        'news':result,
        'len':len(result),
        'paginator': paginator,
        'page':int(page)

    }
    return render(request,'category.html',ctx)


def view(request, pk):
    one_new = New.objects.filter(id=pk).first()
    if not one_new:
        return render(request, 'view.html',{"error":404})
    one_new.views += 1
    one_new.save()

    if request.POST:
        user = request.POST.get('user',None)
        message = request.POST.get('message',None)
        parent_id = request.POST.get('parent_id', 0)
        if None in [user, message]:
            pass
        else:
            Comment.objects.create(
                new=one_new,
                user=user,
                message=message,
                parent_id=None if not parent_id else int(parent_id),
                is_sub=bool(parent_id)
            )
            return redirect('view', pk=pk)

    news = New.objects.filter(ctg = one_new.ctg)
    comments = Comment.objects.filter(is_sub=False, new=one_new ).order_by('-post')
    ctx = {
        'one_new' : one_new,
        'count' : len(comments),
        'comments':comments
    }
    if len(news) > 2:
        random_news = [news[random.randint(0, len(news) - 1)], news[random.randint(0, len(news) - 1)]]
        ctx['random_news'] = random_news

    return render(request, 'view.html', ctx)


def search(request):
    key = request.GET.get('search',None)
    if not key:
        return render(request, 'search.html', {"error": 404})
    news = New.objects.filter(Q(title__icontains=key) |
                              Q(short_desc__icontains=key) |
                              Q(description__icontains=key)|
                              Q(tags__icontains=key))
    paginator = Paginator(news,5)
    page = request.GET.get('page',1)
    result = paginator.get_page(page)

    ctx = {
        "news" : result,
        "count" : paginator.count,
        "paginator" : paginator,
        "page" : page,
        "key" : key,

    }
    return render(request, 'search.html', ctx)


def cnt(request):
    if request.POST:
        try:
            contact = Contact.objects.create(
                ism = request.POST['ism'],
                phone = request.POST['phone'],
                xabar = request.POST['xabar'],
            )
            request.session['succes'] = "Xabaringiz qabul qilindi."
            message = f"Saytdan Yangi Kontakt\n"\
                      f"Ism: {contact.ism}\n"\
                      f"Telefon Raqam: {contact.phone}\n"\
                      f"Xabar: {contact.xabar}"
            
            url = f'https://api.telegram.org/bot{settings.TG_TOKEN}/sendMessage?chat_id={7509489027}&text={message}&parse_mode=HTML'
            requests.get(url)
        except: ...
        return redirect('contact')
    success =  request.session.get('success',None)
    try:
        del request.session['success']
    except: ...

    ctx = {
        "success" : success or ""
    }
    return render(request, 'contact.html', ctx)


def add_to_subs(request,path):
    if request.POST:
        try:
            Subscribe.objects.create(
                email = request.POST['email']
            )
        except:
            pass

    return redirect(path)