import streamlit as st
from agents import run_security_audit

st.set_page_config(page_title="AI Security Audit Agent", layout="wide")

# -----------------------------
# CUSTOM CYBERPUNK CSS
# -----------------------------

st.markdown("""
<style>

body {
    background-color: #000000;
}

.stApp {
    background: linear-gradient(180deg, #000000, #050505);
    color: white;
}

/* Title Neon Glow */
.title {
    text-align: center;
    font-size: 50px;
    font-weight: bold;
    color: #00ffff;
    text-shadow: 
        0 0 10px #00ffff,
        0 0 20px #00ffff,
        0 0 40px #00ffff;
}

/* Neon box */
.neon-box {
    border: 2px solid #00ffff;
    border-radius: 12px;
    padding: 20px;
    background-color: #050505;
    box-shadow:
        0 0 10px #00ffff,
        0 0 20px #00ffff;
}

/* Button styling */
div.stButton > button {
    background-color: black;
    color: #00ffff;
    border: 2px solid #00ffff;
    border-radius: 10px;
    padding: 10px 20px;
    font-size: 18px;
    transition: 0.3s;
    box-shadow: 0 0 10px #00ffff;
}

div.stButton > button:hover {
    background-color: #00ffff;
    color: black;
    box-shadow:
        0 0 20px #00ffff,
        0 0 40px #00ffff;
}

/* Text area styling */
textarea {
    background-color: black !important;
    color: #00ff9f !important;
    border: 2px solid #00ffff !important;
    box-shadow: 0 0 10px #00ffff;
    font-family: monospace;
}

/* Floating animation */
@keyframes float {
    0% {transform: translateY(0px);}
    50% {transform: translateY(-10px);}
    100% {transform: translateY(0px);}
}

.float {
    animation: float 3s ease-in-out infinite;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# TITLE
# -----------------------------

st.markdown('<p class="title float">🔐 AI SECURITY AUDIT AGENT</p>', unsafe_allow_html=True)

st.write("### Paste your code below and scan for vulnerabilities")

# -----------------------------
# CODE INPUT
# -----------------------------

code = st.text_area(
    "Code Input",
    height=300,
    placeholder="Paste your code here..."
)

# -----------------------------
# BUTTON
# -----------------------------
if st.button("🚀 Run Security Audit"):

    if code.strip() == "":
        st.warning("Please paste some code first.")
    else:
        with st.spinner("Scanning for vulnerabilities..."):

            result = run_security_audit(code)  # can be string, list, dict

        st.markdown('<div class="neon-box">', unsafe_allow_html=True)

        # Single report title
        st.markdown(
            '<h3 style="color:#ff66cc; text-shadow: 0 0 10px #ff66cc, 0 0 20px #ff66cc;">🧠 AI Security Report</h3>',
            unsafe_allow_html=True
        )

        # Function to format report properly
        def format_report(data, level=0):
            letters = 'abcdefghijklmnopqrstuvwxyz'
            roman = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x']
            indent = level * 25

            html = '<div style="color:#ff99cc; text-shadow: 0 0 2px #ff66cc; font-family: monospace; line-height:1.6;">'

            if isinstance(data, dict):
                # Numbered main headings
                for idx, (key, value) in enumerate(data.items(), start=1):
                    html += f'<b>{idx}. {key}:</b><br>'
                    html += format_report(value, level=1)
                    html += '<br>'
            elif isinstance(data, list):
                html += f'<ul style="list-style-type:none; padding-left:{indent}px;">'
                for i, item in enumerate(data):
                    # Level 1 -> letters, Level 2 -> roman numerals, deeper -> bullets
                    if level == 1:
                        html += f'<li>{letters[i]}. {format_report(item, level+1)}</li>'
                    elif level == 2:
                        html += f'<li>{roman[i]}. {format_report(item, level+1)}</li>'
                    else:
                        html += f'<li>{format_report(item, level+1)}</li>'
                html += '</ul>'
            else:
                # Split long strings into lettered/roman subpoints automatically
                lines = [line.strip() for line in str(data).split('. ') if line.strip()]
                if len(lines) > 1 and level >= 1:
                    html += f'<ul style="list-style-type:none; padding-left:{indent}px;">'
                    for i, line in enumerate(lines):
                        if level == 1:
                            html += f'<li>{letters[i]}. {line}</li>'
                        elif level == 2:
                            html += f'<li>{roman[i]}. {line}</li>'
                        else:
                            html += f'<li>{line}</li>'
                    html += '</ul>'
                else:
                    html += f'{data}<br>'

            html += '</div>'
            return html

        st.markdown(format_report(result), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<hr style="border:1px solid #00ffff">

<center style="color:#00ffff">
AI Powered Cybersecurity Scanner • Hackathon Demo
</center>
""", unsafe_allow_html=True)