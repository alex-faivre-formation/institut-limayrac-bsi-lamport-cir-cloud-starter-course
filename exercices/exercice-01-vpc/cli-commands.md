# Résumé des Commandes - VPC

Ce fichier contient les commandes AWS CLI équivalentes pour créer le VPC via la ligne de commande.

## Création du VPC

```bash
# Créer le VPC
aws ec2 create-vpc \
    --cidr-block 10.0.0.0/16 \
    --tag-specifications 'ResourceType=vpc,Tags=[{Key=Name,Value=mon-premier-vpc}]'

# Récupérer l'ID du VPC
VPC_ID=$(aws ec2 describe-vpcs \
    --filters "Name=tag:Name,Values=mon-premier-vpc" \
    --query 'Vpcs[0].VpcId' \
    --output text)

# Activer DNS hostnames
aws ec2 modify-vpc-attribute \
    --vpc-id $VPC_ID \
    --enable-dns-hostnames '{"Value":true}'

# Activer DNS resolution
aws ec2 modify-vpc-attribute \
    --vpc-id $VPC_ID \
    --enable-dns-support '{"Value":true}'
```

## Création de l'Internet Gateway

```bash
# Créer l'Internet Gateway
aws ec2 create-internet-gateway \
    --tag-specifications 'ResourceType=internet-gateway,Tags=[{Key=Name,Value=mon-premier-igw}]'

# Récupérer l'ID de l'IGW
IGW_ID=$(aws ec2 describe-internet-gateways \
    --filters "Name=tag:Name,Values=mon-premier-igw" \
    --query 'InternetGateways[0].InternetGatewayId' \
    --output text)

# Attacher l'IGW au VPC
aws ec2 attach-internet-gateway \
    --internet-gateway-id $IGW_ID \
    --vpc-id $VPC_ID
```

## Création des Subnets

```bash
# Subnet Public AZ-A
aws ec2 create-subnet \
    --vpc-id $VPC_ID \
    --cidr-block 10.0.1.0/24 \
    --availability-zone eu-west-3a \
    --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=public-subnet-az-a}]'

# Subnet Public AZ-B
aws ec2 create-subnet \
    --vpc-id $VPC_ID \
    --cidr-block 10.0.2.0/24 \
    --availability-zone eu-west-3b \
    --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=public-subnet-az-b}]'

# Subnet Privé AZ-A
aws ec2 create-subnet \
    --vpc-id $VPC_ID \
    --cidr-block 10.0.10.0/24 \
    --availability-zone eu-west-3a \
    --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=private-subnet-az-a}]'

# Subnet Privé AZ-B
aws ec2 create-subnet \
    --vpc-id $VPC_ID \
    --cidr-block 10.0.20.0/24 \
    --availability-zone eu-west-3b \
    --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=private-subnet-az-b}]'

# Activer auto-assign public IP sur subnets publics
PUBLIC_SUBNET_A=$(aws ec2 describe-subnets \
    --filters "Name=tag:Name,Values=public-subnet-az-a" \
    --query 'Subnets[0].SubnetId' \
    --output text)

PUBLIC_SUBNET_B=$(aws ec2 describe-subnets \
    --filters "Name=tag:Name,Values=public-subnet-az-b" \
    --query 'Subnets[0].SubnetId' \
    --output text)

aws ec2 modify-subnet-attribute \
    --subnet-id $PUBLIC_SUBNET_A \
    --map-public-ip-on-launch

aws ec2 modify-subnet-attribute \
    --subnet-id $PUBLIC_SUBNET_B \
    --map-public-ip-on-launch
```

## Création des Route Tables

