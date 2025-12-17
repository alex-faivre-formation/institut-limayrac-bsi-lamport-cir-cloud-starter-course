"""
AWS Lambda - CSV Analyzer
Analyse les fichiers CSV uploadés sur S3 et génère des statistiques.
"""

import json
import boto3
import csv
from io import StringIO
from datetime import datetime

s3_client = boto3.client("s3")


def lambda_handler(event, context):
    """
    Point d'entrée de la fonction Lambda.
    Déclenché automatiquement lors d'un upload S3.

    Args:
        event: Événement S3 contenant les informations du fichier
        context: Contexte d'exécution Lambda

    Returns:
        dict: Résultat de l'analyse avec code de statut
    """
    # Récupérer les informations de l'événement S3
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = event["Records"][0]["s3"]["object"]["key"]

    print(f"📁 Traitement du fichier: s3://{bucket}/{key}")

    try:
        # Télécharger le fichier CSV
        response = s3_client.get_object(Bucket=bucket, Key=key)
        content = response["Body"].read().decode("utf-8")

        # Analyser le CSV
        stats = analyze_csv(content, key)

        # Générer le nom du fichier de sortie
        output_key = key.replace("input/", "output/").replace(".csv", "_stats.json")

        # Sauvegarder les statistiques
        s3_client.put_object(
            Bucket=bucket,
            Key=output_key,
            Body=json.dumps(stats, indent=2, ensure_ascii=False),
            ContentType="application/json",
        )

        print(f"✅ Statistiques sauvegardées: s3://{bucket}/{output_key}")

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "CSV analysé avec succès", "stats": stats}),
        }

    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        raise e


def analyze_csv(content: str, file_name: str) -> dict:
    """
    Analyse le contenu d'un fichier CSV.

    Args:
        content: Contenu du fichier CSV en string
        file_name: Nom du fichier pour référence

    Returns:
        dict: Statistiques du fichier CSV
    """
    csv_reader = csv.DictReader(StringIO(content))
    rows = list(csv_reader)

    if not rows:
        return {
            "file_name": file_name,
            "analyzed_at": datetime.now().isoformat(),
            "total_rows": 0,
            "columns": [],
            "column_count": 0,
            "message": "Fichier CSV vide",
        }

    columns = list(rows[0].keys())

    # Statistiques de base
    stats = {
        "file_name": file_name,
        "analyzed_at": datetime.now().isoformat(),
        "total_rows": len(rows),
        "columns": columns,
        "column_count": len(columns),
        "sample_data": rows[:3] if len(rows) >= 3 else rows,
    }

    # Statistiques par colonne
    column_stats = {}
    for col in columns:
        values = [row[col] for row in rows if row[col]]
        column_stats[col] = {
            "non_empty_count": len(values),
            "empty_count": len(rows) - len(values),
            "unique_values": len(set(values)),
        }

        # Tenter de calculer des stats numériques
        numeric_values = []
        for v in values:
            try:
                numeric_values.append(float(v))
            except ValueError:
                pass

        if numeric_values:
            column_stats[col]["numeric"] = {
                "min": min(numeric_values),
                "max": max(numeric_values),
                "avg": sum(numeric_values) / len(numeric_values),
            }

    stats["column_stats"] = column_stats

    return stats
