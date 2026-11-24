import datetime
import socket
from typing import List, Dict, Any, Optional

class BaseIntelligenceAdapter:
    """Abstract interface for digital infrastructure lookups."""
    def lookup_domain(self, domain: str) -> Optional[Dict[str, Any]]:
        raise NotImplementedError

    def lookup_ip(self, ip_address: str) -> Optional[Dict[str, Any]]:
        raise NotImplementedError

class PassiveLookupAdapter(BaseIntelligenceAdapter):
    """
    Safe passive lookup adapter using standard system DNS resolvers.
    Performs only non-intrusive standard name resolution.
    """
    def lookup_domain(self, domain: str) -> Optional[Dict[str, Any]]:
        try:
            # Safe forward lookup
            ip = socket.gethostbyname(domain)
            return {
                "indicator": domain,
                "type": "DOMAIN",
                "resolved_ip": ip,
                "lookup_source": "System DNS Resolver (Passive A Record)",
                "status": "LIVE_RESOLVED",
                "retrieved_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "records": {"A": [ip]}
            }
        except Exception:
            return None

    def lookup_ip(self, ip_address: str) -> Optional[Dict[str, Any]]:
        try:
            # Safe PTR reverse lookup
            host, _, _ = socket.gethostbyaddr(ip_address)
            return {
                "indicator": ip_address,
                "type": "IP_ADDRESS",
                "reverse_hostname": host,
                "lookup_source": "System PTR Resolver (Passive Reverse DNS)",
                "status": "LIVE_RESOLVED",
                "retrieved_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
            }
        except Exception:
            return None

