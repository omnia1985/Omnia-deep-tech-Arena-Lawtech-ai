import streamlit as st
import html

# ==========================================
# 1. إعدادات الصفحة
# ==========================================
st.set_page_config(
    page_title="Omnia DeepArena IA",
    layout="wide",
    page_icon="⚽",
    initial_sidebar_state="expanded"
)

def esc(t):
    return html.escape(str(t)).replace("$", "&#36;")

# ==========================================
# 2. قاموس اللغات الست (الترجمة الكاملة)
# ==========================================
LANG_DATA = {
    "🇸🇦 العربية": {
        "title1": "نصنع مادة تصدير جديدة:",
        "title2": "المواهب الرياضية الرقمية",
        "sub": "نحن لا نبيع اشتراكات برمجية. نحن نصنع خط إنتاج رقمي لتصدير المواهب. نكتشف لاعب الأزقة، ونؤهله رقمياً، ونمنع ضياعه (نمنع صفقات فاشلة مثل هازارد)، لنربط المواهب العربية بالأندية العالمية بناءً على بيانات دقيقة.",
        "choose": "اختر بوابتك للانطلاق 🚀",
        "c1_title": "بوابة الناشئين (أقل من 16)",
        "c1_desc": "حلل مستواك، احمِ بياناتك (GDPR)، واحصل على بطاقة رقمية وتشبيه بالنجوم العالميين.",
        "c1_btn": "دخول بوابة الناشئين",
        "c2_title": "بوابة الاحتراف (16+ سنة)",
        "c2_desc": "تحليل متقدم، بطاقة بيانات احترافية، وتقييم سوقي. ظهور طوعي في جدول السوق.",
        "c2_btn": "دخول بوابة الاحتراف",
        "c3_title": "رادار الكشافين والوكلاء",
        "c3_desc": "ابحث عن المواهب، فلتر اللاعبين، واطلب تقارير 'التوافق التكتيكي' لمنع الصفقات الفاشلة.",
        "c3_btn": "دخول رادار الكشافين",
        "c4_title": "لوحة تحكم الأندية",
        "c4_desc": "أدر مواهبك، وافق على طلبات الكشافين، واطلب خدمات التحليل الميداني (قبل، أثناء، بعد).",
        "c4_btn": "دخول لوحة الأندية",
        "sidebar_lang": "🌐 Language / اللغة",
        "sidebar_music": "🎵 موسيقى دوري الأبطال",
        "music_btn": "▶️ تشغيل الموسيقى",
        "mission": "مهمتنا: إنقاذ المواهب من الأزقة إلى الملاعب العالمية."
    },
    "🇬🇧 English": {
        "title1": "Creating a New Export:",
        "title2": "Digital Sports Talent",
        "sub": "We don't just sell software. We build a digital pipeline to export talent. We discover street players, qualify them digitally, prevent their loss (avoiding flops like Hazard), and connect Arab talent to global clubs based on precise data.",
        "choose": "Choose Your Gateway 🚀",
        "c1_title": "Youth Portal (< 16)",
        "c1_desc": "Analyze your skills, protect your data (GDPR), and get a digital card with global star comparisons.",
        "c1_btn": "Enter Youth Portal",
        "c2_title": "Pro Portal (16+)",
        "c2_desc": "Advanced analysis, pro data card, market value. Optional appearance in the market table.",
        "c2_btn": "Enter Pro Portal",
        "c3_title": "Scouts & Agents Radar",
        "c3_desc": "Find talents, filter players, and request 'Tactical Fit' reports to prevent failed transfers.",
        "c3_btn": "Enter Scouts Radar",
        "c4_title": "Clubs Dashboard",
        "c4_desc": "Manage your talents, approve scout requests, and order field analysis (Pre, Live, Post-Match).",
        "c4_btn": "Enter Clubs Dashboard",
        "sidebar_lang": "🌐 Language / اللغة",
        "sidebar_music": "🎵 UCL Anthem",
        "music_btn": "▶️ Play Music",
        "mission": "Mission: Saving talent from the streets to global pitches."
    },
    "🇫🇷 Français": {
        "title1": "Créer une nouvelle exportation:",
        "title2": "Talent Sportif Numérique",
        "sub": "Nous ne vendons pas de logiciels. Nous construisons un pipeline numérique pour exporter des talents. Nous découvrons les joueurs de rue, les qualifions numériquement, évitons les flops (comme Hazard), et connectons les talents arabes aux clubs mondiaux.",
        "choose": "Choisissez votre porte 🚀",
        "c1_title": "Portail Jeunes (< 16)",
        "c1_desc": "Analysez vos compétences, protégez vos données (RGPD) et obtenez une carte numérique avec des comparaisons de stars.",
        "c1_btn": "Entrer Portail Jeunes",
        "c2_title": "Portail Pro (16+)",
        "c2_desc": "Analyse avancée, carte de données pro, valeur marchande. Apparition optionnelle dans le tableau.",
        "c2_btn": "Entrer Portail Pro",
        "c3_title": "Radar Scouts & Agents",
        "c3_desc": "Trouvez des talents, filtrez les joueurs et demandez des rapports 'Tactical Fit'.",
        "c3_btn": "Entrer Radar Scouts",
        "c4_title": "Tableau de Bord Clubs",
        "c4_desc": "Gérez vos talents, approuvez les demandes et commandez des analyses (Avant, Live, Après).",
        "c4_btn": "Entrer Tableau Clubs",
        "sidebar_lang": "🌐 Language / اللغة",
        "sidebar_music": "🎵 Hymne UCL",
        "music_btn": "▶️ Lire Musique",
        "mission": "Mission : Sauver les talents de la rue vers les terrains mondiaux."
    },
    "🇪🇸 Español": {
        "title1": "Creando una nueva exportación:",
        "title2": "Talento Deportivo Digital",
        "sub": "No vendemos software. Construimos un pipeline digital para exportar talento. Descubrimos jugadores callejeros, los cualificamos digitalmente, evitamos fracasos (como Hazard) y conectamos talento árabe con clubes globales.",
        "choose": "Elige tu puerta 🚀",
        "c1_title": "Portal Juvenil (< 16)",
        "c1_desc": "Analiza tus habilidades, protege tus datos (GDPR) y obtén una tarjeta digital con comparaciones de estrellas.",
        "c1_btn": "Entrar Portal Juvenil",
        "c2_title": "Portal Pro (16+)",
        "c2_desc": "Análisis avanzado, tarjeta de datos pro, valor de mercado. Aparición opcional en la tabla.",
        "c2_btn": "Entrar Portal Pro",
        "c3_title": "Radar de Ojeadores",
        "c3_desc": "Encuentra talentos, filtra jugadores y solicita informes de 'Ajuste Táctico'.",
        "c3_btn": "Entrar Radar Ojeadores",
        "c4_title": "Panel de Clubes",
        "c4_desc": "Gestiona tus talentos, aprueba solicitudes y pide análisis (Antes, Live, Después).",
        "c4_btn": "Entrar Panel Clubes",
        "sidebar_lang": "🌐 Language / اللغة",
        "sidebar_music": "🎵 Himno UCL",
        "music_btn": "▶️ Reproducir",
        "mission": "Misión: Salvar talentos de las calles a los campos globales."
    },
    "🇮🇹 Italiano": {
        "title1": "Creare una nuova esportazione:",
        "title2": "Talento Sportivo Digitale",
        "sub": "Non vendiamo software. Costruiamo una pipeline digitale per esportare talenti. Scopriamo giocatori di strada, li qualifichiamo digitalmente, evitiamo flop (come Hazard) e colleghiamo i talenti arabi ai club globali.",
        "choose": "Scegli il tuo portale 🚀",
        "c1_title": "Portale Giovani (< 16)",
        "c1_desc": "Analizza le tue abilità, proteggi i tuoi dati (GDPR) e ottieni una carta digitale con confronti stellari.",
        "c1_btn": "Entra Portale Giovani",
        "c2_title": "Portale Pro (16+)",
        "c2_desc": "Analisi avanzata, carta dati pro, valore di mercato. Apparizione opzionale nella tabella.",
        "c2_btn": "Entra Portale Pro",
        "c3_title": "Radar Scout & Agenti",
        "c3_desc": "Trova talenti, filtra giocatori e richiedi report di 'Tactical Fit'.",
        "c3_btn": "Entra Radar Scout",
        "c4_title": "Dashboard Club",
        "c4_desc": "Gestisci i tuoi talenti, approva richieste e ordina analisi (Pre, Live, Post).",
        "c4_btn": "Entra Dashboard Club",
        "sidebar_lang": "🌐 Language / اللغة",
        "sidebar_music": "🎵 Inno UCL",
        "music_btn": "▶️ Riproduci",
        "mission": "Missione: Salvare talenti dalle strade ai campi globali."
    },
    "🇵🇹 Português": {
        "title1": "Criando uma nova exportação:",
        "title2": "Talento Desportivo Digital",
        "sub": "Não vendemos software. Construímos um pipeline digital para exportar talentos. Descobrimos jogadores de rua, qualificamo-los digitalmente, evitamos flops (como Hazard) e ligamos talentos árabes a clubes globais.",
        "choose": "Escolha o seu portal 🚀",
        "c1_title": "Portal Juvenil (< 16)",
        "c1_desc": "Analise as suas habilidades, proteja os seus dados (GDPR) e obtenha um cartão digital com comparações de estrelas.",
        "c1_btn": "Entrar Portal Juvenil",
        "c2_title": "Portal Pro (16+)",
        "c2_desc": "Análise avançada, cartão de dados pro, valor de mercado. Aparição opcional na tabela.",
        "c2_btn": "Entrar Portal Pro",
        "c3_title": "Radar de Olheiros",
        "c3_desc": "Encontre talentos, filtre jogadores e solicite relatórios de 'Ajuste Tático'.",
        "c3_btn": "Entrar Radar Olheiros",
        "c4_title": "Painel de Clubes",
        "c4_desc": "Gerencie os seus talentos, aprove pedidos e solicite análises (Antes, Live, Depois).",
        "c4_btn": "Entrar Painel Clubes",
        "sidebar_lang": "🌐 Language / اللغة",
        "sidebar_music": "🎵 Hino UCL",
        "music_btn": "▶️ Reproduzir",
        "mission": "Missão: Salvar talentos das ruas para os relvados globais."
    }
}

