from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from django.template import loader
from .form import ClinicForm ,ReputationForm
from .models import Clinic ,Reputation
from django.views import generic
from django.urls import reverse

import numpy as np
import matplotlib.pyplot as plt

# functions to get datas

#治療院の各項目の平均評価の割り出し
def get_average_data(filter_rep):
    ave_list = []
    condition_list = []
    staff_list = []
    ven_list = []
    respect_list = []
    growth_list = []
    manage_list = []
    eva_list = []
    comp_list = []

    for rep in filter_rep:
        condition_list.append(rep.condition)
        staff_list.append(rep.staff)
        ven_list.append(rep.ventilation)
        respect_list.append(rep.respect)
        growth_list.append(rep.growth)
        manage_list.append(rep.management)
        eva_list.append(rep.evaluation)
        comp_list.append(rep.compliance)

    con_ave = np.average(condition_list)
    staff_ave = np.average(staff_list)
    ven_ave = np.average(ven_list)
    respect_ave = np.average(respect_list)
    growth_ave = np.average(growth_list)
    manage_ave = np.average(manage_list)
    eva_ave = np.average(eva_list)
    comp_ave = np.average(comp_list)
    ave_list =[con_ave,staff_ave,ven_ave,respect_ave,growth_ave,manage_ave,eva_ave,comp_ave]

    return ave_list


def index(request):
    all_clinics = Clinic.objects.all().order_by('id')[:5]
    context = {'all_clinics':all_clinics}
    return render(request,'clinic/index.html',context)


def all_clinics(request):
    all_clinics = Clinic.objects.all()
    all_ave_list = []

    for c in all_clinics:
        reputations = Reputation.objects.all().filter(clinic_id = c.id)
        ave_list = get_average_data(reputations)
        one_clinics_ave_rep = np.average(ave_list)
        all_ave_list.append([c.id,c.clinic_name,c.directer_name,c.address,c.phone_num,c.homepage,c.station,one_clinics_ave_rep])

    context = {'all_ave_list':all_ave_list}
    return render(request,'clinic/all_clinics.html',context)
    

def detail_clinic(request,clinic_id):
    detail_clinic = Clinic.objects.get(id = clinic_id)
    relation_rep = Reputation.objects.all().filter(clinic_id = clinic_id)

    ave_list = get_average_data(relation_rep)

    labels = ['待遇面','スタッフ間の仲の良さ','風通しの良さ','スタッフ同士の相互尊重','成長環境','経営状況','人事評価の適正さ','法令遵守']

    c = {'d':detail_clinic,'relation_rep':relation_rep,'ave':ave_list,'labels':labels}
    return render(request,'clinic/detail_clinic.html',c)


class UpdateClinicView(generic.edit.UpdateView):
    template_name = 'clinic/update_clinic.html'
    model = Clinic
    fields = ['clinic_name', 'directer_name','address','phone_num','from_hour','to_hour','holiday','treatment','homepage','station']

    def get_success_url(self):
        return reverse('detail_clinic',kwargs={'clinic_id': self.object.pk})
    

def detail_rep(request,clinic_id,reputation_id):
    detail_clinic = Clinic.objects.get(id = clinic_id)
    detail_rep = Reputation.objects.get(id = reputation_id)
    return render(request,'clinic/detail_rep.html',{'clinic':detail_clinic,'rep':detail_rep})


def new_rep(request,clinic_id):
    clinic = get_object_or_404(Clinic, id=clinic_id)
    params = {'message': '', 'form': None}
    if request.method == 'POST':
        form = ReputationForm(request.POST)
        if form.is_valid():
            reputation = form.save(commit=False)
            reputation.clinic = clinic
            reputation.save()
            return redirect('detail_clinic',clinic_id=clinic.id)
        else:
            params['message'] = '再入力して下さい'
            params['form'] = form
    else:
        params['form'] = ReputationForm()
    return render(request, 'clinic/new_rep.html', params)


def new_clinic(request):
    params = {'message': '', 'form': None}
    if request.method == 'POST':
        form = ClinicForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('all_clinics')
        else:
            params['message'] = '再入力して下さい'
            params['form'] = form
    else:
        params['form'] = ClinicForm()
    return render(request, 'clinic/new_clinic.html', params)