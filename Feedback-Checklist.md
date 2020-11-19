ASL 2020
Feedback Group 3:
Délèze Alexandre, Gabbud Yann, Meinen Manuel, Pavliv Valentyna
======================================================================

General:
- basic design (in overview) looks fine, but security design is quite 
incomplete and many details remain to be worked out
- please justify your design choices, e.g., by referring to security principles
- you need to improve the report's organization:
  - Sect 1.2 should describe the system's functionality from a user's
    perspective (similar to assignment)
  - most of your Sect 1.2 would better fit into Sect 1.4 (components), 
    as it describes internal interfaces of the components
  - Sect 1.3: I suggest that you do not organize this by server, but 
    by security topic (access control, key management, etc; see template);
    this avoids redundancies like "server A: talks to B using HTTPS" and 
    "server B: talks to A using HTTPS".
- security design should be based on risk analysis; try to make this more
  coherent (e.g., you mention input sanitization in the risk analysis, but 
  not in the security design)

System Characterization/Overview (see also General comments above!):
- [ ] system overview is missing! (high-level description, including 
  explanation of Fig 1)
- [ ] how does web server communicate with core server (TLS?)
- [ ] unclear why different authentication leads to different revocation behavior
- [x] unclear whether backup server connects to DB server (1.2.5) via SFTP or 
  vice versa (1.2.6)
- [x] Sect 1.2.6: are certificates also backed up?
- [x] Sect 1.2.7: description of external FW missing
- [ ] Can a certificate only be downloaded once? (upon generation)

Security Design (see also General comments above!)
- [ ] quite incomplete
- [ ] several of your services (CA, VPN) need root privilege to access 
  private keys or other data. Do some of these services have to run as 
  root? Could this lead to new risks? 
- [ ] 1.3.5: unclear what "only admin can change data from the servers" means
- [x] backup: unclear whether encrypted or authenticated 
- [ ] missing: session management (cookies? other?)
- [ ] missing: security of data at rest (added for Backups but still missing for DB Server)
- [ ] missing: any protection against common web app vulnerabilities?
  (CSRF, XSS, SQL injection, etc.)

Components:
- [x] backups: frequency? automated?


Assets:
- [x] organize into groups: physical, logical, intangible assets (see book)
  (e.g., "web server" appears to refer both to the machine and the service)
- [x] do not describe functionality under assets (e.g., for certificates)
- [x] do list security requirements with each asset
  (access restrictions, integrity, confidentiality)
- [x] missing: security properties for server keys and certificates? 
  users' private keys and certificates? 
- [x] missing asset: CRL
- [x] should software be an asset as well?
- [x] should employees be assets as well?
- [x] any intangible assets?

Threat sources:
- [ ] quite complete list of possible threat sources
- [ ] add nature? (cf. your threat 15); add malware?

Risk definitions:
- [ ] simplistic likelihood and impact definitions (cf. book)
- [ ] impact: you use the classifications secret, confidential, and internal, 
  but the descriptions of the assets does not refer to these
  (e.g., which level is a user's private key?)
  
Risk Analysis:
- [ ] please always indicate the threat source: who (threat source) does what 
  (threat action).
- [ ] web server: security design should take into account countermeasure
  suggested here against common web vulnerabilities
- [ ] threat 7: limit (not verify) number of tries? Why is the risk still 
  medium after applying this countermeasure?
- [ ] threat 10: which private keys? (CA? server? user? admin SSH?)
  Can they all be treated the same way? (location, security, ...)
- [ ] threat 11: this seems to cover users' certificates
- [ ] threat 15: please state which asset is threatened;
  are all your servers in the same room?
  also: who has access to that room?
- [ ] 2.4.6: there is a separate subsection for risk acceptance (2.4.8)
- [ ] 2.4.8: not additional countermeasures, just repeats previous ones
- [ ] many threats seem to be missing, e.g., malware corrupting servers, 
  software vulnerabilities, ...