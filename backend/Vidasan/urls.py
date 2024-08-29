from django.urls import path
from .views import *

urlpatterns = [
    path('siparis/', SiparisListCreateView.as_view(), name='siparis-list-create'),
    path('siparis/<int:pk>/', SiparisDetailView.as_view(), name='siparis-detail'),
    path('siparis/<int:siparis_id>/activity/', SiparisActivityDetailView.as_view(), name='siparis-activity-detail'),
    path('siparis/<int:siparis_id>/next-step/', GetNextStepView.as_view(), name='get-next-step'),
    path('siparis/<int:siparis_id>/go-next-step/', GoNextStepView.as_view(), name='go-next-step'),
    path('siparis/<int:siparis_id>/siparis-file/', SiparisFileListCreateView.as_view(), name='siparis-file-list-create'),
    path('siparis/<int:siparis_id>/siparis-file/<int:pk>/', SiparisFileDetailView.as_view(), name='siparis-file-detail'),
    path('work-order/<int:siparis_id>/', CreateWorkOrderView.as_view(), name='create_work_order'),
    path('machines/', MachineListCreateView.as_view(), name='machine-list-create'),
    path('machines/<int:pk>/', MachineDetailView.as_view(), name='machine-detail'),
]