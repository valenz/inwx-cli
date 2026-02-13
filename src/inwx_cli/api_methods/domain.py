# inwx_cli/api_methods/domain.py

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
            "transferLock": {"type": bool, "help": "Lock domain"},
            "renewalMode": {"type": str, "help": "Domain renewal mode"},
            "whoisProvider": {"type": str, "help": "Whois provider"},
            "whoisUrl": {"type": str, "help": "Whois URL"},
            "scDate": {"type": str, "help": "Scheduled execution date"},
            "extData": {"type": str, "help": "Extra domain data"},
            "asynchron": {"type": bool, "help": "Asynchronous execution"},
            "voucher": {"type": str, "help": "Voucher code"},
            "testing": {"type": bool, "help": "Testing mode"},
        }
    },
    "domain.delete": {
        "params": {
            "domain": {"type": str, "help": "Domain name", "required": True},
            "scDate": {"type": str, "help": "Scheduled execution date"},
            "testing": {"type": bool, "help": "Testing mode"},
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
            "vat": {"type": bool, "help": "Include VAT"},
            "vatCC": {"type": str, "help": "Country code for VAT"},
            "voucher": {"type": str, "help": "Voucher code"},
            "page": {"type": int, "help": "Page number"},
            "pagelimit": {"type": int, "help": "Max results"},
        }
    },
    "domain.getPromos": {
        "params": {
            "tlds": {"type": str, "help": "Specific TLDs to check promos", "nargs": "+"},
            "promoType": {"type": str, "help": "Promo type (e.g. REG|RENEWAL)"},
            "period": {"type": int, "help": "Promotion period"},
            "periodUnit": {"type": str, "help": "Period unit (Y/M etc.)"},
            "executionDate": {"type": str, "help": "Promo execution date"},
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
            "roId": {"type": str, "help": "Repository Object ID"},
            "wide": {"type": int, "help": "More detailed output"},
        }
    },
    "domain.list": {
        "params": {
            "domain": {"type": str, "help": "Filter by domain name"},
            "roId": {"type": str, "help": "Domain id"},
            "status": {"type": str, "help": "Filter by status"},
            "registrant": {"type": int, "help": "Registrant id"},
            "admin": {"type": int, "help": "Admin id"},
            "tech": {"type": int, "help": "Tech id"},
            "billing": {"type": int, "help": "Billing id"},
            "renewalMode": {"type": str, "help": "Filter by renewal mode"},
            "transferLock": {"type": bool, "help": "Filter by transfer lock status"},
            "noDelegation": {"type": bool, "help": "Filter by delegation status"},
            "tag": {"type": int, "help": "Filter by tag ids"},
            "wide": {"type": int, "help": "More detailed output"},
            "order": {"type": str, "help": "Sort order"},
            "page": {"type": int, "help": "Page number"},
            "pagelimit": {"type": int, "help": "Max results"},
            "withPrivacy": {"type": int, "help": "Filter by privacy flag"},
        }
    },
    "domain.log": {
        "params": {
            "domain": {"type": str, "help": "Filter result by domain name"},
            "status": {"type": str, "help": "Filter by status"},
            "invoice": {"type": str, "help": "Filter by invoice id"},
            "dateFrom": {"type": str, "help": "Filter by start date"},
            "dateTo": {"type": str, "help": "Filter by end date"},
            "priceMin": {"type": float, "help": "Minimum price"},
            "priceMax": {"type": float, "help": "Maximum price"},
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
            "scDate": {"type": str, "help": "Scheduled date"},
            "testing": {"type": bool, "help": "Testing mode"},
        }
    },
    "domain.removeClientHold": {
        "params": {
            "domain": {"type": str, "help": "Domain name", "required": True},
            "testing": {"type": bool, "help": "Testing mode"},
        }
    },
    "domain.renew": {
        "params": {
            "domain": {"type": str, "help": "Domain name", "required": True},
            "period": {"type": str, "help": "Renewal period", "required": True},
            "expiration": {"type": str, "help": "Current expiration date", "required": True},
            "asynchron": {"type": bool, "help": "Async execution"},
            "testing": {"type": bool, "help": "Testing mode"},
        }
    },
    "domain.restore": {
        "params": {
            "domain": {"type": str, "help": "Domain name", "required": True},
            "renewalMode": {"type": str, "help": "Domain renewal mode"},
            "testing": {"type": bool, "help": "Testing mode"},
        }
    },
    "domain.setClientHold": {
        "params": {
            "domain": {"type": str, "help": "Domain name", "required": True},
            "testing": {"type": bool, "help": "Testing mode"},
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
            "authCode": {"type": str, "help": "Authorization code"},
            "whoisProvider": {"type": str, "help": "Whois provider"},
            "whoisUrl": {"type": str, "help": "Whois url"},
            "scDate": {"type": str, "help": "Scheduled date"},
            "extData": {"type": str, "help": "Extra domain data"},
            "asynchron": {"type": bool, "help": "Async mode"},
            "testing": {"type": bool, "help": "Testing mode"},
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
            "nsTakeover": {"type": bool, "help": "Keep existing nameservers"},
            "contactTakeover": {"type": bool, "help": "Transfer contact data"},
            "transferLock": {"type": bool, "help": "Domain lock"},
            "authCode": {"type": str, "help": "Authorization code"},
            "renewalMode": {"type": str, "help": "Renewal mode"},
            "whoisProvider": {"type": str, "help": "Whois provider"},
            "whoisUrl": {"type": str, "help": "Whois url"},
            "extData": {"type": str, "help": "Extra domain data"},
            "scDate": {"type": str, "help": "Scheduled date"},
            "asynchron": {"type": bool, "help": "Async mode"},
            "voucher": {"type": str, "help": "Voucher code"},
            "testing": {"type": bool, "help": "Testing mode"},
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
            "testing": {"type": bool, "help": "Testing mode"},
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
            "transferLock": {"type": bool, "help": "Domain lock"},
            "period": {"type": str, "help": "Registration/renewal period"},
            "authCode": {"type": str, "help": "Authorization code"},
            "scDate": {"type": str, "help": "Scheduled date"},
            "renewalMode": {"type": str, "help": "Renewal mode"},
            "transferMode": {"type": str, "help": "Transfer mode"},
            "whoisProvider": {"type": str, "help": "Whois provider"},
            "whoisUrl": {"type": str, "help": "Whois url"},
            "extData": {"type": str, "help": "Extra domain data"},
            "asynchron": {"type": bool, "help": "Async mode"},
            "testing": {"type": bool, "help": "Testing mode"},
        }
    },
    "domain.whois": {
        "params": {
            "domain": {"type": str, "help": "Domain name", "required": True},
        }
    },
}
