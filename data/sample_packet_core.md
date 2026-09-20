# Sample domain documentation (synthetic, for demo)

## Packet Core Overview
The packet core handles UE attach, session management, and user-plane forwarding.

## Example Procedure: UE Attach
1. UE sends Attach Request
2. MME/AMF authenticates the subscriber
3. Session is established toward SGW/SMF and PGW/UPF
4. Default bearer / PDU session is activated

## Configuration Snippet (YAML, illustrative)
amf:
  name: amf-1
  plmn: "25001"
  guami: "a1b2c3"
