"""
AWS Lambda - File Validator (Quarantine System)
Valide les fichiers et les déplace selon leur validité.
"""

import json
import boto3
import os
from datetime import datetime

s3_client = boto3.client("s3")

# Extensions autorisées
ALLOWED_EXTENSIONS = {".csv", ".json", ".txt", ".xml"}
# Taille maximale (5 MB)
MAX_SIZE_BYTES = 5 * 1024 * 1024


def lambda_handler(event, context):
    """
    Valide un fichier uploadé et le déplace vers approved/ ou quarantine/.
    """
    record = event["Records"][0]
    bucket = record["s3"]["bucket"]["name"]
    key = record["s3"]["object"]["key"]
    size = record["s3"]["object"].get("size", 0)

    print(f"🔍 Validation du fichier: s3://{bucket}/{key}")

    # Effectuer les validations
    validation_result = validate_file(key, size)

    # Déterminer la destination
    if validation_result["is_valid"]:
        destination = key.replace("inbox/", "approved/")
        status = "✅ APPROVED"
    else:
        destination = key.replace("inbox/", "quarantine/")
        status = "❌ QUARANTINED"

    # Déplacer le fichier
    try:
        # Copier vers la destination
        s3_client.copy_object(
            Bucket=bucket, CopySource={"Bucket": bucket, "Key": key}, Key=destination
        )

        # Supprimer l'original
        s3_client.delete_object(Bucket=bucket, Key=key)

        print(f"{status}: {key} -> {destination}")

        # Créer un rapport
        report = {
            "timestamp": datetime.now().isoformat(),
            "original_file": key,
            "destination": destination,
            "status": "approved" if validation_result["is_valid"] else "quarantined",
            "validation_details": validation_result,
        }

        # Sauvegarder le rapport
        report_key = destination.rsplit(".", 1)[0] + "_report.json"
        s3_client.put_object(
            Bucket=bucket,
            Key=report_key,
            Body=json.dumps(report, indent=2),
            ContentType="application/json",
        )

        return {"statusCode": 200, "body": json.dumps(report)}

    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        raise e


def validate_file(key: str, size: int) -> dict:
    """
    Valide un fichier selon plusieurs critères.

    Returns:
        dict: Résultat de la validation avec détails
    """
    errors = []
    warnings = []

    # Extraire l'extension
    extension = "." + key.rsplit(".", 1)[-1].lower() if "." in key else ""

    # Vérification 1: Extension autorisée
    if extension not in ALLOWED_EXTENSIONS:
        errors.append(
            f"Extension '{extension}' non autorisée. Autorisées: {ALLOWED_EXTENSIONS}"
        )

    # Vérification 2: Taille du fichier
    if size > MAX_SIZE_BYTES:
        errors.append(f"Fichier trop volumineux: {size} bytes (max: {MAX_SIZE_BYTES})")

    if size == 0:
        warnings.append("Le fichier est vide")

    # Vérification 3: Nom de fichier (pas de caractères spéciaux dangereux)
    filename = key.split("/")[-1]
    dangerous_chars = ["..", "~", "$", "`", "|", ";", "&"]
    for char in dangerous_chars:
        if char in filename:
            errors.append(f"Caractère dangereux '{char}' dans le nom de fichier")

    # Vérification 4: Pas de fichiers cachés
    if filename.startswith("."):
        errors.append("Les fichiers cachés ne sont pas autorisés")

    return {
        "is_valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "checks_performed": [
            "extension_check",
            "size_check",
            "filename_security_check",
            "hidden_file_check",
        ],
    }
