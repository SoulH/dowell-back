from rest_framework.fields import CharField, IntegerField
from rest_framework.serializers import ModelSerializer


class InfoSerializer(ModelSerializer):
    class Meta:
        fields = '__all__'


