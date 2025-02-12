from .models import Category,NewBuilding,BaseOwners,Company,Agency,OwnerApartment,AgencyApartment,BaseApartment,CompanyApartment
from modeltranslation.translator import TranslationOptions,register


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('category_name',)


@register(BaseApartment)
class BaseApartmentTranslationOptions(TranslationOptions):
    fields = ('description','region', 'sentence_type', 'rental_period', 'series',
    'house', 'telephone', 'internet', 'storey', 'state', 'square', 'heating', 'bathroom', 'gas', 'balcony',
    'entrance_door', 'parking', 'furniture', 'floor', 'ceiling_height', 'safety', 'miscellaneous',
    'description', 'address', 'price', 'data',)


@register(OwnerApartment)
class OwnerApartmentTranslationOptions(TranslationOptions):
    fields = ('owner',)


@register(BaseOwners)
class BaseOwnersTranslationOptions(TranslationOptions):
    fields = ('description','address_office',)


@register(AgencyApartment)
class AgencyApartmentTranslationOptions(TranslationOptions):
    fields = ('agency',)


@register(CompanyApartment)
class CompanyApartmentTranslationOptions(TranslationOptions):
    fields = ('company',)


@register(NewBuilding)
class NewBuildingTranslationOptions(TranslationOptions):
    fields = ('jk_name', 'description')


@register(Company)
class CompanyTranslationOptions(TranslationOptions):
    fields = ('company_name', )


@register(Agency)
class AgencyTranslationOptions(TranslationOptions):
    fields = ( 'agency_name',)
