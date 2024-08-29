from django.db import models
from backend.models import BaseModel, Enum
from django.conf import settings
from Authentication.models import User

class MachineType( Enum ):
    PRESS = 'press'
    OVALAMA = 'ovalama'
    KAPLAMA = 'kaplama'

class MachineVariation( Enum ):
    CH3 = 'CH3'
    CH5 = 'CH5'
    CH5S = 'CH5S'
    CH5L = 'CH5L'
    CH6 = 'CH6'
    KAPLAMA_TEDARIKCISI = 'Kaplama Tedarikcisi'

class SiparisState( Enum ):
    PLANLAMA = 'Planlama'
    IMALAT = 'İmalat'
    SIPARIS_TAMAMLANDI = 'Sipariş Tamamlandı'

class Materials( Enum ):
    _20MnB4 = "20MnB4"
    _15B2 = "15B2"
    CQ15 = "CQ15"
    SAE100GC = "SAE100GC"
    _304Cu = "304Cu(Paslanmaz)"
    DirectCekim = "Direct Çekim"
    _23MnB4 = "23MnB4"

class QualityTypes( Enum ):
    _48 = "4.8"
    _68 = "6.8"
    _88 = "8.8"
    _108 = "10.8"
    KARBONHIDRATION = "Karbonhidrasyon"

class KaplamaTypes( Enum ):
    CinkoKaplama = "Çinko Kaplama"
    CinkoNikelSeffafKaplama = "Çinko Nikel Şeffaf Kaplama"
    Nikel = "Nikel Kaplama"
    CinkoNikelSiyahKaplama = "Çinko Nikel Siyah Kaplama"
    CinkoSiyahKaplama = "Çinko Siyah Kaplama"
    JanjanKaplama = "Janjan Kaplama"
    GeometKaplama = "Geomet Kaplama"
    SariKaplama = "Sarı Kaplama"

class ProcessState( Enum ):
    BASLAMADI = 'Başlamadı'
    CALISIYOR = 'Çalışıyor'
    BEKLEMEDE = 'Beklemede'
    BITTI = 'Bitti'
    HACKY = 'Hacky'

class Machine( BaseModel ):
    name = models.CharField( max_length=300, blank=True, null=True )
    type = models.CharField( max_length=100, choices=MachineType.get_choices() )
    variation = models.CharField( max_length=100, choices=MachineVariation.get_choices() )

    def __str__( self ):
        return self.name

class Siparis( BaseModel ):
    definition = models.CharField( max_length=1000 )
    description = models.TextField( max_length=10000 )
    amount = models.IntegerField( default=0 )
    deadline = models.DateField( blank=True, null=True )
    orderDate = models.DateField( blank=True, null=True )
    isOEM = models.BooleanField( default=False )
    isActive = models.BooleanField( default=False )
    
    material = models.CharField( max_length=300, choices=Materials.get_choices(), default=Materials._20MnB4 )
    quality = models.CharField( max_length=300, choices=QualityTypes.get_choices(), null=True, blank=True, default="" )
    kaplama = models.CharField( max_length=300, choices=KaplamaTypes.get_choices(), null=True, blank=True, default="" )
    patch = models.CharField( max_length=300, blank=True, null=True, default="" )

    materialNumber = models.CharField( max_length=300, null=True, blank=True, default="" )
    orderNumber = models.IntegerField(unique=True, blank=True, null=True, default=None)
    clientOrderNumber = models.CharField(max_length=300, default="", null=True, blank=True)
    company = models.CharField( max_length=1000, null=True, blank=True, default="" )

    state = models.CharField( max_length=100, choices=SiparisState.get_choices(), default=SiparisState.PLANLAMA )
    pressState = models.CharField( max_length=100, choices=ProcessState.get_choices(), default=ProcessState.BASLAMADI )
    byckState = models.CharField( max_length=100, choices=ProcessState.get_choices(), default=ProcessState.BASLAMADI )
    ovalamaState = models.CharField( max_length=100, choices=ProcessState.get_choices(), default=ProcessState.BASLAMADI )
    sementasyonState = models.CharField( max_length=100, choices=ProcessState.get_choices(), default=ProcessState.BASLAMADI )
    kaplamaState = models.CharField( max_length=100, choices=ProcessState.get_choices(), default=ProcessState.BASLAMADI )
    ambalajState = models.CharField( max_length=100, choices=ProcessState.get_choices(), default=ProcessState.BASLAMADI )

    def changeAvailable( self, processStateFrom, processStateTo ):
        if ProcessState.HACKY in [ processStateFrom, processStateTo ]:
            return True
        availableChanges = {
            ProcessState.BASLAMADI: [ ProcessState.CALISIYOR ],
            ProcessState.CALISIYOR: [ ProcessState.BEKLEMEDE, ProcessState.BITTI ],
            ProcessState.BEKLEMEDE: [ ProcessState.CALISIYOR, ProcessState.BITTI ],
            ProcessState.BITTI: [],
        }
        return processStateTo in availableChanges[ processStateFrom ]

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.orderNumber is None:
                start_value = getattr(settings, 'ORDER_NUMBER_STARTING_POINT', 0)
                max_number = Siparis.objects.aggregate(models.Max('orderNumber'))['orderNumber__max']
                if max_number is None:
                    self.orderNumber = start_value
                else:
                    self.orderNumber = max_number + 1
        else:
            oldInstance = Siparis.objects.get( pk=self.pk )
            for process in [ "press", "byck", "ovalama", "sementasyon", "kaplama", "ambalaj" ]:
                oldState = getattr( oldInstance, f"{process}State" )
                newState = getattr( self, f"{process}State" )
                if oldState != newState:
                    if not self.changeAvailable( oldState, newState ):
                        raise Exception( f"{process} cannot go from {oldState} to {newState}" )
                    if hasattr( self, 'activity' ):
                        machine = getattr( self.activity, f'{process}Machine' )
                        SiparisLog.objects.create( siparis=self, machine=machine, fromState=oldState, toState=newState )
                    

        super().save(*args, **kwargs)

        if not getattr( self, 'activity', None ):
            SiparisActivity.objects.create( siparis=self )
    
    def isIsilIslemExists( self ):
        return self.quality in [ QualityTypes._88, QualityTypes._108, QualityTypes.KARBONHIDRATION ]

    def __str__( self ):
        return self.definition

