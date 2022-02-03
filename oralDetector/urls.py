from django.contrib import admin
from django.urls import path
from detector import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('OralDetective/admin', admin.site.urls),
    path('',views.index,name='index'),
    path('OralDetective/details',views.details,name='details'),
    path('OralDetective/report',views.report,name='details'),
    path('OralDetective/detection',views.detection,name='detection')
]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)