# ==========================================
# 3. التقنيات العالية: CSS السينمائي
# ==========================================
st.markdown("""
<style>
    .stApp {
        background: radial-gradient(circle at 15% 20%, rgba(0, 255, 136, 0.12) 0%, transparent 40%),
                    radial-gradient(circle at 85% 80%, rgba(0, 212, 255, 0.10) 0%, transparent 40%),
                    linear-gradient(160deg, #040a18 0%, #01100a 100%);
        background-attachment: fixed; color: #eaf6f0; font-family: 'Inter', sans-serif;
    }
    [data-testid="stHeader"] { background: transparent; }
    footer { visibility: hidden; }
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(4,10,12,.95) 0%, rgba(0,20,15,.92) 100%) !important;
        border-inline-end: 1px solid rgba(0,255,136,.2);
    }

    .hero {
        position: relative; padding: 60px 40px; margin-bottom: 40px; border-radius: 25px;
        border: 1px solid rgba(0,255,136,.2);
        background-image: linear-gradient(180deg, rgba(0,0,0,.3) 0%, rgba(0,10,8,.85) 60%, rgba(0,0,0,.95) 100%),
                          url("https://images.unsplash.com/photo-1522778119026-d647f0596c20?w=1920&q=85&auto=format&fit=crop");
        background-size: cover; background-position: center;
        box-shadow: 0 30px 90px rgba(0,0,0,.85), 0 0 80px rgba(0,255,136,.1);
        animation: heroFade 1.5s ease-out; overflow: hidden;
    }
    @keyframes heroFade { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
    
    .hero-eyebrow { color: #00ff88; font-size: .85rem; letter-spacing: 8px; text-transform: uppercase; font-weight: 800; margin-bottom: 15px; text-shadow: 0 0 20px rgba(0,255,136,.8); }
    .hero-title { font-size: clamp(2rem, 5vw, 3.8rem); font-weight: 900; line-height: 1.1; letter-spacing: -1.5px; color: #fff; text-shadow: 0 8px 30px rgba(0,0,0,.9); }
    .hero-text { background: linear-gradient(90deg, #00ff88 0%, #00d4ff 50%, #ffaa00 100%); background-size: 200% auto; -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; animation: shimmer 5s linear infinite; }
    @keyframes shimmer { 0%{background-position:0% center} 100%{background-position:200% center} }
    .hero-sub { color: rgba(234,246,240,.85); margin-top: 20px; font-size: 1.1rem; line-height: 1.8; max-width: 750px; }

    .ball-float {
        position: absolute; top: 40px; right: 40px; width: 60px; height: 60px; border-radius: 50%;
        background: radial-gradient(circle at 30% 30%, #fff 0%, #d8d8d8 35%, #444 100%);
        box-shadow: 0 0 30px rgba(0,255,136,.8), 0 0 60px rgba(0,255,136,.4), inset -6px -8px 16px rgba(0,0,0,.6);
        animation: ballSpin 8s linear infinite, ballFloat 3.5s ease-in-out infinite;
        display: flex; align-items: center; justify-content: center; font-size: 30px; z-index: 3;
    }
    @keyframes ballSpin { from{transform:rotate(0deg)} to{transform:rotate(360deg)} }
    @keyframes ballFloat { 0%,100%{margin-top:0} 50%{margin-top:-15px} }

    .glass-card {
        background: linear-gradient(180deg, rgba(20,25,22,.75) 0%, rgba(5,10,8,.95) 100%);
        border: 1px solid rgba(0,255,136,.2); border-radius: 20px; padding: 25px; margin-bottom: 20px;
        box-shadow: 0 20px 50px rgba(0,0,0,.7), inset 0 1px 0 rgba(255,255,255,.06);
        transition: all .4s cubic-bezier(.2,.8,.2,1); text-align: center; height: 100%; position: relative;
    }
    .glass-card:hover { transform: translateY(-8px) scale(1.02); border-color: #00ff88; box-shadow: 0 30px 70px rgba(0,0,0,.85), 0 0 50px rgba(0,255,136,.3); }
    
    .card-icon { font-size: 45px; margin-bottom: 10px; text-shadow: 0 0 20px rgba(0,255,136,.5); }
    .card-title { color: #fff; font-weight: 800; font-size: 1.3rem; margin-bottom: 10px; }
    .card-desc { color: rgba(220,235,225,.75); font-size: .9rem; line-height: 1.6; margin-bottom: 15px; min-height: 45px; }
    
    .price-badge {
        display: inline-block; background: linear-gradient(135deg, #ffcc44 0%, #ffaa00 35%, #ff6600 100%);
        color: #000; font-weight: 900; font-size: 1.3rem; letter-spacing: 1px;
        padding: 8px 25px; border-radius: 40px; margin-bottom: 15px; border: 1px solid rgba(255,255,255,.4);
        animation: badgePulse 2.4s ease-in-out infinite;
    }
    @keyframes badgePulse { 0%,100% { box-shadow: 0 6px 25px rgba(255,170,0,.65), 0 0 40px rgba(255,170,0,.3); } 50% { box-shadow: 0 6px 30px rgba(255,170,0,.95), 0 0 60px rgba(255,170,0,.55); } }

    div.stButton > button {
        width: 100%; background: linear-gradient(180deg, rgba(0,255,136,.15) 0%, rgba(0,255,136,.05) 100%);
        color: #00ff88; border: 1.5px solid rgba(0,255,136,.5); border-radius: 12px; font-weight: 800; letter-spacing: 1px; padding: 12px; transition: all .3s ease;
    }
    div.stButton > button:hover { background: linear-gradient(180deg, rgba(0,255,136,.3) 0%, rgba(0,255,136,.1) 100%); border-color: #00ff88; color: #fff; box-shadow: 0 8px 30px rgba(0,255,136,.5); transform: translateY(-2px); }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 4. إدارة الحالة والشريط الجانبي
# ==========================================
if "lang" not in st.session_state:
    st.session_state.lang = "🇸🇦 العربية"

with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/football2.png", width=80)
    
    # اختيار اللغة (متزامن)
    lang_options = list(LANG_DATA.keys())
    lang_idx = lang_options.index(st.session_state.lang)
    selected_lang = st.selectbox(LANG_DATA["🇸🇦 العربية"]["sidebar_lang"], lang_options, index=lang_idx)
    
    if selected_lang != st.session_state.lang:
        st.session_state.lang = selected_lang
        st.rerun()
        
    d = LANG_DATA[st.session_state.lang]
    
    st.markdown("---")
    st.markdown(f"### {d['sidebar_music']}")
    if st.button(d["music_btn"]):
        st.audio("https://static.calcionapoli1926.it/202109/Uefa-Champions-League.mp3", format="audio/mp3")
    
    st.markdown("---")
    st.success(f"🚀 Omnia DeepArena IA\n\n**{d['mission']}**")

# ==========================================
# 5. المحتوى الرئيسي (Hero + الأبواب)
# ==========================================
st.markdown(f"""
<div class="hero" dir="auto">
    <div class="ball-float">⚽</div>
    <div class="hero-eyebrow">OMNIA DEEPARENA • 2030</div>
    <div class="hero-title">
        {d['title1']} <br>
        <span class="hero-text">{d['title2']}</span>
    </div>
    <div class="hero-sub">{d['sub']}</div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"<h2 style='text-align:center; color:#fff; margin-bottom:30px;'>{d['choose']}</h2>", unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    # 1. الناشئين
    st.markdown(f"""
    <div class="glass-card" dir="auto">
        <div class="card-icon">🥅</div>
        <div class="card-title">{d['c1_title']}</div>
        <div class="card-desc">{d['c1_desc']}</div>
        <div class="price-badge">10$ / Mo</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button(d['c1_btn'], key="btn_youth", use_container_width=True):
        st.switch_page("pages/1_Youth.py")

    st.markdown("<br>", unsafe_allow_html=True)
    
    # 3. الكشافين
    st.markdown(f"""
    <div class="glass-card" dir="auto">
        <div class="card-icon">📡</div>
        <div class="card-title">{d['c3_title']}</div>
        <div class="card-desc">{d['c3_desc']}</div>
        <div class="price-badge">50$ / Mo</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button(d['c3_btn'], key="btn_scouts", use_container_width=True):
        st.switch_page("pages/3_Scouts.py")

with col2:
    # 2. الكبار
    st.markdown(f"""
    <div class="glass-card" dir="auto">
        <div class="card-icon">👟</div>
        <div class="card-title">{d['c2_title']}</div>
        <div class="card-desc">{d['c2_desc']}</div>
        <div class="price-badge">30$ / Mo</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button(d['c2_btn'], key="btn_seniors", use_container_width=True):
        st.switch_page("pages/2_Seniors.py")

    st.markdown("<br>", unsafe_allow_html=True)

    # 4. الأندية
    st.markdown(f"""
    <div class="glass-card" dir="auto">
        <div class="card-icon">🏟️</div>
        <div class="card-title">{d['c4_title']}</div>
        <div class="card-desc">{d['c4_desc']}</div>
        <div class="price-badge">150$ / Mo</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button(d['c4_btn'], key="btn_clubs", use_container_width=True):
        st.switch_page("pages/4_Clubs.py")

# ==========================================
# 6. تذييل الصفحة
# ==========================================
st.markdown("<hr style='border-color: rgba(0,255,136,.2); margin-top: 50px;'>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666; font-size: 0.8rem;'>Omnia DeepArena IA © 2026 | Youth Secure Sandbox & GDPR Compliance</p>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# 🏛️ لوحة الحقوق المالية والتضامن (Legal & Financial HUD) - Multilingual
# ══════════════════════════════════════════════════════════════
LEGAL_TEXTS = {
    "🇸🇦 العربية": {
        "title": "الحقوق المالية والامتثال (FIFA Solidarity)",
        "desc": "منصة Omnia تضمن جميع الحقوق المالية والقانونية تلقائياً. نظام آمن ومحمي بموجب قوانين الفيفا والاتحاد الأوروبي.",
        "s1": "FIFA Solidarity", "s1d": "2.5% Youth Academy Rights",
        "s2": "Player Equity", "s2d": "Tokenized Shares (2.5% Fee)",
        "s3": "GDPR Shield", "s3d": "100% Data Protection"
    },
    "🇬🇧 English": {
        "title": "Financial Rights & Compliance (FIFA Solidarity)",
        "desc": "Omnia automatically guarantees all financial and legal rights. A secure system protected under FIFA and UEFA laws.",
        "s1": "FIFA Solidarity", "s1d": "2.5% Youth Academy Rights",
        "s2": "Player Equity", "s2d": "Tokenized Shares (2.5% Fee)",
        "s3": "GDPR Shield", "s3d": "100% Data Protection"
    },
    "🇫🇷 Français": {
        "title": "Droits Financiers & Conformité (FIFA Solidarity)",
        "desc": "Omnia garantit automatiquement tous les droits financiers et juridiques. Un système sécurisé protégé par la FIFA et l'UEFA.",
        "s1": "Solidarité FIFA", "s1d": "2.5% Droits Académie",
        "s2": "Équité Joueur", "s2d": "Actions Tokénisées (Frais 2.5%)",
        "s3": "Bouclier RGPD", "s3d": "100% Protection Données"
    },
    "🇪🇸 Español": {
        "title": "Derechos Financieros y Cumplimiento (FIFA Solidarity)",
        "desc": "Omnia garantiza automáticamente todos los derechos financieros y legales. Un sistema seguro protegido por las leyes de la FIFA y la UEFA.",
        "s1": "Solidaridad FIFA", "s1d": "2.5% Derechos Academia",
        "s2": "Equidad Jugador", "s2d": "Acciones Tokenizadas (Tarifa 2.5%)",
        "s3": "Escudo GDPR", "s3d": "100% Protección Datos"
    },
    "🇮🇹 Italiano": {
        "title": "Diritti Finanziari e Conformità (FIFA Solidarity)",
        "desc": "Omnia garantisce automaticamente tutti i diritti finanziari e legali. Un sistema sicuro protetto dalle leggi FIFA e UEFA.",
        "s1": "Solidarietà FIFA", "s1d": "2.5% Diritti Accademia",
        "s2": "Equità Giocatore", "s2d": "Azioni Tokenizzate (Tariffa 2.5%)",
        "s3": "Scudo GDPR", "s3d": "100% Protezione Dati"
    },
    "🇵🇹 Português": {
        "title": "Direitos Financeiros e Conformidade (FIFA Solidarity)",
        "desc": "A Omnia garante automaticamente todos os direitos financeiros e legais. Um sistema seguro protegido pelas leis da FIFA e da UEFA.",
        "s1": "Solidariedade FIFA", "s1d": "2.5% Direitos Academia",
        "s2": "Equidade Jogador", "s2d": "Ações Tokenizadas (Taxa 2.5%)",
        "s3": "Escudo GDPR", "s3d": "100% Proteção Dados"
    }
}

# جلب النص بناءً على اللغة الحالية
lt = LEGAL_TEXTS.get(lang, LEGAL_TEXTS["🇬🇧 English"])

st.markdown("---")
st.markdown(f"### 🏛️ {lt['title']}")

st.markdown(f"""
<div style="background: rgba(255, 170, 0, 0.05); border: 2px solid #ffaa00; border-radius: 15px; padding: 20px; text-align: center; box-shadow: 0 0 20px rgba(255,170,0,0.2);">
    <h4 style="color: #ffaa00; margin-top: 0;">⚖️ Omnia LawTech & FinTech Core</h4>
    <p style="color: #dbe7e1; font-size: 0.95rem;">
        {lt['desc']}
    </p>
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
