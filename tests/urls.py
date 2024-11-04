from django.urls import path
from .views import (
    TestViewSet,
    TestTakeView,
    TestResultSubmitView,
)

urlpatterns = [
    path('', TestViewSet.as_view({'get': 'list', 'post': 'create'}), name='test-list'),
    path('<int:id>/', TestViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='test-detail'),
    path('<int:test_id>/take/', TestTakeView.as_view({'post': 'create'}), name='take-test'),
    path('<int:test_id>/submit/', TestResultSubmitView.as_view({'post': 'create'}), name='submit-test-results'),
]