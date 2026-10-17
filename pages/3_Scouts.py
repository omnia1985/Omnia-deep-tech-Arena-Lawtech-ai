import streamlit as st
import pandas as pd
import numpy as np

# ═══════════════════════════════════════════════════════════════
# 1️⃣ إعدادات الصفحة والتصميم السينمائي
# ═══════════════════════════════════════════════════════════════
st.set_page_config(layout="wide", page_icon="📡", page_title="Scouts & Agents")

st.markdown("""
<style>
.stApp{background:linear-gradient(rgba(4,10,24,0.97),rgba(1,16,10,0.97));color:#fff;}
.scout-card{background:rgba(255,255,255,0.03);border:1px solid #00d4ff;padding:20px;border-radius:15px;margin-bottom:15px;}
.metric-box{text-align:center; padding: 10px; background: rgba(0, 212, 255, 0.1); border-radius: 10px;}
.metric-val{font-size:1.5rem; font-weight:bold; color:#00d4ff;}
.metric-lbl{font-size:0.8rem; color:#b4c7bf;}
/* تحسين مظهر الجدول */
[data-testid="stDataFrame"] { border: 1px solid #00d4ff; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# 2️⃣ قاموس اللغات الست
# ═══════════════════════════════════════════════════════════════
LANG_SCOUTS = {
    "🇸🇦 العربية": [
        "📡 باقة الكشافين ووكلاء الأندية (سوق المواهب)",
        "💰 السعر الثابت: 50 دولار/شهرياً | 🚫 حماية صارمة: لا يتم عرض اللاعبين تحت 16 سنة إطلاقاً",
        "🔍 محرك البحث الموحد عن المواهب (فوق 16 سنة)",
        "تصفية حسب المركز:",
        "الكل", "حراس المرمى", "المدافعون", "خط الوسط", "المهاجمون",
        "الحد الأدنى لنسبة التطابق:",
        "اللاعب", "العمر", "المركز", "النادي/الأكاديمية", "السرعة (كم/س)", "نسبة التطابق", "البلد",
        "إجمالي اللاعبين المتاحين", "متوسط العمر", "أعلى سرعة مسجلة",
        "⬅️ العودة إلى الرئيسية"
    ],
    "🇬🇧 English": [
        "📡 Scouts & Agents Premium Market",
        "💰 Fixed Price: $50/Mo | 🚫 Strict Protection: Players under 16 are never displayed",
        "🔍 Unified Talent Discovery Engine (16+ Only)",
        "Filter by Position:",
        "All", "Goalkeepers", "Defenders", "Midfielders", "Forwards",
        "Minimum Match Score:",
        "Player", "Age", "Position", "Club/Academy", "Speed (km/h)", "Match %", "Country",
        "Total Available Players", "Average Age", "Top Recorded Speed",
        "⬅️ Back to Home"
    ],
    "🇫🇷 Français": [
        "📡 Marché Premium des Recruteurs & Agents",
        "💰 Prix Fixe: 50$/Mois | 🚫 Protection stricte: Les moins de 16 ans ne sont jamais affichés",
        "🔍 Moteur de Découverte de Talents (16+ uniquement)",
        "Filtrer par poste:",
        "Tous", "Gardiens", "Défenseurs", "Milieux", "Attaquants",
        "Score de correspondance minimum:",
        "Joueur", "Âge", "Poste", "Club/Académie", "Vitesse (km/h)", "Correspondance %", "Pays",
        "Total des joueurs disponibles", "Âge moyen", "Meilleure vitesse",
        "⬅️ Retour à l'Accueil"
    ],
    "🇪🇸 Español": [
        "📡 Mercado Premium de Ojeadores y Agentes",
        "💰 Precio Fijo: 50$/Mes | 🚫 Protección estricta: Menores de 16 nunca se muestran",
        "🔍 Motor Unificado de Descubrimiento de Talentos (Solo 16+)",
        "Filtrar por posición:",
        "Todos", "Porteros", "Defensas", "Centrocampistas", "Delanteros",
        "Puntuación mínima de coincidencia:",
        "Jugador", "Edad", "Posición", "Club/Academia", "Velocidad (km/h)", "Coincidencia %", "País",
        "Total de jugadores disponibles", "Edad media", "Velocidad máxima",
        "⬅️ Volver al Inicio"
    ],
    "🇮🇹 Italiano": [
        "📡 Mercato Premium Scout & Agenti",
        "💰 Prezzo Fisso: 50$/Mese | 🚫 Protezione rigorosa: I minori di 16 anni non vengono mai mostrati",
        "🔍 Motore Unificato di Scoperta dei Talenti (Solo 16+)",
        "Filtra per posizione:",
        "Tutti", "Portieri", "Difensori", "Centrocampisti", "Attaccanti",
        "Punteggio minimo di corrispondenza:",
        "Giocatore", "Età", "Posizione", "Club/Accademia", "Velocità (km/h)", "Corrispondenza %", "Paese",
        "Totale giocatori disponibili", "Età media", "Velocità massima",
        "⬅️ Torna alla Home"
    ],
    "🇵🇹 Português": [
        "📡 Mercado Premium de Olheiros & Agentes",
        "💰 Preço Fixo: 50$/Mês | 🚫 Proteção rigorosa: Menores de 16 nunca são exibidos",
        "🔍 Motor Unificado de Descoberta de Talentos (Apenas 16+)",
        "Filtrar por posição:",
        "Todos", "Goleiros", "Defensores", "Meio-campistas", "Atacantes",
        "Pontuação mínima de correspondência:",
        "Jogador", "Idade", "Posição", "Clube/Academia", "Velocidade (km/h)", "Correspondência %", "País",
        "Total de jogadores disponíveis", "Idade média", "Velocidade máxima",
        "⬅️ Voltar ao Início"
    ]
}

sel_lang = st.session_state.get("lang", "🇸🇦 العربية")
d = LANG_SCOUTS.get(sel_lang, LANG_SCOUTS["🇸🇦 العربية"])

st.error(d[1])
st.title(d[0])
st.write("---")

# ═══════════════════════════════════════════════════════════════
# 3️⃣ توليد البيانات التجريبية (Mock Data) - محاكاة لـ Supabase
# ═══════════════════════════════════════════════════════════════
@st.cache_data
def load_mock_data():
    # ملاحظة: جميع الأعمار هنا >= 16 (احتراماً لقواعد GDPR)
    data = {
        "Name": ["Youssef T.", "Amine B.", "Karim D.", "Mehdi S.", "Rayan M.", "Ziad K.", "Omar F.", "Walid H."],
        "Age": [17, 18, 16, 21, 19, 23, 17, 20],
        "Position": ["FW", "MF", "DF", "GK", "FW", "MF", "DF", "FW"],
        "Club": ["Academy Tunis", "Algiers Youth", "Carthage FC", "Casablanca Acad", "Elite Tunis", "Oran FC", "Algiers Youth", "Sfax Academy"],
        "Speed (km/h)": [33.5, 31.2, 30.8, 28.5, 34.1, 32.0, 29.9, 35.0],
        "Match %": [89, 85, 82, 78, 92, 88, 75, 94],
        "Country": ["🇹🇳 Tunisia", "🇩🇿 Algeria", "🇹🇳 Tunisia", "🇲🇦 Morocco", "🇹🇳 Tunisia", "🇩🇿 Algeria", "🇩🇿 Algeria", "🇹🇳 Tunisia"],
        "Position_Ar": ["مهاجم", "وسط", "مدافع", "حارس", "مهاجم", "وسط", "مدافع", "مهاجم"] # للترجمة لاحقاً
    }
    return pd.DataFrame(data)

df = load_mock_data()

# ═══════════════════════════════════════════════════════════════
# 4️⃣ واجهة الفلاتر (Filters)
# ═══════════════════════════════════════════════════════════════
st.subheader(d[2])

# إنشاء 3 أعمدة للفلاتر
col1, col2, col3 = st.columns(3)

with col1:
    pos_filter = st.selectbox(
        d[3], 
        [d[4], d[5], d[6], d[7], d[8]] # All, GK, DF, MF, FW
    )

with col2:
    min_match = st.slider(d[9], min_value=0, max_value=100, value=70, step=5)

# فلترة البيانات بناءً على الاختيارات
filtered_df = df.copy()

if pos_filter == d[5]: filtered_df = filtered_df[filtered_df["Position"] == "GK"]
elif pos_filter == d[6]: filtered_df = filtered_df[filtered_df["Position"] == "DF"]
elif pos_filter == d[7]: filtered_df = filtered_df[filtered_df["Position"] == "MF"]
elif pos_filter == d[8]: filtered_df = filtered_df[filtered_df["Position"] == "FW"]

filtered_df = filtered_df[filtered_df["Match %"] >= min_match]

# ═══════════════════════════════════════════════════════════════
# 5️⃣ إحصائيات سريعة (KPIs)
# ═══════════════════════════════════════════════════════════════
st.write("---")
kpi1, kpi2, kpi3 = st.columns(3)

with kpi1:
    st.markdown(f'<div class="metric-box"><div class="metric-val">{len(filtered_df)}</div><div class="metric-lbl">{d[15]}</div></div>', unsafe_allow_html=True)
with kpi2:
    avg_age = round(filtered_df["Age"].mean(), 1) if not filtered_df.empty else 0
    st.markdown(f'<div class="metric-box"><div class="metric-val">{avg_age}</div><div class="metric-lbl">{d[16]}</div></div>', unsafe_allow_html=True)
with kpi3:
    max_speed = round(filtered_df["Speed (km/h)"].max(), 1) if not filtered_df.empty else 0
    st.markdown(f'<div class="metric-box"><div class="metric-val">{max_speed} km/h</div><div class="metric-lbl">{d[17]}</div></div>', unsafe_allow_html=True)

st.write("---")

# ═══════════════════════════════════════════════════════════════
# 6️⃣ عرض الجدول الموحد
# ═══════════════════════════════════════════════════════════════
if not filtered_df.empty:
    # إعادة تسمية الأعمدة للعرض حسب اللغة المختارة
    display_df = filtered_df.rename(columns={
        "Name": d[10],
        "Age": d[11],
        "Position": d[12],
        "Club": d[13],
        "Speed (km/h)": d[14],
        "Match %": d[15], # إعادة استخدام مؤشر التطابق
        "Country": d[16]  # البلد
    })

    # إخفاء العمود العربي المساعد
    display_df = display_df.drop(columns=["Position_Ar"])

    # عرض الجدول بشكل تفاعلي واحترافي
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            d[15]: st.column_config.ProgressColumn(
                d[15],
                help="YOLO26 Kinematic Match Score",
                format="%d%%",
                min_value=0,
                max_value=100,
            )
        }
    )
    
    # زر وهمي للتواصل (للمستقبل)
    st.info("💡 Note: In the live version, scouts can click on any player to request contact details via the platform (Stripe payment integration required).")
else:
    st.warning("No players match your current filters.")

# ═══════════════════════════════════════════════════════════════
# 7️⃣ زر العودة
# ═══════════════════════════════════════════════════════════════
st.write("---")
if st.button(d[18], use_container_width=True):
    st.switch_page("app.py")
