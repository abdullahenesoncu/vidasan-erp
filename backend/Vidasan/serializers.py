from rest_framework import serializers
from .models import *

class IsilIslemTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IsilIslemType
        fields = ['id', 'name']

class KaplamaTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = KaplamaType
        fields = ['id', 'name']

class PatchTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatchType
        fields = ['id', 'name']

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
    isilIslem = IsilIslemTypeSerializer(read_only=True)
    kaplama = KaplamaTypeSerializer(read_only=True)
    patch = PatchTypeSerializer(read_only=True)
    
    # Allow kaplama, isilIslem, and patch to be writable via their ID
    kaplama_id = serializers.PrimaryKeyRelatedField(
        queryset=KaplamaType.objects.all(), source='kaplama', write_only=True, required=False, allow_null=True
    )
    isilIslem_id = serializers.PrimaryKeyRelatedField(
        queryset=IsilIslemType.objects.all(), source='isilIslem', write_only=True, required=False, allow_null=True
    )
    patch_id = serializers.PrimaryKeyRelatedField(
        queryset=PatchType.objects.all(), source='patch', write_only=True, required=False, allow_null=True
    )

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
            'state',
            'isilIslem',
            'isilIslem_id',  # Writable field
            'kaplama',
            'kaplama_id',  # Writable field
            'patch',
            'patch_id',  # Writable field
            'created_at',
            'deadline',
        ]
        read_only_fields = ['state']


class SiparisReadOnlySerializer(serializers.ModelSerializer):
    isilIslem = IsilIslemTypeSerializer(read_only=True)
    kaplama = KaplamaTypeSerializer(read_only=True)
    patch = PatchTypeSerializer(read_only=True)

    class Meta:
        model = Siparis
        fields = [
            'id',
            'definition',
            'description',
            'amount',
            'isOEM',
            'orderNumber',
            'state',
            'isilIslem',
            'kaplama',
            'patch',
            'created_at',
            'deadline',
        ]
        read_only_fields = fields
