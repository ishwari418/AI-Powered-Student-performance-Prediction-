from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from apps.users import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Auth
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', user_views.signup, name='signup'),
    
    # Apps
    path('', include('apps.analytics.urls')),
    path('students/', include('apps.students.urls')),
    path('predictions/', include('apps.predictions.urls')),
    path('api/', include('apps.api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
