from rest_framework.routers import DefaultRouter

import app.views as views

router = DefaultRouter()

router.register(r"bands", views.BandViewSet, basename="band")