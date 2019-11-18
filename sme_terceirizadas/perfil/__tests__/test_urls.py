import datetime
import uuid

import pytest
from rest_framework import status

from .conftest import mocked_request_api_eol, mocked_request_api_eol_usuario_diretoria_regional
from ..api.helpers import ofuscar_email
from ..api.serializers import UsuarioUpdateSerializer
from ..api.viewsets import UsuarioUpdateViewSet
from ..models import Usuario

pytestmark = pytest.mark.django_db


def test_get_usuarios(client_autenticado):
    response = client_autenticado.get('/usuarios/')
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), dict)
    json = response.json()
    assert json['count'] == 1
    assert json['results'][0]['email'] == 'test@test.com'


def test_get_meus_dados_admin_escola(users_admin_escola):
    client, email, password, rf, user = users_admin_escola
    response = client.get('/usuarios/meus-dados/')
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), dict)
    json = response.json()
    keys = ['uuid', 'nome', 'email', 'registro_funcional', 'date_joined', 'vinculo_atual', 'tipo_usuario']
    for key in keys:
        assert key in json.keys()
    assert json['email'] == email
    assert json['registro_funcional'] == rf
    assert json['tipo_usuario'] == 'escola'
    assert json['vinculo_atual'] == {
        'instituicao': {'nome': 'EMEI NOE AZEVEDO, PROF', 'uuid': 'b00b2cf4-286d-45ba-a18b-9ffe4e8d8dfd',
                        'quantidade_alunos': 420, 'lotes': [], 'periodos_escolares': [], 'escolas': []},
        'perfil': {'nome': 'Admin', 'uuid': 'd6fd15cc-52c6-4db4-b604-018d22eeb3dd'}}


def test_get_meus_dados_diretor_escola(users_diretor_escola):
    client, email, password, rf, cpf, user = users_diretor_escola
    response = client.get('/usuarios/meus-dados/')
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), dict)
    json = response.json()
    keys = ['uuid', 'nome', 'email', 'registro_funcional', 'date_joined', 'vinculo_atual', 'tipo_usuario']
    for key in keys:
        assert key in json.keys()
    assert json['email'] == email
    assert json['registro_funcional'] == rf
    assert json['tipo_usuario'] == 'escola'
    assert json['vinculo_atual'] == {
        'instituicao': {'nome': 'EMEI NOE AZEVEDO, PROF', 'uuid': 'b00b2cf4-286d-45ba-a18b-9ffe4e8d8dfd',
                        'quantidade_alunos': 420, 'lotes': [], 'periodos_escolares': [], 'escolas': []},
        'perfil': {'nome': 'DIRETOR', 'uuid': '41c20c8b-7e57-41ed-9433-ccb92e8afaf1'}}


def test_cadastro_vinculo_diretor_escola(users_diretor_escola, monkeypatch):
    client, email, password, rf, cpf, user = users_diretor_escola
    escola_ = user.vinculo_atual.instituicao
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data = {
        'registro_funcional': '5696569'
    }

    monkeypatch.setattr(UsuarioUpdateSerializer, 'get_informacoes_usuario',
                        lambda p1, p2: mocked_request_api_eol())
    response = client.post(f'/vinculos-escolas/{str(escola_.uuid)}/criar_equipe_administradora/', headers=headers,
                           data=data)
    assert response.status_code == status.HTTP_200_OK
    response.json().pop('date_joined')
    response.json().pop('uuid')
    assert response.json() == {'cpf': '95887745002', 'nome': 'IARA DAREZZO',
                               'email': '95887745002@emailtemporario.prefeitura.sp.gov.br',
                               'registro_funcional': '5696569',
                               'tipo_usuario': 'escola',
                               'vinculo_atual': {
                                   'instituicao': {'nome': 'EMEI NOE AZEVEDO, PROF',
                                                   'uuid': 'b00b2cf4-286d-45ba-a18b-9ffe4e8d8dfd',
                                                   'quantidade_alunos': 420,
                                                   'lotes': [],
                                                   'periodos_escolares': [], 'escolas': []},
                                   'perfil': {'nome': 'ADMINISTRADOR_ESCOLA',
                                              'uuid': '48330a6f-c444-4462-971e-476452b328b2'}}}
    usuario_novo = Usuario.objects.get(registro_funcional='5696569')
    assert usuario_novo.is_active is False
    assert usuario_novo.vinculo_atual is not None
    assert usuario_novo.vinculo_atual.perfil.nome == 'ADMINISTRADOR_ESCOLA'


