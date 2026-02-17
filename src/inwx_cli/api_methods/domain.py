# inwx_cli/api_methods/domain.py

import argparse


"""
Domain API Methods for INWX
Based on official DomRobot API documentation:
https://www.inwx.com/en/help/apidoc/f/ch02s09.html

Domain API Methods for INWX.
Contains:
  domain.check              Prüft die Verfügbarkeit von Domains
  domain.create             Domain registrieren / anlegen
  domain.delete             Domain löschen
  domain.getalldomainprices Preise für alle Domains abrufen
  domain.getdomainprice     Preis für eine bestimmte Domain abrufen
  domain.getextradatarules  Regeln für Domain-Extra-Daten abrufen
  domain.getPrices          Domainpreise abrufen
  domain.getPromos          Aktuelle Promotions abrufen
  domain.getRules           Regeln für TLDs abrufen
  domain.getTldGroups       TLD-Gruppen abrufen
  domain.info               Details einer Domain abfragen
  domain.list               Domains auflisten
  domain.log                Logeinträge zu Domains abrufen
  domain.priceChanges       Preisänderungen abrufen
  domain.push               Domain zu einem anderen Registrar übertragen
  domain.removeClientHold   ClientHold aufheben
  domain.renew              Domain verlängern / renew
  domain.restore            Domain wiederherstellen
  domain.setClientHold      ClientHold setzen
  domain.stats              Statistiken zu Domains abrufen
  domain.trade              Domain auf einen anderen Besitzer übertragen
  domain.transfer           Domain übertragen (INWX Transfer)
  domain.transfercancel     Domain-Transfer stornieren
  domain.transferOut        Domain-Transfer bestätigen oder ablehnen
  domain.update             Domain aktualisieren
  domain.whois              Whois-Informationen einer Domain abrufen
"""


def parse_bool(value: str) -> bool:
    value = value.lower()
    if value in ("true", "1", "yes", "y", "t", "on"):
        return True
    if value in ("false", "0", "no", "n", "f", "off"):
        return False
    raise argparse.ArgumentTypeError(
        f"invalid boolean value: '{value}' (use true/false)"
    )


