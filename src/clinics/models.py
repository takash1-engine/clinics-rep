from django.db import models
from django.core.validators import RegexValidator

# Create your models here.

class Clinic(models.Model):
    clinic_name = models.CharField('治療院名',max_length = 255)
    directer_name = models.CharField('代表者',max_length = 255)
    address = models.CharField('住所',max_length = 255)
    phone_num_regex = RegexValidator(regex=r'^[0-9]+$', message = ("Tel Number must be entered in the format: '09012345678'. Up to 15 digits allowed."))
    phone_num = models.CharField(validators=[phone_num_regex], max_length=15, verbose_name='電話番号')
    from_hour = models.TimeField()
    to_hour = models.TimeField()
    holiday = models.CharField('休日',max_length = 255)
    treatment = models.TextField('施術内容',max_length = 1000)
    homepage = models.CharField('HP',max_length = 255)
    station = models.CharField('最寄り駅',max_length = 255)

    def __str__(self):
        return self.clinic_name
        return self.directer_name
        return self.address
        return self.phone_num
        return self.from_hour
        return self.to_hour
        return self.holiday
        return self.treatment
        return self.homepage
        return self.station

    class Meta:

        verbose_name_plural = '治療院情報'




class Reputation(models.Model):
    rep_num = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    condition = models.PositiveIntegerField('待遇面', choices=rep_num)
    staff = models.PositiveIntegerField('スタッフ間の仲の良さ', choices=rep_num)
    ventilation = models.PositiveIntegerField('風通しの良さ', choices=rep_num)
    respect = models.PositiveIntegerField('スタッフ同士の相互尊重', choices=rep_num)
    growth = models.PositiveIntegerField('成長環境', choices=rep_num)
    management = models.PositiveIntegerField('経営状況', choices=rep_num)
    evaluation = models.PositiveIntegerField('人事評価の適正さ', choices=rep_num)
    compliance = models.PositiveIntegerField('法令遵守', choices=rep_num)

    reason = models.TextField('入社理由・ギャップ',max_length = 1000)
    culture = models.TextField('組織文化',max_length = 1000)
    reward_growth = models.TextField('働きがいや成長環境',max_length = 1000)
    supply = models.TextField('給与制度',max_length = 1000)
    women_work = models.TextField('女性の働きやすさ',max_length = 1000)
    worklife = models.TextField('ワークライフバランス',max_length = 1000)
    strength_weak = models.TextField('治療院の強みや弱み',max_length = 1000)
    director = models.TextField('治療院の代表者',max_length = 1000)

    def __str__(self):
        return self.reason
        return self.culture
        return self.reward_growth
        return self.supply
        return self.women_work
        return self.worklife
        return self.strength_weak
        return self.director

    def __int__(self):
        return self.condition
        return self.staff
        return self.ventilation
        return self.respect
        return self.growth
        return self.management
        return self.evaluation
        return self.compliance

    class Meta:

        verbose_name_plural = '評価情報'