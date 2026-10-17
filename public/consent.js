// Souhlas s cookies a Meta Pixel. Pixel se načte AŽ po kliknutí na „Přijmout“ (vyžaduje to GDPR a zákon o elektronických komunikacích).
// Volbu si pamatujeme v prohlížeči 12 měsíců. Odkaz s data-cookie-settings otevře lištu znovu (odvolání souhlasu).
(function () {
  var PIXEL_ID = "1438867787970217";
  var KEY = "ep-consent", MAX_AGE = 365 * 24 * 3600 * 1000;

  function read() {
    try { var c = JSON.parse(localStorage.getItem(KEY) || "null"); if (c && Date.now() - c.at < MAX_AGE) return c; } catch (e) {}
    return null;
  }
  function save(marketing) {
    try { localStorage.setItem(KEY, JSON.stringify({ v: 1, marketing: marketing, at: Date.now() })); } catch (e) {}
  }
  function clearMetaCookies() {
    ["_fbp", "_fbc"].forEach(function (n) {
      var host = location.hostname.replace(/^www\./, "");
      [host, "." + host, location.hostname].forEach(function (d) { document.cookie = n + "=; Max-Age=0; path=/; domain=" + d; });
      document.cookie = n + "=; Max-Age=0; path=/";
    });
  }

  var loaded = false;
  function loadPixel() {
    if (loaded) return; loaded = true;
    !function (f, b, e, v, n, t, s) {
      if (f.fbq) return; n = f.fbq = function () { n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments); };
      if (!f._fbq) f._fbq = n; n.push = n; n.loaded = !0; n.version = "2.0"; n.queue = []; t = b.createElement(e); t.async = !0;
      t.src = v; s = b.getElementsByTagName(e)[0]; s.parentNode.insertBefore(t, s);
    }(window, document, "script", "https://connect.facebook.net/en_US/fbevents.js");
    window.fbq("init", PIXEL_ID);
    window.fbq("track", "PageView");
  }

  // Pro ostatní skripty na webu: událost se odešle jen se souhlasem.
  window.epTrack = function (event, params) { if (loaded && window.fbq) window.fbq("track", event, params || {}); };

  var css = ".ckb{position:fixed;left:16px;right:16px;bottom:16px;z-index:2147483647;max-width:560px;margin:0 auto;background:#fffdf8;color:#14313a;border:1px solid #e6dfcf;border-radius:20px;box-shadow:0 18px 50px rgba(20,49,58,.22);padding:20px 22px;font:15px/1.5 'Nunito Sans',system-ui,sans-serif}"
    + ".ckb h2{font:700 18px 'Outfit',system-ui,sans-serif;margin:0 0 6px;color:#14313a}.ckb p{margin:0 0 14px;color:#4a6168}.ckb a{color:#0c8a83}"
    + ".ckb .row{display:flex;gap:10px;flex-wrap:wrap}.ckb button{flex:1 1 140px;font:700 15px 'Nunito Sans',system-ui,sans-serif;border-radius:999px;padding:12px 18px;cursor:pointer;border:2px solid #13a39b}"
    + ".ckb .yes{background:#13a39b;color:#fff}.ckb .no{background:#fff;color:#0c8a83}.ckb button:focus-visible{outline:3px solid #14313a;outline-offset:2px}";

  function show() {
    if (document.querySelector(".ckb")) return;
    if (!document.getElementById("ckb-css")) { var st = document.createElement("style"); st.id = "ckb-css"; st.textContent = css; document.head.appendChild(st); }
    var box = document.createElement("div");
    box.className = "ckb"; box.setAttribute("role", "dialog"); box.setAttribute("aria-labelledby", "ckbT"); box.setAttribute("aria-describedby", "ckbD");
    box.innerHTML = '<h2 id="ckbT">Cookies na tomto webu</h2>'
      + '<p id="ckbD">Se souhlasem použijeme Meta Pixel (Facebook, Instagram), abychom měřili účinnost reklam. Bez souhlasu web funguje stejně a nic se neměří. Volbu můžete kdykoli změnit v patičce. <a href="/chat-gdpr.html#cookies" target="_blank" rel="noopener">Více informací</a></p>'
      + '<div class="row"><button type="button" class="no">Odmítnout</button><button type="button" class="yes">Přijmout</button></div>';
    document.body.appendChild(box);
    box.querySelector(".yes").addEventListener("click", function () { save(true); box.remove(); loadPixel(); });
    box.querySelector(".no").addEventListener("click", function () {
      var had = loaded; save(false); box.remove(); clearMetaCookies();
      if (had) location.reload(); // odvolání souhlasu: pixel z běžící stránky jinak odstranit nejde
    });
  }

  function init() {
    var c = read();
    if (c && c.marketing) loadPixel();
    if (!c) show();
    document.addEventListener("click", function (e) {
      var a = e.target.closest && e.target.closest("[data-cookie-settings]");
      if (a) { e.preventDefault(); show(); }
    });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init); else init();
})();
