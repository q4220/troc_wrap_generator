#!/usr/bin/env python3
"""
Trocador Swap Page Generator
Generates professional crypto swap pages with Trocador referral integration
"""

import re
import subprocess
import sys
import time
from html import escape
from pathlib import Path

# Model configuration
MODEL_LOCAL = "llama3.2"
MODEL_CLOUD = "qwen3-vl:235b-cloud"

# Template presets with complete color schemes
TEMPLATES = {
    "1": {
        "name": "Matrix Green",
        "colors": {
            "ACCENT": "#00ff96",
            "ACCENT_BRIGHT": "#33ffaa",
            "ACCENT_DIM": "rgba(0, 255, 150, 0.1)",
            "BG_PRIMARY": "#000000",
            "BG_SECONDARY": "rgba(0, 0, 0, 0.8)",
            "BORDER_COLOR": "rgba(0, 255, 150, 0.2)",
            "TEXT_PRIMARY": "#ffffff",
            "TEXT_SECONDARY": "rgba(255, 255, 255, 0.7)",
        },
    },
    "2": {
        "name": "Monero Orange",
        "colors": {
            "ACCENT": "#ff6600",
            "ACCENT_BRIGHT": "#ff8533",
            "ACCENT_DIM": "rgba(255, 102, 0, 0.1)",
            "BG_PRIMARY": "#0a0a0a",
            "BG_SECONDARY": "rgba(15, 15, 15, 0.9)",
            "BORDER_COLOR": "rgba(255, 102, 0, 0.2)",
            "TEXT_PRIMARY": "#ffffff",
            "TEXT_SECONDARY": "rgba(255, 255, 255, 0.7)",
        },
    },
    "3": {
        "name": "Purple Cyber",
        "colors": {
            "ACCENT": "#b026ff",
            "ACCENT_BRIGHT": "#c653ff",
            "ACCENT_DIM": "rgba(176, 38, 255, 0.1)",
            "BG_PRIMARY": "#050510",
            "BG_SECONDARY": "rgba(10, 10, 20, 0.9)",
            "BORDER_COLOR": "rgba(176, 38, 255, 0.2)",
            "TEXT_PRIMARY": "#ffffff",
            "TEXT_SECONDARY": "rgba(255, 255, 255, 0.7)",
        },
    },
    "4": {
        "name": "Blue Terminal",
        "colors": {
            "ACCENT": "#00d9ff",
            "ACCENT_BRIGHT": "#33e3ff",
            "ACCENT_DIM": "rgba(0, 217, 255, 0.1)",
            "BG_PRIMARY": "#000a0f",
            "BG_SECONDARY": "rgba(0, 15, 20, 0.9)",
            "BORDER_COLOR": "rgba(0, 217, 255, 0.2)",
            "TEXT_PRIMARY": "#ffffff",
            "TEXT_SECONDARY": "rgba(255, 255, 255, 0.7)",
        },
    },
}

