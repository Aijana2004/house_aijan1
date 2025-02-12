from rest_framework import routers
from .views import *
from django.urls import path, include

router = routers.SimpleRouter()

router.register(r'users', UserProfileViewSet, basename='users')
router.register(r'category', CategoryViewSet, basename='category')
router.register(r'agency_review', AgencyReviewViewSet, basename='agency_review')
router.register(r'company_review', CompanyReviewViewSet, basename='company_review')


urlpatterns = [
    path('', include(router.urls)),
    path('forgot_password/', ForgotPasswordView.as_view(), name=' forgot_password'),
    path('verify_reset_password/', VerifyResetTokenView.as_view(), name=' verify_reset_password'),
    path('reset_password/', ResetPasswordView.as_view(), name=' reset_password'),
    path('company/', CompanyListAPIView.as_view(), name=' company_list'),
    path('company/<int:pk>/', CompanyDetailAPIView.as_view(), name=' company_detail'),
    path('company/create/', CompanyCreateAPIView.as_view(), name='company_create'),
    path('company/edit/<int:pk>/', CompanyEditAPIView.as_view(), name='company_edit'),
    path('agency/',AgencyAPIView.as_view(),name='agency_list'),
    path('agency/create/', AgencyCreateAPIView.as_view(), name='agency_create'),
    path('agency/edit/<int:pk>/', AgencyEditAPIView.as_view(), name='agency_edit'),
    path('apartment/', OwnerApartmentAPIView.as_view(), name=' apartment_list'),
    path('apartment/<int:pk>/', OwnerApartmentDetailAPIView.as_view(), name=' apartment_detail'),
    path('apartment/create/',OwnerApartmentCreateAPIView.as_view(),name = 'apartment_create'),
    path('apartment/edit/<int:pk>/', ApartmentUpdateAPIView.as_view(), name='apartment_edit'),
    path('new_building/', NewBuildingAPIView.as_view(), name=' new_building_list'),
    path('new_building/<int:pk>/', NewBuildingDetailAPIView.as_view(), name=' new_building_detail'),
    path('new_building/create/',NewBuildingCreateAPIView.as_view(),name = 'new_building_create'),
    path('new_building/edit/<int:pk>/', NewBuildingEditAPIView.as_view(), name='new_building_edit'),
    path('apartment/agency/', AgencyApartmentAPIView.as_view(), name=' apartment_agency_list'),
    path('apartment/agency/<int:pk>/', AgencyApartmentDetailAPIView.as_view(), name=' apartment_agency_detail'),
    path('apartment/agency/create/', AgencyApartmentCreateAPIView.as_view(), name='apartment_agency_create'),
    path('apartment/agency/edit/<int:pk>/', AgencyApartmentEditAPIView.as_view(), name='apartment_agency_edit'),
    path('apartment/company/', CompanyApartmentAPIView.as_view(), name=' apartment_company_list'),
    path('apartment/company/<int:pk>/', CompanyApartmentDetailAPIView.as_view(), name=' apartment_company_detail'),
    path('apartment/company/create/', CompanyApartmentCreateAPIView.as_view(), name='apartment_company_create'),
    path('apartment/company/edit/<int:pk>/', CompanyApartmentEditAPIView.as_view(), name='apartment_company_edit'),
    ]