# DNSfilters

Unified personal DNS blocklist curated for [AdGuard Home](https://adguard.com/en/adguard-home/overview.html).

### AdGuard Home Import URL

Add this single URL to AdGuard Home under **Filters** > **DNS blocklists** > **Add blocklist**:

```text
https://raw.githubusercontent.com/IAndrexI/DNSfilters/main/dist/blocklist.txt
```

---

### Adding & Modifying Domains

Raw source categories are organized in [`src/`](src/).

1. Open the target category file inside [`src/`](src/).
2. Add your domains (one per line):
   ```text
   example.com
   tracker-domain.net
   ```
   - Lines prefixed with `#` are treated as comments.
   - Do not include protocols (`http://`, `https://`) or trailing paths.
   - Domains in [`src/whitelist.txt`](src/whitelist.txt) are strictly excluded from the build.
3. Commit and push your changes.
4. GitHub Actions automatically recompiles everything into the single [`dist/blocklist.txt`](dist/blocklist.txt) file.
