from rest_framework import serializers

class PredictionSerializer(serializers.Serializer):
    holding_report = serializers.DictField()
    holding_f1_score = serializers.FloatField()
    churn_report = serializers.DictField()
    churn_f1_score = serializers.FloatField()
    matriz_holding_url = serializers.CharField()
    matriz_churn_url = serializers.CharField()
    importancia_holding_url = serializers.CharField()
    importancia_churn_url = serializers.CharField()
    relatorio_holding_url = serializers.CharField()
    metrics = serializers.DictField()
    performance = serializers.DictField()
    stats = serializers.DictField()