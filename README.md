# ☁️ Formation AWS - Institut Limayrac

## 🎯 Objectifs du cours

Ce cours vous propose une introduction pratique aux services fondamentaux d'Amazon Web Services (AWS). À travers 5 exercices progressifs, vous découvrirez les concepts essentiels du cloud computing et apprendrez à déployer des infrastructures réelles sur AWS.

## 📚 Prérequis

- Un compte AWS (Free Tier recommandé)
- AWS CLI installé et configuré
- Connaissances de base en ligne de commande (bash/zsh)
- Git installé sur votre machine

## 🚀 Démarrage rapide

### 1. Cloner le repository

```bash
git clone https://github.com/alex-faivre-formation/institut-limayrac-bsi-lamport-cir-cloud-starter-course.git
cd institut-limayrac-bsi-lamport-cir-cloud-starter-course
```

### 2. Configurer AWS CLI

```bash
aws configure
# Entrez vos credentials AWS :
# - AWS Access Key ID
# - AWS Secret Access Key
# - Default region name: eu-west-1 (ou votre région préférée)
# - Default output format: json
```

### 3. Vérifier la configuration

```bash
aws sts get-caller-identity
```

## 📚 Structure du Cours

Le cours est organisé en 5 exercices pratiques progressifs qui couvrent les fondamentaux d'AWS.

### 🔹 Exercice 01 - Networking avec VPC

**Objectifs** : Comprendre et créer un réseau virtuel isolé sur AWS.

**Services AWS** :
- VPC (Virtual Private Cloud)
- Subnets (Public et Private)
- Internet Gateway
- Route Tables
- Security Groups

**Compétences acquises** :
- Utiliser AWS CLI pour créer des ressources réseau
- Comprendre l'architecture VPC (CIDR, AZs, Subnets)
- Configurer la connectivité Internet
- Sécuriser le réseau avec des Security Groups

**Documentation** : [exercises/exercise-01-vpc/README.md](./exercises/exercise-01-vpc/README.md)

---

### 🔹 Exercice 02 - Hébergement Web avec S3

**Objectifs** : Déployer un site web statique sur S3 avec un contenu éducatif sur AWS.

**Services AWS** :
- S3 (Simple Storage Service)
- Static Website Hosting
- Bucket Policies

**Compétences acquises** :
- Créer et configurer un bucket S3
- Activer l'hébergement de site web statique
- Gérer les permissions publiques
- Déployer du contenu HTML/CSS/JS

**Documentation** : [exercises/exercise-02-s3-static-website/README.md](./exercises/exercise-02-s3-static-website/README.md)

---

### 🔹 Exercice 03 - Traitement Serverless avec Lambda

**Objectifs** : Créer des fonctions Lambda déclenchées par des événements S3.

**Services AWS** :
- Lambda
- S3 Events
- IAM Roles et Policies
- CloudWatch Logs

**Compétences acquises** :
- Développer des fonctions Lambda en Python
- Configurer des déclencheurs S3
- Gérer les permissions IAM pour Lambda
- Monitorer avec CloudWatch
- Traiter des fichiers CSV automatiquement

**Documentation** : [exercises/exercise-03-lambda-s3-trigger/README.md](./exercises/exercise-03-lambda-s3-trigger/README.md)

---

### 🔹 Exercice 04 - Sécurité avec IAM

**Objectifs** : Gérer les utilisateurs, groupes et politiques de sécurité.

**Services AWS** :
- IAM (Identity and Access Management)
- Users et Groups
- Policies (Managed et Custom)
- MFA (Multi-Factor Authentication)

**Compétences acquises** :
- Créer des utilisateurs et groupes IAM
- Écrire des politiques personnalisées JSON
- Appliquer le principe du moindre privilège
- Configurer MFA pour les actions sensibles
- Gérer l'accès aux ressources S3

**Documentation** : [exercises/exercise-04-iam-users-policies/README.md](./exercises/exercise-04-iam-users-policies/README.md)

---

### 🔹 Exercice 05 - Compute avec EC2

**Objectifs** : Déployer une instance EC2 avec un serveur web Apache automatisé.

**Services AWS** :
- EC2 (Elastic Compute Cloud)
- User Data Scripts
- IMDSv2 (Instance Metadata Service v2)
- Security Groups
- Key Pairs

**Compétences acquises** :
- Lancer et configurer une instance EC2
- Automatiser le déploiement avec User Data
- Utiliser IMDSv2 pour les métadonnées
- Configurer un serveur web Apache
- Gérer les clés SSH et l'accès distant

**Documentation** : [exercises/exercise-05-ec2-web-server/README.md](./exercises/exercise-05-ec2-web-server/README.md)

