from rest_framework.routers import DefaultRouter

from v1.views.info import FileViewSet

urlpatterns = []

router = DefaultRouter()

router.register(r'info', FileViewSet, basename='info')

urlpatterns += router.urls
