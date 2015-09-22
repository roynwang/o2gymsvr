from rest_framework import serializers
from sms.models import *

class SmsVcodeSerializer(serializers.ModelSerializer):
	class Meta:
		model = Sms
