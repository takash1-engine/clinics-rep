from django import forms
from .models import Clinic,Reputation
 
 
class ClinicForm(forms.ModelForm):
    class Meta:
        model = Clinic
        fields = ('clinic_name', 'directer_name','address','phone_num','from_hour','to_hour','holiday','treatment','homepage','station')
        labels = {
            'clinic_name': '治療院名',
            'directer_name': '代表者',
            'address': '住所',
            'phone_num': '電話番号',
            'from_hour': '営業開始時間',
            'to_hour': '営業終了時間',
            'holiday': '休日',
            'treatment': '施術内容',
            'homepage': 'ホームページ',
            'station': '最寄り駅'
        }


class ReputationForm(forms.ModelForm):
    class Meta:
        model = Reputation
        fields = ('gender','age','condition', 'staff','ventilation','respect','growth','management','evaluation','compliance','reason','culture','reward_growth','supply','women_work','worklife','strength_weak','director')
        labels = {
            'gender': '性別',
            'age': '年齢',
            'condition': '待遇面',
            'staff': 'スタッフ間の仲の良さ',
            'ventilation': '風通しの良さ',
            'respect': 'スタッフ同士の相互尊重',
            'growth': '成長環境',
            'management': '経営状況',
            'evaluation': '人事評価の適正さ',
            'compliance': '法令遵守',
            'reason': '入社理由、ギャップ',
            'culture': '組織文化',
            'reward_growth': '働きがいや成長環境',
            'supply': '給与制度',
            'women_work': '女性の働きやすさ',
            'worklife': 'ワークライフバランス',
            'strength_weak': '治療院の強みや弱み',
            'director': '治療院の代表者について'
        }