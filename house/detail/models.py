from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.timezone import now,timedelta


REGION_CHOICES = (
    ('Чуйская область', 'Чуйская область'),
    ('Таласская область', 'Таласская область'),
    ('Иссык-Кульская область', 'Иссык-Кульская  область'),
    ('Нарынская область', 'Нарынская область'),
    ('Джалал-Абадская область', 'Джалал-Абадская область'),
    ('Ошская область', 'Ошская область'),
    ('Баткенская область', 'Баткенская область')
)


class UserProfile(models.Model):
    AUTH_PROVIDERS = (
        ('local', 'local'),
        ('google', 'google'),
        ('github', 'github'),

    )
    auth_provider = models.CharField(max_length=20, choices=AUTH_PROVIDERS, default='local')
    reset_token = models.CharField(max_length=255, blank=True, null=True)
    reset_token_expire = models.DateTimeField(blank=True, null=True)

    STATUS_CHOICES = (
        ('client', 'client'),
        ('owner', 'owner'),
        ('company_owner', 'company_owner'),
        ('agency_owner', 'agency_owner'),

    )
    first_name = models.CharField(max_length=30,null=True,blank=True)
    user_role = models.CharField(max_length=20,choices=STATUS_CHOICES,default='client')
    profile_picture = models.ImageField(upload_to='user_images/')
    phone_number = PhoneNumberField(region='KG', null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')],
                              null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=50, null=True, blank=True)
    data_registration = models.DateField(auto_now_add=True)

    def is_reset_token_valid(self):
        return self.reset_token and self.reset_token_expire and now() < self.reset_token_expire


class Category(models.Model):
    category_name = models.CharField(max_length=40,unique=True)

    def __str__(self):
        return self.category_name


class BaseOwners(models.Model):
    logo = models.ImageField(upload_to='logo_images/')
    address_office = models.CharField(max_length=40)
    year_founded = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    web_site = models.CharField(max_length=30)
    description = models.TextField()
    phone_number = PhoneNumberField(region='KG', null=True, blank=True)


class Agency(BaseOwners):
    owner = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='owner_agency')
    agency_name = models.CharField(max_length=30,unique=True)

    def __str__(self):
        return self.agency_name

    def get_avg_rating(self):
        ratings = self.reviews.all()
        if ratings.exists():
            return round(sum(i.rating for i in ratings) / ratings.count(),1)
        return 0

    def get_count_people(self):
        total = self.reviews.all()
        if total.exists():
            if total.count() > 3:
                return '3+'
            return total.count()
        return 0

    def get_count_good_grade(self):
        total = self.reviews.all()
        if total.exists():
            num = 0
            for i in total:
                if i.rating > 3:
                    num += 1
            return f'{round((num * 100)/ total.count()) }%'

        return '0%'


class AgencyReview(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_reviews',null=True,blank=True)
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, related_name='reviews',null=True,blank=True)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], null=True, blank=True)
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.user} , {self.agency} , {self.rating}'


class BaseApartment(models.Model):
    property_type = models.CharField(max_length=10, choices=[('продажа', 'продажа'), ('аренда', 'аренда'), ('посуточно', 'посуточно')],)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    region = models.CharField(max_length=30, choices=REGION_CHOICES, default='Чуйская область')
    sentence_type = models.CharField(max_length=50,verbose_name='Тип предложения')
    rental_period = models.CharField(max_length=50,verbose_name='Период аренды')
    series = models.CharField(max_length=50,verbose_name='Серия ')
    house = models.CharField(max_length=50,verbose_name='Дом')
    telephone = models.CharField(max_length=50,verbose_name='телефон')
    internet = models.CharField(max_length=50,verbose_name='интернет')
    storey = models.CharField(max_length=50,verbose_name='этаж')
    state = models.CharField(max_length=50,verbose_name='площадь')
    square = models.CharField(max_length=50,verbose_name='отопление')
    heating = models.CharField(max_length=50,verbose_name='состояние')
    bathroom = models.CharField(max_length=50,verbose_name='санузел')
    gas = models.CharField(max_length=50,verbose_name='газ')
    balcony = models.CharField(max_length=50,verbose_name='балкон ')
    entrance_door = models.CharField(max_length=50,verbose_name='входная дверь')
    parking = models.CharField(max_length=50,verbose_name='парковка')
    furniture = models.CharField(max_length=50,verbose_name='мебель ')
    floor = models.CharField(max_length=50,verbose_name='пол ')
    ceiling_height = models.CharField(max_length=50,verbose_name='высота потолков')
    safety = models.CharField(max_length=100,verbose_name='безопасность')
    miscellaneous = models.CharField(max_length=100,verbose_name='разное')
    description = models.TextField()
    address = models.CharField(max_length=100,verbose_name='адрес')
    price = models.PositiveSmallIntegerField(default=0,verbose_name='цена в месяц')
    data = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'  {self.price} $  -  {self.address}'