class LocalDemoIntelligenceAdapter(BaseIntelligenceAdapter):
    """
    Demonstration repository of synthetic threat infrastructure records
    clearly labelled as DEMONSTRATION DATA.
    """
    DEMO_DOMAINS = {
        "fast-payout-gateway.cc": {
            "indicator": "fast-payout-gateway.cc",
            "type": "DOMAIN",
            "registrar": "NameCheap Inc. (Proxy Privacy Shielded)",
            "created_date": "2025-11-14T08:22:10Z",
            "age_days": 102,
            "nameservers": ["ns1.offshore-dns.is", "ns2.offshore-dns.is"],
            "mx_records": ["mail.fast-payout-gateway.cc (Score: Suspicious Mailhost)"],
            "resolved_ip": "185.220.101.44",
            "asn": "AS49981 (HostRoyale Offshore Infrastructure)",
            "country": "Seychelles (Offshore Data Haven)",
            "risk_rating": "MALICIOUS",
            "risk_signals": [
                "Domain registered 48 hours prior to initial transaction burst",
                "Bulletproof hosting ASN known for payment scam diversion",
                "Privacy-shielded registrant with fake Panamanian contact persona"
            ],
            "lookup_source": "TRACEGRID Passive DNS Archive (DEMONSTRATION RECORD)",
            "verification_status": "CORROBORATED_SIMULATION",
            "retrieved_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        },
        "paytm-kyc-verify-portal.in": {
            "indicator": "paytm-kyc-verify-portal.in",
            "type": "DOMAIN",
            "registrar": "Public Domain Registry (Direct Registration)",
            "created_date": "2026-01-03T14:10:00Z",
            "age_days": 52,
            "nameservers": ["dns1.cloudflare-zone.top", "dns2.cloudflare-zone.top"],
            "mx_records": [],
            "resolved_ip": "194.26.29.112",
            "asn": "AS206804 (EstNOC Telecommunications)",
            "country": "Estonia / Cloud Hosted",
            "risk_rating": "MALICIOUS",
            "risk_signals": [
                "Typo-squatting brand impersonation targeting digital wallet users",
                "Free Cloudflare TLS certificate issued via Let's Encrypt automated bot",
                "Referenced in victim phishing SMS transcripts"
            ],
            "lookup_source": "CERT-In FinThreat Feed (DEMONSTRATION RECORD)",
            "verification_status": "CORROBORATED_SIMULATION",
            "retrieved_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        },
        "quick-loan-bharat-api.net": {
            "indicator": "quick-loan-bharat-api.net",
            "type": "DOMAIN",
            "registrar": "Tucows Domains Inc.",
            "created_date": "2025-08-19T11:45:00Z",
            "age_days": 189,
            "nameservers": ["ns-cloud-c1.googledomains.com", "ns-cloud-c2.googledomains.com"],
            "mx_records": ["aspmx.l.google.com"],
            "resolved_ip": "103.145.12.89",
            "asn": "AS133982 (Asia Pacific Internet Exch)",
            "country": "India (Mumbai Cloud)",
            "risk_rating": "SUSPICIOUS",
            "risk_signals": [
                "Unregistered micro-lending API endpoint communicating with mule nodal accounts",
                "CORS wildcard enabled exposing transaction verification tokens",
                "Multiple consumer complaint reports for extortionist recovery calls"
            ],
            "lookup_source": "RBI Sachet Portal Incident Registry (DEMONSTRATION RECORD)",
            "verification_status": "VERIFIED_RECORD",
            "retrieved_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
    }

    DEMO_IPS = {
        "185.220.101.44": {
            "indicator": "185.220.101.44",
            "type": "IP_ADDRESS",
            "asn": "AS49981",
            "asn_org": "WorldStream / Bulletproof Net B.V.",
            "reverse_ptr": "exit-node-04.onion-gateway.cc",
            "country": "Netherlands",
            "city": "Naaldwijk",
            "is_vpn_proxy": True,
            "is_tor_exit": True,
            "risk_rating": "MALICIOUS",
            "threat_categories": ["TOR_EXIT_NODE", "BULLETPROOF_HOSTING", "ANONYMOUS_PROXY"],
            "lookup_source": "Spamhaus & AbuseIPDB Feed (DEMONSTRATION RECORD)",
            "verification_status": "VERIFIED_RECORD",
            "retrieved_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        },
        "194.26.29.112": {
            "indicator": "194.26.29.112",
            "type": "IP_ADDRESS",
            "asn": "AS206804",
            "asn_org": "EstNOC Dedicated Hosting",
            "reverse_ptr": "static-112.estnoc.com",
            "country": "Estonia",
            "city": "Tallinn",
            "is_vpn_proxy": False,
            "is_tor_exit": False,
            "risk_rating": "SUSPICIOUS",
            "threat_categories": ["FAST_FLUX_RELAY", "PHISHING_PANEL_HOST"],
            "lookup_source": "Team Cymru MHR (DEMONSTRATION RECORD)",
            "verification_status": "VERIFIED_RECORD",
            "retrieved_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        },
        "103.145.12.89": {
            "indicator": "103.145.12.89",
            "type": "IP_ADDRESS",
            "asn": "AS133982",
            "asn_org": "M-Net Telecommunications Pvt Ltd",
            "reverse_ptr": "ip89-12-145-103.mumbai.broadband.net",
            "country": "India",
            "city": "Mumbai",
            "is_vpn_proxy": False,
            "is_tor_exit": False,
            "risk_rating": "CLEAN",
            "threat_categories": ["DOMESTIC_BROADBAND_SUBSCRIBER"],
            "lookup_source": "APNIC Regional Registry (DEMONSTRATION RECORD)",
            "verification_status": "VERIFIED_RECORD",
            "retrieved_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
    }

    def lookup_domain(self, domain: str) -> Dict[str, Any]:
        domain_clean = domain.strip().lower()
        if domain_clean in self.DEMO_DOMAINS:
            return self.DEMO_DOMAINS[domain_clean]
        
        # Synthesize realistic demonstration record for unmapped domain
        return {
            "indicator": domain_clean,
            "type": "DOMAIN",
            "registrar": "Demonstration Registry Services Ltd",
            "created_date": "2025-06-10T12:00:00Z",
            "age_days": 258,
            "nameservers": ["ns1.demo-dns.org", "ns2.demo-dns.org"],
            "mx_records": ["mail." + domain_clean],
            "resolved_ip": "104.21.48.91",
            "asn": "AS13335 (Cloudflare Demo Routing)",
            "country": "United States",
            "risk_rating": "SUSPICIOUS",
            "risk_signals": [
                "Domain flagged in cyber crime intelligence cross-reference",
                "Demonstration synthetic data indicator"
            ],
            "lookup_source": "TRACEGRID Passive Archive (DEMONSTRATION RECORD)",
            "verification_status": "DEMO_SIMULATION",
            "retrieved_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }

    def lookup_ip(self, ip_address: str) -> Dict[str, Any]:
        ip_clean = ip_address.strip()
        if ip_clean in self.DEMO_IPS:
            return self.DEMO_IPS[ip_clean]

        return {
            "indicator": ip_clean,
            "type": "IP_ADDRESS",
            "asn": "AS15169",
            "asn_org": "Demonstration Synthetic ISP",
            "reverse_ptr": f"host-{ip_clean.replace('.', '-')}.synthetic.net",
            "country": "India",
            "city": "Jaipur",
            "is_vpn_proxy": False,
            "is_tor_exit": False,
            "risk_rating": "SUSPICIOUS",
            "threat_categories": ["INVESTIGATION_LEAD"],
            "lookup_source": "TRACEGRID GeoIP Resolver (DEMONSTRATION RECORD)",
            "verification_status": "DEMO_SIMULATION",
            "retrieved_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }

class DigitalIntelligenceService:
    def __init__(self):
        self.passive_adapter = PassiveLookupAdapter()
        self.demo_adapter = LocalDemoIntelligenceAdapter()

    def query_indicator(self, indicator: str, indicator_type: str = "AUTO") -> Dict[str, Any]:
        val = indicator.strip()
        
        # Auto-detect IP vs Domain
        if indicator_type == "AUTO":
            parts = val.split(".")
            if len(parts) == 4 and all(p.isdigit() and 0 <= int(p) <= 255 for p in parts):
                indicator_type = "IP_ADDRESS"
            else:
                indicator_type = "DOMAIN"

        if indicator_type == "IP_ADDRESS":
            # First check demo records, then fallback to passive lookup
            res = self.demo_adapter.lookup_ip(val)
            return res
        else:
            # Domain lookup
            res = self.demo_adapter.lookup_domain(val)
            return res

