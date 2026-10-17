import streamlit as st
import html
from pathlib import Path

# ══════════════════════════════════════════════════════════════
# 1) إعدادات الصفحة
# ══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Omnia DeepArena IA",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ══════════════════════════════════════════════════════════════
# 2) التصميم السينمائي (CSS)
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
:root { --neon:#00ff88; --cyan:#00d4ff; --gold:#ffaa00; --ink:#eaf6f0; --muted:#b4c7bf; }
.stApp {
    background:
        radial-gradient(1000px 560px at 8% -8%, rgba(0,255,136,.13), transparent 60%),
        radial-gradient(900px 600px at 100% 108%, rgba(0,212,255,.11), transparent 60%),
        linear-gradient(160deg, #040a18 0%, #01100a 100%);
    background-attachment: fixed; color: var(--ink);
}
[data-testid="stHeader"] { background: transparent; }
footer { visibility: hidden; }
.block-container { padding-top: 1.5rem; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: rgba(255,255,255,.04) !important;
    backdrop-filter: blur(16px);
    border-inline-end: 1px solid rgba(0,255,136,.18);
}
[data-testid="stSidebar"] label p { color: var(--ink) !important; }
[data-testid="stSidebar"] div[data-baseweb="select"] > div {
    background: rgba(255,255,255,.06) !important;
    border: 1px solid rgba(0,255,136,.25) !important;
}

/* Hero */
.hero {
    position: relative; overflow: hidden;
    padding: 40px 26px; margin-bottom: 20px; border-radius: 22px;
    border: 1px solid rgba(0,255,136,.25);
    background-image: linear-gradient(135deg, rgba(4,10,24,.88) 0%, rgba(1,16,10,.75) 100%), url("https://images.unsplash.com/photo-1522778119026-d647f0596c20?w=1600&q=80&auto=format&fit=crop");
    background-size: cover; background-position: center;
    backdrop-filter: blur(14px);
    box-shadow: 0 20px 60px rgba(0,0,0,.55), 0 0 40px rgba(0,255,136,.10);
}
.hero-title { font-size: clamp(1.55rem, 5vw, 2.6rem); font-weight: 800; line-height: 1.25; }
.hero-text {
    background: linear-gradient(90deg, var(--neon), var(--cyan), var(--neon));
    background-size: 200% auto; -webkit-background-clip: text; background-clip: text;
    -webkit-text-fill-color: transparent; animation: shimmer 4s linear infinite;
}
@keyframes shimmer { 0%{background-position:0% center} 100%{background-position:200% center} }
.hero-sub { color: var(--muted); margin-top: 10px; font-size: .98rem; line-height: 1.75; max-width: 720px; }
.hero-line { height: 2px; margin-top: 16px; background: linear-gradient(90deg, var(--neon), transparent); box-shadow: 0 0 14px var(--neon); }

/* Cards */
.glass-card {
    background: rgba(255,255,255,.05); backdrop-filter: blur(14px);
    border: 1px solid rgba(0,255,136,.18); border-radius: 18px;
    padding: 0; margin-bottom: 12px;
    box-shadow: 0 8px 32px rgba(0,0,0,.4);
    transition: all .25s ease;
}
.glass-card:hover {
    transform: translateY(-4px); border-color: var(--neon);
    box-shadow: 0 16px 44px rgba(0,255,136,.22);
}
.card-img { width: 100%; height: 120px; object-fit: cover; border-radius: 18px 18px 0 0; filter: brightness(.7); }
.card-body { padding: 15px 20px 20px 20px; }
.card-title { color: var(--neon); font-weight: 800; font-size: 1.1rem; }
.card-desc { color: #dbe7e1; font-size: .85rem; line-height: 1.6; margin-top: 6px; }
.price-badge {
    display: inline-block; margin-top: 12px; padding: 6px 16px;
    background: linear-gradient(135deg, #ffcc44, #ff6600);
    color: #000; font-weight: 900; border-radius: 20px;
    box-shadow: 0 4px 15px rgba(255,170,0,.5);
}

/* Buttons */
div.stButton > button {
    width: 100%; background: rgba(0,255,136,.06); color: var(--neon);
    border: 1px solid rgba(0,255,136,.4); border-radius: 12px; font-weight: 600;
    transition: all .2s ease;
}
div.stButton > button:hover {
    background: rgba(0,255,136,.16); border-color: var(--neon); color: #fff;
    box-shadow: 0 0 20px rgba(0,255,136,.45); transform: translateY(-1px);
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# 3) قاموس اللغات (4 باقات فقط)
# ══════════════════════════════════════════════════════════════
LANG_DATA = {
    "🇸🇦 العربية": {
        "title": "🏟️ Omnia DeepArena الرقمية العالمية",
        "sub": "⚽ كل ما يهم كرة القدم — وكرة القدم فقط. تصفح الباقات واللوائح بسهولة.",
        "music": "🎵 الأجواء والموسيقى",
        "open": "🚀 فتح الخدمة",
        "soon": "🛠️ قيد الإعداد",
        "p1_title": "🥅 باقة الناشئين", "p1_desc": "مجاناً دون 16 سنة بموافقة الولي والـ GDPR.", "p1_price": "20$/ش",
        "p2_title": "👟 باقة اللاعبين الكبار", "p2_desc": "تتبع YOLO26 والجاهزية البدنية الكاملة.", "p2_price": "30$/ش",
        "p3_title": "📡 باقة الكشافين", "p3_desc": "رادار الفرز وقنوات التفاوض المشفرة.", "p3_price": "50$/ش",
        "p4_title": "🏟️ أندية الهواة", "p4_desc": "لوحة المدرب ومحرك الريمونتادا (VIP).", "p4_price": "150$/ش"
    },
    "🇬🇧 English": {
        "title": "🏟️ Omnia DeepArena Global",
        "sub": "⚽ Everything that matters in football — and only football.",
        "music": "🎵 Audio HUD & Atmosphere",
        "open": "🚀 Open service",
        "soon": "🛠️ Coming soon",
        "p1_title": "🥅 Youth Pack", "p1_desc": "Free under 16 with Parental Consent & GDPR.", "p1_price": "$20/Mo",
        "p2_title": "👟 Seniors Pack", "p2_desc": "YOLO26 Kinematic Tracking & Readiness.", "p2_price": "$30/Mo",
        "p3_title": "📡 Scouts Market", "p3_desc": "Ingestion Radar & Encrypted Channels.", "p3_price": "$50/Mo",
        "p4_title": "🏟️ Amateur Clubs", "p4_desc": "Coach HUD & Remontada Engine (VIP).", "p4_price": "$150/Mo"
    },
    "🇫🇷 Français": {
        "title": "🏟️ Omnia DeepArena Mondiale",
        "sub": "⚽ Tout ce qui compte pour le football — et rien que le football.",
        "music": "🎵 Ambiance & Audio HUD",
        "open": "🚀 Ouvrir le service",
        "soon": "🛠️ Bientôt",
        "p1_title": "🥅 Pack Jeunes", "p1_desc": "Gratuit -16 ans avec Consentement & GDPR.", "p1_price": "20$/M",
        "p2_title": "👟 Pack Seniors", "p2_desc": "Suivi YOLO26 & Préparation Physique.", "p2_price": "30$/M",
        "p3_title": "📡 Recruteurs", "p3_desc": "Radar d'Ingestion & Canaux Chiffrés.", "p3_price": "50$/M",
        "p4_title": "🏟️ Clubs Amateurs", "p4_desc": "HUD Entraîneur & Remontada (VIP).", "p4_price": "150$/M"
    },
    "🇪🇸 Español": {
        "title": "🏟️ Omnia DeepArena Global",
        "sub": "⚽ Todo lo que importa en el fútbol — y solo fútbol.",
        "music": "🎵 Audio HUD y Atmósfera",
        "open": "🚀 Abrir servicio",
        "soon": "🛠️ Próximamente",
        "p1_title": "🥅 Paquete Juvenil", "p1_desc": "Gratis -16 años con Consentimiento & GDPR.", "p1_price": "20$/M",
        "p2_title": "👟 Paquete Seniors", "p2_desc": "YOLO26 y Preparación Física.", "p2_price": "30$/M",
        "p3_title": "📡 Ojeadores", "p3_desc": "Radar y Canales Cifrados.", "p3_price": "50$/M",
        "p4_title": "🏟️ Amateurs", "p4_desc": "HUD Entrenador y Remontada (VIP).", "p4_price": "150$/M"
    },
    "🇮🇹 Italiano": {
        "title": "🏟️ Omnia DeepArena Globale",
        "sub": "⚽ Tutto ciò che conta nel calcio — e solo il calcio.",
        "music": "🎵 Audio HUD & Atmosfera",
        "open": "🚀 Apri servizio",
        "soon": "🛠️ In arrivo",
        "p1_title": "🥅 Giovani", "p1_desc": "Gratis -16 con Consenso & GDPR.", "p1_price": "20$/M",
        "p2_title": "👟 Seniors", "p2_desc": "YOLO26 e Preparazione Fisica.", "p2_price": "30$/M",
        "p3_title": "📡 Scout", "p3_desc": "Radar e Canali Crittografati.", "p3_price": "50$/M",
        "p4_title": "🏟️ Dilettanti", "p4_desc": "HUD Allenatore e Remontada (VIP).", "p4_price": "150$/M"
    },
    "🇵🇹 Português": {
        "title": "🏟️ Omnia DeepArena Global",
        "sub": "⚽ Tudo o que importa no futebol — e só futebol.",
        "music": "🎵 Áudio HUD & Atmosfera",
        "open": "🚀 Abrir serviço",
        "soon": "🛠️ Em breve",
        "p1_title": "🥅 Juvenil", "p1_desc": "Grátis -16 com Consentimento & GDPR.", "p1_price": "20$/M",
        "p2_title": "👟 Seniors", "p2_desc": "YOLO26 e Prontidão Física.", "p2_price": "30$/M",
        "p3_title": "📡 Olheiros", "p3_desc": "Radar e Canais Cifrados.", "p3_price": "50$/M",
        "p4_title": "🏟️ Amadores", "p4_desc": "HUD Treinador e Remontada (VIP).", "p4_price": "150$/M"
    }
}

# ══════════════════════════════════════════════════════════════
# 4) لوحة الحقوق (المترجمة)
# ══════════════════════════════════════════════════════════════
LEGAL_TEXTS = {
    "🇸🇦 العربية": {"title": "الحقوق المالية والامتثال (FIFA Solidarity)", "desc": "منصة Omnia تضمن الحقوق المالية والقانونية تلقائياً بموجب قوانين الفيفا.", "s1": "FIFA Solidarity", "s1d": "2.5% Youth Academy Rights", "s2": "Player Equity", "s2d": "Tokenized Shares (2.5% Fee)", "s3": "GDPR Shield", "s3d": "100% Data Protection"},
    "🇬🇧 English": {"title": "Financial Rights & Compliance (FIFA Solidarity)", "desc": "Omnia automatically guarantees all financial and legal rights under FIFA laws.", "s1": "FIFA Solidarity", "s1d": "2.5% Youth Academy Rights", "s2": "Player Equity", "s2d": "Tokenized Shares (2.5% Fee)", "s3": "GDPR Shield", "s3d": "100% Data Protection"},
    "🇫🇷 Français": {"title": "Droits Financiers & Conformité", "desc": "Omnia garantit automatiquement tous les droits financiers et juridiques.", "s1": "Solidarité FIFA", "s1d": "2.5% Droits Académie", "s2": "Équité Joueur", "s2d": "Actions Tokénisées (2.5%)", "s3": "Bouclier RGPD", "s3d": "100% Protection"},
    "🇪🇸 Español": {"title": "Derechos Financieros y Cumplimiento", "desc": "Omnia garantiza automáticamente todos los derechos financieros y legales.", "s1": "Solidaridad FIFA", "s1d": "2.5% Derechos Academia", "s2": "Equidad Jugador", "s2d": "Acciones Tokenizadas (2.5%)", "s3": "Escudo GDPR", "s3d": "100% Protección"},
    "🇮🇹 Italiano": {"title": "Diritti Finanziari e Conformità", "desc": "Omnia garantisce automaticamente tutti i diritti finanziari e legali.", "s1": "Solidarietà FIFA", "s1d": "2.5% Diritti Accademia", "s2": "Equità Giocatore", "s2d": "Azioni Tokenizzate (2.5%)", "s3": "Scudo GDPR", "s3d": "100% Protezione"},
    "🇵🇹 Português": {"title": "Direitos Financeiros e Conformidade", "desc": "A Omnia garante automaticamente todos os direitos financeiros e legais.", "s1": "Solidariedade FIFA", "s1d": "2.5% Direitos Academia", "s2": "Equidade Jogador", "s2d": "Ações Tokenizadas (2.5%)", "s3": "Escudo GDPR", "s3d": "100% Proteção"}
}

# ══════════════════════════════════════════════════════════════
# 5) الشريط الجانبي والتحكم
# ══════════════════════════════════════════════════════════════
if "lang" not in st.session_state:
    st.session_state.lang = "🇸🇦 العربية"

lang_options = list(LANG_DATA.keys())
lang_idx = lang_options.index(st.session_state.lang)
selected_lang = st.sidebar.selectbox("🌐 Language / اللغة", lang_options, index=lang_idx)

if selected_lang != st.session_state.lang:
    st.session_state.lang = selected_lang
    st.rerun()

# جلب البيانات بناءً على اللغة
d = LANG_DATA[st.session_state.lang]
lt = LEGAL_TEXTS[st.session_state.lang]

st.sidebar.markdown("---")
st.sidebar.markdown(f"### {d['music']}")
if st.sidebar.button("▶️ Play Music"):
    st.sidebar.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
st.sidebar.markdown("---")
st.sidebar.success("🚀 Omnia DeepArena IA")

# ══════════════════════════════════════════════════════════════
# 6) الواجهة الرئيسية (Hero)
# ══════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="hero">
    <div class="hero-title">
        <span style="font-size: 2rem;">⚽</span> <span class="hero-text">{d['title']}</span>
    </div>
    <div class="hero-sub">{d['sub']}</div>
    <div class="hero-line"></div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# 7) عرض الباقات الأربعة (مع المسارات الصحيحة)
# ══════════════════════════════════════════════════════════════
col1, col2 = st.columns(2, gap="large")

with col1:
    # الباقة 1
    st.markdown(f"""
    <div class="glass-card">
        <img class="card-img" src="https://images.unsplash.com/photo-1517466787929-bc90951d0974?w=600&q=80">
        <div class="card-body">
            <div class="card-title">{d['p1_title']}</div>
            <div class="card-desc">{d['p1_desc']}</div>
            <div class="price-badge">{d['p1_price']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button(d['open'], key="btn1"):
        st.switch_page("pages/1_Youth.py")

    # الباقة 3
    st.markdown(f"""
    <div class="glass-card" style="margin-top: 20px;">
        <img class="card-img" src="https://images.unsplash.com/photo-1552667466-07770ae110d0?w=600&q=80">
        <div class="card-body">
            <div class="card-title">{d['p3_title']}</div>
            <div class="card-desc">{d['p3_desc']}</div>
            <div class="price-badge">{d['p3_price']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button(d['open'], key="btn1"):
        st.switch_page("pages/1_Youth.py")

with col2:
    # الباقة 2
    st.markdown(f"""
    <div class="glass-card">
        <img class="card-img" src="https://images.unsplash.com/photo-1579952363873-27f3bade9f55?w=600&q=80">
        <div class="card-body">
            <div class="card-title">{d['p2_title']}</div>
            <div class="card-desc">{d['p2_desc']}</div>
            <div class="price-badge">{d['p2_price']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
        if st.button(d['open'], key="btn1"):
        st.switch_page("pages/1_Youth.py")

    # الباقة 4
    st.markdown(f"""
    <div class="glass-card" style="margin-top: 20px;">
        <img class="card-img" src="https://images.unsplash.com/photo-1459865264687-595d652de67e?w=600&q=80">
        <div class="card-body">
            <div class="card-title">{d['p4_title']}</div>
            <div class="card-desc">{d['p4_desc']}</div>
            <div class="price-badge">{d['p4_price']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
        if st.button(d['open'], key="btn1"):
        st.switch_page("pages/1_Youth.py")

# ══════════════════════════════════════════════════════════════
# 8) لوحة الحقوق المالية (في الأسفل)
# ══════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown(f"### 🏛️ {lt['title']}")

st.markdown(f"""
<div style="background: rgba(255, 170, 0, 0.05); border: 2px solid #ffaa00; border-radius: 15px; padding: 20px; text-align: center;">
    <h4 style="color: #ffaa00; margin-top: 0;">⚖️ Omnia LawTech & FinTech Core</h4>
    <p style="color: #dbe7e1; font-size: 0.95rem;">{lt['desc']}</p>
    <div style="display: flex; justify-content: space-around; flex-wrap: wrap; margin-top: 15px;">
        <div style="margin: 10px;">
            <span style="font-size: 1.5rem;">🤝</span><br>
            <b style="color:#00ff88;">{lt['s1']}</b><br>
            <span style="color:#aaa; font-size: 0.85rem;">{lt['s1d']}</span>
        </div>
        <div style="margin: 10px;">
            <span style="font-size: 1.5rem;">📊</span><br>
            <b style="color:#00ff88;">{lt['s2']}</b><br>
            <span style="color:#aaa; font-size: 0.85rem;">{lt['s2d']}</span>
        </div>
        <div style="margin: 10px;">
            <span style="font-size: 1.5rem;">🛡️</span><br>
            <b style="color:#00ff88;">{lt['s3']}</b><br>
            <span style="color:#aaa; font-size: 0.85rem;">{lt['s3d']}</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
