#!/bin/bash
set -e

# ============================================
# setup.sh
# Script de setup inicial para EC2 Ubuntu/Amazon Linux
# Rodar como root ou com sudo
# ============================================

echo ">>> Atualizando sistema..."
apt-get update && apt-get upgrade -y

echo ">>> Instalando dependências..."
apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    git

echo ">>> Instalando Docker..."
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod a+r /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  tee /etc/apt/sources.list.d/docker.list > /dev/null

apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

echo ">>> Habilitando Docker..."
systemctl enable docker
systemctl start docker

echo ">>> Adicionando usuário ao grupo docker..."
usermod -aG docker ubuntu

echo ">>> Docker instalado:"
docker --version
docker compose version

echo ""
echo "============================================"
echo " PRÓXIMOS PASSOS:"
echo "============================================"
echo " 1. Clone o repositório"
echo " 2. cp .env.example .env && edite o .env"
echo " 3. chmod +x nginx/init-letsencrypt.sh"
echo " 4. ./nginx/init-letsencrypt.sh seudominio.com seu@email.com"
echo " 5. docker compose up -d"
echo "============================================"
