from django.shortcuts import render
from .models import Acidente, Log
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .serializers import AcidenteSerializer
from django.utils import timezone
import requests
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import pickle
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
import pandas as pd
from rest_framework.views import APIView
import numpy as np



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
    ORDER BY num_boletim DESC
    LIMIT 10;
    """

    ultimos_acidentes = Acidente.objects.raw(consulta_sql)
    serializer = AcidenteSerializer(ultimos_acidentes, many=True)
    user_id = request.session.get('user_id')
    Log.objects.create(user_id=user_id, acao='Criar Acidente', descricao=f'Usuário criou um novo acidente: {serializer.data}', timestamp=timezone.now())
    return Response(serializer.data)

@api_view(['POST'])
def criar_acidente(request):
    serializer = AcidenteSerializer(data=request.data)
    print(request.data)
    if serializer.is_valid():
        serializer.save()
        user_id = request.session.get('user_id')
        Log.objects.create(user_id=user_id, acao='Criar Acidente', descricao=f'Usuário criou um novo acidente: {serializer.data}', timestamp=timezone.now())
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response({"error": "Erro na validação", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def atualizar_acidente(request, num_boletim):
    try:
        acidente = Acidente.objects.get(num_boletim=num_boletim)
    except Acidente.DoesNotExist:
        return Response({'error': 'Acidente não encontrado'}, status=status.HTTP_404_NOT_FOUND)
    
    current_num_boletim = acidente.num_boletim
    serializer = AcidenteSerializer(acidente, data=request.data)  # Modificação aqui
    
    if serializer.is_valid():
        serializer.save()
        user_id = request.session.get('user_id')
        updated_num_boletim = serializer.validated_data.get('num_boletim', current_num_boletim)
        Log.objects.create(
            user_id=user_id,
            acao='Usuário atualizou acidente',
            descricao=f'Usuário atualizou acidente: {updated_num_boletim}',
            timestamp=timezone.now()
        )
        return Response(serializer.data)
    print(serializer.errors)
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
    

@api_view(['GET'])
def getinfocep(request, cep):
    # Verifica se o CEP foi fornecido
    if not cep:
        return Response({"error": "CEP não fornecido"}, status=status.HTTP_400_BAD_REQUEST)

    # Consulta as informações do CEP utilizando a função consultar_cep
    dados_cep = consultar_cep(cep)

    # Verifica se as informações do CEP foram encontradas
    if dados_cep:
        return Response(dados_cep)
    else:
        return Response({"error": "Não foi possível obter as informações do CEP"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

def consultar_cep(cep):
    url = f"https://viacep.com.br/ws/{cep}/json/"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except requests.RequestException as e:
        print(f"Erro ao consultar o CEP: {e}")
        return None


@api_view(['DELETE'])
def excluir_acidente(request, num_boletim):
    try:
        acidente = Acidente.objects.get(num_boletim=num_boletim)
        acidente.delete()
        return Response({'message': f'Acidente com num_boletim {num_boletim} foi excluído com sucesso.'}, status=status.HTTP_204_NO_CONTENT)
    except Acidente.DoesNotExist:
        return Response({'error': 'Acidente não encontrado'}, status=status.HTTP_404_NOT_FOUND)