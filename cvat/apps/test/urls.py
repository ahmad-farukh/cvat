from django.urls import path
from .views import ClassWiseCountView

urlpatterns = [
    path("analytics/class-wise-count/", ClassWiseCountView.as_view(), name="class_wise_count"),
]