```bash
# Créer la route table publique
aws ec2 create-route-table \
    --vpc-id $VPC_ID \
    --tag-specifications 'ResourceType=route-table,Tags=[{Key=Name,Value=public-route-table}]'

# Récupérer l'ID de la route table publique
PUBLIC_RT_ID=$(aws ec2 describe-route-tables \
    --filters "Name=tag:Name,Values=public-route-table" \
    --query 'RouteTables[0].RouteTableId' \
    --output text)

# Ajouter la route vers Internet
aws ec2 create-route \
    --route-table-id $PUBLIC_RT_ID \
    --destination-cidr-block 0.0.0.0/0 \
    --gateway-id $IGW_ID

# Associer les subnets publics à la route table
aws ec2 associate-route-table \
    --route-table-id $PUBLIC_RT_ID \
    --subnet-id $PUBLIC_SUBNET_A

aws ec2 associate-route-table \
    --route-table-id $PUBLIC_RT_ID \
    --subnet-id $PUBLIC_SUBNET_B

# Créer la route table privée
aws ec2 create-route-table \
    --vpc-id $VPC_ID \
    --tag-specifications 'ResourceType=route-table,Tags=[{Key=Name,Value=private-route-table}]'

# Associer les subnets privés
PRIVATE_RT_ID=$(aws ec2 describe-route-tables \
    --filters "Name=tag:Name,Values=private-route-table" \
    --query 'RouteTables[0].RouteTableId' \
    --output text)

PRIVATE_SUBNET_A=$(aws ec2 describe-subnets \
    --filters "Name=tag:Name,Values=private-subnet-az-a" \
    --query 'Subnets[0].SubnetId' \
    --output text)

PRIVATE_SUBNET_B=$(aws ec2 describe-subnets \
    --filters "Name=tag:Name,Values=private-subnet-az-b" \
    --query 'Subnets[0].SubnetId' \
    --output text)

aws ec2 associate-route-table \
    --route-table-id $PRIVATE_RT_ID \
    --subnet-id $PRIVATE_SUBNET_A

aws ec2 associate-route-table \
    --route-table-id $PRIVATE_RT_ID \
    --subnet-id $PRIVATE_SUBNET_B
```

## Création des Security Groups

```bash
# Security Group pour serveurs Web
aws ec2 create-security-group \
    --group-name web-server-sg \
    --description "Security group for web servers" \
    --vpc-id $VPC_ID

WEB_SG_ID=$(aws ec2 describe-security-groups \
    --filters "Name=group-name,Values=web-server-sg" "Name=vpc-id,Values=$VPC_ID" \
    --query 'SecurityGroups[0].GroupId' \
    --output text)

# Règles pour le Security Group Web
aws ec2 authorize-security-group-ingress \
    --group-id $WEB_SG_ID \
    --protocol tcp \
    --port 22 \
    --cidr 0.0.0.0/0

aws ec2 authorize-security-group-ingress \
    --group-id $WEB_SG_ID \
    --protocol tcp \
    --port 80 \
    --cidr 0.0.0.0/0

aws ec2 authorize-security-group-ingress \
    --group-id $WEB_SG_ID \
    --protocol tcp \
    --port 443 \
    --cidr 0.0.0.0/0

# Security Group pour bases de données
aws ec2 create-security-group \
    --group-name database-sg \
    --description "Security group for databases" \
    --vpc-id $VPC_ID

DB_SG_ID=$(aws ec2 describe-security-groups \
    --filters "Name=group-name,Values=database-sg" "Name=vpc-id,Values=$VPC_ID" \
    --query 'SecurityGroups[0].GroupId' \
    --output text)

# Autoriser MySQL depuis le SG web
aws ec2 authorize-security-group-ingress \
    --group-id $DB_SG_ID \
    --protocol tcp \
    --port 3306 \
    --source-group $WEB_SG_ID
```

## Nettoyage complet

```bash
# Script de nettoyage (exécuter dans l'ordre)

# 1. Terminer les instances EC2 (si existantes)
# aws ec2 terminate-instances --instance-ids <instance-id>

# 2. Supprimer les Security Groups
aws ec2 delete-security-group --group-id $DB_SG_ID
aws ec2 delete-security-group --group-id $WEB_SG_ID

# 3. Dissocier et supprimer les route tables
aws ec2 delete-route-table --route-table-id $PRIVATE_RT_ID
aws ec2 delete-route-table --route-table-id $PUBLIC_RT_ID

# 4. Supprimer les subnets
aws ec2 delete-subnet --subnet-id $PUBLIC_SUBNET_A
aws ec2 delete-subnet --subnet-id $PUBLIC_SUBNET_B
aws ec2 delete-subnet --subnet-id $PRIVATE_SUBNET_A
aws ec2 delete-subnet --subnet-id $PRIVATE_SUBNET_B

# 5. Détacher et supprimer l'IGW
aws ec2 detach-internet-gateway --internet-gateway-id $IGW_ID --vpc-id $VPC_ID
aws ec2 delete-internet-gateway --internet-gateway-id $IGW_ID

# 6. Supprimer le VPC
aws ec2 delete-vpc --vpc-id $VPC_ID
```
