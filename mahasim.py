"""
MahaSim — Maharashtra Simulation Engine
चोटा पॅकेट, बडा धमाका 🌾
"""

import streamlit as st
import json
import time
import os
from openai import OpenAI

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MahaSim — Maharashtra Simulation Engine",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Styling ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tiro+Devanagari+Marathi&family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --saffron: #FF6B1A;
    --deep-saffron: #E85D04;
    --turmeric: #F4A228;
    --leaf: #2D6A4F;
    --soil: #5C3317;
    --cream: #FFF8F0;
    --charcoal: #1A1A2E;
    --mist: #F0EAE2;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--cream);
}

.main { background-color: var(--cream); }

/* Header */
.mahasim-header {
    background: linear-gradient(135deg, var(--deep-saffron) 0%, var(--turmeric) 100%);
    padding: 2rem 2.5rem;
    border-radius: 16px;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.mahasim-header::before {
    content: "🌾";
    position: absolute;
    right: 2rem;
    top: 50%;
    transform: translateY(-50%);
    font-size: 5rem;
    opacity: 0.2;
}
.mahasim-header h1 {
    font-family: 'Space Mono', monospace;
    color: white;
    font-size: 2.2rem;
    margin: 0;
    letter-spacing: -1px;
}
.mahasim-header p {
    color: rgba(255,255,255,0.85);
    font-size: 1rem;
    margin: 0.4rem 0 0 0;
    font-family: 'Tiro Devanagari Marathi', serif;
}

/* Persona cards */
.persona-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.8rem;
    margin: 1rem 0;
}
.persona-card {
    background: white;
    border: 2px solid var(--mist);
    border-radius: 12px;
    padding: 1rem;
    cursor: pointer;
    transition: all 0.2s;
    text-align: center;
}
.persona-card:hover, .persona-card.active {
    border-color: var(--saffron);
    background: var(--cream);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(255,107,26,0.15);
}
.persona-card .emoji { font-size: 2rem; }
.persona-card .title { font-weight: 600; font-size: 0.9rem; color: var(--charcoal); margin-top: 0.3rem; }
.persona-card .marathi { font-family: 'Tiro Devanagari Marathi', serif; font-size: 0.75rem; color: #888; }

/* Agent message bubbles */
.agent-bubble {
    background: white;
    border-left: 4px solid var(--saffron);
    border-radius: 0 12px 12px 0;
    padding: 0.8rem 1rem;
    margin: 0.6rem 0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
.agent-name {
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    font-weight: 700;
    color: var(--deep-saffron);
    margin-bottom: 0.3rem;
}
.agent-role {
    font-size: 0.7rem;
    color: #999;
    font-style: italic;
}
.agent-text {
    font-family: 'Tiro Devanagari Marathi', serif;
    font-size: 1rem;
    color: var(--charcoal);
    line-height: 1.6;
}

/* Verdict box */
.verdict-box {
    background: linear-gradient(135deg, var(--leaf) 0%, #40916C 100%);
    color: white;
    padding: 1.5rem 2rem;
    border-radius: 16px;
    margin-top: 1.5rem;
}
.verdict-box h3 {
    font-family: 'Space Mono', monospace;
    font-size: 1rem;
    opacity: 0.8;
    margin: 0 0 0.5rem 0;
    text-transform: uppercase;
    letter-spacing: 2px;
}
.verdict-text {
    font-family: 'Tiro Devanagari Marathi', serif;
    font-size: 1.15rem;
    line-height: 1.7;
}

/* Round divider */
.round-header {
    background: var(--mist);
    border-radius: 8px;
    padding: 0.4rem 1rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    color: #888;
    margin: 1rem 0 0.5rem 0;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* Sidebar */
.stSidebar { background-color: var(--charcoal) !important; }

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, var(--deep-saffron), var(--turmeric));
    color: white;
    border: none;
    border-radius: 10px;
    padding: 0.6rem 2rem;
    font-family: 'Space Mono', monospace;
    font-weight: 700;
    font-size: 0.9rem;
    letter-spacing: 0.5px;
    transition: all 0.2s;
    width: 100%;
}
.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 15px rgba(232,93,4,0.4);
}

.stat-box {
    background: white;
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
    border: 1px solid var(--mist);
}
.stat-num { font-family: 'Space Mono', monospace; font-size: 1.8rem; color: var(--saffron); font-weight: 700; }
.stat-label { font-size: 0.75rem; color: #888; margin-top: 0.2rem; }
</style>
""", unsafe_allow_html=True)

# ─── Persona Definitions ─────────────────────────────────────────────────────
PERSONAS = {
    "🌾 Shetkari": {
        "marathi": "शेतकरी",
        "desc": "Farmer — crop prices, MSP, rain, loans",
        "agent_types": [
            "Vidarbha cotton farmer", "Nashik grape grower", "Marathwada soybean farmer",
            "Sugarcane farmer near Kolhapur", "Onion farmer near Nashik",
            "Farm labour activist", "Agricultural cooperative leader",
            "Village sarpanch with farming land", "Kisan sabha organiser",
            "Young farmer using tech"
        ],
        "system_context": "You are simulating Maharashtra farmers discussing agricultural news. Agents speak in Marathi mixed with local dialect. They care about MSP, rainfall, loans, mandi prices, fertiliser costs, and government schemes like PM-KISAN.",
        "verdict_prompt": "Based on the simulation, what is the collective farmer sentiment? Will they benefit or suffer? What action will they take?"
    },
    "🏛️ Politician": {
        "marathi": "राजकारणी",
        "desc": "Politician — seat safety, alliance, votes",
        "agent_types": [
            "BJP MLA from Vidarbha", "Shiv Sena (Thackeray) corporator from Mumbai",
            "NCP (Sharad) veteran leader", "Congress district president",
            "Independent MLA with swing votes", "BJP shakha pramukh",
            "Mahayuti alliance coordinator", "MVA campaign strategist",
            "Rebel party worker", "Young politician eyeing next election"
        ],
        "system_context": "You are simulating Maharashtra politicians analysing a political development. Agents are calculating, strategic, focused on seat safety, vote banks, and alliance dynamics. Mix of Marathi and political jargon.",
        "verdict_prompt": "Based on simulation, which political camp benefits most? What is the likely political outcome? Who gains, who loses?"
    },
    "📣 Supporter": {
        "marathi": "समर्थक",
        "desc": "Party supporter — rally, emotion, loyalty",
        "agent_types": [
            "Die-hard Thackeray Sainik", "Committed BJP karyakarta",
            "Sharad Pawar loyalist from western Maharashtra", "Congress social media warrior",
            "Maratha agitation supporter", "OBC rights activist",
            "Hindu nationalist youth", "Ambedkarite Buddhist voter",
            "Warkari community member", "First-time young voter"
        ],
        "system_context": "You are simulating passionate Maharashtra political supporters reacting to news. Agents are emotional, loyal, opinionated. Heavy Marathi, WhatsApp-forward style language. Strong opinions.",
        "verdict_prompt": "What is the emotional temperature of supporters? Which side is more energised? What will they do next — rally, share news, vote?"
    },
    "📰 Reporter": {
        "marathi": "पत्रकार",
        "desc": "Reporter — story angles, public reaction, impact",
        "agent_types": [
            "Sakal political correspondent", "Loksatta senior editor",
            "Maharashtra Times rural reporter", "TV9 Marathi anchor",
            "Digital news portal journalist", "Investigative reporter",
            "Opposition beat reporter", "Government press room journalist",
            "Freelance journalist from Aurangabad", "Photo journalist"
        ],
        "system_context": "You are simulating Maharashtra journalists analysing a story. Agents discuss news angles, public reaction, political impact. Professional Marathi with journalistic perspective. They debate what the real story is.",
        "verdict_prompt": "What is the main news story? What angles will different outlets pursue? What will public reaction be in 24 hours, 1 week?"
    },
    "🗳️ Voter": {
        "marathi": "मतदार",
        "desc": "Voter — who to vote for, policy impact on life",
        "agent_types": [
            "Undecided urban voter from Pune", "Rural woman voter, Ladki Bahin beneficiary",
            "Young first-time voter", "Maratha community voter",
            "Dalit Buddhist voter", "Muslim voter from Aurangabad",
            "OBC voter from Nashik", "Senior citizen BJP loyalist",
            "Working class voter from Mumbai", "Upper middle class disillusioned voter"
        ],
        "system_context": "You are simulating ordinary Maharashtra voters discussing an issue. Agents are common people — not politicians. They talk about how this affects their daily life, job, family, future. Authentic Marathi with everyday language.",
        "verdict_prompt": "How will this issue affect voting decisions? Which party benefits from voter sentiment? What do ordinary people actually feel about this?"
    },
    "😄 Timepass": {
        "marathi": "टाइमपास",
        "desc": "What if scenarios — fun, viral, crazy predictions",
        "agent_types": [
            "Puneri social media influencer", "Mumbai college student",
            "Cricket-obsessed Maharashtra fan", "Marathi meme page admin",
            "Auto rickshaw driver philosopher", "Chai tapri owner",
            "IT employee from Pune", "Housewife with strong opinions",
            "Retired government officer", "Village youth with smartphone"
        ],
        "system_context": "You are simulating fun, opinionated Maharashtra people discussing a wild 'what if' scenario. Casual Marathi, lots of humour, cricket references, Puneri style bluntness. WhatsApp group energy. Keep it entertaining.",
        "verdict_prompt": "What is the funniest/most unexpected prediction from this scenario? What would go viral on Maharashtra WhatsApp groups?"
    }
}

# ─── LLM Client ──────────────────────────────────────────────────────────────
def get_client(api_key, base_url):
    return OpenAI(api_key=api_key, base_url=base_url)

def llm_call(client, model, messages, max_tokens=800, retries=3):
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=0.85
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            err = str(e)
            if "429" in err and attempt < retries - 1:
                wait = (attempt + 1) * 8
                time.sleep(wait)
                continue
            return f"[Error: {err}]"
    return "[Error: Max retries reached]"

# ─── Simulation Functions (BATCHED — all rounds in ONE API call) ─────────────
def run_full_simulation(client, model, persona_key, seed_text, n_agents, n_rounds):
    """Single API call generates agents + all rounds + verdict. Saves ~80% of API quota."""
    import re
    persona = PERSONAS[persona_key]
    agent_types_str = "\n".join([f"- {a}" for a in persona["agent_types"][:n_agents]])

    prompt = f"""You are running a complete Maharashtra social simulation in ONE response.

PERSONA: {persona['marathi']} — {persona['system_context']}
SEED: {seed_text}

STEP 1 — Create {n_agents} agents from these types:
{agent_types_str}

STEP 2 — Simulate {n_rounds} rounds of discussion between agents.
Each round: all agents respond to each other. Disagree, debate, challenge. Authentic Marathi dialect.

STEP 3 — Write final verdict answering: {persona['verdict_prompt']}

Respond ONLY as this JSON (no extra text):
{{
  "agents": [
    {{
      "name": "Authentic Maharashtra name ONLY like Ramesh Deshmukh, Sunita Patil — NO Korean/foreign names",
      "type": "agent type from list",
      "location": "Maharashtra district/city",
      "background": "1-line background",
      "initial_opinion": "First reaction in Marathi (2 sentences)"
    }}
  ],
  "rounds": [
    {{
      "round": 1,
      "messages": [
        {{"name": "agent name", "message": "Marathi message (2-3 sentences)"}}
      ]
    }}
  ],
  "verdict": {{
    "marathi": "Final verdict in Marathi (3-4 sentences)",
    "english": "English summary (2 sentences)"
  }}
}}

CRITICAL: All agent names must be authentic Maharashtra Marathi names. All messages in Marathi script."""

    response = llm_call(client, model, [{"role": "user", "content": prompt}], max_tokens=4000)

    # Parse JSON
    match = re.search(r'\{.*\}', response, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except:
            pass

    # Fallback minimal structure
    return {
        "agents": [{"name": f"शेतकरी {i+1}", "type": persona["agent_types"][i % len(persona["agent_types"])],
                    "location": "Maharashtra", "background": "", "initial_opinion": "सिम्युलेशन सुरू होत आहे..."} 
                   for i in range(n_agents)],
        "rounds": [{"round": 1, "messages": [{"name": "System", "message": response[:300]}]}],
        "verdict": {"marathi": response[-300:], "english": "Simulation complete."}
    }

def parse_verdict(verdict_text):
    import re
    # Remove stray HTML tags
    verdict_text = re.sub(r'</?\w+>', '', verdict_text).strip()

    m_match = re.search(r'MARATHI_VERDICT[:\s]+(.*?)(?=ENGLISH_SUMMARY|$)', verdict_text, re.DOTALL | re.IGNORECASE)
    e_match = re.search(r'ENGLISH_SUMMARY[:\s]+(.*?)$', verdict_text, re.DOTALL | re.IGNORECASE)

    marathi = m_match.group(1).strip() if m_match else ""
    english = e_match.group(1).strip() if e_match else ""

    if not marathi:
        # Fallback: show full text, no english section
        cleaned = re.sub(r'(MARATHI_VERDICT|ENGLISH_SUMMARY)[:\s]*', '', verdict_text).strip()
        return cleaned, ""

    return marathi, english

# ─── Sidebar ──────────────────────────────────────────────────────────────────
# Load API key from Streamlit secrets if available
_default_key = ""
_default_model = "google/gemma-3n-e2b-it:free"
try:
    _default_key = st.secrets.get("OPENROUTER_API_KEY", "") or st.secrets.get("api_key", "")
except:
    pass

with st.sidebar:
    st.markdown("### ⚙️ Configuration")

    api_key = st.text_input("API Key", value=_default_key, type="password",
                             placeholder="sk-or-...",
                             help="OpenRouter API key")

    base_url = st.selectbox("API Provider", [
        "https://openrouter.ai/api/v1",
        "https://generativelanguage.googleapis.com/v1beta/openai/",
        "https://api.openai.com/v1"
    ])

    model = st.text_input("Model", value=_default_model,
                           help="Model name for your provider")
    
    st.divider()
    st.markdown("### 🎛️ Simulation Settings")
    n_agents = st.slider("Number of Agents", 4, 10, 6)
    n_rounds = st.slider("Simulation Rounds", 2, 8, 3)
    
    st.divider()
    st.markdown("""
    **🌾 MahaSim v1.0**  
    Maharashtra Simulation Engine  
    चोटा पॅकेट, बडा धमाका
    
    *Built for Maharashtra, by Maharashtra* 🧡
    """)

# ─── Main UI ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="mahasim-header">
    <h1>MahaSim</h1>
    <p>महाराष्ट्राचे डिजिटल सँडबॉक्स — Simulate. Predict. Understand.</p>
</div>
""", unsafe_allow_html=True)

# Persona Selection
st.markdown("### तुम्ही कोण आहात? / Who are you?")

persona_cols = st.columns(6)
persona_keys = list(PERSONAS.keys())

if "selected_persona" not in st.session_state:
    st.session_state.selected_persona = persona_keys[0]

for i, (col, key) in enumerate(zip(persona_cols, persona_keys)):
    with col:
        persona = PERSONAS[key]
        emoji = key.split()[0]
        name = key.split(" ", 1)[1]
        is_active = st.session_state.selected_persona == key
        border = "3px solid #FF6B1A" if is_active else "2px solid #F0EAE2"
        bg = "#FFF8F0" if is_active else "white"
        
        st.markdown(f"""
        <div style="background:{bg}; border:{border}; border-radius:12px; 
                    padding:0.8rem 0.5rem; text-align:center; margin-bottom:0.5rem;">
            <div style="font-size:1.8rem">{emoji}</div>
            <div style="font-weight:600; font-size:0.8rem; color:#1A1A2E; margin-top:0.3rem">{name}</div>
            <div style="font-family:'Tiro Devanagari Marathi',serif; font-size:0.7rem; color:#888">{persona['marathi']}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"Select", key=f"btn_{i}", use_container_width=True):
            st.session_state.selected_persona = key
            st.rerun()

selected = st.session_state.selected_persona
persona_data = PERSONAS[selected]

st.markdown(f"""
<div style="background:white; border-radius:10px; padding:0.8rem 1.2rem; 
            margin:0.5rem 0 1.5rem 0; border-left:4px solid #FF6B1A;">
    <b>{selected}</b> — {persona_data['desc']}
</div>
""", unsafe_allow_html=True)

# Seed Input
st.markdown("### बातमी / प्रश्न टाका — Enter News or Question")

seed_examples = {
    "🌾 Shetkari": "महाराष्ट्र सरकारने सोयाबीनचा हमीभाव ₹४,८९२ प्रति क्विंटल जाहीर केला. पण बाजारात फक्त ₹३,८०० मिळतोय.",
    "🏛️ Politician": "मनोज जरांगे यांनी मराठा आरक्षणासाठी पुन्हा उपोषण सुरू केले. विधानसभा निवडणुकीला ६ महिने बाकी आहेत.",
    "📣 Supporter": "उद्धव ठाकरेंनी जाहीर केले की ते पुढील निवडणुकीत स्वतंत्र लढणार, कोणाशीही युती नाही.",
    "📰 Reporter": "पुण्यात एका मोठ्या IT कंपनीने ५,००० कर्मचाऱ्यांना काढून टाकले. बहुतेक महाराष्ट्रातील तरुण आहेत. कंपनीने कोणतेही कारण दिले नाही.",
    "🗳️ Voter": "लाडकी बहीण योजनेत पात्रता निकष बदलले. आता फक्त BPL कार्डधारकांनाच फायदा मिळणार.",
    "😄 Timepass": "जर सचिन तेंडुलकर महाराष्ट्राचे मुख्यमंत्री झाले तर काय होईल?"
}

seed_text = st.text_area(
    "Seed (Marathi or English)",
    value=seed_examples.get(selected, ""),
    height=120,
    placeholder="बातमी, प्रश्न, किंवा what if scenario टाका...",
    help="Enter news, question, or scenario to simulate"
)

# Run Button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    run_sim = st.button("🚀 सिम्युलेशन सुरू करा — Start Simulation", use_container_width=True)

# ─── Simulation Execution ────────────────────────────────────────────────────
if run_sim:
    if not api_key:
        st.error("⚠️ API key घाला! Add your API key in the sidebar.")
        st.stop()
    
    if not seed_text.strip():
        st.error("⚠️ Seed text टाका!")
        st.stop()
    
    client = get_client(api_key, base_url)
    
    st.divider()
    st.markdown("## 🎬 Simulation चालू आहे...")
    
    # Stats row
    stat1, stat2, stat3, stat4 = st.columns(4)
    agents_metric = stat1.empty()
    rounds_metric = stat2.empty()
    messages_metric = stat3.empty()
    status_metric = stat4.empty()
    
    agents_metric.markdown(f"""<div class="stat-box">
        <div class="stat-num">{n_agents}</div>
        <div class="stat-label">Agents</div></div>""", unsafe_allow_html=True)
    rounds_metric.markdown(f"""<div class="stat-box">
        <div class="stat-num">{n_rounds}</div>
        <div class="stat-label">Rounds</div></div>""", unsafe_allow_html=True)
    messages_metric.markdown(f"""<div class="stat-box">
        <div class="stat-num">0</div>
        <div class="stat-label">Messages</div></div>""", unsafe_allow_html=True)
    status_metric.markdown(f"""<div class="stat-box">
        <div class="stat-num">⚙️</div>
        <div class="stat-label">Building agents...</div></div>""", unsafe_allow_html=True)
    
    # ── SINGLE BATCHED API CALL — agents + rounds + verdict in one shot ──
    status_metric.markdown('''<div class="stat-box">
        <div class="stat-num">⚙️</div>
        <div class="stat-label">Simulating...</div></div>''', unsafe_allow_html=True)

    with st.spinner("🌾 Maharashtra simulation चालू आहे... (1 API call)"):
        result = run_full_simulation(client, model, selected, seed_text, n_agents, n_rounds)

    agents   = result.get("agents", [])
    rounds   = result.get("rounds", [])
    verdict  = result.get("verdict", {})
    total_messages = sum(len(r.get("messages", [])) for r in rounds)

    # Update stats
    agents_metric.markdown(f'''<div class="stat-box">
        <div class="stat-num">{len(agents)}</div>
        <div class="stat-label">Agents</div></div>''', unsafe_allow_html=True)
    rounds_metric.markdown(f'''<div class="stat-box">
        <div class="stat-num">{len(rounds)}</div>
        <div class="stat-label">Rounds</div></div>''', unsafe_allow_html=True)
    messages_metric.markdown(f'''<div class="stat-box">
        <div class="stat-num">{total_messages}</div>
        <div class="stat-label">Messages</div></div>''', unsafe_allow_html=True)
    status_metric.markdown('''<div class="stat-box">
        <div class="stat-num">✅</div>
        <div class="stat-label">Done!</div></div>''', unsafe_allow_html=True)

    # Show agents
    st.markdown("### 🧑‍🤝‍🧑 Simulation Agents")
    agent_cols = st.columns(min(len(agents), 4))
    for i, agent in enumerate(agents):
        with agent_cols[i % len(agent_cols)]:
            st.markdown(f"""
            <div style="background:white; border-radius:10px; padding:0.8rem;
                        margin-bottom:0.5rem; border-top:3px solid #FF6B1A;
                        box-shadow:0 2px 8px rgba(0,0,0,0.05);">
                <div style="font-weight:700; color:#1A1A2E">{agent.get('name','Agent')}</div>
                <div style="font-size:0.75rem; color:#FF6B1A">{agent.get('type','')}</div>
                <div style="font-size:0.7rem; color:#888">📍 {agent.get('location','')}</div>
                <div style="font-size:0.8rem; margin-top:0.5rem; font-style:italic; color:#555">
                    {agent.get('background','')[:80]}</div>
            </div>""", unsafe_allow_html=True)

    # Show initial opinions
    st.markdown("### 💬 Initial Reactions")
    for agent in agents:
        if agent.get('initial_opinion'):
            st.markdown(f"""
            <div class="agent-bubble">
                <div class="agent-name">{agent.get('name','')}
                    <span class="agent-role">— {agent.get('type','')} ({agent.get('location','')})</span>
                </div>
                <div class="agent-text">{agent.get('initial_opinion','')}</div>
            </div>""", unsafe_allow_html=True)

    # Show rounds
    st.markdown("### 🔄 Simulation Rounds")
    for round_data in rounds:
        rnum = round_data.get("round", "")
        st.markdown(f'<div class="round-header">⚡ Round {rnum} / {len(rounds)}</div>',
                   unsafe_allow_html=True)
        for msg in round_data.get("messages", []):
            agent_info = next((a for a in agents if a.get('name') == msg.get('name')), {})
            st.markdown(f"""
            <div class="agent-bubble">
                <div class="agent-name">{msg.get('name','')}
                    <span class="agent-role">— {agent_info.get('type','')} ({agent_info.get('location','')})</span>
                </div>
                <div class="agent-text">{msg.get('message','')}</div>
            </div>""", unsafe_allow_html=True)

    # Verdict
    st.markdown("### 🏆 Final Verdict")
    import re as _re
    marathi_verdict = _re.sub(r'<[^>]+>', '', verdict.get("marathi", "")).strip()
    english_summary = _re.sub(r'<[^>]+>', '', verdict.get("english", "")).strip()
    st.markdown('<div class="verdict-box"><h3>🎯 Simulation Verdict</h3>', unsafe_allow_html=True)
    st.markdown(f'<div class="verdict-text">{marathi_verdict}</div>', unsafe_allow_html=True)
    if english_summary:
        st.markdown(f'<div style="color:white;opacity:0.85;font-size:0.95rem;margin-top:1rem">{english_summary}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Share text
    st.markdown("### 📤 WhatsApp वर शेअर करा")
    share_text = f"🌾 MahaSim Result\n\nScenario: {seed_text[:100]}...\n\nVerdict: {english_summary}\n\n#MahaSim #Maharashtra"
    st.text_area("Copy & Share:", value=share_text, height=120)
    
    st.success("✅ सिम्युलेशन पूर्ण झाले! Simulation complete!")

# ─── Empty state ─────────────────────────────────────────────────────────────
else:
    st.markdown("""
    <div style="text-align:center; padding:3rem; color:#888;">
        <div style="font-size:3rem">🌾</div>
        <div style="font-size:1.2rem; font-weight:600; margin:1rem 0">
            तुमची भूमिका निवडा, बातमी टाका, सुरू करा
        </div>
        <div style="font-size:0.9rem">
            Choose your persona → Enter news or scenario → Hit Start
        </div>
    </div>
    """, unsafe_allow_html=True)
