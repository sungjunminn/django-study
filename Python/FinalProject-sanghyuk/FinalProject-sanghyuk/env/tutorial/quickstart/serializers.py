from rest_framework import serializers
from django.contrib.auth.models import User, Group
from .models import AA, Post, Chart


class AASerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AA
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('table', 'm_lcc', 'm_mcc', 'm_scc')


class ChartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chart
        fields = ('si', 'gu', 'dong')

