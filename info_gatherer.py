import dns.resolver
import shodan
import requests
import argparse
import whois
import socket
from dotenv import load_dotenv
import os

parser = argparse.ArgumentParser(description="This is a basic information gathering tool.", usage="python3 info_gatherer.py -d example.com -s IP")
parser.add_argument("-d", "--domain", help="Enter the domain name for gathering info.")
parser.add_argument("-s", "--shodan", help="Enter the IP address for shodan search.")

args = parser.parse_args()
domain = args.domain
ip = args.shodan

if not ip:
    response = input("Do you want to perform a shodan search on the given domain? [Y/N]: ").strip().lower()
    if response == 'y':
        ip = socket.gethostbyname(domain)
    else:
        pass
    
if ip:
    print(f"Gathering information for domain: {domain} & IP: {ip}")
else:
    print(f"Gathering information for domain: {domain}")
          
print("Gathering WHOIS info... ")
try:
    d = whois.whois(domain)
    print("[+] WHOIS info found!")

    print(f"Name: {d.domain_name[0]}")
    print(f"Registrar: {d.registrar}")
    print(f"Creation Date: {d.creation_date[0]}")
    print(f"Expiration Date: {d.expiration_date[0]}")
    print(f"Registrant: {d.org}")
    print(f"Registrant Country: {d.country}")
    
except Exception as e:
    print("[-] Could not extract WHOIS info!")
    print(f"Error: {e}")
    
    
print("[+] Gathering DNS info...")

try:
    for a in dns.resolver.resolve(domain, 'A'):
        print(f"[*] A Record: {a.to_text()}")
except:
    print("[-] Could not extract A Records!")

try:
    for ns in dns.resolver.resolve(domain, 'NS'):
        print(f"[*] NS Record: {ns.to_text()}")
except:
    print("[-] Could not extract NS Records!")

try:
    for mx in dns.resolver.resolve(domain, 'MX'):
        print(f"[*] MX Record: {mx.to_text()}")
except:
    print("[-] Could not extract MX Records!")

try:
    for t in dns.resolver.resolve(domain, 'TXT'):
        print(f"[*] TXT Record: {t.to_text()}")
except:
    print("[-] Could not extract TXT Records!")
    
    
print("[+] Gathering geolocation info...")
try:
    response = requests.request('GET', "https://api.ip2location.io/?ip=" + socket.gethostbyname(domain)).json()
    print(f"Country: {response['country_name']}")
    print(f"State: {response['region_name']}")
    print(f"City: {response['city_name']}")
    print(f"Latitude: {response['latitude']}")
    print(f"Longitude: {response['longitude']}")
except:
    print("[-] Could not obtain Geolocation info!")    
    

if ip:
    print(f"[+] Gathering info from Shodan for IP: {ip}...")
    load_dotenv()
    key = os.getenv('SHODAN_API_KEY')
    api = shodan.Shodan(key)
    
    try:
        results = api.host(ip)
        number_of_results = len(results.get('data', []))
        print(f"[+] Number of different results found: {number_of_results}")

        print(f"\n[+] IP: {results.get('ip_str', 'N/A')}")
        print(f"[*] Organization: {results.get('org', 'N/A')}")
        print(f"[*] ISP: {results.get('isp', 'N/A')}")
        print(f"[*] Country: {results.get('country_name', 'N/A')}")
        print(f"[*] City: {results.get('city', 'N/A')}")
        print(f"[*] Ports: {results.get('ports', [])}")

        for index, result in enumerate(results.get('data', []), start=1):
            print(f"\n[+] Result {index}:")
            print(f"IP: {result.get('ip_str', 'N/A')}")
            print(f"Port: {result.get('port', 'N/A')}")
            print(f"Data: \n{result.get('data', 'N/A')}")
            print(f"Hostnames: {result.get('hostnames', [])}")
            print(f"Location: {result.get('location', {})}")
            print("-" * 150)

    except Exception as e:
        print("[-] Shodan search error!")
        print(e)