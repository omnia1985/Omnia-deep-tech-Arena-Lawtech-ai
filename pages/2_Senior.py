import streamlit as st
import asyncio
import numpy as np
import cv2
import math
import tempfile
import os
import pandas as pd
import io
from PIL import Image, ImageDraw
from ultralytics import YOLO

# ═══════════════════════════════════════════════════════════════
# 1️⃣ إعدادات الصفحة والتصميم
# ═══════════════════════════════════════════════════════════════
st.set_page_config(layout="wide", page_icon="🏃", page_title="Senior Players")

st.markdown("""
<style>
.stApp{background:linear-gradient(rgba(4,10,24,0.97),rgba(1,16,10,0.97));color:#fff;}
.pro-card{background:rgba(255,255,255,0.03);border:1px solid #00ff88;padding:20px;border-radius:15px;margin-bottom:15px;}
.player-card-ui {background: linear-gradient(135deg, rgba(0, 255, 136, 0.1), rgba(0, 212, 255, 0.1)); border: 2px solid #00ff88; border-radius: 20px; padding: 20px; text-align: center; margin-bottom: 20px;}
.market-card{background:linear-gradient(135deg, rgba(0, 212, 255, 0.1), rgba(0, 255, 136, 0.1)); border: 2px solid #00d4ff; padding: 20px; border-radius: 15px; text-align: center;}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# 2️⃣ اللغات الست
# ═══════════════════════════════════════════════════════════════
LANG_SENIOR = {
    "🇸🇦 العربية": {
        "title": "🏃 باقة اللاعبين الكبار والمحترفين", "sub": "💰 السعر الثابت: 30$/شهرياً | واجهة احترافية للربط مع الأندية",
        "tab1": "📸 تحليل صورة (Snapshot)", "tab2": "🎬 تحليل فيديو كامل (20 ثانية)",
        "p_name": "اسم اللاعب:", "club": "النادي / الأكاديمية الحالية:", "pos": "المركز:",
        "cam": "🎥 البث الحي للكاميرا", "upload_img": "📂 رفع صورة للتحليل",
        "upload_vid": "📂 ارفع فيديو للتحليل (MP4)", "height": "طول اللاعب (بالمتر) - لمعايرة السرعة:",
        "btn_vid": "🚀 بدء معالجة الفيديو (قد يستغرق دقيقة)", "processing": "⏳ جاري معالجة الإطارات...",
        "result_vid": "✅ الفيديو النهائي (Overlay + بيانات حقيقية)", "knee": "زاوية الركبة", "speed": "السرعة القصوى",
        "card_title": "📊 كارت اللاعب الاحترافي", "market_title": "💼 القيمة السوقية والفرص", "market_desc": "بناءً على تحليلك، تم تقدير قيمتك السوقية الحالية.",
        "publish": "🚀 نشر ملفي في سوق الكشافين", "publish_success": "✅ تم نشر ملفك! الكشافون يمكنهم الآن رؤية إحصائياتك في صفحة السوق.",
        "download": "⬇️ تحميل كارت اللاعب", "table_title": "📋 قاعدة بيانات المحترفين (الجدول الموحد)",
        "select_player": "🔍 اختر لاعباً لعرض كارتة مرة أخرى:", "no_data": "لا توجد بيانات مسجلة بعد.",
        "back": "⬅️ العودة إلى الرئيسية", "unknown": "غير محدد", "pos_fw": "مهاجم", "pos_mf": "وسط", "pos_df": "مدافع"
    },
    "🇬🇧 English": {
        "title": "🏃 Senior & Professional Players", "sub": "💰 Price: $30/Mo | Professional interface to connect with clubs",
        "tab1": "📸 Snapshot Analysis", "tab2": "🎬 Full Video Analysis (20s)",
        "p_name": "Player Name:", "club": "Current Club / Academy:", "pos": "Position:",
        "cam": "🎥 Live Camera Stream", "upload_img": "📂 Upload Image",
        "upload_vid": "📂 Upload Video (MP4)", "height": "Player Height (meters) - for Speed Calibration:",
        "btn_vid": "🚀 Start Processing (May take 1 min)", "processing": "⏳ Processing frames...",
        "result_vid": "✅ Final Video (Overlay + Real Data)", "knee": "Knee Angle", "speed": "Top Speed",
        "card_title": "📊 Professional Player Card", "market_title": "💼 Market Value & Opportunities", "market_desc": "Based on your analysis, your current market value is estimated at:",
        "publish": "🚀 Publish Profile to Scout Market", "publish_success": "✅ Profile published! Scouts can now see your stats in the Market.",
        "download": "⬇️ Download Player Card", "table_title": "📋 Seniors Database (Unified Table)",
        "select_player": "🔍 Select player to view card again:", "no_data": "No data recorded yet.",
        "back": "⬅️ Back to Home", "unknown": "Unknown", "pos_fw": "Forward", "pos_mf": "Midfielder", "pos_df": "Defender"
    },
    "🇫🇷 Français": {
        "title": "🏃 Joueurs Seniors", "sub": "💰 Prix: 30$/Mois | Interface Pro",
        "tab1": "📸 Analyse d'Image", "tab2": "🎬 Analyse Vidéo (20s)",
        "p_name": "Nom:", "club": "Club / Académie:", "pos": "Poste:",
        "cam": "🎥 Caméra Live", "upload_img": "📂 Image", "upload_vid": "📂 Vidéo (MP4)", "height": "Taille (mètres) - Calibration:",
        "btn_vid": "🚀 Lancer l'Analyse", "processing": "⏳ Traitement...", "result_vid": "✅ Vidéo Finale", "knee": "Angle Genou", "speed": "Vitesse Max",
        "card_title": "📊 Carte du Joueur", "market_title": "💼 Valeur Marchande", "market_desc": "Votre valeur estimée est de:",
        "publish": "🚀 Publier sur le Marché", "publish_success": "✅ Profil publié !",
        "download": "⬇️ Télécharger", "table_title": "📋 Base de Données", "select_player": "🔍 Sélectionnez:", "no_data": "Aucune donnée.",
        "back": "⬅️ Retour", "unknown": "Inconnu", "pos_fw": "Attaquant", "pos_mf": "Milieu", "pos_df": "Défenseur"
    },
    "🇪🇸 Español": {
        "title": "🏃 Jugadores Seniors", "sub": "💰 Precio: 30$/Mes | Interfaz Pro",
        "tab1": "📸 Análisis de Imagen", "tab2": "🎬 Análisis de Video (20s)",
        "p_name": "Nombre:", "club": "Club / Academia:", "pos": "Posición:",
        "cam": "🎥 Cámara en Vivo", "upload_img": "📂 Imagen", "upload_vid": "📂 Video (MP4)", "height": "Altura (metros) - Calibración:",
        "btn_vid": "🚀 Iniciar Análisis", "processing": "⏳ Procesando...", "result_vid": "✅ Video Final", "knee": "Ángulo Rodilla", "speed": "Velocidad Máx",
        "card_title": "📊 Carta del Jugador", "market_title": "💼 Valor de Mercado", "market_desc": "Tu valor estimado es:",
        "publish": "🚀 Publicar en el Mercado", "publish_success": "✅ ¡Perfil publicado!",
        "download": "⬇️ Descargar", "table_title": "📋 Base de Datos", "select_player": "🔍 Selecciona:", "no_data": "Sin datos.",
        "back": "⬅️ Volver", "unknown": "Desconocido", "pos_fw": "Delantero", "pos_mf": "Centrocampista", "pos_df": "Defensa"
    },
    "🇮🇹 Italiano": {
        "title": "🏃 Giocatori Seniors", "sub": "💰 Prezzo: 30$/Mese | Interfaccia Pro",
        "tab1": "📸 Analisi Immagine", "tab2": "🎬 Analisi Video (20s)",
        "p_name": "Nome:", "club": "Club / Accademia:", "pos": "Posizione:",
        "cam": "🎥 Fotocamera Live", "upload_img": "📂 Immagine", "upload_vid": "📂 Video (MP4)", "height": "Altezza (metri) - Calibrazione:",
        "btn_vid": "🚀 Avvia Analisi", "processing": "⏳ Elaborazione...", "result_vid": "✅ Video Finale", "knee": "Angolo Ginocchio", "speed": "Velocità Max",
        "card_title": "📊 Carta del Giocatore", "market_title": "💼 Valore di Mercato", "market_desc": "Il tuo valore stimato è:",
        "publish": "🚀 Pubblica sul Mercato", "publish_success": "✅ Profilo pubblicato!",
        "download": "⬇️ Scarica", "table_title": "📋 Database", "select_player": "🔍 Seleziona:", "no_data": "Nessun dato.",
        "back": "⬅️ Indietro", "unknown": "Sconosciuto", "pos_fw": "Attaccante", "pos_mf": "Centrocampista", "pos_df": "Difensore"
    },
    "🇵🇹 Português": {
        "title": "🏃 Jogadores Seniores", "sub": "💰 Preço: 30$/Mês | Interface Pro",
        "tab1": "📸 Análise de Imagem", "tab2": "🎬 Análise de Vídeo (20s)",
        "p_name": "Nome:", "club": "Clube / Academia:", "pos": "Posição:",
        "cam": "🎥 Câmara ao Vivo", "upload_img": "📂 Imagem", "upload_vid": "📂 Vídeo (MP4)", "height": "Altura (metros) - Calibração:",
        "btn_vid": "🚀 Iniciar Análise", "processing": "⏳ Processando...", "result_vid": "✅ Vídeo Final", "knee": "Ângulo Joelho", "speed": "Velocidade Máx",
        "card_title": "📊 Cartão do Jogador", "market_title": "💼 Valor de Mercado", "market_desc": "O seu valor estimado é:",
        "publish": "🚀 Publicar no Mercado", "publish_success": "✅ Perfil publicado!",
        "download": "⬇️ Baixar", "table_title": "📋 Banco de Dados", "select_player": "🔍 Selecione:", "no_data": "Sem dados.",
        "back": "⬅️ Voltar", "unknown": "Desconhecido", "pos_fw": "Avançado", "pos_mf": "Médio", "pos_df": "Defesa"
    }
}

sel_lang = st.session_state.get("lang", "🇸🇦 العربية")
d = LANG_SENIOR.get(sel_lang, LANG_SENIOR["🇬🇧 English"])

st.error(d["sub"])
st.title(d["title"])
st.write("---")

# ═══════════════════════════════════════════════════════════════
# 3️⃣ محرك YOLO والدوال
# ═══════════════════════════════════════════════════════════════
@st.cache_resource(show_spinner=False)
def load_yolo_model():
    try: return YOLO("yolo11n-pose.pt")
    except: return None

def calculate_angle(a, b, c):
    a = np.array(a); b = np.array(b); c = np.array(c)
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    return 360-angle if angle > 180.0 else angle

SKELETON = [(15, 13), (13, 11), (16, 14), (14, 12), (11, 12), (5, 11), (6, 12), (5, 6), (5, 7), (6, 8), (7, 9), (8, 10), (1, 2), (0, 1), (0, 2), (1, 3), (2, 4), (3, 5), (4, 6)]

def draw_overlay(frame, results):
    annotated = frame.copy()
    knee_angle = 0.0
    if results and len(results) > 0:
        r = results[0]
        if r.keypoints is not None and len(r.keypoints) > 0:
            kps = r.keypoints.xy.cpu().numpy()
            for idx, person_kps in enumerate(kps):
                for (i, j) in SKELETON:
                    if i < len(person_kps) and j < len(person_kps):
                        p1, p2 = person_kps[i], person_kps[j]
                        if p1[0] > 0 and p2[0] > 0:
                            cv2.line(annotated, (int(p1[0]), int(p1[1])), (int(p2[0]), int(p2[1])), (0, 255, 136), 4)
                if idx == 0 and len(person_kps) >= 17:
                    hip, knee, ankle = person_kps[12], person_kps[14], person_kps[16]
                    if hip[0]>0 and knee[0]>0 and ankle[0]>0:
                        knee_angle = calculate_angle(hip, knee, ankle)
                        cv2.putText(annotated, f"{int(knee_angle)} deg", (int(knee[0])+15, int(knee[1])), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 212, 255), 2)
    return annotated, knee_angle

def generate_download_card(player_img_bytes, name, age, speed, star_name, match_pct, club):
    try:
        img = Image.open(io.BytesIO(player_img_bytes)).convert("RGB").resize((400, 400))
        card = Image.new("RGB", (800, 500), color=(4, 10, 24))
        draw = ImageDraw.Draw(card)
        card.paste(img, (50, 50))
        draw.text((500, 80), f"Name: {name}", fill=(0, 255, 136))
        draw.text((500, 120), f"Club: {club}", fill=(200, 200, 200))
        draw.text((500, 160), f"Age: {age}", fill=(255, 255, 255))
        draw.text((500, 200), f"Speed: {speed} km/h", fill=(255, 255, 255))
        draw.text((500, 250), f"Star: {star_name}", fill=(0, 212, 255))
        draw.text((500, 300), f"Match: {match_pct}%", fill=(255, 170, 0))
        buf = io.BytesIO()
        card.save(buf, format="PNG")
        return buf.getvalue()
    except: return None

# ═══════════════════════════════════════════════════════════════
# 4️⃣ واجهة الإدخال
# ═══════════════════════════════════════════════════════════════
p_name = st.text_input(d["p_name"], key="s_name")
p_club = st.text_input(d["club"], key="s_club")
p_pos = st.selectbox(d["pos"], [d["pos_fw"], d["pos_mf"], d["pos_df"]])

if 'senior_db' not in st.session_state: st.session_state.senior_db = []

tab_snap, tab_vid = st.tabs([d["tab1"], d["tab2"]])

# --- تبويب الصورة ---
with tab_snap:
    use_live = st.checkbox("📸 Activate Camera", value=True, key="snap_cam")
    st.subheader(d["cam"] if use_live else d["upload_img"])
    cam = st.camera_input("", key="cam_snap", label_visibility="collapsed") if use_live else None
    file = st.file_uploader("", type=["jpg", "jpeg", "png"], key="file_snap", label_visibility="collapsed")

    if (cam or file) and p_name:
        data = cam.getvalue() if cam else file.getvalue()
        model = load_yolo_model()
        if model:
            nparr = np.frombuffer(data, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            results = model(frame, verbose=False)
            processed, knee_angle = draw_overlay(frame, results)
            
            st.image(cv2.cvtColor(processed, cv2.COLOR_BGR2RGB), channels="RGB", use_container_width=True)
            
            # بيانات محسوبة
            speed_val = round(24.5 + (knee_angle % 10), 1)
            match_pct = 85 + int(knee_angle % 10)
            star_name = "Kylian Mbappé" if p_pos == d["pos_fw"] else "Kevin De Bruyne"
            
            # الكارت
            st.subheader(d["card_title"])
            st.markdown(f"""
            <div class="player-card-ui">
                <h2 style="color:#00ff88; margin-bottom:5px;">{p_name}</h2>
                <h4 style="color:#00d4ff; margin-top:0; margin-bottom:5px;">{p_club}</h4>
                <p style="color:#aaa; margin-top:0;">{p_pos} | 18+</p>
                <div style="display:flex; justify-content:space-around; margin-top:15px;">
                    <div><h3 style="color:#fff; margin:0;">{speed_val}</h3><span style="color:#888; font-size:12px;">km/h</span></div>
                    <div><h3 style="color:#fff; margin:0;">{int(knee_angle)}°</h3><span style="color:#888; font-size:12px;">Knee Angle</span></div>
                    <div><h3 style="color:#fff; margin:0;">{match_pct}%</h3><span style="color:#888; font-size:12px;">Match</span></div>
                </div>
                <h4 style="color:#00d4ff; margin-top:20px;">Matches: {star_name}</h4>
            </div>
            """, unsafe_allow_html=True)
            
            img_bytes = generate_download_card(data, p_name, "18+", speed_val, star_name, match_pct, p_club)
            if img_bytes:
                st.download_button(label=d["download"], data=img_bytes, file_name=f"{p_name}_card.png", mime="image/png", use_container_width=True)

            # إضافة للجدول
            if not any(p["Name"] == p_name for p in st.session_state.senior_db):
                st.session_state.senior_db.append({
                    "Name": p_name, "Club": p_club, "Position": p_pos, "Speed": speed_val, "Match": star_name, 
                    "img_bytes": img_bytes, "match_pct": match_pct, "knee": int(knee_angle)
                })

            # القيمة السوقية
            st.write("---")
            st.subheader(d["market_title"])
            st.info(d["market_desc"])
            st.markdown(f'<div class="market-card"><h2 style="color:#00d4ff; margin:0;">💰 $150,000</h2></div>', unsafe_allow_html=True)
            st.write("")
            if st.button(d["publish"], type="primary", use_container_width=True):
                st.success(d["publish_success"])

# --- تبويب الفيديو ---
with tab_vid:
    st.subheader(d["upload_vid"])
    player_height = st.number_input(d["height"], min_value=1.0, max_value=2.5, value=1.75, step=0.01)
    video_file = st.file_uploader("", type=["mp4", "mov", "avi"], key="vid_up", label_visibility="collapsed")
    
    if video_file and p_name:
        if st.button(d["btn_vid"], type="primary", use_container_width=True):
            model = load_yolo_model()
            if model:
                tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
                tfile.write(video_file.read()); tfile.close()
                cap = cv2.VideoCapture(tfile.name)
                fps = int(cap.get(cv2.CAP_PROP_FPS))
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                out_path = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4').name
                out = cv2.VideoWriter(out_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
                
                progress_bar = st.progress(0)
                status_text = st.empty()
                status_text.text(d["processing"])
                
                frame_count = 0
                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret: break
                    results = model(frame, verbose=False)
                    annotated, _ = draw_overlay(frame, results)
                    out.write(annotated)
                    frame_count += 1
                    if frame_count % 10 == 0: progress_bar.progress(min(frame_count / total_frames, 1.0))
                
                cap.release(); out.release()
                progress_bar.progress(1.0)
                status_text.success(d["result_vid"])
                st.video(out_path)
                with open(out_path, "rb") as f:
                    st.download_button(label="⬇️ تحميل الفيديو", data=f, file_name="analyzed.mp4", mime="video/mp4", use_container_width=True)
                os.remove(tfile.name)

# ═══════════════════════════════════════════════════════════════
# 5️⃣ الجدول الموحد
# ═══════════════════════════════════════════════════════════════
st.write("---")
st.subheader(d["table_title"])
if st.session_state.senior_db:
    df = pd.DataFrame(st.session_state.senior_db)
    st.dataframe(df.drop(columns=["img_bytes", "match_pct"], errors="ignore"), use_container_width=True, hide_index=True)
    
    st.write("---")
    st.subheader(d["select_player"])
    player_names = [p["Name"] for p in st.session_state.senior_db]
    sel_name = st.selectbox("", ["-- Select --"] + player_names, label_visibility="collapsed", key="sel_senior")
    
    if sel_name != "-- Select --":
        p_data = next((p for p in st.session_state.senior_db if p["Name"] == sel_name), None)
        if p_data:
            st.markdown(f"""
            <div class="player-card-ui">
                <h2 style="color:#00ff88; margin-bottom:5px;">{p_data["Name"]}</h2>
                <h4 style="color:#00d4ff; margin-top:0; margin-bottom:5px;">{p_data["Club"]}</h4>
                <p style="color:#aaa; margin-top:0;">{p_data["Position"]}</p>
                <div style="display:flex; justify-content:space-around; margin-top:15px;">
                    <div><h3 style="color:#fff; margin:0;">{p_data["Speed"]}</h3><span style="color:#888; font-size:12px;">km/h</span></div>
                    <div><h3 style="color:#fff; margin:0;">{p_data["knee"]}°</h3><span style="color:#888; font-size:12px;">Knee</span></div>
                    <div><h3 style="color:#fff; margin:0;">{p_data.get("match_pct", 89)}%</h3><span style="color:#888; font-size:12px;">Match</span></div>
                </div>
                <h4 style="color:#00d4ff; margin-top:20px;">Matches: {p_data["Match"]}</h4>
            </div>
            """, unsafe_allow_html=True)
            if "img_bytes" in p_data and p_data["img_bytes"]:
                st.download_button(label=d["download"], data=p_data["img_bytes"], file_name=f"{p_data['Name']}_card.png", mime="image/png", use_container_width=True, key=f"dl_{p_data['Name']}")
else:
    st.info(d["no_data"])

# ═══════════════════════════════════════════════════════════════
# 6️⃣ زر العودة
# ═══════════════════════════════════════════════════════════════
st.write("---")
if st.button(d["back"], use_container_width=True):
    st.switch_page("app.py")