FAQ_CONTENT = """How does Trocador.app work?
When you fill in your desired transaction, we search the best possible rates in our partner exchanges, so you can pick the exchange with the best price and swap directly with them. This means there's no need for you to open an account in a centralized exchange.

You transfer the chosen amount to the address provided by the exchange, the trade is made and you receive your desired crypto directly in your chosen address. It's a fast and safe way of exchanging your coins without the hassle and risks of using centralized exchanges.

We also monitor exchanges' rate reliability, transaction delay and any maintenance or server problems to make sure everything runs smoothly for your trade and to prevent any exchange abuse. And if you encounter any problems, you can reach out to us and we'll do all we can to solve your problem!

Trocador provides software that allows users to choose between exchanges and trade directly with them, we never have access, receive or transfer any of the funds between the parties.

Why trust us?
Our service was designed from the ground up focused on your needs. We only keep the minimum amount of logs for exchanges that require this and we let you know each one's log policies before creating the transaction. Logs kept at Trocador are never sold or ceded to third parties and are only provided on an individual basis upon request from law enforcement.

We use minimal JavaScript to improve user experience (like in dropdown selection), but never to track or fingerprint users. It is entirely optional for most of our services, so you can block JavaScript and use our website without any problems if you want!

We only redirect your order to known and reliable instant exchanges, that receive your deposit, process the trade and transfer your funds directly to your chosen address. We do not have access to your coins at any point of the transaction.

What is the Trocador Guarantee?
Transactions made through our website enjoy our Trocador Guarantee, if for some reason you do not receive your funds and the exchange does not provide us sufficient proof of unusually high AML risk or that it was blocked by their Liquidity Provider's AML system, Trocador will reimburse you up to the insured amount. This amount varies between exchanges and you can check it by hovering or clicking the shield icon besides each exchange option. Please note, however, that trades with exchanges rated as 'D' are not covered by this Guarantee. Trades blocked because of high AML risk or funds that came from mixers are also not covered by the Guarantee, as those are generally considered as very high AML risk by most providers.

To get compensation, contact us through email or Telegram informing your transaction's ID at Trocador. We'll talk to your chosen exchange and try to solve your problem. Failing that and if the exchange doesn't provide sufficient proof that the transaction was halted due to a police request, legal order or unusually high AML risk, we'll reimburse your transaction up to the amount defined when your trade was created. The whole process can take a week or a bit longer, as we try to sort things out with the exchange.

So please be aware that:
• Our Guarantee DOES NOT cover cases where funds are blocked due to proven AML issues, as this could be abused to launder illicit funds.
• The refund process can take a week or longer, as we'll first try solving your issue with the partner exchange.

What are the Swap Modes?
Standard Mode is your usual way to convert from one coin to the other. You choose an amount for the crypto you'll send and which crypto you want to receive. We'll show you the best floating and fixed rates from all our partner exchanges and you can choose the one you want.

Payment Mode is meant to be used when you need to pay for something, so you choose the amount of the crypto to be received instead of sent and which crypto you'll use to pay. We'll show you the best fixed rates from all our partner exchanges that support this mode. This is useful for paying stores or services in your preferred crypto. An example: Protonmail doesn't yet accept Monero as payment. No problem! Choose payment in BTC, copy their address and use it with our payment mode!

The Buy/Sell tab is for using fiat currencies to buy or sell crypto. It may have fewer crypto options available, but you can circumvent this by using a more common crypto (like the ones listed as recommended) as an intermediary between your fiat currency and your desired crypto.

How does the Fiat Gateway (Buy/Sell) work?
In our Fiat Gateway Aggregator you can choose which crypto you want to buy or sell, which fiat currency you use and the amount to be traded. Trocador will then find the best rates among our partners and you can choose your preferred one to complete the process on their website. Depending on the selected currency, there are many payment methods available like credit card, bank transfer, GooglePay, ApplePay, UPI, IMPS, GCash, Paymaya, GrabPay and others.

Be aware that to complete the transaction you'll need to access the partner's website, which may require JavaScript. Each one has their own KYC/Verification policy, so make sure to check their Terms of Use. Trocador never has access to your funds nor any control over their KYC process, we only refer you to your chosen exchange.

How long does it take to complete a transaction?
Usually a transaction takes between 5 and 60 minutes to complete. Depending mostly on the selected crypto and the existence of congestion on their respective networks. Cryptos with a long transaction confirmation time take longer and the opposite is true for cryptos with a short transaction confirmation time.

We provide an approximate ETA on the exchange selection screen that takes into account the exchange's recent history. This way you can better choose your preferred exchange.

What fees are included in the rates shown?
All fees are already included in the shown rate. They consist of network transaction fees and exchange fees. This means bigger transactions can have better rates, as the network transaction fees are diluted. You do not pay anything extra for using our service instead of using directly your chosen exchange. We do receive a comission for referring the exchange, but it comes out of the exchange's fee so it doesn't change your rate.

The floating rates shown in the exchange selection screen are automatically adjusted to more accurately predict the final amount you'll receive. This takes into account each exchange's recent trades and their deviation from the predicted rate. The amount shown in the status screen is not adjusted, and will show the actual rate provided by the exchange.

Is it really private? Isn't KYC required?
Each exchange has their own KYC/AML policy, and they may halt your transaction and demand KYC/AML verification before completing it. All our partners exchanges perform due dilligence on the funds received before swapping them. We explicitly warn users not to send funds with very high AML risk, or involved with mixers or illegal activities, as these orders will be refused by our partners. You can check each exchange's policies on their websites.

To help you in your choice we provide a simple KYC/AML Rating for each exchange. To determine an exchange's rating we read their terms of use and privacy policy, ask them directly about how they handle refunding in case of verification refusal and take in account their past history on Trocador. We use the following ratings:

• This exchange uses its own liquidity and is privacy-friendly.
• This exchange refunds transactions that fail their AML check. In very rare cases funds may be blocked if a legal order demands it or stolen coins are involved. Past history at Trocador is very good.
• This exchange usually refunds transactions that fail their AML check, but if the deposit triggers their Liquidity Provider's AML system, funds may be blocked until KYC/SoF verification is passed.
• This exchange blocks transactions that fail their AML check until KYC/SoF verification is passed.

Your chosen exchange may also store your transaction details (amount, coins and addresses). Please be aware some exchanges require logs of the user's IP, UserAgent and AcceptLanguage to be kept at Trocador. These can be seen on the exchange screen by hovering/clicking their rating. Logs kept at Trocador are never sold or ceded to third parties and are only provided on an individual basis upon request from law enforcement.

Why do only a few exchanges appear as options for my trade?
While a few exchanges accept trades as small as $10, many of them have larger minimum amounts for trading, since network transaction fees may severely impact the rates of small trades. So if you are only checking rates, make sure to use amounts close to what you'll actually trade to get more precise rates.

Sometimes it may be difficult finding rates when trading directly one less popular crypto for another. In this case, using a more popular crypto as an intermediary can help.

What's the difference between Floating and Fixed Rate?
A floating rate is an estimate. When the exchange confirms your deposit, they will check market conditions and pick an appropriate new rate. If it's far enough from the original estimate, some exchanges prompt you if you want to proceed with this new rate or request a refund. Floating rates are recommended for most transactions where you have a known starting amount that you want to convert, since variable rates are better than fixed rates.

Fixed rates are good for paying invoices. If you know you need to pay 0.1 XMR, you can "lock in" a fixed amount of BTC necessary to get 0.1 XMR. However, if the market moves too much, the exchange may still decide to refund the transaction instead of proceeding with the quote.

For these reasons we suggest you use floating rate whenever possible. In any case we recommend you have your wallet ready before confirming your transaction to avoid having your transaction expire before blockchain confirmation.

What happens if I send the wrong amount to the address provided?
Depends on the chosen exchange, some of them accept slightly different amounts and will complete your trade proportionately, while others may halt your transaction or even have trouble detecting your deposit. Always take care to send the exact amount to the address provided to avoid such problems. This information can be seen on the status page, where we show a tooltip letting you know if the exchange requires exact amounts or not.

My transaction has failed and I haven't got my funds back. What do I do now?
Although very rare, this can happen. Simply contact our Support through the Telegram or email located at the footer of the website and we'll be happy to help you! At your transaction's status screen we provide you with all its details. With this information you could also contact the exchange directly to solve your problem if you prefer."""


