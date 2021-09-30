from django.urls import path, include
from . import views
from django.views.generic import TemplateView 

app_name = 'clinics'

urlpatterns = [
    path('', views.index, name='index'),
    path('clinics/', views.all_clinics, name='all_clinics'),
    path('clinics/<int:clinic_id>/', views.detail_clinic, name='detail_clinic'),
    path('clinics/<int:pk>/update/', views.UpdateClinicView.as_view(), name='update_clinic'),
    path('clinics/<int:clinic_id>/<int:reputation_id>/', views.detail_rep, name='detail_rep'),
    path('clinics/<int:clinic_id>/new_rep/', views.new_rep, name='new_rep'),
    path('new_clinic/', views.new_clinic, name='new_clinic'),
]