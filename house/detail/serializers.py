from rest_framework import serializers
from .models import *


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class SetNewPasswordSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField(min_length=8,write_only=True)


class UserProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class UserProfileReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name']


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_name']


class BaseApartmentSerializers(serializers.ModelSerializer):
    class Meta:
        model = BaseApartment
        fields = '__all__'


class BaseOwnersSerializers(serializers.ModelSerializer):
    class Meta:
        model = BaseOwners
        fields = '__all__'


class AgencyReviewSerializers(serializers.ModelSerializer):
    user = UserProfileReviewSerializers()

    class Meta:
        model = AgencyReview
        fields = ['user', 'rating', 'comment', ]


class AgencySerializers(serializers.ModelSerializer):
    avg_rating = serializers.SerializerMethodField()
    count_people = serializers.SerializerMethodField()
    count_good_grade = serializers.SerializerMethodField()

    class Meta:
        model = Agency
        fields = ['id','owner','agency_name','logo','description','phone_number',
                  'email','year_founded','address_office','web_site',
                  'avg_rating', 'count_people', 'count_good_grade'
                  ]

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_count_people(self, obj):
        return obj.get_count_people()

    def get_count_good_grade(self, obj):
        return obj.get_count_good_grade()


class AgencyCreateSerializers(serializers.ModelSerializer):

    class Meta:
        model = Agency
        fields = ['id','owner','agency_name','logo','description','phone_number',
                  'email', 'year_founded', 'address_office', 'web_site']


class ApartmentPhotosSerializers(serializers.ModelSerializer):
    class Meta:
        model = ApartmentPhotos
        fields = ['image']


class AgencyApartmentListSerializers(serializers.ModelSerializer):
    data = serializers.DateField(format='%Y-%m-%d ')
    house_photos = ApartmentPhotosSerializers(many=True,read_only=True)

    class Meta:
        model = AgencyApartment
        fields = ['id','agency','category',
                  'description','address',
                  'price','data','house_photos']


class AgencyApartmentDetailSerializers(serializers.ModelSerializer):
    data = serializers.DateField(format='%Y-%m-%d ')
    house_photos = ApartmentPhotosSerializers(many=True, read_only=True)

    class Meta:
        model = AgencyApartment
        fields = ['id', 'agency', 'category', 'region', 'sentence_type', 'rental_period', 'series',
                  'house', 'telephone', 'internet', 'storey', 'state', 'square', 'heating', 'bathroom', 'gas',
                  'balcony',
                  'entrance_door', 'parking', 'furniture', 'floor', 'ceiling_height', 'safety', 'miscellaneous',
                  'description', 'address', 'price', 'data', 'house_photos']


class AgencyApartmentCreateSerializers(serializers.ModelSerializer):
    data = serializers.DateField(format='%Y-%m-%d ')
    house_photos = ApartmentPhotosSerializers(many=True, read_only=True)

    class Meta:
        model = AgencyApartment
        fields = ['id', 'agency', 'category', 'region', 'sentence_type', 'rental_period', 'series',
                  'house', 'telephone', 'internet', 'storey', 'state', 'square', 'heating', 'bathroom', 'gas',
                  'balcony',
                  'entrance_door', 'parking', 'furniture', 'floor', 'ceiling_height', 'safety', 'miscellaneous',
                  'description', 'address', 'price', 'data','house_photos']


class OwnerApartmentListSerializers(serializers.ModelSerializer):
    data = serializers.DateField(format='%Y-%m-%d ')
    house_photos = ApartmentPhotosSerializers(many=True,read_only=True)

    class Meta:
        model = OwnerApartment
        fields = ['id','owner','category',
                  'description','address',
                  'price','data','house_photos']


class OwnerApartmentDetailSerializers(serializers.ModelSerializer):
    data = serializers.DateField(format='%Y-%m-%d ')
    house_photos = ApartmentPhotosSerializers(many=True,read_only=True)

    class Meta:
        model = OwnerApartment
        fields = ['id','owner', 'category', 'region', 'sentence_type', 'rental_period', 'series',
                  'house','telephone', 'internet', 'storey', 'state', 'square', 'heating', 'bathroom', 'gas', 'balcony',
                  'entrance_door','parking', 'furniture', 'floor', 'ceiling_height', 'safety', 'miscellaneous',
                  'description','address','price', 'data','house_photos']