---

## 🎯 Progression Recommandée

### Semaine 1 : Fondations
- **Jour 1-2** : Exercice 01 (VPC) - Comprendre le réseau AWS
- **Jour 3-4** : Exercice 02 (S3) - Hébergement web statique
- **Jour 5** : Révision et approfondissement

### Semaine 2 : Compute et Serverless
- **Jour 1-2** : Exercice 03 (Lambda) - Traitement automatisé
- **Jour 3-4** : Exercice 05 (EC2) - Serveurs virtuels
- **Jour 5** : Projet intégratif

### Semaine 3 : Sécurité et Bonnes Pratiques
- **Jour 1-2** : Exercice 04 (IAM) - Gestion des accès
- **Jour 3-4** : Révision complète avec sécurité renforcée
- **Jour 5** : Évaluation finale

---

## 💡 Concepts AWS Clés

### Modèles de Service Cloud

#### IaaS (Infrastructure as a Service)
Services de base : EC2, VPC, S3, EBS
- Contrôle maximal sur l'infrastructure
- Gestion du système d'exploitation et des applications

#### PaaS (Platform as a Service)
Services managés : Elastic Beanstalk, RDS, ECS
- AWS gère l'infrastructure sous-jacente
- Focus sur le déploiement d'applications

#### SaaS (Software as a Service)
Services applicatifs : WorkSpaces, Chime, WorkDocs
- Applications prêtes à l'emploi
- Aucune gestion d'infrastructure

#### FaaS (Function as a Service)
Serverless : Lambda, API Gateway
- Exécution de code sans gestion de serveurs
- Facturation à la milliseconde d'exécution

### Infrastructure Globale AWS

#### Régions
- Zones géographiques indépendantes (ex: eu-west-1 = Irlande)
- Chaque région contient plusieurs Availability Zones
- Choix de la région selon : latence, conformité, coûts

#### Availability Zones (AZ)
- Data centers isolés dans une région
- Haute disponibilité et tolérance aux pannes
- Connexion réseau à faible latence entre AZs

### AWS Free Tier
- **Gratuit 12 mois** : 750h EC2 t2.micro/mois, 5GB S3
- **Toujours gratuit** : 1M requêtes Lambda/mois, DynamoDB 25GB
- **Essais gratuits** : Services temporairement gratuits

---

## 🛠️ Commandes AWS CLI Essentielles

### Configuration et Identité
```bash
# Vérifier l'identité
aws sts get-caller-identity

# Lister les régions disponibles
aws ec2 describe-regions --output table

# Changer de région (temporaire)
aws configure set region us-east-1
```

### S3
```bash
# Créer un bucket
aws s3 mb s3://mon-bucket-unique

# Lister les buckets
aws s3 ls

# Copier des fichiers
aws s3 cp ./website/ s3://mon-bucket-unique/ --recursive

# Synchroniser des dossiers
aws s3 sync ./local-folder s3://mon-bucket-unique/
```

### EC2
```bash
# Lister les instances
aws ec2 describe-instances --query 'Reservations[*].Instances[*].[InstanceId,State.Name,PublicIpAddress]' --output table

# Lancer une instance
aws ec2 run-instances --image-id ami-xxxxx --instance-type t2.micro --key-name ma-cle

# Arrêter une instance
aws ec2 stop-instances --instance-ids i-xxxxx

# Terminer une instance
aws ec2 terminate-instances --instance-ids i-xxxxx
```

### Lambda
```bash
# Lister les fonctions
aws lambda list-functions

# Invoquer une fonction
aws lambda invoke --function-name ma-fonction output.json

# Voir les logs
aws logs tail /aws/lambda/ma-fonction --follow
```

### IAM
```bash
# Lister les utilisateurs
aws iam list-users

# Créer un utilisateur
aws iam create-user --user-name john-doe

# Attacher une policy
aws iam attach-user-policy --user-name john-doe --policy-arn arn:aws:iam::aws:policy/ReadOnlyAccess
```

---

## 🔧 Troubleshooting

### Problèmes Courants

#### ❌ Erreur : Access Denied
**Cause** : Permissions IAM insuffisantes
**Solution** :
```bash
# Vérifier vos permissions actuelles
aws iam get-user
aws iam list-attached-user-policies --user-name VOTRE_USER
```

#### ❌ Erreur : InvalidKeyPair.NotFound
**Cause** : Clé SSH non trouvée ou dans la mauvaise région
**Solution** :
```bash
# Lister les key pairs dans la région
aws ec2 describe-key-pairs

# Créer une nouvelle key pair
aws ec2 create-key-pair --key-name ma-cle-ec2 --query 'KeyMaterial' --output text > ma-cle-ec2.pem
chmod 400 ma-cle-ec2.pem
```