def test_erro_403_usuario_nao_pertence_a_escola_cadastro_vinculos(escola, users_diretor_escola, monkeypatch):
    client, email, password, rf, cpf, user = users_diretor_escola
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data = {
        'registro_funcional': '5696569'
    }

    monkeypatch.setattr(UsuarioUpdateSerializer, 'get_informacoes_usuario',
                        lambda p1, p2: mocked_request_api_eol())
    response = client.post(f'/vinculos-escolas/{str(escola.uuid)}/criar_equipe_administradora/', headers=headers,
                           data=data)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_erro_401_usuario_nao_e_diretor_ou_nao_esta_logado_cadastro_vinculos(client, escola):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data = {
        'registro_funcional': '5696569'
    }
    response = client.post(f'/vinculos-escolas/{str(escola.uuid)}/criar_equipe_administradora/', headers=headers,
                           data=data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_equipe_administradora_vinculos_escola(users_diretor_escola):
    client, email, password, rf, cpf, user = users_diretor_escola
    escola_ = user.vinculo_atual.instituicao
    response = client.get(f'/vinculos-escolas/{str(escola_.uuid)}/get_equipe_administradora/')
    assert response.status_code == status.HTTP_200_OK
    response.json()[0].get('usuario').pop('date_joined')
    response.json()[0].pop('data_final')
    response.json()[0].pop('uuid')
    assert response.json() == [
        {'data_inicial': datetime.date.today().strftime('%d/%m/%Y'),
         'perfil': {'nome': 'ADMINISTRADOR_ESCOLA', 'uuid': '48330a6f-c444-4462-971e-476452b328b2'},
         'usuario': {'uuid': '8344f23a-95c4-4871-8f20-3880529767c0', 'nome': 'Fulano da Silva',
                     'email': 'fulano@teste.com', 'registro_funcional': '1234567'}}]


def test_cadastro_vinculo_diretoria_regional(users_cogestor_diretoria_regional, monkeypatch):
    client, email, password, rf, cpf, user = users_cogestor_diretoria_regional
    diretoria_regional_ = user.vinculo_atual.instituicao
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data = {
        'registro_funcional': '6812805'
    }

    monkeypatch.setattr(UsuarioUpdateSerializer, 'get_informacoes_usuario',
                        lambda p1, p2: mocked_request_api_eol_usuario_diretoria_regional())
    response = client.post(
        f'/vinculos-diretorias-regionais/{str(diretoria_regional_.uuid)}/criar_equipe_administradora/', headers=headers,
        data=data)
    assert response.status_code == status.HTTP_200_OK
    response.json().pop('date_joined')
    response.json().pop('uuid')
    assert response.json() == {'cpf': '47088910080', 'nome': 'LUIZA MARIA BASTOS',
                               'email': '47088910080@emailtemporario.prefeitura.sp.gov.br',
                               'registro_funcional': '6812805',
                               'tipo_usuario': 'diretoriaregional',
                               'vinculo_atual': {
                                   'instituicao': {'nome': 'DIRETORIA REGIONAL DE EDUCACAO CAPELA DO SOCORRO',
                                                   'uuid': 'b00b2cf4-286d-45ba-a18b-9ffe4e8d8dfd',
                                                   'quantidade_alunos': None,
                                                   'lotes': [],
                                                   'periodos_escolares': [], 'escolas': []},
                                   'perfil': {'nome': 'ADMINISTRADOR_DRE',
                                              'uuid': '48330a6f-c444-4462-971e-476452b328b2'}}}
    usuario_novo = Usuario.objects.get(registro_funcional='6812805')
    assert usuario_novo.is_active is False
    assert usuario_novo.vinculo_atual is not None
    assert usuario_novo.vinculo_atual.perfil.nome == 'ADMINISTRADOR_DRE'


def test_get_equipe_administradora_vinculos_dre(users_cogestor_diretoria_regional):
    client, email, password, rf, cpf, user = users_cogestor_diretoria_regional
    diretoria_regional_ = user.vinculo_atual.instituicao
    response = client.get(f'/vinculos-diretorias-regionais/{str(diretoria_regional_.uuid)}/get_equipe_administradora/')
    assert response.status_code == status.HTTP_200_OK
    response.json()[0].get('usuario').pop('date_joined')
    response.json()[0].pop('data_final')
    response.json()[0].pop('uuid')
    assert response.json() == [
        {'data_inicial': datetime.date.today().strftime('%d/%m/%Y'),
         'perfil': {'nome': 'ADMINISTRADOR_DRE', 'uuid': '48330a6f-c444-4462-971e-476452b328b2'},
         'usuario': {'uuid': '8344f23a-95c4-4871-8f20-3880529767c0', 'nome': 'Fulano da Silva',
                     'email': 'fulano@teste.com', 'registro_funcional': '1234567'}}]


def test_erro_403_usuario_nao_pertence_a_dre_cadastro_vinculos(diretoria_regional,
                                                               users_cogestor_diretoria_regional,
                                                               monkeypatch):
    client, email, password, rf, cpf, user = users_cogestor_diretoria_regional
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data = {
        'registro_funcional': '5696569'
    }

    monkeypatch.setattr(UsuarioUpdateSerializer, 'get_informacoes_usuario',
                        lambda p1, p2: mocked_request_api_eol_usuario_diretoria_regional())
    response = client.post(
        f'/vinculos-diretorias-regionais/{str(diretoria_regional.uuid)}/criar_equipe_administradora/',
        headers=headers, data=data)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_erro_401_usuario_nao_e_cogestor_nem_suplente_ou_nao_esta_logado_cadastro_vinculos(client,
                                                                                           diretoria_regional):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data = {
        'registro_funcional': '5696569'
    }
    response = client.post(
        f'/vinculos-diretorias-regionais/{str(diretoria_regional.uuid)}/criar_equipe_administradora/',
        headers=headers, data=data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_cadastro_vinculo_codae_gestao_alimentacao(users_codae_gestao_alimentacao, monkeypatch):
    client, email, password, rf, cpf, user = users_codae_gestao_alimentacao
    codae_ = user.vinculo_atual.instituicao
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data = {
        'registro_funcional': '6812805'
    }

    monkeypatch.setattr(UsuarioUpdateSerializer, 'get_informacoes_usuario',
                        lambda p1, p2: mocked_request_api_eol_usuario_diretoria_regional())
    response = client.post(
        f'/vinculos-codae-gestao-alimentacao-terceirizada/{str(codae_.uuid)}/criar_equipe_administradora/',
        headers=headers,
        data=data)
    assert response.status_code == status.HTTP_200_OK
    response.json().pop('date_joined')
    response.json().pop('uuid')
    assert response.json() == {'cpf': '47088910080', 'nome': 'LUIZA MARIA BASTOS',
                               'email': '47088910080@emailtemporario.prefeitura.sp.gov.br',
                               'registro_funcional': '6812805',
                               'tipo_usuario': 'gestao_alimentacao_terceirizada',
                               'vinculo_atual': {
                                   'instituicao': {'nome': 'CODAE',
                                                   'uuid': 'b00b2cf4-286d-45ba-a18b-9ffe4e8d8dfd',
                                                   'quantidade_alunos': None,
                                                   'lotes': [],
                                                   'periodos_escolares': [], 'escolas': []},
                                   'perfil': {'nome': 'ADMINISTRADOR_GESTAO_ALIMENTACAO_TERCEIRIZADA',
                                              'uuid': '48330a6f-c444-4462-971e-476452b328b2'}}}
    usuario_novo = Usuario.objects.get(registro_funcional='6812805')
    assert usuario_novo.is_active is False
    assert usuario_novo.vinculo_atual is not None
    assert usuario_novo.vinculo_atual.perfil.nome == 'ADMINISTRADOR_GESTAO_ALIMENTACAO_TERCEIRIZADA'


def test_get_equipe_administradora_vinculos_codae(users_codae_gestao_alimentacao):
    client, email, password, rf, cpf, user = users_codae_gestao_alimentacao
    codae_ = user.vinculo_atual.instituicao
    response = client.get(
        f'/vinculos-codae-gestao-alimentacao-terceirizada/{str(codae_.uuid)}/get_equipe_administradora/')
    assert response.status_code == status.HTTP_200_OK
    response.json()[0].get('usuario').pop('date_joined')
    response.json()[0].pop('data_final')
    response.json()[0].pop('uuid')
    assert response.json() == [
        {'data_inicial': datetime.date.today().strftime('%d/%m/%Y'),
         'perfil': {'nome': 'ADMINISTRADOR_GESTAO_ALIMENTACAO_TERCEIRIZADA',
                    'uuid': '48330a6f-c444-4462-971e-476452b328b2'},
         'usuario': {'uuid': '8344f23a-95c4-4871-8f20-3880529767c0', 'nome': 'Fulano da Silva',
                     'email': 'fulano@teste.com', 'registro_funcional': '1234567'}}]


def test_erro_401_usuario_nao_e_coordenador_ou_nao_esta_logado_cadastro_vinculos(client,
                                                                                 codae):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data = {
        'registro_funcional': '5696569'
    }
    response = client.post(
        f'/vinculos-codae-gestao-alimentacao-terceirizada/{str(codae.uuid)}/criar_equipe_administradora/',
        headers=headers, data=data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_cadastro_erro(client):
    response = client.post('/cadastro/', data={
        'email': 'string',
        'registro_funcional': 'string',
        'password': 'string',
        'confirmar_password': 'string',
        'cpf': 'string'
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert isinstance(response.json(), dict)
    assert response.json() == {
        'detail': 'Erro ao cadastrar usuário'
    }


def test_cadastro_diretor(client, users_diretor_escola, monkeypatch):
    _, email, password, rf, cpf, user = users_diretor_escola
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data = {
        'email': email,
        'registro_funcional': rf,
        'password': password,
        'confirmar_password': password,
        'cpf': cpf
    }
    assert user.registro_funcional == rf

    monkeypatch.setattr(UsuarioUpdateViewSet, '_get_usuario', lambda p1, p2: user)
    monkeypatch.setattr(Usuario, 'pode_efetuar_cadastro',
                        lambda: True)
    response = client.post('/cadastro/', headers=headers, data=data)
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    keys = ['uuid', 'nome', 'email', 'registro_funcional', 'date_joined', 'vinculo_atual', 'tipo_usuario']
    for key in keys:
        assert key in json.keys()
    assert json['email'] == email
    assert json['registro_funcional'] == rf
    assert json['tipo_usuario'] == 'escola'
    assert json['vinculo_atual'] == {
        'instituicao': {'nome': 'EMEI NOE AZEVEDO, PROF', 'uuid': 'b00b2cf4-286d-45ba-a18b-9ffe4e8d8dfd',
                        'quantidade_alunos': 420, 'lotes': [], 'periodos_escolares': [], 'escolas': []},
        'perfil': {'nome': 'DIRETOR', 'uuid': '41c20c8b-7e57-41ed-9433-ccb92e8afaf1'}}


def test_post_usuarios(client_autenticado):
    response = client_autenticado.post('/usuarios/')
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    response = client_autenticado.put('/usuarios/')
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_confirmar_email(client, usuarios_pendentes_confirmacao):
    usuario = usuarios_pendentes_confirmacao
    assert usuario.is_active is False  # deve estar inativo no sistema
    assert usuario.is_confirmed is False  # deve estar com email nao confirmado
    response = client.get(f'/confirmar_email/{usuario.uuid}/{usuario.confirmation_key}/')  # ativacao endpoint

    usuario_apos_ativacao = Usuario.objects.get(id=usuario.id)
    assert usuario_apos_ativacao.is_confirmed is True  # apos a ativacao pelo link confirma email
    assert usuario_apos_ativacao.is_active is True  # # apos a ativacao pelo link ativa no sistema

    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    keys = ['uuid', 'cpf', 'nome', 'email', 'registro_funcional', 'tipo_usuario', 'date_joined', 'vinculo_atual']
    for key in keys:
        assert key in json.keys()
    assert len(json.keys()) == len(keys)
    json.pop('date_joined')

    assert json == {
        'cpf': usuario.cpf, 'uuid': usuario.uuid, 'nome': usuario.nome, 'email': usuario.email,
        'registro_funcional': usuario.registro_funcional, 'tipo_usuario': 'escola',
        'vinculo_atual': {
            'instituicao': {'nome': usuario.vinculo_atual.instituicao.nome,
                            'uuid': str(usuario.vinculo_atual.instituicao.uuid),
                            'quantidade_alunos': usuario.vinculo_atual.instituicao.quantidade_alunos,
                            'lotes': [], 'periodos_escolares': [], 'escolas': []
                            },
            'perfil': {'nome': usuario.vinculo_atual.perfil.nome, 'uuid': str(usuario.vinculo_atual.perfil.uuid)}}}


def test_confirmar_error(client, usuarios_pendentes_confirmacao):
    usuario = usuarios_pendentes_confirmacao
    respo = client.get(
        f'/confirmar_email/{uuid.uuid4()}/{usuario.confirmation_key}/')  # chave email correta uuid errado
    assert respo.status_code == status.HTTP_400_BAD_REQUEST
    assert respo.json() == {'detail': 'Erro ao confirmar email'}


def test_recuperar_senha(client, usuarios_pendentes_confirmacao):
    usuario = usuarios_pendentes_confirmacao
    response = client.get(f'/cadastro/recuperar-senha/{usuario.registro_funcional}/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'email': ofuscar_email(usuario.email)}

    response2 = client.get(f'/cadastro/recuperar-senha/{usuario.email}/')
    assert response2.status_code == status.HTTP_200_OK
    assert response2.json() == {'email': ofuscar_email(usuario.email)}


def test_recuperar_senha_invalido(client, usuarios_pendentes_confirmacao):
    response = client.get(f'/cadastro/recuperar-senha/NAO-EXISTE/')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': 'Não existe usuário com este e-mail ou RF'}