from django.db import models


# Create your models here.
class User(models.Model):
    # create the attributes of user
    sid = models.CharField(verbose_name='User ID', max_length=10, default='', primary_key=True)
    name = models.CharField(verbose_name='Name', max_length=10, default='')
    email = models.EmailField(verbose_name='Email', default='')
    password = models.CharField(verbose_name='Password', max_length=20,default='')
    introduction = models.TextField(verbose_name='Personal introduction', default='')
    creation_date = models.DateTimeField(verbose_name='Creation date', auto_now_add=True)
    portrait = models.ImageField(verbose_name='User portrait', upload_to='portrait', default='default/default.jpg')
    is_active = models.BooleanField(verbose_name='Active', default=True)

    # change the output format
    def __str__(self):
        return '%s|%s|%s|%s|%s|%s' % (
        self.sid, self.name, self.email, self.password, self.introduction, self.creation_date)

    # change the table name from cusell_user to user
    class Meta:
        db_table = 'User'


class Merchandise(models.Model):
    # create the attributes of merchandise
    mid = models.AutoField(verbose_name='Merchandise ID', primary_key=True)
    sid = models.ForeignKey(User, models.CASCADE)
    name = models.CharField(verbose_name='Merchandise Name', max_length=30, default='')
    price = models.DecimalField(verbose_name='Price', max_digits=10, decimal_places=2, default=0)
    keyword = models.CharField(verbose_name='Keyword', max_length=15, default='')
    description = models.TextField(verbose_name='Description', default='')
    pub_date = models.DateTimeField(verbose_name='Publish time', auto_now_add=True)
    update_date = models.DateTimeField('Update time', auto_now=True)
    image_1 = models.ImageField(verbose_name='image_1', upload_to='image', default='')
    image_2 = models.ImageField(verbose_name='image_2', upload_to='image', default='')
    image_3 = models.ImageField(verbose_name='image_3', upload_to='image', default='')
    image_4 = models.ImageField(verbose_name='image_4', upload_to='image', default='')
    # Liked = models.IntegerField(verbose_name='Liked_Number', default=0)

    # change the output format
    def __str__(self):
        return '%s|%s|%s|%s|%s' % (self.mid, self.price, self.description, self.pub_date, self.update_date)

    # change the table name from cusell_merchandise to merchandise
    class Meta:
        db_table = 'Merchandise'


class Liked(models.Model):
    sid = models.CharField(verbose_name='User ID', max_length=10, default='')
    mid = models.CharField(verbose_name='Merchandise ID', max_length=10, default='')
    add_date = models.DateTimeField(verbose_name='Add time', auto_now_add=True)

    class Meta:
        db_table = 'Liked'