# Enhanced CSS template with cyberpunk aesthetics
CSS_TEMPLATE = """/* Cyberpunk-inspired swap page */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif;
    background: {BG_PRIMARY};
    color: {TEXT_PRIMARY};
    line-height: 1.6;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    position: relative;
    overflow-x: hidden;
}

/* Cyberpunk grid background */
body::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image:
        linear-gradient({BORDER_COLOR} 1px, transparent 1px),
        linear-gradient(90deg, {BORDER_COLOR} 1px, transparent 1px);
    background-size: 50px 50px;
    opacity: 0.15;
    pointer-events: none;
    z-index: 0;
}

/* Radial gradient overlay */
body::after {
    content: "";
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 150%;
    height: 150%;
    background: radial-gradient(circle, {ACCENT_DIM} 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
}

/* Header & Navigation */
header {
    background: {BG_SECONDARY};
    border-bottom: 1px solid {BORDER_COLOR};
    position: sticky;
    top: 0;
    z-index: 1000;
    backdrop-filter: blur(10px);
    box-shadow: 0 2px 20px rgba(0, 0, 0, 0.5);
}

nav {
    max-width: 1200px;
    margin: 0 auto;
    padding: 1.5rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: relative;
    z-index: 1;
}

nav h1 {
    font-size: 1.5rem;
    font-weight: 600;
    color: {TEXT_PRIMARY};
    letter-spacing: -0.5px;
    text-shadow: 0 0 20px {ACCENT_DIM};
}

nav a {
    color: {ACCENT};
    text-decoration: none;
    font-weight: 500;
    font-size: 0.95rem;
    transition: all 0.2s ease;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    border: 1px solid transparent;
}

nav a:hover {
    background: {ACCENT_DIM};
    color: {ACCENT_BRIGHT};
    border-color: {ACCENT};
    box-shadow: 0 0 15px {ACCENT_DIM};
}

/* Main content */
main {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
    position: relative;
    z-index: 1;
}

.swap-section {
    width: 100%;
    max-width: 500px;
    text-align: center;
}

.swap-section h2 {
    font-size: 2rem;
    font-weight: 300;
    margin-bottom: 2rem;
    color: {TEXT_PRIMARY};
    letter-spacing: -1px;
    text-shadow: 0 0 30px {ACCENT_DIM};
}

.swap-widget {
    background: {BG_SECONDARY};
    border: 1px solid {BORDER_COLOR};
    border-radius: 12px;
    overflow: hidden;
    box-shadow:
        0 20px 60px rgba(0, 0, 0, 0.5),
        0 0 40px {ACCENT_DIM},
        inset 0 1px 0 rgba(255, 255, 255, 0.05);
    transition: all 0.3s ease;
    position: relative;
}

.swap-widget::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, {ACCENT}, transparent);
    opacity: 0;
    transition: opacity 0.3s ease;
}

.swap-widget:hover {
    transform: translateY(-4px);
    box-shadow:
        0 25px 70px rgba(0, 0, 0, 0.6),
        0 0 60px {ACCENT_DIM};
    border-color: {ACCENT};
}

.swap-widget:hover::before {
    opacity: 1;
}

.swap-widget iframe {
    display: block;
    width: 100%;
    height: 600px;
    border: none;
}

/* FAQ Page Specific */
.faq-container {
    max-width: 900px;
    margin: 0 auto;
    padding: 3rem 2rem;
    position: relative;
    z-index: 1;
}

.faq-container h1 {
    font-size: 2.5rem;
    font-weight: 300;
    margin-bottom: 0.5rem;
    color: {TEXT_PRIMARY};
    letter-spacing: -1px;
    text-shadow: 0 0 30px {ACCENT_DIM};
}

.faq-container > p {
    color: {TEXT_SECONDARY};
    margin-bottom: 3rem;
    font-size: 1.1rem;
}

.faq-section {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.faq-item {
    background: {BG_SECONDARY};
    border: 1px solid {BORDER_COLOR};
    border-radius: 8px;
    overflow: hidden;
    transition: all 0.3s ease;
}

.faq-item:hover {
    border-color: {ACCENT};
    box-shadow: 0 4px 20px {ACCENT_DIM};
}

.faq-question {
    color: {ACCENT};
    font-size: 1.05rem;
    font-weight: 500;
    padding: 1.25rem 1.5rem;
    margin: 0;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    user-select: none;
    transition: all 0.2s ease;
}

.faq-question:hover {
    background: {ACCENT_DIM};
}

.faq-question::after {
    content: "+";
    font-size: 1.5rem;
    font-weight: 300;
    color: {ACCENT};
    transition: transform 0.3s ease;
    flex-shrink: 0;
}

.faq-item.active .faq-question::after {
    transform: rotate(45deg);
}

.faq-answer {
    max-height: 0;
    overflow: hidden;
    transition: max-height 0.3s ease;
    color: {TEXT_SECONDARY};
    line-height: 1.8;
}

.faq-answer-content {
    padding: 0 1.5rem 1.5rem 1.5rem;
}

.faq-item.active .faq-answer {
    max-height: 2000px;
}

.faq-answer p {
    margin-bottom: 1rem;
}

.faq-answer p:last-child {
    margin-bottom: 0;
}

/* Footer */
footer {
    background: {BG_SECONDARY};
    border-top: 1px solid {BORDER_COLOR};
    padding: 2rem;
    text-align: center;
    position: relative;
    z-index: 1;
    box-shadow: 0 -2px 20px rgba(0, 0, 0, 0.3);
}

footer::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, {ACCENT}, transparent);
    opacity: 0.3;
}

footer p {
    color: {TEXT_SECONDARY};
    font-size: 0.9rem;
    margin: 0.5rem 0;
}

footer a {
    color: {ACCENT};
    text-decoration: none;
    transition: all 0.2s ease;
}

footer a:hover {
    color: {ACCENT_BRIGHT};
    text-shadow: 0 0 10px {ACCENT_DIM};
}

/* Responsive */
@media (max-width: 768px) {
    body::before {
        background-size: 30px 30px;
    }

    nav {
        padding: 1rem;
    }

    nav h1 {
        font-size: 1.25rem;
    }

    .swap-section h2 {
        font-size: 1.5rem;
    }

    .swap-widget iframe {
        height: 550px;
    }

    .faq-container {
        padding: 2rem 1rem;
    }

    .faq-container h1 {
        font-size: 2rem;
    }
}

@media (max-width: 480px) {
    main {
        padding: 1rem;
    }

    .swap-widget iframe {
        height: 500px;
    }

    .faq-question {
        font-size: 1rem;
        padding: 1rem;
    }

    .faq-answer-content {
        padding: 0 1rem 1rem 1rem;
        font-size: 0.95rem;
    }
}
"""


