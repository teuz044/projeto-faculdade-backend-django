from django.shortcuts import render
from .models import Acidente, Log
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .serializers import AcidenteSerializer
from django.utils import timezone
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
def atualizar_acidente(request, pk):
    try:
        acidente = Acidente.objects.get(pk=pk)
    except Acidente.DoesNotExist:
        return Response({'error': 'Acidente não encontrado'}, status=status.HTTP_404_NOT_FOUND)
    
    current_num_boletim = acidente.num_boletim
    serializer = AcidenteSerializer(acidente, data=request.data)
    if serializer.is_valid():
        serializer.save()
        user_id = request.session.get('user_id')
        updated_num_boletim = serializer.data.get('num_boletim', current_num_boletim)
        Log.objects.create(user_id=user_id, acao='Usuário atualizou acidente', descricao=f'Usuário atualizou acidente: {updated_num_boletim}', timestamp=timezone.now())
       
        return Response(serializer.data)
    print(serializer.erros)
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

