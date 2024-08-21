from django.urls import path
from .views import *

urlpatterns = [
    path('siparis/', SiparisListCreateView.as_view(), name='siparis-list-create'),
    path('siparis/<int:pk>/', SiparisDetailView.as_view(), name='siparis-detail'),
    path('siparis/<int:siparis_id>/next-step/', GetNextStepView.as_view(), name='get-next-step'),
    path('siparis/<int:siparis_id>/go-next-step/', GoNextStepView.as_view(), name='go-next-step'),
    path('siparis/<int:siparis_id>/siparis-file/', SiparisFileListCreateView.as_view(), name='siparis-file-list-create'),
    path('siparis/<int:siparis_id>/siparis-file/<int:pk>/', SiparisFileDetailView.as_view(), name='siparis-file-detail'),
    path('kaplama/', KaplamaListCreateView.as_view(), name='kaplama-list-create'),
    path('kaplama/<int:pk>/', KaplamaDetailView.as_view(), name='kaplama-detail'),
    path('patch/', PatchListCreateView.as_view(), name='patch-list-create'),
    path('patch/<int:pk>/', PatchDetailView.as_view(), name='patch-detail'),    
    path('isil-islem/', IsilIslemListCreateView.as_view(), name='isil-islem-list-create'),
    path('isil-islem/<int:pk>/', IsilIslemDetailView.as_view(), name='isil-islem-detail'),
    path('work-order/<int:siparis_id>/', CreateWorkOrderView.as_view(), name='create_work_order')
]