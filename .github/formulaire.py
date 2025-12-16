import re
import json
import hashlib
from getpass import getpass
from pathlib import Path
from typing import Dict, Optional

USERS_FILE = Path.cwd() / "users.json"


def is_valid_email(email: str) -> bool:
    """Validation simple d'email."""
    return bool(re.match(r"^[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+$", email))


def hash_password(password: str) -> str:
    """Retourne le hash SHA-256 hexadécimal du mot de passe."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def save_user(user: Dict[str, str], filename: Optional[Path] = None) -> None:
    """Ajoute l'utilisateur au fichier JSON (liste d'utilisateurs)."""
    target = filename or USERS_FILE
    data = []
    if target.exists():
        try:
            with target.open("r", encoding="utf-8") as f:
                data = json.load(f)
                if not isinstance(data, list):
                    data = []
        except Exception:
            data = []
    data.append(user)
    with target.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def prompt_nonempty(prompt_text: str) -> str:
    while True:
        val = input(prompt_text).strip()
        if val:
            return val
        print("Valeur obligatoire — réessayer.")


def main() -> None:
    """Formulaire CLI simple : nom, email, mot de passe (haché)."""
    try:
        print("=== Formulaire utilisateur ===")
        nom = prompt_nonempty("Nom complet : ")
        email = prompt_nonempty("Email : ")
        while not is_valid_email(email):
            print("Email invalide — exemple: utilisateur@domaine.tld")
            email = prompt_nonempty("Email : ")

        # Mot de passe (masqué)
        while True:
            pwd = getpass("Mot de passe : ")
            if not pwd:
                print("Mot de passe obligatoire.")
                continue
            pwd2 = getpass("Confirmer le mot de passe : ")
            if pwd != pwd2:
                print("Les mots de passe ne correspondent pas — réessayer.")
                continue
            break

        hashed = hash_password(pwd)
        user = {"nom": nom, "email": email, "password_hash": hashed}

        save_user(user)
        print("Utilisateur enregistré. (mot de passe stocké sous forme de hash)")
        print(f"Email: {email}")
    except KeyboardInterrupt:
        print("\nAnnulé par l'utilisateur.")
    except Exception as e:
        print("Erreur:", e)


if __name__ == "__main__":
    main()