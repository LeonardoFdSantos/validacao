#!/bin/bash
set -e

# ============================================
# init-letsencrypt.sh
# Gera certificado SSL inicial com Let's Encrypt
# Rodar UMA VEZ antes do primeiro docker compose up
# ============================================

if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Uso: ./init-letsencrypt.sh <dominio> <email>"
    exit 1
fi

DOMAIN=$1
EMAIL=$2
DATA_PATH="./certbot"

echo ">>> Criando diretórios..."
mkdir -p "$DATA_PATH/conf/live/$DOMAIN"
mkdir -p "$DATA_PATH/www"

echo ">>> Baixando parâmetros TLS recomendados..."
curl -s https://raw.githubusercontent.com/certbot/certbot/master/certbot-nginx/certbot_nginx/_internal/tls_configs/options-ssl-nginx.conf > "$DATA_PATH/conf/options-ssl-nginx.conf"
curl -s https://raw.githubusercontent.com/certbot/certbot/master/certbot/certbot/ssl-dhparams.pem > "$DATA_PATH/conf/ssl-dhparams.pem"

echo ">>> Criando certificado dummy para nginx iniciar..."
openssl req -x509 -nodes -newkey rsa:2048 -days 1 \
    -keyout "$DATA_PATH/conf/live/$DOMAIN/privkey.pem" \
    -out "$DATA_PATH/conf/live/$DOMAIN/fullchain.pem" \
    -subj "/CN=localhost"

echo ">>> Subindo nginx..."
docker compose up -d nginx

echo ">>> Removendo certificado dummy..."
rm -rf "$DATA_PATH/conf/live/$DOMAIN"

echo ">>> Solicitando certificado real..."
docker compose run --rm certbot certonly \
    --webroot \
    --webroot-path=/var/www/certbot \
    --email "$EMAIL" \
    --agree-tos \
    --no-eff-email \
    -d "$DOMAIN"

echo ">>> Reiniciando nginx com certificado real..."
docker compose restart nginx

echo ">>> SSL configurado com sucesso para $DOMAIN"