def loading_animation(text, duration=2):
    """Simple loading animation"""
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        print(f"\r{frames[i % len(frames)]} {text}", end="", flush=True)
        time.sleep(0.1)
        i += 1
    print(f"\r✓ {text}")


def call_ollama(model, prompt):
    """Call Ollama API with timeout and error handling"""
    try:
        result = subprocess.run(
            ["ollama", "run", model, prompt],
            capture_output=True,
            text=True,
            timeout=120,
        )
        if result.returncode != 0:
            print(f"\n✗ Ollama error: {result.stderr}")
            sys.exit(1)
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        print("\n✗ Model timeout. Try a smaller model or increase timeout.")
        sys.exit(1)
    except FileNotFoundError:
        print("\n✗ Ollama not found. Install from https://ollama.ai")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        sys.exit(1)


def extract_colors_from_description(model, description):
    """Use AI to extract color scheme from custom description"""
    prompt = f"""Based on this aesthetic description: "{description}"

Extract a color scheme for a dark mode website. Respond with ONLY a JSON object, no other text:

{{
  "accent": "#HEXCODE",
  "background": "#HEXCODE"
}}

Requirements:
- accent: main highlight color (vibrant, stands out)
- background: dark background color
- Output ONLY the JSON, no markdown, no explanation"""

    response = call_ollama(model, prompt)

    # Clean response
    response = re.sub(r"```json\s*|\s*```", "", response)
    response = response.strip()

    # Extract hex codes
    try:
        import json

        data = json.loads(response)
        accent = data.get("accent", "#00ff96")
        bg = data.get("background", "#000000")
    except Exception:
        hex_pattern = r"#[0-9a-fA-F]{6}"
        matches = re.findall(hex_pattern, response)
        accent = matches[0] if len(matches) > 0 else "#00ff96"
        bg = matches[1] if len(matches) > 1 else "#000000"

    return generate_color_scheme(accent, bg)


