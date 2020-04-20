from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

# create our default router the default router is a feature
# of the Django rest framework that will
# automatically generate the URLs for our viewset

# when you have a viewset you may have multiple URLs
# associated with that one viewset.

router = DefaultRouter()
router.register('tags', views.TagViewSet)
# registers our viewset with our router
router.register('ingredients', views.IngredientViewSet)

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls))
]
