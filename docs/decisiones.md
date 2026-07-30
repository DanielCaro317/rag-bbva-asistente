# Decisiones de diseño y evidencia

Registro breve de decisiones técnicas relevantes y su justificación. Se amplía a medida que avanza el proyecto.

## ADR-001 · Fuente de datos: Scotiabank Colpatria (no BBVA)

**Contexto.** La prueba propone scrapear `bbva.com.co` y permite explícitamente usar otro banco.

**Problema.** El sitio de BBVA está detrás de un WAF anti-bot que responde `403` a toda petición programática, incluido `robots.txt`. No es posible scrapearlo de forma fiable ni verificar qué permite su `robots.txt`.

**Evidencia (reproducible).**

```bash
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"

curl -sS -A "$UA" -o /dev/null -w "%{http_code}\n" https://www.bbva.com.co/robots.txt   # -> 403
curl -sS -A "$UA" -o /dev/null -w "%{http_code}\n" https://www.bbva.com.co/              # -> 403
curl -sS -A "$UA" -o /dev/null -w "%{http_code}\n" https://www.scotiabankcolpatria.com/  # -> 200
```

**Alternativas evaluadas.**

| Banco | HTTP | Observación |
|---|---|---|
| BBVA | 403 | WAF anti-bot; `robots.txt` inaccesible |
| Davivienda | 403 | WAF anti-bot |
| Banco de Bogotá | 200 | SPA sin contenido server-rendered (requeriría navegador headless) |
| Bancolombia | 200 | `robots.txt` bloquea crawlers de IA (`GPTBot`/`ClaudeBot` → `Disallow: /`) |
| **Scotiabank Colpatria** | **200** | server-rendered; `robots.txt` permisivo (solo bloquea `/Handlers`, `/Views`, `/Images`, `/Fonts`) |

**Decisión.** Usar **Scotiabank Colpatria**: es server-rendered (basta `requests` + BeautifulSoup, sin navegador headless), su `robots.txt` permite las páginas informativas, y el scraper lo respeta (`urllib.robotparser`).

**Consecuencia.** El sistema es agnóstico del banco: cambiar la fuente es cambiar `SCRAPER_BASE_URL` en `.env`. Si en el futuro se requiere un sitio JS-only, se añadiría un backend de scraping con navegador headless sin tocar el resto del pipeline.
