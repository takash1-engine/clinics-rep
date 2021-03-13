from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from django.template import loader
from .form import ClinicForm ,ReputationForm
from .models import Clinic ,Reputation
from django.views.generic import ListView,UpdateView

import numpy as np
import matplotlib.pyplot as plt

# Create your views here.
def index(request):
    all_clinics = Clinic.objects.all().order_by('id')[:5]
    context = {'all_clinics':all_clinics}
    return render(request,'clinic/index.html',context)


def all_clinics(request):
    all_clinics = Clinic.objects.all()
    all_ave_list = []
    result_list = []

    for c in all_clinics:
        reputations = Reputation.objects.filter(clinic__id = c.id)
        ave_list = []
        condition_list = []
        staff_list = []
        ven_list = []
        respect_list = []
        growth_list = []
        manage_list = []
        eva_list = []
        comp_list = []

        for r in reputations:
            condition_list.append(r.condition)
            staff_list.append(r.staff)
            ven_list.append(r.ventilation)
            respect_list.append(r.respect)
            growth_list.append(r.growth)
            manage_list.append(r.management)
            eva_list.append(r.evaluation)
            comp_list.append(r.compliance)

        con_ave = np.average(condition_list)
        staff_ave = np.average(staff_list)
        ven_ave = np.average(ven_list)
        respect_ave = np.average(respect_list)
        growth_ave = np.average(growth_list)
        manage_ave = np.average(manage_list)
        eva_ave = np.average(eva_list)
        comp_ave = np.average(comp_list)
        ave_list =[con_ave,staff_ave,ven_ave,respect_ave,growth_ave,manage_ave,eva_ave,comp_ave]
        all_ave_list = all_ave_list + np.average(ave_list)

    for c , r in zip(all_clinics,all_ave_list):
        result_list = result_list + [c.id,c.clinic_name,c.directer_name,c.address,c.phone_num,c.homepage,c.station,r]

    context = {'result_list':result_list}
    return render(request,'clinic/all_clinics.html',context)
    

def detail_clinic(request,clinic_id):
    condition_list = []
    staff_list = []
    ven_list = []
    respect_list = []
    growth_list = []
    manage_list = []
    eva_list = []
    comp_list = []

    detail_clinic = Clinic.objects.get(id = clinic_id)
    relation_rep = Reputation.objects.all().filter(clinic_id = clinic_id)

    for rep in relation_rep:
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


    labels = ['待遇面','スタッフ間の仲の良さ','風通しの良さ','スタッフ同士の相互尊重','成長環境','経営状況','人事評価の適正さ','法令遵守']

    c = {'d':detail_clinic,'relation_rep':relation_rep,'ave':ave_list,'labels':labels}
    return render(request,'clinic/detail_clinic.html',c)

class UpdateClinicView(UpdateView):
    template_name = 'clinic/update_clinic.html'
    model = Clinic
    fields = ['clinic_name', 'directer_name','address','phone_num','from_hour','to_hour','holiday','treatment','homepage','station']
    success_url = "detail_clinic.html"
    

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