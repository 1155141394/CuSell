from django.db import models


# Create your models here.
class User(models.Model):
    sid = models.CharField('User ID', max_length=10, default='', primary_key=True)
    name = models.CharField('Name', max_length=10, default='')
    email = models.EmailField('Email', default='')
    password = models.CharField('Password', max_length=20,default='')
    introduction = models.TextField('Personal introduction', default='')
    creation_date = models.DateTimeField('Creation date', auto_now_add=True)
    portrait = models.ImageField('User portrait', upload_to='portrait', default='default/default.jpg')
    is_active = models.BooleanField('Active', default=True)

    def __str__(self):
        return '%s|%s|%s|%s|%s|%s' % (
        self.sid, self.name, self.email, self.password, self.introduction, self.creation_date)


    class Meta:
        db_table = 'User'


class Merchandise(models.Model):
    mid = models.CharField('Merchandise ID', max_length=10, primary_key=True, default='')
    price = models.DecimalField('Price', max_digits=10, decimal_places=2, default=0)
    description = models.TextField('Description', default='')
    pub_date = models.DateTimeField('Publish time', auto_now_add=True)
    update_date = models.DateTimeField('Update time', auto_now=True)

    def __str__(self):
        return '%s|%s|%s|%s|%s' % (self.mid, self.price, self.description, self.pub_date, self.update_date)

    class Meta:
        db_table = 'Merchandise'


class Image(models.Model):
    image_id = models.CharField('Image ID', max_length=10, default='', primary_key=True)


    def __str__(self):
        return '%s' % self.image_id

    class Meta:
        db_table = 'Image'
