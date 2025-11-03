import datetime

from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=56)
    slug = models.CharField(max_length=50,unique=True)
    is_menu = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(slef.name)

        return super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Kategoriya'
        verbose_name_plural = '1.Kategoriyalar'


class New(models.Model):
    title = models.CharField(max_length=256)
    short_desc = models.TextField()
    description = models.TextField()
    image1 = models.ImageField(upload_to="news/")
    image2 = models.ImageField(upload_to="news/",null=True,blank=True)
    ctg = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.CharField(max_length=100)
    create = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(editable=False,default=0)

    def save(self, *args, **kwargs):
        if '#'not in self.tags:
            self.tags = '#' + '#'.join(self.strip().split())
        return super(New, self).save(*args, **kwargs)

    def get_tags(self):
        return self.tags.strip('#').replace(" ","").split('#')

    def get_date(self):
        now = datetime.datetime.now()
        calc = int((now - self.create).total_seconds() // 60)
        if calc == 0:
            return "Hozirgina"
        if 0 < calc < 60:
            return f"{calc} minut oldin"
        if 60*1 <= calc <60 * 24:
            return f"{int(calc // 60)} soat oldin"
        return self.create.strftime("%H:%M / %d-%B %Y")

    def __str__(self):
        return self.tags
    class Meta:
        verbose_name = 'Yanglik'
        verbose_name_plural = '4.Yangliklar'






class Contact(models.Model):
    ism = models.CharField(max_length=56)
    phone = models.CharField(max_length=15)
    xabar = models.TextField()
    is_trash = models.BooleanField(default=False)

    def __str__(self):
        return self.xabar

    class Meta:
        verbose_name = 'Kontakt'
        verbose_name_plural = '3.Kontaktlar'


class Subscribe(models.Model):
    email = models.EmailField()
    is_trash = models.BooleanField(default=False)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Subscribe'
        verbose_name_plural = '5.Subscribes'

class Comment(models.Model):
    new = models.ForeignKey(New,on_delete=models.CASCADE,related_name='comments')
    user = models.CharField(max_length=50)
    message = models.TextField()
    post = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self',on_delete=models.SET_NULL, null=True, blank=True, related_name='subs')
    is_sub = models.BooleanField(default=False)


    def __str__(self):
        return f'{self.user} -> {self.message} '

    class Meta:
        verbose_name = 'Komentariya'
        verbose_name_plural = '2.Komentariyalar'

    def get_date(self):
        import datetime
        now = datetime.datetime.now()
        calc = int((now - self.post).total_seconds() // 60)
        if calc == 0:
            return "Hozirgina"
        if 0 < calc < 60:
            return f"{calc} minut oldin"
        if 60*1 <= calc <60 * 24:
            return f"{int(calc // 60)} soat oldin"
        return self.post.strftime("%H:%M / %d-%B %Y")
