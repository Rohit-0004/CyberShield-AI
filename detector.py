"""Rule-based screening helpers for the CyberShield AI prototype."""
import re
from urllib.parse import urlparse

MESSAGE_RULES = [
    (r"\b(urgent|immediately|act now|last chance|account suspended)\b", "Pressure or urgency language"),
    (r"\b(otp|password|passcode|pin|cvv)\b", "Mentions sensitive credentials"),
    (r"\b(prize|winner|lottery|free money|reward)\b", "Unexpected reward or prize language"),
    (r"\b(pay|payment|processing fee|transfer money|bank details)\b", "Requests payment or financial information"),
    (r"\b(verify your account|click here|login now)\b", "Pushes the recipient to click or sign in"),
]


def extract_urls(text: str) -> list[str]:
    """Extract visible HTTP(S) URLs without visiting them."""
    return re.findall(r"https?://[^\s<>\]\[(){}\"']+", text, flags=re.IGNORECASE)


def inspect_url(url: str) -> list[str]:
    flags = []
    parsed = urlparse(url)
    host = parsed.hostname or ""
    if parsed.scheme.lower() != "https":
        flags.append("Link does not use HTTPS")
    if not host:
        flags.append("Could not identify a valid hostname")
        return flags
    if host.startswith("xn--") or ".xn--" in host:
        flags.append("Domain uses punycode and needs careful verification")
    if re.fullmatch(r"\d{1,3}(\.\d{1,3}){3}", host):
        flags.append("Link uses an IP address instead of a normal domain name")
    if "@" in parsed.netloc:
        flags.append("Link contains an @ symbol in its authority section")
    if len(host) > 45:
        flags.append("Unusually long hostname")
    if host.count("-") >= 3:
        flags.append("Hostname contains several hyphens")
    return flags


def analyze_content(content: str, mode: str = "Message or email") -> dict:
    flags = []
    urls = extract_urls(content)

    if mode == "Message or email":
        for pattern, description in MESSAGE_RULES:
            if re.search(pattern, content, flags=re.IGNORECASE):
                flags.append(description)

    if mode == "URL only" and not urls and content.strip():
        candidate = content.strip()
        if not candidate.startswith(("http://", "https://")):
            candidate = "https://" + candidate
        urls = [candidate]

    for url in urls:
        flags.extend(inspect_url(url))

    flags = list(dict.fromkeys(flags))
    if len(flags) >= 3:
        level = "High"
    elif flags:
        level = "Review"
    else:
        level = "No simple warning patterns found"

    advice = [
        "Do not share passwords, OTPs, PINs, or payment details in response to unexpected messages.",
        "Verify the sender using a trusted contact method or the organisation's official website, typed manually.",
        "If money or an account is involved, contact your bank or service provider through its official channel.",
    ]
    return {"level": level, "flags": flags, "urls": urls, "advice": advice}