def generate_color_scheme(accent, bg):
    """Generate complete color scheme from accent and background"""

    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))

    def rgb_to_hex(rgb):
        return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"

    def lighten(hex_color, factor=1.2):
        rgb = hex_to_rgb(hex_color)
        rgb = tuple(min(255, int(c * factor)) for c in rgb)
        return rgb_to_hex(rgb)

    def rgba(hex_color, alpha):
        rgb = hex_to_rgb(hex_color)
        return f"rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, {alpha})"

    bg_rgb = hex_to_rgb(bg)
    bg_secondary_rgb = tuple(min(255, int(c * 1.2)) for c in bg_rgb)
    bg_secondary = f"rgba({bg_secondary_rgb[0]}, {bg_secondary_rgb[1]}, {bg_secondary_rgb[2]}, 0.9)"

    return {
        "ACCENT": accent,
        "ACCENT_BRIGHT": lighten(accent, 1.3),
        "ACCENT_DIM": rgba(accent, 0.1),
        "BG_PRIMARY": bg,
        "BG_SECONDARY": bg_secondary,
        "BORDER_COLOR": rgba(accent, 0.2),
        "TEXT_PRIMARY": "#ffffff",
        "TEXT_SECONDARY": "rgba(255, 255, 255, 0.7)",
    }


