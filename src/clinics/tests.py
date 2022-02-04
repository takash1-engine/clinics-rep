from django.test import TestCase
from clinics.models import Clinic,Reputation

class MakeClinicTestCase(TestCase):
    def a(b):
        return b

class MakeReputationTestCase(TestCase):
    def setUp(self):
        clinic_sample_info = {"id":1,
                              'clinic_name' : "山田治療院" ,
                              'directer_name' : "山田太郎",
                              'address': "埼玉県",
                              'phone_num':"08012345678",
                              'from_hour':"1000",
                              'to_hour':"2000",
                              'holiday':"土曜日",
                              'treatment':"指圧、針",
                              'homepage':"http://yamada.chiryoin.con",
                              'station':"大宮"}
        Clinic.objects.create(clinic_sample_info)

    def test_rep_post(self):
        reputation_sample_info = {"id":1,
                                  "clinic_id":1,
                                  "gender":"male",
                                  "age":20,
                                  "condition":3,
                                  "staff":3,
                                  "ventilation":3,
                                  "respect":3,
                                  "growth":3,
                                  "management":3,
                                  "evaluation":3,
                                  "compliance":3,
                                  "reason":"sample_text",
                                  "culture":"sample_text",
                                  "reward_growth":"sample_text",
                                  "supply":"sample_text",
                                  "women_work":"sample_text",
                                  "worklife":"sample_text",
                                  "strength_weak":"sample_text",
                                  "director":"sample_text",
        }
        sample_reputation = Reputation.objects.get(reputation_sample_info)
        