class ApartmentPhotos(models.Model):
    home_photo = models.ForeignKey(BaseApartment,related_name='house_photos',on_delete=models.CASCADE)
    image = models.ImageField(upload_to='house_images/')


class OwnerApartment(BaseApartment):
    owner = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='owner_apartment')

    def __str__(self):
        return f'{self.owner} -  {self.price}$ - {self.address}'


class AgencyApartment(BaseApartment):
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, related_name='agency_apartment')

    def __str__(self):
        return f'{self.agency} -  {self.price}$ - {self.address}'


class Company(BaseOwners):
    owner = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='owner_company')
    company_name = models.CharField(max_length=30,unique=True)

    def __str__(self):
        return self.company_name

    def get_avg_rating(self):
        ratings = self.reviews.all()
        if ratings.exists():
            return round(sum(i.rating for i in ratings) / ratings.count(),1)
        return 0

    def get_count_people(self):
        total = self.reviews.all()
        if total.exists():
            if total.count() > 3:
                return '3+'
            return total.count()
        return 0

    def get_count_good_grade(self):
        total = self.reviews.all()
        if total.exists():
            num = 0
            for i in total:
                if i.rating > 3:
                    num += 1
            return f'{round((num * 100)/ total.count()) }%'

        return '0%'


class NewBuilding(models.Model):
    jk_name = models.CharField(max_length=50,verbose_name='Жилой комплекс')
    object_state = models.CharField(max_length=40,verbose_name='состояние объекта')
    region = models.CharField(max_length=40, choices=REGION_CHOICES, default='Чуйская область')
    finish = models.DateField()
    address = models.CharField(max_length=60,verbose_name='адрес')
    series = models.CharField(max_length=50,verbose_name='Серия ')
    storey = models.CharField(max_length=50,verbose_name='этажность')
    types = models.CharField(max_length=20, verbose_name='класс')
    company = models.ForeignKey(Company,on_delete=models.CASCADE,verbose_name='застройщик',related_name='company')
    house_type = models.CharField(max_length=20,verbose_name='тип дома')
    square = models.CharField(max_length=50,verbose_name='отопление')
    description = models.TextField()

    def __str__(self):
        return f'{self.jk_name} -  {self.company}'


class NewBuildingPhotos(models.Model):
    photo = models.ForeignKey(NewBuilding,related_name='new_building_photos',on_delete=models.CASCADE)
    image = models.ImageField(upload_to='new_building_images/')


class CompanyApartment(BaseApartment):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='agency_apartment')

    def __str__(self):
        return f'{self.company} -  {self.price}$ - {self.address}'


class ContactInfo(models.Model):
    contact_info = PhoneNumberField()
    company = models.ForeignKey(BaseOwners,on_delete=models.CASCADE,related_name='contacts')


class CompanyReview(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='reviews',null=True,blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='reviews',null=True,blank=True)
    jk = models.ForeignKey(NewBuilding, on_delete=models.CASCADE, related_name='new_building_reviews')
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], null=True, blank=True)
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.user} , {self.jk} , {self.rating}'


class Favorite(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='favorite_user')
    favorite_house = models.ForeignKey(OwnerApartment, on_delete=models.CASCADE)
    register_date = models.DateTimeField(auto_now_add=True)






















