# Info Gatherer

**Info Gatherer** is a comprehensive information-gathering tool designed to extract and analyze information about domains and IP addresses. This script leverages various APIs and services to collect WHOIS data, DNS records, geolocation information, and Shodan search results.

## Features

- **WHOIS Lookup:** Retrieves domain registration details such as the registrar, creation, and expiration dates.
- **DNS Records:** Collects DNS records including A, NS, MX, and TXT records.
- **Geolocation Information:** Uses IP geolocation services to determine the geographical location of a domain.
- **Shodan Integration:** Searches for information about an IP address using the Shodan API, including ports, hostnames, and data.

## Prerequisites

- Python 3.x
- Required libraries: dns.resolver, shodan, requests, argparse, whois, socket, dotenv, termcolor
- A valid Shodan API key (for Shodan functionality)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/JayGaba/Information_Gatherer.git
   ```

3. Navigate to the project directory:
   ```
   cd Information_Gatherer
   ```

5. Install the required libraries:
   ```
   pip install -r requirements.txt
   ```

7. Set up your environment variables. Create a .env file in the project directory and add your Shodan API key:
   ```
   SHODAN_API_KEY=your_shodan_api_key
   ```

## Usage

To run the script, use the following command:
   ```
   python info_gatherer.py -d example.com -s IP_ADDRESS -o output.txt
   ```

### Arguments

- -d, --domain : Domain name for gathering information (required)
- -s, --shodan : IP address for Shodan search (optional). If not provided, you will be prompted to use the domain's IP.
- -o, --output : File name to write the output (optional)

### Example
   ```
   python info_gatherer.py -d example.com -s 192.168.1.1 -o results.txt
   ```

## Future Scope

- **Multiple Domain/IP Handling:** Extend functionality to handle and process multiple domains or IP addresses in a single run.
- **Interactive Mode:** Implement an interactive mode to allow users to dynamically select options and configure searches.
- **More Structured Code:** Refactor code to improve readability and maintainability, possibly by breaking it into modules or classes.