class OwnerApartmentCreateSerializers(serializers.ModelSerializer):

    class Meta:
        model = OwnerApartment
        fields = ['id','owner', 'category', 'region', 'sentence_type', 'rental_period', 'series',
                  'house','telephone', 'internet', 'storey', 'state', 'square', 'heating', 'bathroom', 'gas', 'balcony',
                  'entrance_door','parking', 'furniture', 'floor', 'ceiling_height', 'safety', 'miscellaneous',
                  'description','address','price', 'data','house_photos']


class CompanyReviewSerializers(serializers.ModelSerializer):
    user = UserProfileReviewSerializers()

    class Meta:
        model = CompanyReview
        fields = ['user', 'rating', 'comment', ]


class ContactInfoSerializers(serializers.ModelSerializer):
    class Meta:
        model = ContactInfo
        fields = ['contact_info']


class CompanyListSerializers(serializers.ModelSerializer):
    avg_rating = serializers.SerializerMethodField()
    count_people = serializers.SerializerMethodField()
    count_good_grade = serializers.SerializerMethodField()
    owner = UserProfileReviewSerializers()

    class Meta:
        model = Company
        fields = ['id','owner','company_name','logo','address_office',
                  'avg_rating','count_people','count_good_grade',]

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_count_people(self, obj):
        return obj.get_count_people()

    def get_count_good_grade(self, obj):
        return obj.get_count_good_grade()


class CompanyDetailSerializers(serializers.ModelSerializer):
    contacts = ContactInfoSerializers(many=True,read_only=True)
    reviews = CompanyReviewSerializers(many= True,read_only=True)
    owner = UserProfileReviewSerializers()

    class Meta:
        model = Company
        fields = ['id','owner','company_name','logo','address_office','year_founded','email','web_site','description',
                  'reviews','contacts']


class CompanyCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id','owner','company_name','logo','address_office','year_founded','email','web_site','description',]


class NewBuildingPhotosSerializers(serializers.ModelSerializer):
    class Meta:
        model = NewBuildingPhotos
        fields = ['image']


class NewBuildingSerializers(serializers.ModelSerializer):
    new_building_photos = NewBuildingPhotosSerializers(many=True,read_only=True)

    class Meta:
        model = NewBuilding
        fields = ['id','jk_name','object_state','address','company','new_building_photos',]


class NewBuildingDetailSerializers(serializers.ModelSerializer):
    new_building_photos = NewBuildingPhotosSerializers(many=True,read_only=True)

    class Meta:
        model = NewBuilding
        fields = ['id','jk_name','object_state','address','company','region','finish','series','storey','types',
                  'house_type','square','description','new_building_photos']


class NewBuildingCreateSerializers(serializers.ModelSerializer):
    new_building_photos = NewBuildingPhotosSerializers(many=True,read_only=True)

    class Meta:
        model = NewBuilding
        fields = ['id','jk_name','object_state','address','company','region','finish','series','storey','types',
                  'house_type','square','description','new_building_photos']


class FavoriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'







class CompanyApartmentListSerializers(serializers.ModelSerializer):
    data = serializers.DateField(format='%Y-%m-%d ')
    house_photos = ApartmentPhotosSerializers(many=True,read_only=True)

    class Meta:
        model = CompanyApartment
        fields = ['id','company','category',
                  'description','address',
                  'price','data','house_photos']


class CompanyApartmentDetailSerializers(serializers.ModelSerializer):
    data = serializers.DateField(format='%Y-%m-%d ')
    house_photos = ApartmentPhotosSerializers(many=True, read_only=True)

    class Meta:
        model = CompanyApartment
        fields = ['id', 'company', 'category', 'region', 'sentence_type', 'rental_period', 'series',
                  'house', 'telephone', 'internet', 'storey', 'state', 'square', 'heating', 'bathroom', 'gas',
                  'balcony',
                  'entrance_door', 'parking', 'furniture', 'floor', 'ceiling_height', 'safety', 'miscellaneous',
                  'description', 'address', 'price', 'data','house_photos']


class CompanyApartmentCreateSerializers(serializers.ModelSerializer):
    data = serializers.DateField(format='%Y-%m-%d ')
    house_photos = ApartmentPhotosSerializers(many=True, read_only=True)

    class Meta:
        model = CompanyApartment
        fields = ['id', 'company', 'category', 'region', 'sentence_type', 'rental_period', 'series',
                  'house', 'telephone', 'internet', 'storey', 'state', 'square', 'heating', 'bathroom', 'gas',
                  'balcony',
                  'entrance_door', 'parking', 'furniture', 'floor', 'ceiling_height', 'safety', 'miscellaneous',
                  'description', 'address', 'price', 'data','house_photos']



