from django.urls import include, path
from rest_framework import routers
from tresvago.tresvago import views
from django.contrib import admin
from rest_framework.authtoken import views as auth

router = routers.DefaultRouter()
router.register(r'hotels', views.HotelViewSet)
router.register(r'promocoes', views.PromocaoViewSet)
router.register(r'sitesdereserva', views.SiteReservaViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path('auth', views.CustomAuthToken.as_view()),
    path('test-auth/', views.TestAuth.as_view()),
    path('promocao/', views.PromocaoFilter.as_view())
]
