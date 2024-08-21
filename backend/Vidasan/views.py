from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from Authentication.models import UserType
from Authentication.helpers import IsUserVerified
from django.http import HttpResponse
from .models import *
from .serializers import *
from .helpers import createWorkOrder

from LoggingApp import logger


class SiparisListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsUserVerified]

    def get_queryset(self):
        if self.request.user.user_type in [ UserType.ADMIN, UserType.PLANLAMA, UserType.SATIS_PAZARLAMA ]:
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

    def list(self, request, *args, **kwargs):
        logger.info(f'User {self.request.user} is listing Siparis objects')
        queryset = self.get_queryset()
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
        if self.request.user.user_type in [ UserType.ADMIN, UserType.PLANLAMA, UserType.SATIS_PAZARLAMA ]:
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

# Base class to enforce create, update, delete permissions for admins only
class AdminRestrictedAccessMixin:
    permission_classes = [IsUserVerified]

    def check_admin_permission(self, request):
        if request.user.user_type != UserType.ADMIN:
            logger.critical(f'User {request.user} tried to modify {self.serializer_class.Meta.model.__name__} without permission')
            raise PermissionDenied(f'You do not have permission to modify this {self.serializer_class.Meta.model.__name__}.')

# KaplamaType Views
class KaplamaListCreateView(AdminRestrictedAccessMixin, generics.ListCreateAPIView):
    queryset = KaplamaType.objects.all()
    serializer_class = KaplamaTypeSerializer

    def list(self, request, *args, **kwargs):
        logger.info(f'User {request.user} is listing Kaplama objects')
        return super().list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.check_admin_permission(request)  # Only Admins can create
        logger.info(f'User {request.user} is creating a new Kaplama')
        return super().post(request, *args, **kwargs)

