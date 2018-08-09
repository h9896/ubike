from rest_framework import serializers
from ubikeapp.models import Ubike


class UbikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ubike
        # fields = '__all__'
        fields = ('id', 'lng', 'lat', 'sbi', 'sna', 'snaen', 'bemp', 'act', 'created')