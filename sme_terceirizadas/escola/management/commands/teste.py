from django.core.management.base import BaseCommand
import asyncio
import httpx
import openpyxl
import time
import timeit
from datetime import datetime, date
from pathlib import Path
from pprint import pprint
from time import sleep
from rest_framework import status

from utility.carga_dados.helper import excel_to_list_with_openpyxl, progressbar
from sme_terceirizadas.dados_comuns.constants import DJANGO_EOL_API_TOKEN, DJANGO_EOL_API_URL


MDATA = datetime.now().strftime('%Y%m%d_%H%M%S')
DEFAULT_HEADERS = {'Authorization': f'Token {DJANGO_EOL_API_TOKEN}'}
DATA = date.today().isoformat().replace('-', '_')
home = str(Path.home())
dict_codigos_escolas = {}
dict_codigo_aluno_por_codigo_escola = {}
arquivo = '/home/regis/Downloads/banco_de_dietas_ativas_05.02.xlsx'
arquivo_codigos_escolas = '/home/regis/Downloads/unidades_da_rede_28.01_.xlsx'


def get_codigo_eol_escola(valor):
    return valor.strip().zfill(6)


def get_codigo_eol_aluno(valor):
    return str(valor).strip().zfill(7)


def gera_dict_codigos_escolas(items_codigos_escolas):
    for item in items_codigos_escolas:
        dict_codigos_escolas[str(item['CÓDIGO UNIDADE'])] = str(item['CODIGO EOL'])


def gera_dict_codigo_aluno_por_codigo_escola(items):
    for item in items:
        try:
            codigo_eol_escola = dict_codigos_escolas[item['CodEscola']]
        except Exception as e:
            # Grava os CodEscola não existentes em unidades_da_rede_28.01_.xlsx
            with open(f'{home}/codescola_nao_existentes.txt', 'a') as f:
                f.write(f"{item['CodEscola']}\n")

        cod_eol_aluno = get_codigo_eol_aluno(item['CodEOLAluno'])
        dict_codigo_aluno_por_codigo_escola[cod_eol_aluno] = get_codigo_eol_escola(codigo_eol_escola)


def get_escolas_unicas(items):
    # A partir da planilha, pegar todas as escolas únicas "escolas_da_planilha"
    escolas = []
    for item in items:
        escolas.append(item['CodEscola'])
    return set(escolas)


class EOLException(Exception):
    pass


async def get_informacoes_escola_turma_aluno(codigo_eol: str):
    headers = DEFAULT_HEADERS
    async with httpx.AsyncClient(headers=headers, timeout=120) as client:
        url = f'{DJANGO_EOL_API_URL}/escola_turma_aluno/{codigo_eol}'
        response = await client.get(url)
        if response.status_code == status.HTTP_200_OK:
            results = response.json()['results']
            if len(results) == 0:
                raise EOLException(f'Resultados para o código: {codigo_eol} vazios')
            print(len(results))
            with open(f'{home}/resultado.json', 'a') as f:
                f.write(f'{results}')
                f.write('\n')
            return results
        else:
            with open(f'{home}/codigo_eol_erro_da_api_eol.txt', 'a') as f:
                f.write(f"{codigo_eol}\n")
            # raise EOLException(f'API EOL com erro. Status: {response.status_code}')


async def main(escolas_da_planilha):
    task_list = []
    for i, escola in enumerate(escolas_da_planilha):
        try:
            codigo_eol_escola = get_codigo_eol_escola(dict_codigos_escolas[escola])
            task_list.append(get_informacoes_escola_turma_aluno(codigo_eol_escola))
        except Exception as e:
            # Grava os CodEscola não existentes em unidades_da_rede_28.01_.xlsx
            with open(f'{home}/codescola_nao_existentes.txt', 'a') as f:
                f.write(f"{escola}\n")

    await asyncio.gather(*task_list)


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '--start_interval', '-st',
            dest='start_interval',
            default=None,
            help='start_interval.'
        )
        parser.add_argument(
            '--end_interval', '-end',
            dest='end_interval',
            default=None,
            help='end_interval.'
        )

    def handle(self, *args, **options):
        start_time = time.monotonic()

        start_interval = options['start_interval']
        end_interval = options['end_interval']

        items = excel_to_list_with_openpyxl(arquivo, in_memory=False)
        items_codigos_escolas = excel_to_list_with_openpyxl(arquivo_codigos_escolas, in_memory=False)

        gera_dict_codigos_escolas(items_codigos_escolas)
        gera_dict_codigo_aluno_por_codigo_escola(items)

        # A partir da planilha, pegar todas as escolas únicas "escolas_da_planilha"
        escolas_da_planilha = list(get_escolas_unicas(items))[int(start_interval):int(end_interval)]
        print('Escolas:', len(escolas_da_planilha))

        loop = asyncio.get_event_loop()
        loop.run_until_complete(main(escolas_da_planilha))
        time_taken = round(time.monotonic() - start_time, 2)
        print(f"Time Taken:{time_taken}")
        with open('/tmp/tempo.txt', 'a') as f:
            f.write(f'{len(escolas_da_planilha)} escolas em {time_taken} s\n')