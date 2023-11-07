from django.shortcuts import render
from .models import Acidente
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .serializers import AcidenteSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
def acidentes_as_json(request):
    acidentes = Acidente.objects.all()
    serializer = AcidenteSerializer(acidentes, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def ultimos_acidentes(request):
    # Consulta SQL personalizada para obter os 10 registros mais recentes
    consulta_sql = """
    SELECT * FROM acidente
    ORDER BY data_hora_boletim DESC
    LIMIT 10;
    """

    ultimos_acidentes = Acidente.objects.raw(consulta_sql)
    serializer = AcidenteSerializer(ultimos_acidentes, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def criar_acidente(request):
    serializer = AcidenteSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def atualizar_acidente(request, pk):
    try:
        acidente = Acidente.objects.get(pk=pk)
    except Acidente.DoesNotExist:
        return Response({'error': 'Acidente não encontrado'}, status=status.HTTP_404_NOT_FOUND)

    serializer = AcidenteSerializer(acidente, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_fitro_acidentes_severidade(request):
    try:
        severidade_minima = int(request.query_params.get('severidade_minima', 0))
    except ValueError:
        return Response({'error': 'Valor de severidade inválido'}, status=400)

    acidentes = Acidente.objects.filter(cod_severidade__gte=severidade_minima)
    serializer = AcidenteSerializer(acidentes, many=True)
    return Response(serializer.data)

@api_view(['GET'])
# @authentication_classes([TokenAuthentication])  # Adicione esta linha
# @permission_classes([IsAuthenticated])  # Adicione esta linha
def obter_acidentes_por_id(request, num_boletim):
    try:
        acidentes = Acidente.objects.filter(num_boletim=num_boletim)
        serializer = AcidenteSerializer(acidentes, many=True)
        return Response(serializer.data)
    except Acidente.DoesNotExist:
        return Response({"error": "Nenhum acidente encontrado para o ID fornecido."}, status=404)