def apply_theme_to_template(colors):
    """Apply color scheme to CSS template"""
    css_content = CSS_TEMPLATE

    for key, value in colors.items():
        css_content = css_content.replace(f"{{{key}}}", value)

    return css_content


def generate_html(referral_code, page_title, is_faq=False):
    """Generate HTML structure"""

    safe_referral = escape(referral_code)
    safe_title = escape(page_title)

    if is_faq:
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FAQ - {safe_title}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <nav>
            <h1>FAQ</h1>
            <a href="index.html">← Back</a>
        </nav>
    </header>

    <main>
        <div class="faq-container">
            <h1>Frequently Asked Questions</h1>
            <p>Below you can find answers to the most frequent questions and we explain a bit of our service.</p>

            <div class="faq-section">
                {format_faq_html()}
            </div>
        </div>
    </main>

    <footer>
        <p>Powered by <a href="https://trocador.app" target="_blank" rel="noopener">Trocador.app</a></p>
    </footer>

    <script>
    // Minimal JS for FAQ dropdowns
    document.querySelectorAll('.faq-question').forEach(question => {{
        question.addEventListener('click', () => {{
            const item = question.parentElement;
            const wasActive = item.classList.contains('active');

            // Close all others
            document.querySelectorAll('.faq-item').forEach(i => {{
                i.classList.remove('active');
            }});

            // Toggle this one
            if (!wasActive) {{
                item.classList.add('active');
            }}
        }});
    }});
    </script>
</body>
</html>"""

    else:
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{safe_title}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <nav>
            <h1>{safe_title}</h1>
            <a href="faq.html">FAQ</a>
        </nav>
    </header>

    <main>
        <section class="swap-section">
            <h2>Monero Swaps via Trocador</h2>
            <div class="swap-widget">
                <iframe
                    src="https://trocador.app/widget/?ref={safe_referral}"
                    width="400"
                    height="600"
                    title="Trocador Crypto Exchange Widget"
                    loading="lazy">
                </iframe>
            </div>
        </section>
    </main>

    <footer>
        <p>Powered by <a href="https://trocador.app" target="_blank" rel="noopener">Trocador.app</a></p>
        <p><a href="faq.html">FAQ & Info</a></p>
    </footer>
</body>
</html>"""


