from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin,User
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings 
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    """ユーザープロフィールモデル"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                related_name='profile')

    gender = (
        ('male', '男性'),
        ('female', '女性'),
        ('lgbt', 'LGBT'),
        ('noanswer', '未回答'),
    )

    #都道府県
    prefectures = (
        ('hokkaido', '北海道'),('aomori','青森県'),('iwate', '岩手県'),
        ('miyagi', '宮城県'),('akita', '秋田県'),('yamagata', '山形県'),
        ('fukushima', '福島県'),('ibaraki', '茨城県'),('tochigi', '栃木県'),
        ('gunma', '群馬県'),('saitama', '埼玉県'),('chiba', '千葉県'),
        ('tokyo', '東京都'),('kanagawa', '神奈川県'),('niigata', '新潟県'),
        ('toyama', '富山県'),('ishikawa', '石川県'),('fukui', '福井県'),
        ('yamanashi', '山梨県'),('nagano', '長野県'),('gifu', '岐阜県'),
        ('shizuoka', '静岡県'),('aichi', '愛知県'),('mie', '三重県'),
        ('shiga', '滋賀県'),('kyoto', '京都府'),('osaka', '大阪府'),
        ('hyogo', '兵庫県'),('nara', '奈良県'),('wakayama', '和歌山県'),
        ('tottori', '鳥取県'),('shimane', '島根県'),('okayama', '岡山県'),
        ('hiroshima', '広島県'),('yamaguchi', '山口県'),('tokushima', '徳島県'),
        ('kagawa', '香川県'),('ehime', '愛媛県'),('kochi', '高知県'),
        ('fukuoka', '福岡県'),('saga', '佐賀県'),('nagasaki', '長崎県'),
        ('kumamoto', '熊本県'),('oita', '大分県'),('miyazaki', '宮崎県'),
        ('kagoshima', '鹿児島県'),('okinawa', '沖縄県'),
    )
    birthday = models.DateField(verbose_name='生年月日',null=True)
    gender = models.CharField(verbose_name='性別',choices=gender,max_length = 8,null=True)
    address = models.CharField(verbose_name='住所',choices=prefectures,max_length = 10,null=True)
    carrer = models.TextField(verbose_name='キャリア',max_length = 1000,null=True)

    def __str__(self):
        return self.birthday
        return self.gender
        return self.address
        return self.carrer

    

class UserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(_('email address'), unique=True)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
