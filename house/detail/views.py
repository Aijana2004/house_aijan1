from rest_framework import viewsets,generics
from .serializers import *
from .filters import OwnerApartmentFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .permissions import (CheckAgencyCreate,CheckOwnerAgency,CheckCompanyCreate,CheckOwnerCompany,CheckOwnerJK,CheckOwnerApartment,
                          CheckOwnerCreateApartment,CheckAgencyApartment)

from django.utils.timezone import now, timedelta
from django.core.mail import send_mail
from django.conf import settings
import jwt
from .models import UserProfile
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password

SECRET_KEY = settings.SECRET_KEY
RESET_TOKEN_EXPIRY_MINUTES = 30


class ForgotPasswordView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        user = UserProfile.objects.filter(email=email).first()

        if not user:
            return Response({'detail': 'пользовател не найден'},status=status.HTTP_404_NOT_FOUND)
        if user.auth_provider != 'local':
            return Response({'detail': 'используйте вход через соцсеть'},status=status.HTTP_400_BAD_REQUEST)

        reset_token = jwt.encode(
            {'sub': user.email, 'exp': now() + timedelta(minutes=RESET_TOKEN_EXPIRY_MINUTES)},
            SECRET_KEY,
            algorithm='HS256'
        )

        user.reset_token = reset_token
        user.reset_token_expiry = now()+timedelta(minutes=RESET_TOKEN_EXPIRY_MINUTES)
        user.save()

        reset_link = f'http://localhost:3000/reset-password?token={reset_token}'
        send_mail(
            subject='сброс пароля',
            message=f'для сброса пароля перейдите по ссылке:{reset_link}',
            from_email=settings.DEFULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
        return Response({'messege': 'ссылка для сброса пароля отправлена'}, status=status.HTTP_200_OK)


class VerifyResetTokenView(APIView):
    def post(self,request):
        token = request.data.get('token')
        try:
            payload = jwt.decode(token,SECRET_KEY,algorithms=['HS256'])
            email = payload.get('sub')
            user = UserProfile.objects.filter(email=email,reset_token=token).first()
            if not user or not user.is_reset_token_valid():
                raise jwt.ExpiredSignatureError
            return Response({'valid': True}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({'detail': 'токен истек'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.DecodeError:
            return Response({'detail': 'не верный токен'}, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    def post(self, request):
        serializer = SetNewPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data['token']
        new_password = serializer.validated_data['new_password']

        try:
            payload = jwt.decode(token,SECRET_KEY,algorithms=['HS256'])
            email = payload.get('sub')
            user = UserProfile.objects.filter(email=email,reset_token=token).first()
            if not user or not user.is_reset_token_valid():
                raise jwt.ExpiredSignatureError

            user.password = make_password(new_password)
            user.reset_token =None
            user.reset_token_expiry= None
            user.save()
            return Response({'message':'пароль успешно изменен'},status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({'detail': 'токен истек'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.DecodeError:
            return Response({'detail': 'не верный токен'}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializers


class BaseApartmentViewSet(viewsets.ModelViewSet):
    queryset = BaseApartment.objects.all()
    serializer_class = BaseApartmentSerializers


class BaseOwnersViewSet(viewsets.ModelViewSet):
    queryset = BaseOwners.objects.all()
    serializer_class = BaseOwnersSerializers


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers


class AgencyAPIView(generics.ListAPIView):
    queryset = Agency.objects.all()
    serializer_class = AgencySerializers


class AgencyCreateAPIView(generics.CreateAPIView):
    queryset = Agency.objects.all()
    serializer_class = AgencyCreateSerializers
    permission_classes = [CheckAgencyCreate]


class AgencyEditAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Agency.objects.all()
    serializer_class = AgencyCreateSerializers
    permission_classes = [CheckAgencyCreate,CheckOwnerAgency]


class AgencyReviewViewSet(viewsets.ModelViewSet):
    queryset = AgencyReview.objects.all()
    serializer_class = AgencyReviewSerializers


class AgencyApartmentAPIView(generics.ListAPIView):
    queryset = AgencyApartment.objects.all()
    serializer_class = AgencyApartmentListSerializers
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['address']
    ordering_fields = ['price']


class AgencyApartmentDetailAPIView(generics.ListAPIView):
    queryset = AgencyApartment.objects.all()
    serializer_class = AgencyApartmentDetailSerializers


class AgencyApartmentCreateAPIView(generics.CreateAPIView):
    queryset = AgencyApartment.objects.all()
    serializer_class = AgencyApartmentCreateSerializers
    permission_classes = [CheckAgencyCreate]


class AgencyApartmentEditAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AgencyApartment.objects.all()
    serializer_class = AgencyApartmentCreateSerializers
    permission_classes = [CheckAgencyCreate,CheckAgencyApartment]


class OwnerApartmentAPIView(generics.ListAPIView):
    queryset = OwnerApartment.objects.all()
    serializer_class = OwnerApartmentListSerializers
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_class = OwnerApartmentFilter
    search_fields = ['address']
    ordering_fields = ['price']


class OwnerApartmentDetailAPIView(generics.ListAPIView):
    queryset = OwnerApartment.objects.all()
    serializer_class = OwnerApartmentDetailSerializers


class OwnerApartmentCreateAPIView(generics.CreateAPIView):
    queryset = OwnerApartment.objects.all()
    serializer_class = OwnerApartmentCreateSerializers
    permission_classes = [CheckOwnerCreateApartment]


class ApartmentUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OwnerApartment.objects.all()
    serializer_class = OwnerApartmentCreateSerializers
    permission_classes = [CheckOwnerApartment,CheckOwnerCreateApartment]


class ApartmentPhotosViewSet(viewsets.ModelViewSet):
    queryset = ApartmentPhotos.objects.all()
    serializer_class = ApartmentPhotosSerializers


class CompanyListAPIView(generics.ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanyListSerializers


class CompanyDetailAPIView(generics.ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanyDetailSerializers


class CompanyCreateAPIView(generics.CreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanyCreateSerializers
    permission_classes = [CheckCompanyCreate]


class CompanyEditAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanyCreateSerializers
    permission_classes = [CheckCompanyCreate,CheckOwnerCompany]


class NewBuildingAPIView(generics.ListAPIView):
    queryset = NewBuilding.objects.all()
    serializer_class = NewBuildingSerializers


class NewBuildingDetailAPIView(generics.ListAPIView):
    queryset = NewBuilding.objects.all()
    serializer_class = NewBuildingDetailSerializers


class NewBuildingCreateAPIView(generics.CreateAPIView):
    queryset = NewBuilding.objects.all()
    serializer_class = NewBuildingCreateSerializers
    permission_classes = [CheckCompanyCreate,CheckOwnerJK]


class NewBuildingEditAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = NewBuilding.objects.all()
    serializer_class = NewBuildingCreateSerializers
    permission_classes = [CheckCompanyCreate,CheckOwnerJK]


class NewBuildingPhotosViewSet(viewsets.ModelViewSet):
    queryset = NewBuildingPhotos.objects.all()
    serializer_class = NewBuildingPhotosSerializers


class ContactInfoViewSet(viewsets.ModelViewSet):
    queryset = ContactInfo.objects.all()
    serializer_class = ContactInfoSerializers


class CompanyReviewViewSet(viewsets.ModelViewSet):
    queryset = CompanyReview.objects.all()
    serializer_class = CompanyReviewSerializers


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializers





class CompanyApartmentAPIView(generics.ListAPIView):
    queryset = CompanyApartment.objects.all()
    serializer_class = CompanyApartmentListSerializers
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['address']
    ordering_fields = ['price']


class CompanyApartmentDetailAPIView(generics.ListAPIView):
    queryset = CompanyApartment.objects.all()
    serializer_class = CompanyApartmentDetailSerializers


class CompanyApartmentCreateAPIView(generics.CreateAPIView):
    queryset = CompanyApartment.objects.all()
    serializer_class = CompanyApartmentCreateSerializers
    permission_classes = [CheckCompanyCreate]


class CompanyApartmentEditAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CompanyApartment.objects.all()
    serializer_class = CompanyApartmentCreateSerializers
    permission_classes = [CheckCompanyCreate,CheckOwnerJK]
#








