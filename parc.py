def collecter_machine(machine):
    host = machine["host"]
    nom = machine["nom"]
    storage = StorageManager(db_path=f"metrics_{nom}.db")

    if host is None:
        # --- MACHINE LOCALE (déjà OK en général) ---
        import psutil
        cpu = psutil.cpu_percent(interval=1)
        storage.save("cpu", cpu, "%")
        
        # Pour RAM et Disque locaux, on utilise psutil aussi pour être plus fiable que le bash
        ram = psutil.virtual_memory().percent
        storage.save("ram", ram, "%")
        
        disque = psutil.disk_usage('/').percent
        storage.save("disque", disque, "%")
        print(f"[{nom}] Local - CPU: {cpu}%, RAM: {ram}%, DISQUE: {disque}%")

    else:
        # --- MACHINE DISTANTE (SSH) ---
        print(f"[{nom}] Connexion à {host}...")
        
        # CPU distant plus fiable (moyenne sur 1 seconde via mpstat ou calcul simple)
        # On utilise une commande qui marche à tous les coups :
        cmd_cpu = "grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage}'"
        cpu_str = collecter_distant(host, cmd_cpu)
        
        # RAM distante (sans dépendre du script .sh qui peut manquer)
        cmd_ram = "free | grep Mem | awk '{print $3/$2 * 100.0}'"
        ram_str = collecter_distant(host, cmd_ram)
        
        # DISQUE distant (racine /)
        cmd_disque = "df / | tail -1 | awk '{print $5}' | sed 's/%//'"
        disque_str = collecter_distant(host, cmd_disque)

        try:
            cpu = round(float(cpu_str), 2)
            ram = round(float(ram_str), 2)
            disque = round(float(disque_str), 2)
            
            storage.save("cpu", cpu, "%")
            storage.save("ram", ram, "%")
            storage.save("disque", disque, "%")
            print(f"[{nom}] Distant - CPU: {cpu}%, RAM: {ram}%, DISQUE: {disque}%")
        except Exception as e:
            print(f"[{nom}] Erreur lors de la conversion des données distantes : {e}")
            print(f"Brut reçu -> CPU: {cpu_str}, RAM: {ram_str}, DISK: {disque_str}")
