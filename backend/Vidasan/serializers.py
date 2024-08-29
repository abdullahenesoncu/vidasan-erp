from rest_framework import serializers
from .models import *
from Authentication.serializers import UserSerializerPublic

class SiparisFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiparisFile
        fields = ['id', 'title', 'file']

class SiparisFileReadOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = SiparisFile
        fields = ['id', 'title', 'file']
        read_only_fields = fields

class SiparisSerializer(serializers.ModelSerializer):
    activityId = serializers.SerializerMethodField()

    def get_activityId(self, obj):
        if hasattr(obj, 'activity'):
            return obj.activity.id
        return None

    class Meta:
        model = Siparis
        fields = [
            'id',
            'definition',
            'description',
            'amount',
            'isOEM',
            'isActive',
            'orderNumber',
            'clientOrderNumber',
            'materialNumber',
            'company',
            'quality',
            'kaplama',
            'patch',
            'material',
            'created_at',
            'deadline',
            'orderDate',
            'activityId',
            'pressState',
            'byckState',
            'ovalamaState',
            'sementasyonState',
            'kaplamaState',
            'ambalajState',
            'state',
        ]
        read_only_fields = ['orderNumber', 'state']

class SiparisReadOnlySerializer(serializers.ModelSerializer):
    activityId = serializers.SerializerMethodField()

    def get_activityId(self, obj):
        if hasattr(obj, 'activity'):
            return obj.activity.id
        return None

    class Meta:
        model = Siparis
        fields = [
            'id',
            'definition',
            'description',
            'amount',
            'isOEM',
            'isActive',
            'orderNumber',
            'clientOrderNumber',
            'materialNumber',
            'company',
            'quality',
            'kaplama',
            'patch',
            'material',
            'created_at',
            'deadline',
            'orderDate',
            'activityId',
            'pressState',
            'byckState',
            'ovalamaState',
            'sementasyonState',
            'kaplamaState',
            'ambalajState',
            'state',
        ]
        read_only_fields = fields

class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = ['id', 'name', 'type', 'variation']

class MachineReadOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = ['id', 'name', 'type', 'variation']

class SiparisActivitySerializer(serializers.ModelSerializer):
    siparis = serializers.SerializerMethodField()
    pressMachine = serializers.PrimaryKeyRelatedField(queryset=Machine.objects.all(), required=False, allow_null=True)
    pressOperator = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, allow_null=True)
    byckMachine = serializers.PrimaryKeyRelatedField(queryset=Machine.objects.all(), required=False, allow_null=True)
    byckOperator = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, allow_null=True)
    ovalamaMachine = serializers.PrimaryKeyRelatedField(queryset=Machine.objects.all(), required=False, allow_null=True)
    ovalamaOperator = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, allow_null=True)
    sementasyonMachine = serializers.PrimaryKeyRelatedField(queryset=Machine.objects.all(), required=False, allow_null=True)
    sementasyonOperator = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, allow_null=True)
    kaplamaMachine = serializers.PrimaryKeyRelatedField(queryset=Machine.objects.all(), required=False, allow_null=True)
    kaplamaOperator = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, allow_null=True)
    ambalajMachine = serializers.PrimaryKeyRelatedField(queryset=Machine.objects.all(), required=False, allow_null=True)
    ambalajOperator = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, allow_null=True)

    class Meta:
        model = SiparisActivity
        fields = [
            'siparis',
            'pressMachine', 'pressAmount', 'pressOutputKg', 'pressWastageKg', 'pressStartDateTime', 'pressFinishDateTime', 'pressOperator',
            'byckMachine', 'byckAmount', 'byckOutputKg', 'byckWastageKg', 'byckStartDateTime', 'byckFinishDateTime', 'byckOperator',
            'ovalamaMachine', 'ovalamaAmount', 'ovalamaOutputKg', 'ovalamaWastageKg', 'ovalamaStartDateTime', 'ovalamaFinishDateTime', 'ovalamaOperator',
            'sementasyonMachine', 'sementasyonAmount', 'sementasyonOutputKg', 'sementasyonWastageKg', 'sementasyonStartDateTime', 'sementasyonFinishDateTime', 'sementasyonOperator',
            'kaplamaMachine', 'kaplamaAmount', 'kaplamaOutputKg', 'kaplamaWastageKg', 'kaplamaStartDateTime', 'kaplamaFinishDateTime', 'kaplamaOperator',
            'ambalajMachine', 'ambalajAmount', 'ambalajOutputKg', 'ambalajWastageKg', 'ambalajStartDateTime', 'ambalajFinishDateTime', 'ambalajOperator'
        ]

    def get_siparis(self, obj):
        return {
            'id': obj.siparis.id,
            'definition': obj.siparis.definition
        }