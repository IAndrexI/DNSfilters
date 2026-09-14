# DNS Blocklists for AdGuard Home

A personal collection of categorized DNS blocklists configured for use with [AdGuard Home](https://adguard.com/en/adguard-home/overview.html).

Compiled blocklists for subscription are located in the [`dist/`](dist/) folder. Raw category source files can be browsed in the [`src/`](src/) directory.

---

## ➕ How to Add & Modify Domains

1. Browse to the [`src/`](src/) directory and open the file you want to edit.
2. Add your domains (one domain per line):
   ```text
   example.com
   bad-domain.net
   ```
   * Lines starting with `#` are treated as comments.
   * Do not include `http://`, `https://`, or paths—just the plain domain.
   * If there is a domain that should never be blocked, add it to [`src/whitelist.txt`](src/whitelist.txt).
3. Commit and push your changes.
4. GitHub Actions will automatically recompile the lists in [`dist/`](dist/) and apply AdGuard formatting (`||domain^`).
