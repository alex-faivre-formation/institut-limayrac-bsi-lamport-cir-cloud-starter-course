#!/bin/bash
# User Data Script - Installation Apache & Page Métadonnées EC2
# Exercice 05 - Formation AWS Cloud

set -e

echo "🚀 Installation..."

# Installation Apache
yum update -y
yum install -y httpd
systemctl start httpd
systemctl enable httpd

# Récupération des métadonnées via IMDSv2
TOKEN=$(curl -s -X PUT "http://169.254.169.254/latest/api/token" \
    -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")

get_metadata() {
    curl -s -H "X-aws-ec2-metadata-token: $TOKEN" \
        "http://169.254.169.254/latest/meta-data/$1"
}

INSTANCE_ID=$(get_metadata instance-id)
AZ=$(get_metadata placement/availability-zone)
PUBLIC_IP=$(get_metadata public-ipv4 2>/dev/null || echo "N/A")
INSTANCE_TYPE=$(get_metadata instance-type)
AMI_ID=$(get_metadata ami-id)
PRIVATE_IP=$(get_metadata local-ipv4)
REGION=$(get_metadata placement/region)

# Copier les fichiers web
WEB_BASE="/var/www/html"

# Méthode 1: Depuis un repo Git (recommandé)
if command -v git &> /dev/null; then
    cd /tmp
    git clone https://github.com/votre-user/votre-repo.git ec2-web 2>/dev/null && \
    cp ec2-web/exercises/exercise-05-ec2-web-server/web/* "$WEB_BASE/" && \
    rm -rf ec2-web && \
    echo "✅ Fichiers web téléchargés depuis Git"
fi

# Vérifier que les fichiers sont présents
if [ ! -f "$WEB_BASE/index.html" ]; then
    echo "⚠️  Fichiers web manquants, création d'une page par défaut"
    cat > "$WEB_BASE/index.html" <<'HTML'
<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>EC2 Metadata</title>
<style>body{font-family:system-ui;max-width:800px;margin:50px auto;padding:20px;background:#1a1a2a;color:#fff}
.card{background:#2a2a3a;padding:20px;margin:10px 0;border-radius:8px}code{background:#000;padding:2px 6px;border-radius:4px}</style>
</head><body><h1>🚀 Instance EC2 Active</h1><div id="data"></div>
<script>fetch('/metadata.json').then(r=>r.json()).then(d=>{document.getElementById('data').innerHTML=Object.entries(d).map(([k,v])=>`<div class="card"><strong>${k}:</strong> <code>${v}</code></div>`).join('')})</script>
</body></html>
HTML
fi

# Fichier JSON pour les métadonnées
cat > "$WEB_BASE/metadata.json" <<EOF
{
  "instance_id": "$INSTANCE_ID",
  "instance_type": "$INSTANCE_TYPE",
  "az": "$AZ",
  "region": "$REGION",
  "public_ip": "$PUBLIC_IP",
  "private_ip": "$PRIVATE_IP",
  "ami_id": "$AMI_ID",
  "created_date": "$(date '+%d/%m/%Y à %H:%M:%S')"
}
EOF

chmod 644 "$WEB_BASE"/*

echo "✅ Installé !"
echo "📊 Instance: $INSTANCE_ID | Type: $INSTANCE_TYPE | Zone: $AZ"