class SiparisActivity( BaseModel ):
    siparis = models.OneToOneField( Siparis, related_name='activity', on_delete=models.CASCADE )

    pressMachine = models.ForeignKey( Machine, null=True, blank=True, on_delete=models.SET_NULL, related_name='siparis_activity_by_press' )
    pressAmount = models.IntegerField( null=True, blank=True )
    pressOutputKg = models.FloatField( null=True, blank=True )
    pressWastageKg = models.FloatField( null=True, blank=True )
    pressStartDateTime = models.DateTimeField( null=True, blank=True )
    pressFinishDateTime = models.DateTimeField( null=True, blank=True )
    pressOperator = models.ForeignKey( User, null=True, blank=True, on_delete=models.SET_NULL, related_name='siparis_activity_by_press' )

    byckMachine = models.ForeignKey( Machine, null=True, blank=True, on_delete=models.SET_NULL, related_name='siparis_activity_by_byck' )
    byckAmount = models.IntegerField( null=True, blank=True )
    byckOutputKg = models.FloatField( null=True, blank=True )
    byckWastageKg = models.FloatField( null=True, blank=True )
    byckStartDateTime = models.DateTimeField( null=True, blank=True )
    byckFinishDateTime = models.DateTimeField( null=True, blank=True )
    byckOperator = models.ForeignKey( User, null=True, blank=True, on_delete=models.SET_NULL, related_name='siparis_activity_by_byck' )

    ovalamaMachine = models.ForeignKey( Machine, null=True, blank=True, on_delete=models.SET_NULL, related_name='siparis_activity_by_ovalama' )
    ovalamaAmount = models.IntegerField( null=True, blank=True )
    ovalamaOutputKg = models.FloatField( null=True, blank=True )
    ovalamaWastageKg = models.FloatField( null=True, blank=True )
    ovalamaStartDateTime = models.DateTimeField( null=True, blank=True )
    ovalamaFinishDateTime = models.DateTimeField( null=True, blank=True )
    ovalamaOperator = models.ForeignKey( User, null=True, blank=True, on_delete=models.SET_NULL, related_name='siparis_activity_by_ovalama' )

    sementasyonMachine = models.ForeignKey( Machine, null=True, blank=True, on_delete=models.SET_NULL, related_name='siparis_activity_by_sementasyon' )
    sementasyonAmount = models.IntegerField( null=True, blank=True )
    sementasyonOutputKg = models.FloatField( null=True, blank=True )
    sementasyonWastageKg = models.FloatField( null=True, blank=True )
    sementasyonStartDateTime = models.DateTimeField( null=True, blank=True )
    sementasyonFinishDateTime = models.DateTimeField( null=True, blank=True )
    sementasyonOperator = models.ForeignKey( User, null=True, blank=True, on_delete=models.SET_NULL, related_name='siparis_activity_by_sementasyon' )

    kaplamaMachine = models.ForeignKey( Machine, null=True, blank=True, on_delete=models.SET_NULL, related_name='siparis_activity_by_kaplama' )
    kaplamaAmount = models.IntegerField( null=True, blank=True )
    kaplamaOutputKg = models.FloatField( null=True, blank=True )
    kaplamaWastageKg = models.FloatField( null=True, blank=True )
    kaplamaStartDateTime = models.DateTimeField( null=True, blank=True )
    kaplamaFinishDateTime = models.DateTimeField( null=True, blank=True )
    kaplamaOperator = models.ForeignKey( User, null=True, blank=True, on_delete=models.SET_NULL, related_name='siparis_activity_by_kaplama' )

    ambalajMachine = models.ForeignKey( Machine, null=True, blank=True, on_delete=models.SET_NULL, related_name='siparis_activity_by_ambalaj' )
    ambalajAmount = models.IntegerField( null=True, blank=True )
    ambalajOutputKg = models.FloatField( null=True, blank=True )
    ambalajWastageKg = models.FloatField( null=True, blank=True )
    ambalajStartDateTime = models.DateTimeField( null=True, blank=True )
    ambalajFinishDateTime = models.DateTimeField( null=True, blank=True )
    ambalajOperator = models.ForeignKey( User, null=True, blank=True, on_delete=models.SET_NULL, related_name='siparis_activity_by_ambalaj' )

    def __str__( self ):
        return self.siparis.definition

class SiparisFile( BaseModel ):
    siparis = models.ForeignKey( Siparis, on_delete=models.CASCADE, related_name='files' )
    title = models.CharField( max_length=1000, null=True, blank=True )
    file = models.FileField()

class SiparisLog( BaseModel ):
    siparis = models.ForeignKey( Siparis, on_delete=models.SET_NULL, null=True, blank=True )
    machine = models.ForeignKey( Machine, on_delete=models.SET_NULL, null=True, blank=True )
    fromState = models.CharField( max_length=100, choices=ProcessState.get_choices(), default=ProcessState.HACKY )
    toState = models.CharField( max_length=100, choices=ProcessState.get_choices(), default=ProcessState.HACKY )