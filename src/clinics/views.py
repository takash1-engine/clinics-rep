from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from django.template import loader
from .form import ClinicForm ,ReputationForm
from .models import Clinic ,Reputation

import numpy as np
import matplotlib.pyplot as plt

# Create your views here.
def index(request):
    all_clinics = Clinic.objects.all().order_by('id')[:5]
    context = {'all_clinics':all_clinics}
    return render(request,'clinic/index.html',context)


def all_clinics(request):
    all_clinics = Clinic.objects.all
    context = {'all_clinics':all_clinics}
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

    values = np.array(ave_list)
    labels = ['待遇面','スタッフ間の仲の良さ','風通しの良さ','スタッフ同士の相互尊重','成長環境','経営状況','人事評価の適正さ','法令遵守']

    # 多角形を閉じるためにデータの最後に最初の値を追加する。
    radar_values = np.concatenate([values, [values[0]]])
    # プロットする角度を生成する。
    angles = np.linspace(0, 2 * np.pi, len(labels) + 1, endpoint=True)
    # メモリ軸の生成
    rgrids = [0, 1, 2, 3, 4, 5]


    fig = plt.figure(facecolor="w")
    # 極座標でaxを作成
    ax = fig.add_subplot(1, 1, 1, polar=True)
    # レーダーチャートの線を引く
    ax.plot(angles, radar_values)
    #　レーダーチャートの内側を塗りつぶす
    ax.fill(angles, radar_values, alpha=0.2)
    # 項目ラベルの表示
    ax.set_thetagrids(angles[:-1] * 180 / np.pi, labels)
    # 円形の目盛線を消す
    ax.set_rgrids([])
    # 一番外側の円を消す
    ax.spines['polar'].set_visible(False)
    # 始点を上(北)に変更
    ax.set_theta_zero_location("N")
    # 時計回りに変更(デフォルトの逆回り)
    ax.set_theta_direction(-1)

    # 多角形の目盛線を引く
    for grid_value in rgrids:
        grid_values = [grid_value] * (len(labels)+1)
        ax.plot(angles, grid_values, color="gray",  linewidth=0.5)

    # メモリの値を表示する
    for t in rgrids:
        # xが偏角、yが絶対値でテキストの表示場所が指定される
        ax.text(x=0, y=t, s=t)

    # rの範囲を指定
    ax.set_rlim([min(rgrids), max(rgrids)])
    ax.set_title("レーダーチャート", pad=20)
    plt.show()

    c = {'d':detail_clinic,'relation_rep':relation_rep,'ave':ave_list,'labels':labels,'plt':plt.show()}
    return render(request,'clinic/detail_clinic.html',c)


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