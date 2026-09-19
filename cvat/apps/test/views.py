from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from cvat.apps.engine.models import Label, LabeledImage, LabeledShape, TrackedShape

class ClassWiseCountView(APIView):
    permission_classes = [AllowAny]
    iam_organization_field = None

    def get(self, request, *args, **kwargs):
        try:
            counts = {}

            for label in Label.objects.all():
                shape_count = LabeledShape.objects.filter(label=label).count()
                image_count = LabeledImage.objects.filter(label=label).count()
                track_count = TrackedShape.objects.filter(track__label=label).count()

                counts[label.name] = shape_count + image_count + track_count

            return Response({
                "status": "success",
                "total_classes": len(counts),
                "data": counts
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "status": "error",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    