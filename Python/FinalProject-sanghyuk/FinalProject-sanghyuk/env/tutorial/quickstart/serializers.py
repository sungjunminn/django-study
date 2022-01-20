# tutorial/quickstart/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User, Group
from .models import AA

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
        fields = ('m_number', 'm_name', 'm_lcc', 'm_lcn', 'm_mcc', 'm_mcn', 'm_scc', 'm_scn', 'c_code', 'c_name',
                  'gg_code', 'gg_name', 'ad_name', 'st_name', 'stad_name', 'o_mb', 'n_mb', 'lng', 'lat')