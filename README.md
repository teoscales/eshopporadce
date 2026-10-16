# eshop-poradce.eu

Web AI nákupního asistenta pro e-shopy (Shoptet). Čistě statický web – žádný build, žádné API klíče.

```
public/
  index.html             úvodní stránka
  shop-assistant.js      skript chatbota (vkládá se do Shoptetu)
  chat-gdpr.html         Moje data a GDPR
  chat-pristupnost.html  Přístupnost + video „Jak funguje“
  chat-admin.html        administrace pro firmy (heslo)
  owner.html             panel provozovatele (token)
  chat-test.html         testovací stránka chatu
  videa/                 videa (mp4 + webm + náhled)
```

Backend (Supabase Edge Functions) je v repozitáři `shoptet-ai-asistent`.
Nový `shop-assistant.js` se vytváří tam (`npm run build`) a kopíruje sem do `public/`.

**Do tohoto repozitáře nikdy nepatří API klíče ani obsah `.env`.**