# -----------------------------
# API Method Definitions
# -----------------------------
METHODS = {
    "domain.check": {
        "params": {
            "domain": {"type": str, "help": "Domain names to check", "nargs": "+"},
            "sld": {"type": str, "help": "Second level domain name"},
            "tld": {"type": str, "help": "Top level domains", "nargs": "+"},
            "region": {"type": str, "help": "Check region TLD groups", "nargs": "+"},
            "wide": {"type": int, "help": "More detailed output"},
        }
    },
    "domain.create": {
        "params": {
            "domain": {"type": str, "help": "Domain name", "required": True},
            "period": {"type": str, "help": "Renewal period"},
            "registrant": {"type": int, "help": "Registrant contact handle id", "required": True},
            "admin": {"type": int, "help": "Admin contact handle id"},
            "tech": {"type": int, "help": "Tech contact handle id"},
            "billing": {"type": int, "help": "Billing contact handle id"},
            "ns": {"type": str, "help": "List of nameservers", "nargs": "+"},
            "transferLock": {"action": "store_true", "dest": "transferLock", "help": "Lock domain"},
            "renewalMode": {"type": str, "dest": "renewalMode", "help": "Domain renewal mode"},
            "whoisProvider": {"type": str, "dest": "whoisProvider", "help": "Whois provider"},
            "whoisUrl": {"type": str, "dest": "whoisUrl", "help": "Whois URL"},
            "scDate": {"type": str, "dest": "scDate", "help": "Scheduled execution date"},
            "extData": {"type": str, "dest": "extData", "help": "Extra domain data"},
            "asynchron": {"action": "store_true", "help": "Asynchronous execution"},
            "voucher": {"type": str, "help": "Voucher code"},
            "testing": {"action": "store_true", "help": "Testing mode"},
        }
    },
    "domain.delete": {
        "params": {
            "domain": {"type": str, "help": "Domain name", "required": True},
            "scDate": {"type": str, "dest": "scDate", "help": "Scheduled execution date"},
            "testing": {"action": "store_true", "help": "Testing mode"},
        }
    },
    "domain.getalldomainprices": {
        "params": {
            "domain": {"type": str, "help": "Domain name(s)", "nargs": "+"},
            "period": {"type": str, "help": "Period to fetch prices for"},
            "voucher": {"type": str, "help": "Voucher code"},
        }
    },
    "domain.getdomainprice": {
        "params": {
            "domain": {"type": str, "help": "Domain name(s)", "nargs": "+"},
            "pricetype": {"type": str, "help": "Price type (reg|renewal|transfer|update|trade)", "required": True},
            "period": {"type": str, "help": "Period for price"},
            "voucher": {"type": str, "help": "Voucher code"},
        }
    },
    "domain.getextradatarules": {
        "params": {
            "tld": {"type": str, "help": "TLD to fetch extra data rules for", "nargs": "+"},
        }
    },
    "domain.getPrices": {
        "params": {
            "tld": {"type": str, "help": "Top level domains", "nargs": "+"},
            "vat": {"action": "store_true", "help": "Include VAT"},
            "vatCC": {"type": str, "dest": "vatCC", "help": "Country code for VAT"},
            "voucher": {"type": str, "help": "Voucher code"},
            "page": {"type": int, "help": "Page number"},
            "pagelimit": {"type": int, "help": "Max results"},
        }
    },
    "domain.getPromos": {
        "params": {
            "tlds": {"type": str, "help": "Specific TLDs to check promos", "nargs": "+"},
            "promoType": {"type": str, "dest": "promoType", "help": "Promo type (e.g. REG|RENEWAL)"},
            "period": {"type": int, "help": "Promotion period"},
            "periodUnit": {"type": str, "dest": "periodUnit", "help": "Period unit (Y/M etc.)"},
            "executionDate": {"type": str, "dest": "executionDate", "help": "Promo execution date"},
            "voucher": {"type": str, "help": "Voucher code"},
        }
    },
    "domain.getRules": {
        "params": {
            "tld": {"type": str, "help": "TLD name(s)", "nargs": "+"},
        }
    },
    "domain.getTldGroups": {
        "params": {
            "tld": {"type": str, "help": "TLD name(s)", "nargs": "+"},
        }
    },
    "domain.info": {
        "params": {
            "domain": {"type": str, "help": "Domain name"},
            "roId": {"type": str, "dest": "roId", "help": "Repository Object ID"},
            "wide": {"type": int, "help": "More detailed output"},
        }
    },
    "domain.list": {
        "params": {
            "domain": {"type": str, "help": "Filter by domain name"},
            "roId": {"type": str, "dest": "roId", "help": "Filter by domain id"},
            "status": {"type": str, "help": "Filter by status"},
            "registrant": {"type": int, "help": "Filter by registrant id"},
            "admin": {"type": int, "help": "Filter by admin id"},
            "tech": {"type": int, "help": "Filter by tech id"},
            "billing": {"type": int, "help": "Filter by billing id"},
            "renewalMode": {"type": str, "dest": "renewalMode", "help": "Filter by renewal mode"},
            "transferLock": {"action": argparse.BooleanOptionalAction, "dest": "transferLock",
                             "help": "Filter by transfer lock status"},
            "noDelegation": {"type": parse_bool, "dest": "noDelegation", "metavar": "{true, false}",
                             "help": "Filter by delegation status"},
            "tag": {"type": int, "help": "Filter by tag ids"},
            "wide": {"type": int, "help": "More detailed output"},
            "order": {"type": str, "help": "Sort order"},
            "page": {"type": int, "help": "Page number"},
            "pagelimit": {"type": int, "help": "Max results"},
            "withPrivacy": {"type": int, "dest": "withPrivacy", "help": "Filter by privacy flag"},
        }
    },
    "domain.log": {
        "params": {
            "domain": {"type": str, "help": "Filter result by domain name"},
            "status": {"type": str, "help": "Filter by status"},
            "invoice": {"type": str, "help": "Filter by invoice id"},
            "dateFrom": {"type": str, "dest": "dateFrom", "help": "Filter by start date"},
            "dateTo": {"type": str, "dest": "dateTo", "help": "Filter by end date"},
            "priceMin": {"type": float, "dest": "priceMin", "help": "Minimum price"},
            "priceMax": {"type": float, "dest": "priceMax", "help": "Maximum price"},
            "order": {"type": str, "help": "Ordering of results"},
            "page": {"type": int, "help": "Page number"},
            "pagelimit": {"type": int, "help": "Max results"},
        }
    },
    "domain.priceChanges": {
        "params": {}
    },
    "domain.push": {
        "params": {
            "domain": {"type": str, "help": "Domain name", "required": True},
            "target": {"type": str, "help": "Target registrar"},
            "scDate": {"type": str, "dest": "scDate", "help": "Scheduled date"},
            "testing": {"action": "store_true", "help": "Testing mode"},
        }
    },
    "domain.removeClientHold": {
        "params": {
            "domain": {"type": str, "help": "Domain name", "required": True},
            "testing": {"action": "store_true", "help": "Testing mode"},
        }
    },
    "domain.renew": {
        "params": {
            "domain": {"type": str, "help": "Domain name", "required": True},
            "period": {"type": str, "help": "Renewal period", "required": True},
            "expiration": {"type": str, "help": "Current expiration date", "required": True},
            "asynchron": {"action": "store_true", "help": "Async execution"},
            "testing": {"action": "store_true", "help": "Testing mode"},
        }
    },
    "domain.restore": {
        "params": {
            "domain": {"type": str, "help": "Domain name", "required": True},
            "renewalMode": {"type": str, "dest": "renewalMode", "help": "Domain renewal mode"},
            "testing": {"action": "store_true", "help": "Testing mode"},
        }
    },
    "domain.setClientHold": {
        "params": {
            "domain": {"type": str, "help": "Domain name", "required": True},
            "testing": {"action": "store_true", "help": "Testing mode"},
        }
    },
    "domain.stats": {
        "params": {}
    },
    "domain.trade": {
        "params": {
            "domain": {"type": str, "help": "Domain name", "required": True},
            "registrant": {"type": int, "help": "New owner contact handle id", "required": True},
            "admin": {"type": int, "help": "New admin id"},
            "tech": {"type": int, "help": "New tech id"},
            "billing": {"type": int, "help": "New billing id"},
            "ns": {"type": str, "help": "Nameservers", "nargs": "+"},
            "authCode": {"type": str, "dest": "authCode", "help": "Authorization code"},
            "whoisProvider": {"type": str, "dest": "whoisProvider", "help": "Whois provider"},
            "whoisUrl": {"type": str, "dest": "whoisUrl", "help": "Whois url"},
            "scDate": {"type": str, "dest": "scDate", "help": "Scheduled date"},
            "extData": {"type": str, "dest": "extData", "help": "Extra domain data"},
            "asynchron": {"action": "store_true", "help": "Async mode"},
            "testing": {"action": "store_true", "help": "Testing mode"},
        }
    },
    "domain.transfer": {
        "params": {
            "domain": {"type": str, "help": "Domain name", "required": True},
            "registrant": {"type": int, "help": "Owner contact"},
            "admin": {"type": int, "help": "Admin contact"},
            "tech": {"type": int, "help": "Tech contact"},
            "billing": {"type": int, "help": "Billing contact"},
            "ns": {"type": str, "help": "Nameservers", "nargs": "+"},
            "nsTakeover": {"action": "store_true", "dest": "nsTakeover", "help": "Keep existing nameservers"},
            "contactTakeover": {"action": "store_true", "dest": "contactTakeover",
                                "help": "Transfer contact data"},
            "transferLock": {"action": "store_true", "dest": "transferLock", "help": "Domain lock"},
            "authCode": {"type": str, "dest": "authCode", "help": "Authorization code"},
            "renewalMode": {"type": str, "dest": "renewalMode", "help": "Renewal mode"},
            "whoisProvider": {"type": str, "dest": "whoisProvider", "help": "Whois provider"},
            "whoisUrl": {"type": str, "dest": "whoisUrl", "help": "Whois url"},
            "extData": {"type": str, "dest": "extData", "help": "Extra domain data"},
            "scDate": {"type": str, "dest": "scDate", "help": "Scheduled date"},
            "asynchron": {"action": "store_true", "help": "Async mode"},
            "voucher": {"type": str, "help": "Voucher code"},
            "testing": {"action": "store_true", "help": "Testing mode"},
        }
    },
    "domain.transfercancel": {
        "params": {
            "domain": {"type": str, "help": "Domain name", "required": True},
        }
    },
    "domain.transferOut": {
        "params": {
            "domain": {"type": str, "help": "Domain name", "required": True},
            "answer": {"type": str, "help": "Acknowledge or deny transfer", "required": True},
            "testing": {"action": "store_true", "help": "Testing mode"},
        }
    },
    "domain.update": {
        "params": {
            "domain": {"type": str, "help": "Domain name", "required": True},
            "registrant": {"type": int, "help": "Owner contact handle id"},
            "admin": {"type": int, "help": "Admin handle id"},
            "tech": {"type": int, "help": "Tech handle id"},
            "billing": {"type": int, "help": "Billing handle id"},
            "ns": {"type": str, "help": "Nameservers", "nargs": "+"},
            "transferLock": {"action": "store_true", "dest": "transferLock", "help": "Domain lock"},
            "period": {"type": str, "help": "Registration/renewal period"},
            "authCode": {"type": str, "dest": "authCode", "help": "Authorization code"},
            "scDate": {"type": str, "dest": "scDate", "help": "Scheduled date"},
            "renewalMode": {"type": str, "dest": "renewalMode", "help": "Renewal mode"},
            "transferMode": {"type": str, "dest": "transferMode", "help": "Transfer mode"},
            "whoisProvider": {"type": str, "dest": "whoisProvider", "help": "Whois provider"},
            "whoisUrl": {"type": str, "dest": "whoisUrl", "help": "Whois url"},
            "extData": {"type": str, "dest": "extData", "help": "Extra domain data"},
            "asynchron": {"action": "store_true", "help": "Async mode"},
            "testing": {"action": "store_true", "help": "Testing mode"},
        }
    },
    "domain.whois": {
        "params": {
            "domain": {"type": str, "help": "Domain name", "required": True},
        }
    },
}
