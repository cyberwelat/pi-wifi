import subprocess

def get_wireless_interface():
    result = subprocess.run(["nmcli", "-t", "-f", "DEVICE,TYPE", "device"],
                            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    output = result.stdout.decode()
    for line in output.splitlines():
        if ":wifi" in line:
            return line.split(":")[0]
    return None

def scan_wifi_networks(interface):
    print("[*] Ağlar taranıyor...\n")
    subprocess.run(["nmcli", "device", "wifi", "rescan"], stdout=subprocess.DEVNULL)
    result = subprocess.run(["nmcli", "-f", "SSID,SIGNAL,SECURITY", "device", "wifi", "list", "ifname", interface],
                            stdout=subprocess.PIPE)
    output = result.stdout.decode().strip().splitlines()
    networks = [line.strip() for line in output[1:] if line.strip()]
    return networks

def connect_to_wifi(ssid, password):
    subprocess.run(["nmcli", "connection", "delete", ssid], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    result = subprocess.run(
        ["nmcli", "dev", "wifi", "connect", ssid, "password", password],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    if result.returncode == 0:
        print(f"[+] '{ssid}' ağına başarıyla bağlanıldı!")
        return True
    else:
        print("[-] Bağlantı başarısız:")
        print(result.stderr.decode())
        return False

if __name__ == "__main__":
    interface = get_wireless_interface()
    if not interface:
        print("[-] Kablosuz ağ arayüzü bulunamadı.")
        exit(1)

    print(f"[✓] Kablosuz arayüz: {interface}")

    networks = scan_wifi_networks(interface)
    if not networks:
        print("[-] Hiçbir Wi-Fi ağı bulunamadı.")
        exit(1)

    print("\n📶 Bulunan Wi-Fi Ağları:")
    for i, net in enumerate(networks):
        print(f"  {i + 1}) {net}")

    try:
        choice = int(input("\n🔢 Bağlanmak istediğiniz ağı seçin (numara): ")) - 1
        ssid = networks[choice].split()[0]
    except (IndexError, ValueError):
        print("[-] Geçersiz seçim.")
        exit(1)

    password = input(f"🔑 '{ssid}' ağı için şifre: ")
    connect_to_wifi(ssid, password)
