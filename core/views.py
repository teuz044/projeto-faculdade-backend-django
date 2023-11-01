from django.shortcuts import render
from .models import Acidente
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import AcidenteSerializer

@api_view(['GET'])
def acidentes_as_json(request):
    acidentes = Acidente.objects.all()
    serializer = AcidenteSerializer(acidentes, many=True)
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
def obter_acidentes_por_id(request, num_boletim):
    try:
        acidentes = Acidente.objects.filter(num_boletim=num_boletim)
        serializer = AcidenteSerializer(acidentes, many=True)
        return Response(serializer.data)
    except Acidente.DoesNotExist:
        return Response({"error": "Nenhum acidente encontrado para o ID fornecido."}, status=404)