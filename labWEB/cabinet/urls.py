from django.urls import path
from . import views

urlpatterns = [
    path('', views.PersonalCabinetView.as_view(), name='personal_cabinet'),
    path('save_theme/', views.save_theme_view, name='save_theme'),
    path('protected_resource/', views.protected_resource, name='protected_resource'),
    path('logout/', views.logout_view, name='logout'),
    path('delete_token/', views.delete_token, name='delete_token'),

    path('retrieve_data/', views.retrieve_data, name='retrieve_data'),
    path('total_records/', views.total_records, name='total_records'),
    path('count_records_last_month/', views.count_records_last_month, name='count_records_last_month'),
    path('last_added_record/', views.last_added_record, name='last_added_record'),
    path('display_results/', views.display_results, name='display_results'),
    path('search_results/', views.search_results, name='search_results'),
    path('search_results_2/', views.search_results_2, name='search_results_2'),
]