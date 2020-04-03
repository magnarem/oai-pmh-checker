# OAI-PMH utilities

## Open Archives Initiative Protocol for Metadata Harvesting
This repo contains some scripts to verify that a given data
provider repository is up and running and responding the
right way.

## Scripts in this repository
### check-OAI-PMH.py
Uses pyoai library to connect to metadata provider in configuration
and check if we get sane response from the repository

#### Usage:
```
./src/checkOAI-PMH.py -c conf/sites2harvest-local.yml
```

### checkOAISimple.py
This uses standard python requests an urlparse libraries to check
online status for the provider. Check that we can ping and get
HTTP 200 OK Response

#### Usage:
```
./src/checkOAISimple.py -c conf/sites2harvest-local.yml
```

    
## Licenses
GPL 3 or higher for software, Creative Commons BY for documents.
