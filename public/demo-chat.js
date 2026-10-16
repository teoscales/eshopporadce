// Živá ukázka chatbota na eshop-poradce.eu (úvodní stránka i ukázkový e-shop).
// Adresu mění jen tenhle řádek: chat funkce ukázkového Supabase projektu.
var DEMO_ENDPOINT = "https://rnklanrhrmubzxxplfzc.supabase.co/functions/v1/chat";

(function () {
  var ready = /^https:\/\/[a-z0-9]{10,}\.supabase\.co\/functions\/v1\/chat$/.test(DEMO_ENDPOINT);
  document.documentElement.classList.toggle("demo-chat-on", ready);
  if (!ready) return;
  var s = document.createElement("script");
  s.src = "/shop-assistant.js";
  s.defer = true;
  var d = {
    endpoint: DEMO_ENDPOINT,
    name: "Ema",
    suggestions: "Hledám dárek pro mámu|Jak chatbota dostanu na svůj e-shop?|Co je teď v akci?",
    privacyUrl: "https://eshop-poradce.eu/chat-gdpr.html",
    accessibilityUrl: "https://eshop-poradce.eu/chat-pristupnost.html",
    videoUrl: "https://eshop-poradce.eu/videa/jak-funguje-chatbot.mp4",
    videoPoster: "https://eshop-poradce.eu/videa/jak-funguje-chatbot.jpg",
    videoLength: "20 s",
    poweredBy: "E-shop poradce",
  };
  for (var k in d) s.dataset[k] = d[k];
  document.head.appendChild(s);
})();

// Tlačítka „Vyzkoušet chat“ (data-open-chat) chat otevřou, případně s připravenou otázkou (data-ask).
document.addEventListener("click", function (e) {
  var b = e.target.closest && e.target.closest("[data-open-chat],[data-ask]");
  if (!b) return;
  e.preventDefault();
  var sa = window.ShopAssistant;
  if (!sa) return;
  if (b.dataset.ask) sa.ask(b.dataset.ask); else sa.open();
});
