import dns.resolver
import shodan
import requests
import argparse
import whois
import socket
from dotenv import load_dotenv
import os
from termcolor import cprint, colored

def main():
    try:
        parser = argparse.ArgumentParser(description="This is a basic information gathering tool.", usage="python3 info_gatherer.py -d example.com -s IP")
        parser.add_argument("-d", "--domain", help="Enter the domain name for gathering info.", required=True)
        parser.add_argument("-s", "--shodan", help="Enter the IP address for shodan search.")
        parser.add_argument("-o", "--output", help="Enter the file name to write the output.")

        args = parser.parse_args()
        domain = args.domain
        ip = args.shodan
        output = args.output

        if not ip:
            prompt = colored("Do you want to perform a shodan search on the given domain? [Y/N]: ", "magenta")
            response = input(prompt).strip().lower()
            if response == 'y':
                ip = socket.gethostbyname(domain)
            else:
                pass
            
        if ip:
            cprint(f"\nGathering information for domain: {domain} & IP: {ip}\n", "cyan", attrs=["bold"])
        else:
            cprint(f"\nGathering information for domain: {domain}\n", "cyan", attrs=["bold"])
                
        cprint("Gathering WHOIS info... ", "light_green", attrs=["bold"])

        whois_result = ""

        try:
            d = whois.whois(domain)

            whois_result += f"Name: {d.domain_name[0]}" + '\n'
            whois_result += f"Registrar: {d.registrar}" + '\n'
            whois_result += f"Creation Date: {d.creation_date[0]}" + '\n'
            whois_result += f"Expiration Date: {d.expiration_date[0]}" + '\n'
            whois_result += f"Registrant: {d.org}" + '\n'
            whois_result += f"Registrant Country: {d.country}" + '\n'
            
        except Exception as e:
            cprint(f"[-] Could not extract WHOIS info! Error: {e}", "red")
            
            
        print(whois_result)
        
        cprint("[+] Gathering DNS info...", "light_green", attrs=["bold"])

        dns_result = ''

        try:
            for a in dns.resolver.resolve(domain, 'A'):
                dns_result += f"[*] A Record: {a.to_text()}" + '\n'
        except:
            cprint("[-] Could not extract A Records!", "red")

        try:
            for ns in dns.resolver.resolve(domain, 'NS'):
                dns_result += f"[*] NS Record: {ns.to_text()}" + '\n'
        except:
            cprint("[-] Could not extract NS Records!", "red")

        try:
            for mx in dns.resolver.resolve(domain, 'MX'):
                dns_result += f"[*] MX Record: {mx.to_text()}" + '\n'
        except:
            cprint("[-] Could not extract MX Records!", "red")

        try:
            for t in dns.resolver.resolve(domain, 'TXT'):
                dns_result += f"[*] TXT Record: {t.to_text()}" + '\n'
        except:
            cprint("[-] Could not extract TXT Records!", "red")
            
        print(dns_result)
            
            
            
        cprint("[+] Gathering geolocation info...", "light_green", attrs=["bold"])

        geo_result = ""

        try:
            response = requests.request('GET', "https://api.ip2location.io/?ip=" + socket.gethostbyname(domain)).json()
            geo_result += f"[*] Country: {response['country_name']}" + '\n'
            geo_result += f"[*] State: {response['region_name']}" + '\n'
            geo_result += f"[*] City: {response['city_name']}" + '\n'
            geo_result += f"[*] Latitude: {response['latitude']}" + '\n'
            geo_result += f"[*] Longitude: {response['longitude']}" + '\n'
        except:
            cprint("[-] Could not obtain Geolocation info!", "red")    
            
        print(geo_result)

            
        shodan_result = ""

        if ip:
            cprint(f"[+] Gathering info from Shodan for IP: {ip}...", "light_green", attrs=["bold"])
            load_dotenv()
            key = os.getenv('SHODAN_API_KEY')
            api = shodan.Shodan(key)
            
            try:
                results = api.host(ip)
                number_of_results = len(results.get('data', []))
                shodan_result += f"[+] Number of different results found: {number_of_results}" + '\n'

                shodan_result += f"\n[+] IP: {results.get('ip_str', 'N/A')}" + '\n'
                shodan_result += f"[*] Organization: {results.get('org', 'N/A')}" + '\n'
                shodan_result += f"[*] ISP: {results.get('isp', 'N/A')}" + '\n'
                shodan_result += f"[*] Country: {results.get('country_name', 'N/A')}" + '\n'
                shodan_result += f"[*] City: {results.get('city', 'N/A')}" + '\n'
                shodan_result += f"[*] Ports: {results.get('ports', [])}" + '\n'

                for index, result in enumerate(results.get('data', []), start=1):
                    shodan_result += f"\n[+] Result {index}:" + '\n'
                    shodan_result += f"IP: {result.get('ip_str', 'N/A')}" + '\n'
                    shodan_result += f"Port: {result.get('port', 'N/A')}" + '\n'
                    shodan_result += f"Data: \n{result.get('data', 'N/A')}" + '\n'
                    shodan_result += f"Hostnames: {result.get('hostnames', [])}" + '\n'
                    shodan_result += f"Location: {result.get('location', {})}" + '\n'
                    shodan_result += "-" * 150 + '\n'

            except Exception as e:
                cprint("[-] Shodan search error!", "red")
                print(e)
                
            print(shodan_result)
            
        if (output):
            with open(output, 'w') as file:
                file.write("WHOIS Info:\n" + whois_result + '\n' + '*'*30 + '\n\n')
                file.write("DNS Info:\n" + dns_result + '\n' + '*'*30 + '\n\n')
                file.write("Geolocation Info:\n" + geo_result + '\n' + '*'*30 + '\n\n')
                file.write("Shodan Info:\n" + shodan_result + '\n' + '*'*30 + '\n')
    except KeyboardInterrupt:
        cprint("Exiting...", "red", attrs=["bold"])
        exit(0)
        
main()