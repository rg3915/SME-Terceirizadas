#!/usr/bin/env bash
find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf

echo "Verificando testes unitários e de integração..."
pytest

echo "Verificando se está usando imports relativos..."
grep -rnw "from sme_terceirizadas" "sme_terceirizadas"

echo "Verificando estilo e qualidade de código..."
flake8

echo "Verificando falhas de segurança média ou superior..."
bandit -r sme_terceirizadas -ll

echo "Verificando tipagem estática..."
mypy sme_terceirizadas


read -p "Deseja rodar o code climate?(S/N)" yn
    case $yn in
        [Ss]* ) echo "Rodando code climate..."
                docker run \
                  --interactive --tty --rm \
                  --env CODECLIMATE_CODE="$PWD" \
                  --volume "$PWD":/code \
                  --volume /var/run/docker.sock:/var/run/docker.sock \
                  --volume /tmp/cc:/tmp/cc \
                  codeclimate/codeclimate analyze
                ;;
    esac
