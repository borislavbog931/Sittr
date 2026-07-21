from django.urls import path
from .views import (
    home_page,
    about_page,
    set_language,
    coming_soon_page,
    help_page,
    pricing_page,
    calculator_page,
    how_it_works_sittrs_page,
    how_it_works_owners_page,
    terms_page,
    privacy_page,
    cookie_policy_page,
)

urlpatterns = [
    path('', home_page, name='home'),
    path('about/', about_page, name='about'),
    path('language/<str:lang_code>/', set_language, name='set_language'),
    path('coming-soon/', coming_soon_page, name='coming_soon'),
    path('help/', help_page, name='help'),
    path('pricing/', pricing_page, name='pricing'),
    path('calculator/', calculator_page, name='calculator'),
    path('how-it-works/sittrs/', how_it_works_sittrs_page, name='how_it_works_sittrs'),
    path('how-it-works/owners/', how_it_works_owners_page, name='how_it_works_owners'),
    path('terms/', terms_page, name='terms'),
    path('privacy/', privacy_page, name='privacy'),
    path('cookies/', cookie_policy_page, name='cookie_policy'),

]
