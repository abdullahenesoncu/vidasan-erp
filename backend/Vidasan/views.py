from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from Authentication.models import UserType
from Authentication.helpers import IsUserVerified
from django.http import HttpResponse
from .models import *
from .serializers import *
from .helpers import createWorkOrder
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from django.utils import timezone
from datetime import timedelta
from rest_framework.views import APIView

from LoggingApp import logger

class SiparisListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsUserVerified]
    pagination_class = PageNumberPagination  # Set the pagination class
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]  # Add filtering, ordering, and search backends

    filterset_fields = ['state']  # Add fields that can be filtered
    search_fields = ['definition', 'description', 'state']
    ordering_fields = ['definition', 'description', 'deadline', 'orderDate']

    def get_queryset(self):
        if self.request.user.user_type in [UserType.ADMIN, UserType.PLANLAMA, UserType.SATIS_PAZARLAMA, UserType.KALITE_KONTROL]:
            return Siparis.objects.all()
        else:
            return Siparis.objects.filter(state__in=[SiparisState.ISIL_ISLEM, SiparisState.KAPLAMA, SiparisState.PATCH])

    def get_serializer_class(self):
        user_type = self.request.user.user_type
        logger.debug(f'User {self.request.user} is requesting serializer for Siparis, user type: {user_type}')
        if user_type in [UserType.ADMIN, UserType.PLANLAMA, UserType.SATIS_PAZARLAMA]:
            return SiparisSerializer
        else:
            return SiparisReadOnlySerializer

    def list(self, request, *args, **kwargs):
        logger.info(f'User {self.request.user} is listing Siparis objects')

        queryset = self.filter_queryset(self.get_queryset())  # Ensure filter_queryset is called

        if self.request.query_params.get('onlyUpcomingOrders', 'false') == 'true':
            queryset = queryset.exclude( state=SiparisState.SIPARIS_TAMAMLANDI ).filter( deadline__gte=timezone.now(), deadline__lte=timezone.now()+timedelta(days=14) )

        if self.request.query_params.get('onlyCompletedOrders', 'false') == 'true':
            queryset = queryset.filter( state=SiparisState.SIPARIS_TAMAMLANDI )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        if self.get_serializer_class() == SiparisReadOnlySerializer:
            logger.critical(f'{self.request.user} tried to create Siparis without permission')
            raise PermissionDenied("You do not have permission to create this object.")

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f'User {self.request.user} created a new Siparis: ID={serializer.data["id"]}, Definition={serializer.data["definition"]}, Amount={serializer.data["amount"]}')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        logger.error(f'Failed to create Siparis, errors: {serializer.errors}')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SiparisDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsUserVerified]

    def get_queryset(self):
        if self.request.user.user_type in [ UserType.ADMIN, UserType.PLANLAMA, UserType.SATIS_PAZARLAMA, UserType.KALITE_KONTROL ]:
            return Siparis.objects.all()
        else:
            return Siparis.objects.filter( state__in=[ SiparisState.ISIL_ISLEM, SiparisState.KAPLAMA, SiparisState.PATCH ] )

    def get_serializer_class(self):
        user_type = self.request.user.user_type
        logger.debug(f'User {self.request.user} is requesting serializer for Siparis, user type: {user_type}')
        if user_type in [UserType.ADMIN, UserType.PLANLAMA, UserType.SATIS_PAZARLAMA]:
            return SiparisSerializer
        else:
            return SiparisReadOnlySerializer

    def get(self, request, *args, **kwargs):
        logger.info(f'User {self.request.user} is retrieving a Siparis object')
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        siparis = self.get_object()  # Fetch the Siparis instance to log its details
        if self.get_serializer_class() == SiparisReadOnlySerializer:
            logger.critical(f'{self.request.user} tried to update Siparis without permission: ID={siparis.id}, Definition={siparis.definition}')
            raise PermissionDenied("You do not have permission to update this object.")

        logger.info(f'User {self.request.user} is updating Siparis: ID={siparis.id}, Definition={siparis.definition}')
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        siparis = self.get_object()  # Fetch the Siparis instance to log its details
        if self.get_serializer_class() == SiparisReadOnlySerializer:
            logger.critical(f'{self.request.user} tried to delete Siparis without permission: ID={siparis.id}, Definition={siparis.definition}')
            raise PermissionDenied("You do not have permission to delete this object.")

        logger.info(f'User {self.request.user} is deleting Siparis: ID={siparis.id}, Definition={siparis.definition}, Amount={siparis.amount}')
        return self.destroy(request, *args, **kwargs)

class SiparisFileListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsUserVerified]

    def get_serializer_class(self):
        user_type = self.request.user.user_type
        logger.debug(f'User {self.request.user} is requesting serializer for SiparisFile, user type: {user_type}')
        if user_type in [UserType.ADMIN, UserType.PLANLAMA, UserType.SATIS_PAZARLAMA]:
            return SiparisFileSerializer
        else:
            return SiparisFileReadOnlySerializer

    def get_queryset(self):
        siparis_id = self.kwargs.get('siparis_id')
        return SiparisFile.objects.filter(siparis_id=siparis_id)

    def list(self, request, *args, **kwargs):
        logger.info(f'User {self.request.user} is listing SiparisFile objects for Siparis ID={self.kwargs.get("siparis_id")}')
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        if self.get_serializer_class() == SiparisFileReadOnlySerializer:
            logger.critical(f'{self.request.user} tried to create SiparisFile without permission')
            raise PermissionDenied("You do not have permission to create this object.")

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            siparis_id = self.kwargs.get('siparis_id')
            serializer.save(siparis_id=siparis_id)  # Ensure the siparis_id is set
            logger.info(f'User {self.request.user} created a new SiparisFile for Siparis ID={siparis_id}: ID={serializer.data["id"]}, Title={serializer.data["title"]}')
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        logger.error(f'Failed to create SiparisFile, errors: {serializer.errors}')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SiparisFileDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsUserVerified]

    def get_serializer_class(self):
        user_type = self.request.user.user_type
        logger.debug(f'User {self.request.user} is requesting serializer for SiparisFile, user type: {user_type}')
        if user_type in [UserType.ADMIN, UserType.PLANLAMA, UserType.SATIS_PAZARLAMA]:
            return SiparisFileSerializer
        else:
            return SiparisFileReadOnlySerializer

    def get_queryset(self):
        siparis_id = self.kwargs.get('siparis_id')
        return SiparisFile.objects.filter(siparis_id=siparis_id)

    def get(self, request, *args, **kwargs):
        logger.info(f'User {self.request.user} is retrieving SiparisFile object with ID={kwargs.get("pk")} for Siparis ID={self.kwargs.get("siparis_id")}')
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        siparis_file = self.get_object()
        if self.get_serializer_class() == SiparisFileReadOnlySerializer:
            logger.critical(f'{self.request.user} tried to update SiparisFile without permission: ID={siparis_file.id}, Title={siparis_file.title}')
            raise PermissionDenied("You do not have permission to update this object.")

        logger.info(f'User {self.request.user} is updating SiparisFile: ID={siparis_file.id}, Title={siparis_file.title}')
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        siparis_file = self.get_object()
        if self.get_serializer_class() == SiparisFileReadOnlySerializer:
            logger.critical(f'{self.request.user} tried to delete SiparisFile without permission: ID={siparis_file.id}, Title={siparis_file.title}')
            raise PermissionDenied("You do not have permission to delete this object.")

        logger.info(f'User {self.request.user} is deleting SiparisFile: ID={siparis_file.id}, Title={siparis_file.title}')
        return self.destroy(request, *args, **kwargs)

class GetNextStepView(generics.GenericAPIView):
    permission_classes = [IsUserVerified]

    def get(self, request, *args, **kwargs):
        siparis_id = kwargs.get('siparis_id')
        user = request.user
        try:
            siparis = Siparis.objects.get(id=siparis_id)
            if (siparis.state == SiparisState.PLANLAMA and user.user_type not in [UserType.ADMIN, UserType.PLANLAMA] or
                siparis.state == SiparisState.IMALAT and user.user_type not in [UserType.ADMIN, UserType.PLANLAMA, UserType.KALITE_KONTROL, UserType.DEPO]):
                logger.info(f'User {user} is not authorized to see next step for Siparis ID={siparis_id}. Returning None.')
                return Response({'nextStep': None}, status=status.HTTP_200_OK)

            nextStep = None
            if siparis.state == SiparisState.PLANLAMA: nextStep = "İmalata git"
            elif siparis.state == SiparisState.IMALAT: nextStep = "Siparişi Tamamla"

            logger.info(f'User {user} retrieved next step for Siparis ID={siparis_id}: {nextStep}')
            return Response({'nextStep': nextStep}, status=status.HTTP_200_OK)

        except Siparis.DoesNotExist:
            logger.error(f'Siparis with ID={siparis_id} not found')
            return Response({'error': 'Siparis not found'}, status=status.HTTP_404_NOT_FOUND)


class GoNextStepView(generics.UpdateAPIView):
    permission_classes = [IsUserVerified]

    def get(self, request, *args, **kwargs):
        siparis_id = kwargs.get('siparis_id')
        user = request.user
        try:
            siparis = Siparis.objects.get(id=siparis_id)
            if (siparis.state == SiparisState.PLANLAMA and user.user_type not in [UserType.ADMIN, UserType.PLANLAMA] or
                siparis.state == SiparisState.IMALAT and user.user_type not in [UserType.ADMIN, UserType.PLANLAMA, UserType.KALITE_KONTROL, UserType.DEPO]):
                logger.info(f'User {user} is not authorized to advance to the next step for Siparis ID={siparis_id}. Returning error.')
                return Response({}, status=status.HTTP_400_BAD_REQUEST)

            nextStep = None
            if siparis.state == SiparisState.PLANLAMA: nextStep = SiparisState.IMALAT
            elif siparis.state == SiparisState.IMALAT: nextStep = SiparisState.SIPARIS_TAMAMLANDI

            siparis.state = nextStep
            siparis.save()
            logger.info(f'User {user} updated Siparis ID={siparis_id} to the next state: {nextStep}')
            return Response({}, status=status.HTTP_200_OK)

        except Siparis.DoesNotExist:
            logger.error(f'Siparis with ID={siparis_id} not found')
            return Response({'error': 'Siparis not found'}, status=status.HTTP_404_NOT_FOUND)