#### ❌ Erreur : BucketAlreadyExists
**Cause** : Les noms de bucket S3 sont globalement uniques
**Solution** : Utiliser un nom unique avec préfixe (ex: `mon-nom-projet-2024`)

#### ❌ Instance EC2 ne répond pas
**Causes possibles** :
1. Security Group bloque le trafic
2. Subnet sans route vers Internet Gateway
3. User Data script a échoué

**Solutions** :
```bash
# Vérifier les Security Groups
aws ec2 describe-security-groups --group-ids sg-xxxxx

# Vérifier les logs système
aws ec2 get-console-output --instance-id i-xxxxx

# Vérifier les route tables
aws ec2 describe-route-tables --filters "Name=vpc-id,Values=vpc-xxxxx"
```

#### ❌ Lambda Timeout
**Cause** : Fonction Lambda dépasse 3 secondes (timeout par défaut)
**Solution** :
```bash
# Augmenter le timeout à 30 secondes
aws lambda update-function-configuration --function-name ma-fonction --timeout 30
```

### Bonnes Pratiques de Débogage

1. **Activer CloudWatch Logs** pour toutes les ressources
2. **Utiliser AWS CloudTrail** pour auditer les actions
3. **Tester avec `--dry-run`** quand disponible
4. **Vérifier les limites de service** (Service Quotas)
5. **Consulter AWS Health Dashboard** pour incidents régionaux

---

## 📖 Ressources d'Apprentissage

### Documentation Officielle AWS
- [AWS Documentation](https://docs.aws.amazon.com/)
- [AWS CLI Reference](https://awscli.amazonaws.com/v2/documentation/api/latest/index.html)
- [AWS Free Tier](https://aws.amazon.com/free/)
- [AWS Architecture Center](https://aws.amazon.com/architecture/)

### Tutoriels et Labs
- [AWS Skill Builder](https://skillbuilder.aws/) - Formation gratuite officielle
- [AWS Workshops](https://workshops.aws/) - Labs pratiques guidés
- [AWS Samples GitHub](https://github.com/aws-samples) - Exemples de code

### Certifications AWS
- **AWS Certified Cloud Practitioner** - Niveau fondamental
- **AWS Certified Solutions Architect – Associate** - Niveau intermédiaire
- **AWS Certified Developer – Associate** - Focus développement

### Communauté
- [AWS re:Post](https://repost.aws/) - Forum communautaire officiel
- [AWS Blogs](https://aws.amazon.com/blogs/) - Articles techniques
- [AWS Events](https://aws.amazon.com/events/) - Webinaires et conférences

### Outils de Calcul de Coûts
- [AWS Pricing Calculator](https://calculator.aws/) - Estimer les coûts
- [AWS Cost Explorer](https://aws.amazon.com/aws-cost-management/aws-cost-explorer/) - Analyser les dépenses

---

## ⚠️ Avertissements Importants

### Sécurité
- ⚠️ Ne jamais commiter de credentials AWS dans Git
- ⚠️ Toujours utiliser IAM users, jamais le root account
- ⚠️ Activer MFA sur tous les comptes
- ⚠️ Suivre le principe du moindre privilège

### Coûts
- 💰 Toujours vérifier que vos ressources sont dans le Free Tier
- 💰 **IMPÉRATIF** : Supprimer les ressources après chaque exercice
- 💰 Configurer des alertes de facturation (Billing Alerts)
- 💰 Les ressources oubliées peuvent coûter cher !

### Nettoyage des Ressources
```bash
# EC2
aws ec2 terminate-instances --instance-ids i-xxxxx

# S3 (vider puis supprimer)
aws s3 rm s3://mon-bucket --recursive
aws s3 rb s3://mon-bucket

# Lambda
aws lambda delete-function --function-name ma-fonction

# VPC (supprimer dans l'ordre : instances, subnets, IGW, VPC)
aws ec2 delete-vpc --vpc-id vpc-xxxxx
```

---

## 🤝 Support

### Aide pour ce Cours
- Consultez d'abord le README.md de chaque exercice
- Vérifiez la section Troubleshooting ci-dessus
- Posez vos questions sur le forum du cours
- Contactez votre instructeur

### Support AWS
- [AWS Support Center](https://console.aws.amazon.com/support/)
- [AWS re:Post](https://repost.aws/) pour questions techniques
- Documentation officielle pour chaque service

---

## 📝 Licence et Crédits

Ce cours est conçu à des fins éducatives pour l'apprentissage des services AWS.

**Bonne formation sur AWS ! ☁️**
