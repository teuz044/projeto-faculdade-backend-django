from django.test import TestCase
import pytest
from django.contrib.sessions.middleware import SessionMiddleware

from .models import Acidente
from django.test import RequestFactory
from django.urls import reverse
import pytest
from mixer.backend.django import mixer  # Para criar instâncias de modelos de forma fácil
from .views import acidentes_as_json, ultimos_acidentes, criar_acidente, atualizar_acidente, get_fitro_acidentes_severidade, obter_acidentes_por_id

@pytest.mark.django_db
def test_acidentes_as_json():
    factory = RequestFactory()
    request = factory.get(reverse('acidentes-as-json'))
    response = acidentes_as_json(request)
    assert response.status_code == 200

@pytest.mark.django_db
def test_ultimos_acidentes():
    mixer.cycle(10).blend(Acidente)  # Cria 10 instâncias de Acidente usando o Mixer
    factory = RequestFactory()

    request = factory.get(reverse('ultimos-acidentes'))
    middleware = SessionMiddleware(lambda get_response: None)  # Fornecer uma função get_response
    middleware.process_request(request)
    
    response = ultimos_acidentes(request)
    assert response.status_code == 200

@pytest.mark.django_db
def test_get_fitro_acidentes_severidade():
    factory = RequestFactory()
    request = factory.get(reverse('consulta-personalizada'), {'severidade_minima': 3})
    response = get_fitro_acidentes_severidade(request)
    assert response.status_code == 200

@pytest.mark.django_db
def test_obter_acidentes_por_id():
    acidente = mixer.blend(Acidente)  # Cria uma instância de Acidente usando o Mixer
    factory = RequestFactory()
    request = factory.get(reverse('obter_acidentes_por_id', kwargs={'num_boletim': acidente.num_boletim}))
    response = obter_acidentes_por_id(request, acidente.num_boletim)
    assert response.status_code == 200