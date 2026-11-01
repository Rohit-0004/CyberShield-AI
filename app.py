import streamlit as st
from detector import analyze_content

st.set_page_config(page_title="CyberShield AI", page_icon="🛡️", layout="wide")

st.markdown("""
<style>
.main {background: #0b1220;}
.block-container {padding-top: 2rem; max-width: 1050px;}
[data-testid="stMetric"] {background: #111c30; padding: 16px; border-radius: 12px; border: 1px solid #24334d;}
.result-card {background:#111c30;padding:18px;border:1px solid #24334d;border-radius:12px;margin:8px 0;}
.small-muted {color:#9aa9bf;font-size:0.9rem;}
</style>
""", unsafe_allow_html=True)

st.title("🛡️ CyberShield AI")
st.caption("A simple cyber-safety assistant that explains warning signs in suspicious messages and links.")

with st.sidebar:
    st.header("About CyberShield")
    st.write("CyberShield screens text and URLs for common warning signs. It is an educational prototype, not a replacement for security software.")
    st.divider()
    st.caption("Privacy: analysis happens in this app session. Do not paste passwords, OTPs, financial details, or private messages.")

st.subheader("Analyze suspicious content")
mode = st.radio("What would you like to check?", ["Message or email", "URL only"], horizontal=True)
placeholder = (
    "Example: Congratulations! You have won a prize. Pay a processing fee immediately and share your OTP."
    if mode == "Message or email" else "https://example.com/login"
)
content = st.text_area("Paste the message or URL", height=170, placeholder=placeholder)

if st.button("Analyze now", type="primary", use_container_width=True):
    if not content.strip():
        st.warning("Please enter some text before analyzing.")
    else:
        result = analyze_content(content, mode)
        st.divider()
        st.subheader("Analysis report")
        c1, c2 = st.columns(2)
        c1.metric("Risk indicator", result["level"])
        c2.metric("Warning signs found", len(result["flags"]))

        if result["level"] == "High":
            st.error("Several warning signs were found. Treat this content with caution.")
        elif result["level"] == "Review":
            st.warning("Some warning signs were found. Verify independently before taking action.")
        else:
            st.success("No configured warning signs were found. This does not prove the content is safe.")

        st.markdown("#### Why it was flagged")
        if result["flags"]:
            for flag in result["flags"]:
                st.markdown(f"- ⚠️ {flag}")
        else:
            st.write("No matching warning patterns were detected by the current rules.")

        if result["urls"]:
            st.markdown("#### URLs detected (not opened)")
            for url_info in result["urls"]:
                st.code(url_info, language=None)

        st.markdown("#### Recommended next steps")
        for advice in result["advice"]:
            st.markdown(f"- {advice}")

        st.caption("This is a rule-based screening result, not a probability or a definitive security verdict. False positives and missed threats are possible.")

st.divider()
st.markdown("<p class='small-muted'>CyberShield AI • Early prototype • Built for cyber-safety awareness</p>", unsafe_allow_html=True)