def format_faq_html():
    """Convert FAQ content to collapsible HTML"""
    sections = FAQ_CONTENT.split("\n\n")
    html = ""

    for section in sections:
        if not section.strip():
            continue

        lines = [line.strip() for line in section.strip().split("\n") if line.strip()]
        if not lines:
            continue

        question = lines[0]
        answer_lines = lines[1:] if len(lines) > 1 else []

        html += '<div class="faq-item">\n'
        html += f'<div class="faq-question">{escape(question)}</div>\n'
        html += '<div class="faq-answer">\n'
        html += '<div class="faq-answer-content">\n'

        for line in answer_lines:
            if line:
                html += f"<p>{escape(line)}</p>\n"

        html += "</div>\n</div>\n</div>\n\n"

    return html


def main():
    print("\n╔══════════════════════════════════════╗")
    print("║  Trocador Swap Page Generator       ║")
    print("╚══════════════════════════════════════╝\n")

    # Parse arguments
    use_cloud = "--cloud" in sys.argv
    model = MODEL_CLOUD if use_cloud else MODEL_LOCAL

    print(f"Model: {'Cloud' if use_cloud else 'Local'} ({model})\n")

    # Get referral code
    referral_code = input("Enter your Trocador referral code: ").strip()
    if not referral_code:
        print("✗ Referral code required")
        sys.exit(1)

    if len(referral_code) < 3:
        print("✗ Invalid referral code format")
        sys.exit(1)

    # Get page title
    page_title = input("Enter page title (default: Get Monero): ").strip()
    if not page_title:
        page_title = "Get Monero"

    # Template selection
    print("\n╔══════════════════════════════════════╗")
    print("║  Choose a template:                  ║")
    print("╠══════════════════════════════════════╣")
    for key, template in TEMPLATES.items():
        print(f"║  {key}. {template['name']:<30} ║")
    print("║  5. Custom (describe your own)       ║")
    print("╚══════════════════════════════════════╝\n")

    choice = input("Template choice (1-5): ").strip()

    colors = None

    if choice in TEMPLATES:
        template_data = TEMPLATES[choice]
        template_name = template_data["name"]
        colors = template_data["colors"]
        print(f"\n✓ Selected: {template_name}")
    elif choice == "5":
        custom_prompt = input("\nDescribe your desired aesthetic: ").strip()
        if not custom_prompt:
            print("✗ Description required for custom template")
            sys.exit(1)

        print("\n" + "─" * 40)
        loading_animation("Extracting color scheme", 1)
        print("⚙ Analyzing aesthetic...")

        colors = extract_colors_from_description(model, custom_prompt)
        print(f"✓ Generated color scheme: {colors['ACCENT']}")
    else:
        print("✗ Invalid choice")
        sys.exit(1)

    # Apply theme
    print("\n" + "─" * 40)
    loading_animation("Applying theme", 1)

    css_content = apply_theme_to_template(colors)

    # Generate HTML
    loading_animation("Generating HTML", 1)
    index_html = generate_html(referral_code, page_title, is_faq=False)
    faq_html = generate_html(referral_code, page_title, is_faq=True)

    # Write files
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    (output_dir / "index.html").write_text(index_html, encoding="utf-8")
    (output_dir / "faq.html").write_text(faq_html, encoding="utf-8")
    (output_dir / "style.css").write_text(css_content, encoding="utf-8")

    print("\n" + "─" * 40)
    print("✓ Generation complete!\n")
    print("Files created in ./output/:")
    print("  • index.html")
    print("  • faq.html")
    print("  • style.css")
    print("\nTest locally: cd output && python3 -m http.server 8000 --bind 127.0.0.1")
    print("─" * 40 + "\n")


if __name__ == "__main__":
    main()