class CreateWorkOrderView(generics.GenericAPIView):
    permission_classes = [IsUserVerified]

    def get(self, request, *args, **kwargs):
        siparis_id = kwargs.get('siparis_id')
        user = request.user
        try:
            siparis = Siparis.objects.get(id=siparis_id)
            excel_buffer = createWorkOrder(siparis, user)

            # Create HTTP response with Excel content
            response = HttpResponse(excel_buffer, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="work_order.xlsx"'
            
            return response
        except Siparis.DoesNotExist:
            logger.error(f'Siparis with ID={siparis_id} not found')
            return Response({'error': 'Siparis not found'}, status=status.HTTP_404_NOT_FOUND)


class SiparisActivityDetailView(generics.GenericAPIView):
    serializer_class = SiparisActivitySerializer

    def get(self, request, *args, **kwargs):
        siparis_id = kwargs.get('siparis_id')
        try:
            siparis = Siparis.objects.get(id=siparis_id)
            activity = SiparisActivity.objects.get(siparis=siparis)  # Fetch the activity related to Siparis
            serializer = self.get_serializer(activity)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Siparis.DoesNotExist:
            raise NotFound('Siparis not found')
        except SiparisActivity.DoesNotExist:
            raise NotFound('SiparisActivity not found')

    def put(self, request, *args, **kwargs):
        siparis_id = kwargs.get('siparis_id')
        try:
            siparis = Siparis.objects.get(id=siparis_id)
            activity = SiparisActivity.objects.get(siparis=siparis)
            serializer = self.get_serializer(activity, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Siparis.DoesNotExist:
            raise NotFound('Siparis not found')
        except SiparisActivity.DoesNotExist:
            raise NotFound('SiparisActivity not found')

class MachineListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsUserVerified]

    def get_serializer_class(self):
        user_type = self.request.user.user_type
        logger.debug(f'User {self.request.user} is requesting serializer for Machine, user type: {user_type}')
        if user_type in [UserType.ADMIN]:
            return MachineSerializer
        else:
            return MachineReadOnlySerializer

    def get_queryset(self):
        return Machine.objects.all()

    def list(self, request, *args, **kwargs):
        logger.info(f'User {self.request.user} is listing Machine objects')
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        if self.get_serializer_class() == MachineReadOnlySerializer:
            logger.critical(f'{self.request.user} tried to create Machine without permission')
            raise PermissionDenied("You do not have permission to create this object.")

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f'User {self.request.user} created a new Machine: ID={serializer.data["id"]}, Name={serializer.data["name"]}')
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        logger.error(f'Failed to create Machine, errors: {serializer.errors}')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MachineDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsUserVerified]

    def get_serializer_class(self):
        user_type = self.request.user.user_type
        logger.debug(f'User {self.request.user} is requesting serializer for Machine, user type: {user_type}')
        if user_type in [UserType.ADMIN]:
            return MachineSerializer
        else:
            return MachineReadOnlySerializer

    def get_queryset(self):
        return Machine.objects.all()

    def get(self, request, *args, **kwargs):
        logger.info(f'User {self.request.user} is retrieving Machine object with ID={kwargs.get("pk")}')
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        machine = self.get_object()
        if self.get_serializer_class() == MachineReadOnlySerializer:
            logger.critical(f'{self.request.user} tried to update Machine without permission: ID={machine.id}, Name={machine.name}')
            raise PermissionDenied("You do not have permission to update this object.")

        logger.info(f'User {self.request.user} is updating Machine: ID={machine.id}, Name={machine.name}')
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        machine = self.get_object()
        if self.get_serializer_class() == MachineReadOnlySerializer:
            logger.critical(f'{self.request.user} tried to delete Machine without permission: ID={machine.id}, Name={machine.name}')
            raise PermissionDenied("You do not have permission to delete this object.")

        logger.info(f'User {self.request.user} is deleting Machine: ID={machine.id}, Name={machine.name}')
        return self.destroy(request, *args, **kwargs)
    
class MachineLogsList(APIView):

    def get(self, request, machine_id=None, *args, **kwargs):
        if machine_id:
            logs = SiparisLog.objects.filter(machine__id=machine_id).order_by( 'created_at' )
        else:
            logs = SiparisLog.objects.all().order_by('created_at')
        
        logDict = {}
        machineIdToName = {}
        for log in logs:
            if not log.machine:
                continue
            machineId, machineName = log.machine.id, log.machine.name
            machineIdToName[ machine_id ] = machineName
            if machineId not in logDict:
                logDict[ machineId ] = []
            if log.toState == ProcessState.HACKY:
                continue
            logDict[ machineId ].append(
                {
                    'state': log.toState,
                    'process': log.processType,
                    'created_at': log.created_at,
                }
            )
        
        data = {
            'logs': logDict,
            'machineIdToName': machineIdToName,
        }
        
        return Response(data)