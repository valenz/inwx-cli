# inwx_cli/api_methods/nameserver.py

"""
Domain API Methods for INWX
Based on official DomRobot API documentation:
https://account.inwx.de/de/help/apidoc/f/ch02s15.html

Nameserver API Methods for INWX.
Contains:
  nameserver.check          Prüft Nameserver‑Antworten
  nameserver.clone          DNS‑Daten von einer Domain auf eine andere kopieren
  nameserver.create         Nameserver‑Domain anlegen
  nameserver.createRecord   Neuen DNS‑Record anlegen
  nameserver.delete         Nameserver‑Domain löschen
  nameserver.deleteRecord   DNS‑Record löschen
  nameserver.export         Nameserver‑Zone exportieren
  nameserver.exportlist     Liste der Nameserver‑Domains exportieren
  nameserver.exportrecords  Nameserver‑Records exportieren
  nameserver.info           Details einer Nameserver‑Domain abfragen
  nameserver.list           Nameserver‑Domains auflisten
  nameserver.update         Nameserver‑Domain aktualisieren
  nameserver.updateRecord   DNS‑Record aktualisieren
"""


# -----------------------------
# API Method Definitions
# -----------------------------
METHODS = {
    "nameserver.check": {
        "params": {
            "domain": {"type": str, "help": "Domain name", "required": True},
            "ns": {"type": str, "help": "Nameserver list", "nargs": "+", "required": True},
        }
    },
    "nameserver.clone": {
        "params": {
            "sourceDomain": {"type": str, "help": "Source domain", "required": True},
            "targetDomain": {"type": str, "help": "Target domain", "required": True},
        }
    },
    "nameserver.create": {
        "params": {
            "domain": {"type": str, "help": "Domain name", "required": True},
            "type": {"type": str, "help": "Type of nameserver entry", "required": True},
            "ns": {"type": str, "help": "Nameserver list", "nargs": "+"},
            "masterIp": {"type": str, "help": "Master IP address"},
            "web": {"type": str, "help": "Web NS entry"},
            "mail": {"type": str, "help": "Mail NS entry"},
            "soaEmail": {"type": str, "help": "SOA email"},
            "urlRedirectType": {"type": str, "help": "URL redirect type"},
            "urlRedirectTitle": {"type": str, "help": "URL redirect title"},
            "urlRedirectDescription": {"type": str, "help": "URL redirect description"},
            "urlRedirectFavIcon": {"type": str, "help": "URL redirect favicon"},
            "urlRedirectKeywords": {"type": str, "help": "URL redirect keywords"},
            "testing": {"type": bool, "help": "Testing mode", "default": False},
            "ignoreExisting": {"type": bool, "help": "Ignore existing", "default": False},
        }
    },
    "nameserver.createRecord": {
        "params": {
            "domain": {"type": str, "help": "Domain name"},
            "roId": {"type": int, "help": "NS domain id"},
            "type": {"type": str, "help": "Record type", "required": True},
            "content": {"type": str, "help": "Record content", "required": True},
            "name": {"type": str, "help": "Record name"},
            "ttl": {"type": int, "help": "TTL"},
            "prio": {"type": int, "help": "Priority"},
            "urlRedirectType": {"type": str, "help": "URL redirect type"},
            "urlRedirectTitle": {"type": str, "help": "URL redirect title"},
            "urlRedirectDescription": {"type": str, "help": "URL redirect description"},
            "urlRedirectFavIcon": {"type": str, "help": "URL redirect favicon"},
            "urlRedirectKeywords": {"type": str, "help": "URL redirect keywords"},
            "urlAppend": {"type": bool, "help": "Append path", "default": False},
            "testing": {"type": bool, "help": "Testing mode", "default": False},
        }
    },
    "nameserver.delete": {
        "params": {
            "domain": {"type": str, "help": "Domain name"},
            "roId": {"type": int, "help": "NS domain id"},
            "testing": {"type": bool, "help": "Testing mode", "default": False},
        }
    },
    "nameserver.deleteRecord": {
        "params": {
            "id": {"type": int, "help": "Record id", "required": True},
            "testing": {"type": bool, "help": "Testing mode", "default": False},
        }
    },
    "nameserver.export": {
        "params": {
            "domain": {"type": str, "help": "Domain name", "required": True},
        }
    },
    "nameserver.exportlist": {
        "params": {
            "format": {"type": str, "help": "Export format"},
            "domain": {"type": str, "help": "Domain name filter"},
            "wide": {"type": int, "help": "Wide output"},
            "page": {"type": int, "help": "Page number"},
            "pagelimit": {"type": int, "help": "Max results"},
        }
    },
    "nameserver.exportrecords": {
        "params": {
            "format": {"type": str, "help": "Export format"},
            "name": {"type": str, "help": "Record name filter"},
            "page": {"type": int, "help": "Page number"},
            "limit": {"type": int, "help": "Limit"},
        }
    },
    "nameserver.info": {
        "params": {
            "domain": {"type": str, "help": "Domain name"},
            "roId": {"type": int, "help": "NS domain id"},
            "recordId": {"type": int, "help": "Record id"},
            "type": {"type": str, "help": "Record type"},
            "name": {"type": str, "help": "Record name"},
            "content": {"type": str, "help": "Record content"},
            "ttl": {"type": int, "help": "TTL"},
            "prio": {"type": int, "help": "Priority"},
        }
    },
    "nameserver.list": {
        "params": {
            "domain": {"type": str, "help": "Domain name filter"},
            "wide": {"type": int, "help": "Wide output"},
            "page": {"type": int, "help": "Page number"},
            "pagelimit": {"type": int, "help": "Max results"},
        }
    },
    "nameserver.update": {
        "params": {
            "domain": {"type": str, "help": "Domain name"},
            "roId": {"type": int, "help": "NS domain id"},
            "type": {"type": str, "help": "Type of NS entry"},
            "masterIp": {"type": str, "help": "Master IP address"},
            "ns": {"type": str, "help": "Nameservers", "nargs": "+"},
            "web": {"type": str, "help": "Web NS entry"},
            "mail": {"type": str, "help": "Mail NS entry"},
            "urlRedirectType": {"type": str, "help": "URL redirect type"},
            "urlRedirectTitle": {"type": str, "help": "URL redirect title"},
            "urlRedirectDescription": {"type": str, "help": "URL redirect description"},
            "urlRedirectFavIcon": {"type": str, "help": "URL redirect favicon"},
            "urlRedirectKeywords": {"type": str, "help": "URL redirect keywords"},
            "testing": {"type": bool, "help": "Testing mode", "default": False},
        }
    },
    "nameserver.updateRecord": {
        "params": {
            "id": {"type": int, "help": "Record id", "required": True},
            "name": {"type": str, "help": "Record name"},
            "type": {"type": str, "help": "Record type"},
            "content": {"type": str, "help": "Record content"},
            "prio": {"type": int, "help": "Priority"},
            "ttl": {"type": int, "help": "TTL"},
            "urlRedirectType": {"type": str, "help": "URL redirect type"},
            "urlRedirectTitle": {"type": str, "help": "URL redirect title"},
            "urlRedirectDescription": {"type": str, "help": "URL redirect description"},
            "urlRedirectFavIcon": {"type": str, "help": "URL redirect favicon"},
            "urlRedirectKeywords": {"type": str, "help": "URL redirect keywords"},
            "urlAppend": {"type": bool, "help": "Append path", "default": False},
            "testing": {"type": bool, "help": "Testing mode", "default": False},
        }
    },
}
