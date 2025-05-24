from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .v2churn_predictor import run_predictor, predict_single
from .serializers import PredictionSerializer
import os
from django.conf import settings
import logging


logger = logging.getLogger(__name__)

class PredictorView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        logger.debug("Processing GET request for /api/predict/")
        try:
            result = run_predictor(
                cloudinary_url='https://res.cloudinary.com/djz9qsw5v/raw/upload/v1748064726/base_clientes_w1_fake_gpdjxz.csv',
                output_dir=settings.MEDIA_ROOT
            )
            serializer = PredictionSerializer(result)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error in PredictorView GET: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        logger.debug("Processing POST request for /api/predict/")
        try:
            data = request.data
            result = predict_single(data, output_dir=settings.MEDIA_ROOT)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error in PredictorView POST: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MetricsView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        logger.debug("Processing GET request for /api/metrics/")
        try:
            result = run_predictor(
                cloudinary_url='https://res.cloudinary.com/djz9qsw5v/raw/upload/v1748064726/base_clientes_w1_fake_gpdjxz.csv',
                output_dir=settings.MEDIA_ROOT
            )
            return Response(result['metrics'], status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error in MetricsView GET: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PerformanceView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        logger.debug("Processing GET request for /api/model-performance/")
        try:
            result = run_predictor(
                cloudinary_url='https://res.cloudinary.com/djz9qsw5v/raw/upload/v1748064726/base_clientes_w1_fake_gpdjxz.csv',
                output_dir=settings.MEDIA_ROOT
            )
            return Response(result['performance'], status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error in PerformanceView GET: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class StatsView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        logger.debug("Processing GET request for /api/stats/")
        try:
            result = run_predictor(
                cloudinary_url='https://res.cloudinary.com/djz9qsw5v/raw/upload/v1748064726/base_clientes_w1_fake_gpdjxz.csv',
                output_dir=settings.MEDIA_ROOT
            )
            return Response(result['stats'], status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error in StatsView GET: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)