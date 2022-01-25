# tutorial/quickstart/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User, Group
from .models import AA, Post

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class AASerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AA
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('m_lcc', 'm_mcc', 'm_scc')