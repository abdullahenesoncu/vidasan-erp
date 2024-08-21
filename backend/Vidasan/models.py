from django.db import models
from backend.models import BaseModel, Enum

class MachineType( Enum ):
    PRESS = 'press'
    OVALAMA = 'ovalama'

class MachineVariation( Enum ):
    TYPE1 = 'type1'
    TYPE2 = 'type2'

class Machine( BaseModel ):
    name = models.CharField( max_length=300, blank=True, null=True )
    type = models.CharField( max_length=100, choices=MachineType.get_choices() )
    variation = models.CharField( max_length=100, choices=MachineVariation.get_choices() )

    def __str__( self ):
        return self.name

class SiparisState( Enum ):
    PLANLAMA = 'Planlama'
    PRESS = 'Press'
    OVALAMA = 'Ovalama'
    ISIL_ISLEM = 'Isıl İşlem'
    KAPLAMA = 'Kaplama'
    PATCH = 'Patch'
    SIPARIS_TAMAMLANDI = 'Sipariş Tamamlandı'

class IsilIslemType( BaseModel ):
    name = models.CharField( max_length=300 )

    def __str__( self ):
        return self.name

class KaplamaType( BaseModel ):
    name = models.CharField( max_length=300 )

    def __str__( self ):
        return self.name

class PatchType( BaseModel ):
    name = models.CharField( max_length=300 )

    def __str__( self ):
        return self.name

class Siparis( BaseModel ):
    definition = models.CharField( max_length=1000 )
    description = models.TextField( max_length=10000 )
    amount = models.IntegerField( default=0 )
    deadline = models.DateField( blank=True, null=True )
    isOEM = models.BooleanField( default=False )
    isActive = models.BooleanField( default=False )
    orderNumber = models.CharField( max_length=1000, blank=True, null=True )
    state = models.CharField( max_length=300, choices=SiparisState.get_choices(), default=SiparisState.PLANLAMA )
    isilIslem = models.ForeignKey( IsilIslemType, default=None, null=True, blank=True, on_delete=models.SET_NULL )
    kaplama = models.ForeignKey( KaplamaType, default=None, null=True, blank=True, on_delete=models.SET_NULL )
    patch = models.ForeignKey( PatchType, default=None, null=True, blank=True, on_delete=models.SET_NULL )

    def __str__( self ):
        return self.definition

class SiparisFile( BaseModel ):
    siparis = models.ForeignKey( Siparis, on_delete=models.CASCADE, related_name='files' )
    title = models.CharField( max_length=1000, null=True, blank=True )
    file = models.FileField()