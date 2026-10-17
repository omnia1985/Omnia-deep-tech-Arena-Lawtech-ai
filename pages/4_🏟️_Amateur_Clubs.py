import streamlit as st
import pandas as pd
import random

# ═══════════════════════════════════════════════════════════════
# 1️⃣ إعدادات الصفحة والتصميم
# ═══════════════════════════════════════════════════════════════
st.set_page_config(layout="wide", page_icon="🏟️", page_title="Amateur Clubs")

st.markdown("""
<style>
.stApp{background:linear-gradient(rgba(4,10,24,0.97),rgba(1,16,10,0.97));color:#fff;}
.vip-card{background:rgba(255, 170, 0, 0.05);border:2px solid #ffaa00;padding:20px;border-radius:15px;margin-bottom:15px;box-shadow: 0 0 25px rgba(255,170,0,0.3);}
.coach-card{background:rgba(255,255,255,0.03);border:1px solid #00ff88;padding:15px;border-radius:10px;margin-bottom:10px;}
.metric-box{text-align:center; padding: 10px; background: rgba(0, 255, 136, 0.1); border-radius: 10px;}
.metric-val{font-size:1.5rem; font-weight:bold; color:#00ff88;}
.metric-lbl{font-size:0.8rem; color:#b4c7bf;}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# 2️⃣ قاموس اللغات الست
# ═══════════════════════════════════════════════════════════════
LANG_AMATEUR = {
    "🇸🇦 العربية": [
        "🏟️ باقة أندية الهواة والأكاديميات (VIP)",
        "💰 السعر الثابت: 150$/شهرياً | لوحة المدرب الشاملة ومحرك الريمونتادا التكتيكي",
        "📊 لوحة تحكم المدرب (Coach HUD)",
        "إحصائيات الفريق", "اللاعبون المسجلون", "متوسط العمر", "الجاهزية البدنية للفريق",
        "📋 قائمة الفريق (Squad List)",
        "اللاعب", "المركز", "العمر", "نسبة الجاهزية", "الحالة",
        "🔄 محرك الريمونتادا (Remontada Engine)",
        "محاكي تكتيكي فوري لإنقاذ المباريات. أدخل نتيجة المباراة والوقت المتبقي للحصول على خطة بديلة.",
        "نتيجة فريقك:", "نتيجة الخصم:", "الوقت المتبقي (بالدقائق):",
        "⚡ توليد خطة إنقاذ المباراة",
        "الخطة المقترحة:", "التشكيل الجديد:", "تعليمات اللاعبين:",
        "⬅️ العودة إلى الرئيسية"
    ],
    "🇬🇧 English": [
        "🏟️ Amateur Clubs & Academies Pack (VIP)",
        "💰 Fixed Price: $150/Mo | Full Coach HUD & Tactical Remontada Engine",
        "📊 Coach HUD Dashboard",
        "Team Stats", "Registered Players", "Avg Age", "Team Readiness",
        "📋 Squad List",
        "Player", "Position", "Age", "Readiness %", "Status",
        "🔄 Remontada Engine",
        "Instant tactical simulator to rescue matches. Enter score and time left for a backup plan.",
        "Your Score:", "Opponent Score:", "Time Remaining (mins):",
        "⚡ Generate Rescue Plan",
        "Suggested Plan:", "New Formation:", "Player Instructions:",
        "⬅️ Back to Home"
    ],
    "🇫🇷 Français": [
        "🏟️ Pack Clubs Amateurs & Académies (VIP)",
        "💰 Prix Fixe: 150$/Mois | HUD Entraîneur Complet & Moteur Remontada",
        "📊 Tableau de Bord de l'Entraîneur",
        "Stats de l'Équipe", "Joueurs Inscrits", "Âge Moyen", "Préparation de l'Équipe",
        "📋 Liste de l'Effectif",
        "Joueur", "Poste", "Âge", "Préparation %", "Statut",
        "🔄 Moteur Remontada",
        "Simulateur tactique instantané pour sauver des matchs.",
        "Votre Score:", "Score Adverse:", "Temps Restant (min):",
        "⚡ Générer un Plan de Secours",
        "Plan Suggéré:", "Nouvelle Formation:", "Instructions aux Joueurs:",
        "⬅️ Retour à l'Accueil"
    ],
    "🇪🇸 Español": [
        "🏟️ Paquete Clubes Amateurs y Academias (VIP)",
        "💰 Precio Fijo: 150$/Mes | HUD Completo del Entrenador y Motor Remontada",
        "📊 Panel del Entrenador",
        "Estadísticas del Equipo", "Jugadores Registrados", "Edad Media", "Preparación del Equipo",
        "📋 Lista de la Plantilla",
        "Jugador", "Posición", "Edad", "Preparación %", "Estado",
        "🔄 Motor Remontada",
        "Simulador táctico instantáneo para rescatar partidos.",
        "Tu Marcador:", "Marcador Rival:", "Tiempo Restante (min):",
        "⚡ Generar Plan de Rescate",
        "Plan Sugerido:", "Nueva Formación:", "Instrucciones:",
        "⬅️ Volver al Inicio"
    ],
    "🇮🇹 Italiano": [
        "🏟️ Pacchetto Club Dilettanti e Accademie (VIP)",
        "💰 Prezzo Fisso: 150$/Mese | HUD Allenatore Completo & Motore Remontada",
        "📊 Dashboard dell'Allenatore",
        "Statistiche Squadra", "Giocatori Registrati", "Età Media", "Preparazione Squadra",
        "📋 Lista Rosa",
        "Giocatore", "Posizione", "Età", "Preparazione %", "Stato",
        "🔄 Motore Remontada",
        "Simulatore tattico istantaneo per salvare le partite.",
        "Il Tuo Punteggio:", "Punteggio Avversario:", "Tempo Rimanente (min):",
        "⚡ Genera Piano di Salvataggio",
        "Piano Suggerito:", "Nuova Formazione:", "Istruzioni Giocatori:",
        "⬅️ Torna alla Home"
    ],
    "🇵🇹 Português": [
        "🏟️ Pacote Clubes Amadores e Academias (VIP)",
        "💰 Preço Fixo: 150$/Mês | HUD Completo do Treinador e Motor Remontada",
        "📊 Painel do Treinador",
        "Estatísticas da Equipa", "Jogadores Registados", "Idade Média", "Preparação da Equipa",
        "📋 Lista do Plantel",
        "Jogador", "Posição", "Idade", "Preparação %", "Estado",
        "🔄 Motor Remontada",
        "Simulador tático instantâneo para salvar partidas.",
        "O Teu Resultado:", "Resultado Adversário:", "Tempo Restante (min):",
        "⚡ Gerar Plano de Resgate",
        "Plano Sugerido:", "Nova Formação:", "Instruções:",
        "⬅️ Voltar ao Início"
    ]
}

sel_lang = st.session_state.get("lang", "🇸🇦 العربية")
d = LANG_AMATEUR.get(sel_lang, LANG_AMATEUR["🇸🇦 العربية"])

st.error(d[1])
st.title(d[0])
st.write("---")

# ═══════════════════════════════════════════════════════════════
# 3️⃣ لوحة تحكم المدرب (Coach HUD)
# ═══════════════════════════════════════════════════════════════
st.subheader(d[2])
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.markdown(f'<div class="metric-box"><div class="metric-val">28</div><div class="metric-lbl">{d[4]}</div></div>', unsafe_allow_html=True)
with kpi2:
    st.markdown(f'<div class="metric-box"><div class="metric-val">18.5</div><div class="metric-lbl">{d[5]}</div></div>', unsafe_allow_html=True)
with kpi3:
    st.markdown(f'<div class="metric-box"><div class="metric-val" style="color:#ffaa00;">88%</div><div class="metric-lbl">{d[6]}</div></div>', unsafe_allow_html=True)

st.write("---")

# ═══════════════════════════════════════════════════════════════
# 4️⃣ قائمة الفريق (Squad List)
# ═══════════════════════════════════════════════════════════════
st.subheader(d[7])

# بيانات تجريبية للفريق
squad_data = {
    d[8]: ["Ahmed Y.", "Sami K.", "Bilel M.", "Yassine T.", "Oussama D."],
    d[9]: ["FW", "MF", "DF", "GK", "FW"],
    d[10]: [17, 19, 18, 20, 16],
    d[11]: [95, 88, 92, 85, 78],
    d[12]: ["Ready", "Ready", "Recovering", "Ready", "Ready"]
}
df_squad = pd.DataFrame(squad_data)

# عرض الجدول
st.dataframe(
    df_squad, 
    use_container_width=True, 
    hide_index=True,
    column_config={
        d[11]: st.column_config.ProgressColumn(
            d[11],
            format="%d%%",
            min_value=0,
            max_value=100,
        )
    }
)

st.write("---")

# ═══════════════════════════════════════════════════════════════
# 5️⃣ محرك الريمونتادا (Remontada Engine)
# ═══════════════════════════════════════════════════════════════
st.subheader(d[13])
st.info(d[14])

col_s1, col_s2, col_s3 = st.columns(3)

with col_s1:
    our_score = st.number_input(d[15], min_value=0, max_value=5, value=0)
with col_s2:
    opp_score = st.number_input(d[16], min_value=0, max_value=5, value=2)
with col_s3:
    time_left = st.number_input(d[17], min_value=1, max_value=90, value=15)

if st.button(d[18], type="primary", use_container_width=True):
    st.markdown("---")
    
    # منطق بسيط لمحاكاة الذكاء التكتيكي (سيتم تطويره بـ AI لاحقاً)
    if opp_score > our_score:
        st.error(f"⚠️ {d[15]} {our_score} - {opp_score} {d[16]}")
        
        # اقتراحات تكتيكية
        if time_left > 30:
            formation = "4-3-3 (هجومي) - High Press"
            instruction = "زيادة الضغط العالي، تفعيل الأظهرة، وبناء الهجمات من الأطراف."
        elif 10 < time_left <= 30:
            formation = "3-4-3 (هجوم شامل) - All Out Attack"
            instruction = "إدخال مهاجم إضافي، التمرير الطويل المباشر، وشن هجمات سريعة."
        else:
            formation = "3-3-4 (إنقاذ) - Long Ball"
            instruction = "الدفاع برجلين فقط، حارس المرمى يشارك في الهجمات، العرضيات العشوائية."

        st.markdown(f"""
        <div class="vip-card">
            <h3 style="color:#ffaa00; margin-top:0;">{d[19]}</h3>
            <p><b>{d[20]}</b> {formation}</p>
            <p><b>{d[21]}</b> {instruction}</p>
        </div>
        """, unsafe_allow_html=True)
    elif opp_score == our_score:
        st.warning("🤝 التعادل! تحتاج لهدف الفوز. جرب خطة (4-2-3-1) مع تفعيل صانع الألعاب.")
    else:
        st.success("✅ أنت متقدم! حافظ على التمركز الدفاعي (5-3-2) واستغل المساحات بالهجمات المرتدة.")

# ═══════════════════════════════════════════════════════════════
# 6️⃣ زر العودة
# ═══════════════════════════════════════════════════════════════
st.write("---")
if st.button(d[22], use_container_width=True):
    st.switch_page("app.py")
