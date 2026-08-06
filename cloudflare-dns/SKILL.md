---
name: cloudflare-dns
description: Manage Cloudflare DNS records via the Cloudflare API, including listing, adding, updating, and deleting DNS records, as well as querying zone information. This skill must be triggered whenever a user mentions "Cloudflare DNS," "CF DNS," "add DNS record," "delete DNS record," "update DNS," "view DNS records," "cloudflare-dns," or any scenario involving Cloudflare DNS management.
---

# Cloudflare DNS Management

## Environment Setup

### Authentication Configuration

Use an API Token (recommended). Set it in the environment before running any commands:

```bash
export CF_API_TOKEN=<your_token>
```

Optionally, when using multiple accounts:
```bash
export CF_ACCOUNT_ID=<account_id>   # Specify when using multiple accounts
```

Check whether the environment variables are set:
```bash
[ -n "$CF_API_TOKEN" ] && echo "Token: set" || echo "Token: NOT SET"
```

If `CF_API_TOKEN` is not set, tell the user the variable name required and where to create a token:
- API Token: [Create a Cloudflare API Token](https://dash.cloudflare.com/profile/api-tokens) (needs the `Zone.DNS:Edit` permission), then set `CF_API_TOKEN`

Define a reusable base command (assumes `jq` is available; install it if not):

```bash
CF="curl -sS -H 'Authorization: Bearer $CF_API_TOKEN' -H 'Content-Type: application/json'"
```

---

## Common Operations

### Query the Zone List

```bash
curl -sS -H "Authorization: Bearer $CF_API_TOKEN" \
  "https://api.cloudflare.com/client/v4/zones" | jq '.result[] | {id, name, status}'
```

### Get a Zone ID by Name

```bash
curl -sS -H "Authorization: Bearer $CF_API_TOKEN" \
  "https://api.cloudflare.com/client/v4/zones?name=example.com" | jq -r '.result[0].id'
```

### List DNS Records

```bash
# List all records for a zone (use the zone ID)
curl -sS -H "Authorization: Bearer $CF_API_TOKEN" \
  "https://api.cloudflare.com/client/v4/zones/<zone_id>/dns_records" | jq '.result[] | {id, type, name, content, proxied, ttl}'

# Filter by type
curl -sS -H "Authorization: Bearer $CF_API_TOKEN" \
  "https://api.cloudflare.com/client/v4/zones/<zone_id>/dns_records?type=A" | jq '.result[]'

# Filter by name
curl -sS -H "Authorization: Bearer $CF_API_TOKEN" \
  "https://api.cloudflare.com/client/v4/zones/<zone_id>/dns_records?name=sub.example.com" | jq '.result[]'

# Paginate through all records (100 per page)
curl -sS -H "Authorization: Bearer $CF_API_TOKEN" \
  "https://api.cloudflare.com/client/v4/zones/<zone_id>/dns_records?per_page=100&page=1" | jq '.result[]'
```

### Add DNS Records

```bash
# A record (TTL 1 = automatic)
curl -sS -X POST "https://api.cloudflare.com/client/v4/zones/<zone_id>/dns_records" \
  -H "Authorization: Bearer $CF_API_TOKEN" -H "Content-Type: application/json" \
  --data '{"type":"A","name":"sub.example.com","content":"1.2.3.4","ttl":1}'

# CNAME record (enable orange-cloud proxy)
curl -sS -X POST "https://api.cloudflare.com/client/v4/zones/<zone_id>/dns_records" \
  -H "Authorization: Bearer $CF_API_TOKEN" -H "Content-Type: application/json" \
  --data '{"type":"CNAME","name":"www.example.com","content":"example.com","proxied":true}'

# MX record
curl -sS -X POST "https://api.cloudflare.com/client/v4/zones/<zone_id>/dns_records" \
  -H "Authorization: Bearer $CF_API_TOKEN" -H "Content-Type: application/json" \
  --data '{"type":"MX","name":"example.com","content":"mail.example.com","priority":10,"ttl":1}'

# TXT record
curl -sS -X POST "https://api.cloudflare.com/client/v4/zones/<zone_id>/dns_records" \
  -H "Authorization: Bearer $CF_API_TOKEN" -H "Content-Type: application/json" \
  --data '{"type":"TXT","name":"_dmarc.example.com","content":"v=DMARC1; p=none","ttl":1}'

# AAAA record (IPv6)
curl -sS -X POST "https://api.cloudflare.com/client/v4/zones/<zone_id>/dns_records" \
  -H "Authorization: Bearer $CF_API_TOKEN" -H "Content-Type: application/json" \
  --data '{"type":"AAAA","name":"ipv6.example.com","content":"2001:db8::1","ttl":1}'
```

Parameter descriptions:
- `ttl: 1`: Automatic TTL (recommended); other values are in seconds (for example, `ttl: 300`)
- `proxied: true`: Enable the Cloudflare orange-cloud proxy (supported only for A/AAAA/CNAME records)

### Update DNS Records

Updating requires the record `id`. List records to get it first:

```bash
# Get the record ID
curl -sS -H "Authorization: Bearer $CF_API_TOKEN" \
  "https://api.cloudflare.com/client/v4/zones/<zone_id>/dns_records?name=sub.example.com" \
  | jq -r '.result[] | "\(.id) \(.type) \(.name) \(.content)"'

# Update the content
curl -sS -X PATCH "https://api.cloudflare.com/client/v4/zones/<zone_id>/dns_records/<record_id>" \
  -H "Authorization: Bearer $CF_API_TOKEN" -H "Content-Type: application/json" \
  --data '{"content":"5.6.7.8"}'

# Update and enable proxy
curl -sS -X PATCH "https://api.cloudflare.com/client/v4/zones/<zone_id>/dns_records/<record_id>" \
  -H "Authorization: Bearer $CF_API_TOKEN" -H "Content-Type: application/json" \
  --data '{"content":"5.6.7.8","proxied":true}'
```

### Create or Update (upsert)

```bash
# Update if a record with the same type+name exists; create it if it does not.
# Match the existing record's id first:
ID=$(curl -sS -H "Authorization: Bearer $CF_API_TOKEN" \
  "https://api.cloudflare.com/client/v4/zones/<zone_id>/dns_records?type=A&name=sub.example.com" \
  | jq -r '.result[0].id // empty')

if [ -n "$ID" ]; then
  curl -sS -X PATCH "https://api.cloudflare.com/client/v4/zones/<zone_id>/dns_records/$ID" \
    -H "Authorization: Bearer $CF_API_TOKEN" -H "Content-Type: application/json" \
    --data '{"content":"1.2.3.4"}'
else
  curl -sS -X POST "https://api.cloudflare.com/client/v4/zones/<zone_id>/dns_records" \
    -H "Authorization: Bearer $CF_API_TOKEN" -H "Content-Type: application/json" \
    --data '{"type":"A","name":"sub.example.com","content":"1.2.3.4","ttl":1}'
fi
```

### Delete DNS Records

```bash
# Look up the ID first
curl -sS -H "Authorization: Bearer $CF_API_TOKEN" \
  "https://api.cloudflare.com/client/v4/zones/<zone_id>/dns_records?name=sub.example.com" \
  | jq -r '.result[] | "\(.id) \(.type) \(.name)"'

# Delete
curl -sS -X DELETE "https://api.cloudflare.com/client/v4/zones/<zone_id>/dns_records/<record_id>" \
  -H "Authorization: Bearer $CF_API_TOKEN"
```

### Batch Delete Records with the Same Name

```bash
for ID in $(curl -sS -H "Authorization: Bearer $CF_API_TOKEN" \
  "https://api.cloudflare.com/client/v4/zones/<zone_id>/dns_records?name=sub.example.com" \
  | jq -r '.result[].id'); do
  curl -sS -X DELETE "https://api.cloudflare.com/client/v4/zones/<zone_id>/dns_records/$ID" \
    -H "Authorization: Bearer $CF_API_TOKEN"
  echo "Deleted: $ID"
done
```

---

## Workflow

1. **Verify authentication**: Check whether `CF_API_TOKEN` is set
2. **Confirm the zone**: If the user has not specified a zone, first query the zone list so they can choose one; resolve the domain to its zone ID
3. **Perform the operation**: Run list/create/update/delete as needed
4. **Display results**: After the operation, list the DNS records for the zone to show the latest status

## Notes

- Deletions are irreversible; confirm with the user before proceeding
- `proxied: true` supports only A, AAAA, and CNAME record types
- MX records must include `priority`
- TXT record content that contains spaces must be properly escaped in the JSON payload
- The API returns errors in the response body: check `success` (boolean) and the `errors` array on every call
- Use `jq -r` to extract values; do not rely on `python` being installed
