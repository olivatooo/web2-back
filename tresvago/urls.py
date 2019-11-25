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

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    # nem rela nisso
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    # você quer mexer aqui
    path('auth', auth.obtain_auth_token),
    path('test-auth/', views.test_view),
]
