"""
AWS Lambda - Log and Notify
Enregistre chaque upload et envoie une notification.
"""

import json
import boto3
import os
from datetime import datetime

s3_client = boto3.client("s3")
sns_client = boto3.client("sns")


def lambda_handler(event, context):
    """
    Point d'entrée de la fonction Lambda.
    Log l'upload et envoie une notification SNS.
    """
    # Récupérer les informations de l'événement S3
    record = event["Records"][0]
    bucket = record["s3"]["bucket"]["name"]
    key = record["s3"]["object"]["key"]
    size = record["s3"]["object"].get("size", 0)
    event_time = record["eventTime"]

    # Créer le message de log
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "event_time": event_time,
        "bucket": bucket,
        "file": key,
        "size_bytes": size,
        "size_readable": format_size(size),
    }

    print(f"📤 Nouveau fichier uploadé:")
    print(json.dumps(log_entry, indent=2))

    # Envoyer notification SNS (si configuré)
    sns_topic_arn = os.environ.get("SNS_TOPIC_ARN")
    if sns_topic_arn:
        try:
            message = f"""
🆕 Nouveau fichier uploadé sur S3

📁 Fichier: {key}
🪣 Bucket: {bucket}
📦 Taille: {format_size(size)}
🕐 Date: {event_time}
            """

            sns_client.publish(
                TopicArn=sns_topic_arn,
                Subject=f"[S3] Nouveau fichier: {key}",
                Message=message,
            )
            print("📧 Notification envoyée avec succès")
        except Exception as e:
            print(f"⚠️ Erreur envoi notification: {str(e)}")

    return {"statusCode": 200, "body": json.dumps(log_entry)}


def format_size(size_bytes: int) -> str:
    """Formate une taille en bytes en format lisible."""
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} TB"
