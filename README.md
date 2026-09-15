# DNSfilters

Personal DNS blocklists curated for [AdGuard Home](https://adguard.com/en/adguard-home/overview.html).

Compiled subscription lists are stored in [`dist/`](dist/).  
Raw source categories can be inspected in [`src/`](src/).

---

### Adding & Modifying Domains

1. Navigate to [`src/`](src/) and select the target category file.
2. Append domains using one entry per line:
   ```text
   example.com
   tracker-domain.net
   ```
   - Lines prefixed with `#` are ignored as comments.
   - Do not include protocols (`http://`, `https://`) or trailing paths.
   - Critical services that must never be blocked belong in [`src/whitelist.txt`](src/whitelist.txt).
3. Commit and push your changes.
4. GitHub Actions automatically recompiles the subscription lists in [`dist/`](dist/) using standard AdGuard syntax (`||domain^`).