class KaplamaDetailView(AdminRestrictedAccessMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = KaplamaType.objects.all()
    serializer_class = KaplamaTypeSerializer

    def get(self, request, *args, **kwargs):
        logger.info(f'User {request.user} is retrieving a Kaplama object')
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        self.check_admin_permission(request)  # Only Admins can update
        kaplama = self.get_object()
        logger.info(f'User {request.user} is updating Kaplama: ID={kaplama.id}, Name={kaplama.name}')
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.check_admin_permission(request)  # Only Admins can delete
        kaplama = self.get_object()
        logger.info(f'User {request.user} is deleting Kaplama: ID={kaplama.id}, Name={kaplama.name}')
        return self.destroy(request, *args, **kwargs)

# PatchType Views
class PatchListCreateView(AdminRestrictedAccessMixin, generics.ListCreateAPIView):
    queryset = PatchType.objects.all()
    serializer_class = PatchTypeSerializer

    def list(self, request, *args, **kwargs):
        logger.info(f'User {request.user} is listing Patch objects')
        return super().list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.check_admin_permission(request)  # Only Admins can create
        logger.info(f'User {request.user} is creating a new Patch')
        return super().post(request, *args, **kwargs)

class PatchDetailView(AdminRestrictedAccessMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = PatchType.objects.all()
    serializer_class = PatchTypeSerializer

    def get(self, request, *args, **kwargs):
        logger.info(f'User {request.user} is retrieving a Patch object')
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        self.check_admin_permission(request)  # Only Admins can update
        patch = self.get_object()
        logger.info(f'User {request.user} is updating Patch: ID={patch.id}, Name={patch.name}')
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.check_admin_permission(request)  # Only Admins can delete
        patch = self.get_object()
        logger.info(f'User {request.user} is deleting Patch: ID={patch.id}, Name={patch.name}')
        return self.destroy(request, *args, **kwargs)

# IsilIslemType Views
class IsilIslemListCreateView(AdminRestrictedAccessMixin, generics.ListCreateAPIView):
    queryset = IsilIslemType.objects.all()
    serializer_class = IsilIslemTypeSerializer

    def list(self, request, *args, **kwargs):
        logger.info(f'User {request.user} is listing Isil Islem objects')
        return super().list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.check_admin_permission(request)  # Only Admins can create
        logger.info(f'User {request.user} is creating a new Isil Islem')
        return super().post(request, *args, **kwargs)

class IsilIslemDetailView(AdminRestrictedAccessMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = IsilIslemType.objects.all()
    serializer_class = IsilIslemTypeSerializer

    def get(self, request, *args, **kwargs):
        logger.info(f'User {request.user} is retrieving an Isil Islem object')
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        self.check_admin_permission(request)  # Only Admins can update
        isil_islem = self.get_object()
        logger.info(f'User {request.user} is updating Isil Islem: ID={isil_islem.id}, Name={isil_islem.name}')
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.check_admin_permission(request)  # Only Admins can delete
        isil_islem = self.get_object()
        logger.info(f'User {request.user} is deleting Isil Islem: ID={isil_islem.id}, Name={isil_islem.name}')
        return self.destroy(request, *args, **kwargs)


class GetNextStepView(generics.GenericAPIView):
    permission_classes = [IsUserVerified]

    def get(self, request, *args, **kwargs):
        siparis_id = kwargs.get('siparis_id')
        user = request.user
        try:
            siparis = Siparis.objects.get(id=siparis_id)
            if (siparis.state == SiparisState.PLANLAMA and user.user_type not in [UserType.ADMIN, UserType.PLANLAMA] or
                siparis.state == SiparisState.PRESS and user.user_type not in [UserType.ADMIN, UserType.PLANLAMA] or
                siparis.state == SiparisState.OVALAMA and user.user_type not in [UserType.ADMIN, UserType.PLANLAMA] or
                siparis.state == SiparisState.ISIL_ISLEM and user.user_type not in [UserType.ADMIN, UserType.PLANLAMA, UserType.KALITE_KONTROL, UserType.DEPO] or
                siparis.state == SiparisState.KAPLAMA and user.user_type not in [UserType.ADMIN, UserType.PLANLAMA, UserType.KALITE_KONTROL, UserType.DEPO] or
                siparis.state == SiparisState.PATCH and user.user_type not in [UserType.ADMIN, UserType.PLANLAMA, UserType.KALITE_KONTROL, UserType.DEPO]):
                logger.info(f'User {user} is not authorized to see next step for Siparis ID={siparis_id}. Returning None.')
                return Response({'nextStep': None}, status=status.HTTP_200_OK)

            nextStep = None
            if siparis.state == SiparisState.PLANLAMA: nextStep = "Presse git"
            elif siparis.state == SiparisState.PRESS: nextStep = "Ovalamaya git"
            elif siparis.state == SiparisState.OVALAMA and siparis.isilIslem: nextStep = "Isıl işleme git"
            elif siparis.state == SiparisState.OVALAMA and siparis.kaplama: nextStep = "Kaplamaya git"
            elif siparis.state == SiparisState.OVALAMA and siparis.patch: nextStep = "Patche git"
            elif siparis.state == SiparisState.ISIL_ISLEM and siparis.kaplama: nextStep = "Kaplamaya git"
            elif siparis.state == SiparisState.ISIL_ISLEM and siparis.patch: nextStep = "Patche git"
            elif siparis.state == SiparisState.KAPLAMA and siparis.patch: nextStep = "Patche git"
            elif siparis.state != SiparisState.SIPARIS_TAMAMLANDI: nextStep = "Siparişi Tamamla"

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
                siparis.state == SiparisState.PRESS and user.user_type not in [UserType.ADMIN, UserType.PLANLAMA] or
                siparis.state == SiparisState.OVALAMA and user.user_type not in [UserType.ADMIN, UserType.PLANLAMA] or
                siparis.state == SiparisState.ISIL_ISLEM and user.user_type not in [UserType.ADMIN, UserType.PLANLAMA, UserType.KALITE_KONTROL, UserType.DEPO] or
                siparis.state == SiparisState.KAPLAMA and user.user_type not in [UserType.ADMIN, UserType.PLANLAMA, UserType.KALITE_KONTROL, UserType.DEPO] or
                siparis.state == SiparisState.PATCH and user.user_type not in [UserType.ADMIN, UserType.PLANLAMA, UserType.KALITE_KONTROL, UserType.DEPO]):
                logger.info(f'User {user} is not authorized to advance to the next step for Siparis ID={siparis_id}. Returning error.')
                return Response({}, status=status.HTTP_400_BAD_REQUEST)

            nextStep = None
            if siparis.state == SiparisState.PLANLAMA: nextStep = SiparisState.PRESS
            elif siparis.state == SiparisState.PRESS: nextStep = SiparisState.OVALAMA
            elif siparis.state == SiparisState.OVALAMA and siparis.isilIslem: nextStep = SiparisState.ISIL_ISLEM
            elif siparis.state == SiparisState.OVALAMA and siparis.kaplama: nextStep = SiparisState.KAPLAMA
            elif siparis.state == SiparisState.OVALAMA and siparis.patch: nextStep = SiparisState.PATCH
            elif siparis.state == SiparisState.ISIL_ISLEM and siparis.kaplama: nextStep = SiparisState.KAPLAMA
            elif siparis.state == SiparisState.ISIL_ISLEM and siparis.patch: nextStep = SiparisState.PATCH
            elif siparis.state == SiparisState.KAPLAMA and siparis.patch: nextStep = SiparisState.PATCH
            elif siparis.state != SiparisState.SIPARIS_TAMAMLANDI: nextStep = SiparisState.SIPARIS_TAMAMLANDI

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
            pdf = createWorkOrder(siparis, user)

            # Create HTTP response with PDF content
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="work_order.pdf"'
            
            return response
        except Siparis.DoesNotExist:
            logger.error(f'Siparis with ID={siparis_id} not found')
            return Response({'error': 'Siparis not found'}, status=status.HTTP_404_NOT_FOUND)