import collections

# =========================
# Lecture du fichier
# =========================
def lire_logs(nom_fichier):
    logs = []
    with open(nom_fichier, "r") as f:
        for ligne in f:
            ligne = ligne.strip()
            if ligne:
                date, heure, ip, port, protocole, statut = ligne.split(";")
                logs.append({
                    "date": date,
                    "heure": heure,
                    "ip": ip,
                    "port": int(port),
                    "protocole": protocole,
                    "statut": statut
                })
    return logs


# =========================
# Statistiques
# =========================
def calculer_statistiques(logs):
    total = len(logs)
    succes = sum(1 for log in logs if log["statut"] == "SUCCES")
    echec = sum(1 for log in logs if log["statut"] == "ECHEC")

    compteur_ports = collections.Counter(log["port"] for log in logs)
    compteur_ips = collections.Counter(log["ip"] for log in logs)

    port_plus_utilise = compteur_ports.most_common(1)[0][0]
    ip_plus_active = compteur_ips.most_common(1)[0][0]

    return total, succes, echec, compteur_ports, port_plus_utilise, ip_plus_active


# =========================
# Détection IP suspectes
# =========================
def detecter_ips_suspectes(logs):
    echec_par_ip_port = {}

    for log in logs:
        if log["statut"] == "ECHEC":
            cle = (log["ip"], log["port"])
            echec_par_ip_port[cle] = echec_par_ip_port.get(cle, 0) + 1

    ips_suspectes = set()
    for (ip, port), nb in echec_par_ip_port.items():
        if nb > 5:
            ips_suspectes.add(ip)

    return ips_suspectes


# =========================
# Génération du rapport
# =========================
def generer_rapport(nom_fichier, total, succes, echec,
                    compteur_ports, ips_suspectes):
    with open(nom_fichier, "w") as f:
        f.write("===== RAPPORT D'ANALYSE DES LOGS RESEAU =====\n\n")
        f.write(f"Nombre total de connexions : {total}\n")
        f.write(f"Nombre total de succes     : {succes}\n")
        f.write(f"Nombre total d'echecs      : {echec}\n\n")

        f.write("Top 3 des ports les plus utilises :\n")
        for port, nb in compteur_ports.most_common(3):
            f.write(f" - Port {port} : {nb} connexions\n")

        f.write("\nAdresses IP suspectes :\n")
        if ips_suspectes:
            for ip in ips_suspectes:
                f.write(f" - {ip}\n")
        else:
            f.write("Aucune IP suspecte detectee.\n")


# =========================
# Programme principal
# =========================
def main():
    logs = lire_logs("../network_log.txt")

    total, succes, echec, compteur_ports, port_plus_utilise, ip_plus_active = calculer_statistiques(logs)

    ips_suspectes = detecter_ips_suspectes(logs)

    print("===== RESULTATS =====")
    print("Total connexions :", total)
    print("Succes :", succes)
    print("Echecs :", echec)
    print("Port le plus utilise :", port_plus_utilise)
    print("IP la plus active :", ip_plus_active)

    if ips_suspectes:
        print("IP suspectes :", ", ".join(ips_suspectes))
    else:
        print("Aucune IP suspecte detectee.")

    generer_rapport("rapport_analyse.txt", total, succes, echec,
                    compteur_ports, ips_suspectes)


if __name__ == "__main__":
    main()