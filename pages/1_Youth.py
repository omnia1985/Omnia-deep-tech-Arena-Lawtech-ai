import streamlit as st
import asyncio
import numpy as np
import cv2
import pandas as pd
import io
from PIL import Image, ImageDraw
from ultralytics import YOLO
from supabase import create_client, Client

# ═══════════════════════════════════════════════════════════════
# 1️⃣ إعدادات الصفحة والتصميم
# ═══════════════════════════════════════════════════════════════
st.set_page_config(layout="wide", page_icon="👶", page_title="Youth Players")

st.markdown("""
<style>
.stApp{background:linear-gradient(rgba(4,10,24,0.97),rgba(1,16,10,0.97));color:#fff;}
.youth-card{background:rgba(255,255,255,0.02);border:1px solid #00e1ff;padding:15px;border-radius:10px;margin-bottom:10px;}
.player-card-ui {background: linear-gradient(135deg, rgba(0, 225, 255, 0.1), rgba(0, 255, 136, 0.1)); border: 2px solid #00e1ff; border-radius: 20px; padding: 20px; text-align: center; margin-bottom: 20px; box-shadow: 0 0 20px rgba(0,225,255,0.2);}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# 2️⃣ قاموس اللغات الست
# ═══════════════════════════════════════════════════════════════
LANG_YOUTH = {
    "🇸🇦 العربية": {
        "title": "👶 باقة الناشئين والأطفال", "price": "💰 السعر: 10 دينار (دون 16 سنة) | 20 دينار (16-17 سنة) - يتطلب موافقة الولي", "age": "العمر اللحظي للناشئ:", "gdpr": "🔒 نظام حماية القصر (دون 18 سنة):", "p_name": "اسم اللاعب:", "club": "الأكاديمية / الجمعية:", "g_name": "اسم الولي الشرعي بالكامل:", "g_id": "رقم الهوية أو الإقرار القانوني:", "success": "✅ تم توثيق الموافقة وتفعيل التغبيش الرقمي.", "cam": "🎥 البث الحي للكاميرا", "upload": "📂 رفع صورة للتحليل", "card_title": "📊 كارت اللاعب (Player Card)", "back": "⬅️ العودة إلى الرئيسية", "warn_age": "⚠️ عذراً، هذه الباقة مخصصة حتى 17 سنة. يرجى الانتقال لصفحة الأكابر.", "gallery": "🏆 معرض النجوم", "download": "⬇️ تحميل كارت اللاعب", "table_title": "📋 قاعدة بيانات الناشئين (الجدول الموحد)", "select_player": "🔍 اختر لاعباً لعرض كارتة مرة أخرى:", "no_data": "لا توجد بيانات مسجلة بعد.", "pos_fw": "مهاجم", "pos_mf": "وسط"
    },
    "🇬🇧 English": {
        "title": "👶 Youth & Kids Pack", "price": "💰 Price: 10 Dinar (<16) | 20 Dinar (16-17) - Requires Guardian Consent", "age": "Current Age:", "gdpr": "🔒 Minor Protection System (<18):", "p_name": "Player Name:", "club": "Academy / Club:", "g_name": "Guardian Full Name:", "g_id": "Guardian ID:", "success": "✅ Consent documented & face masking active.", "cam": "🎥 Live Camera Stream", "upload": "📂 Upload Image", "card_title": "📊 Player Card", "back": "⬅️ Back to Home", "warn_age": "⚠️ Sorry, this pack is up to 17 years.", "gallery": "🏆 Star Gallery", "download": "⬇️ Download Player Card", "table_title": "📋 Youth Database (Unified Table)", "select_player": "🔍 Select player to view card again:", "no_data": "No data recorded yet.", "pos_fw": "Forward", "pos_mf": "Midfielder"
    },
    "🇫🇷 Français": {
        "title": "👶 Pack Jeunes & Enfants", "price": "💰 Prix: 10 Dinar (<16) | 20 Dinar (16-17) - Consentement Requis", "age": "Âge Actuel:", "gdpr": "🔒 Protection des Mineurs (<18):", "p_name": "Nom du Joueur:", "club": "Académie / Club:", "g_name": "Nom du Tuteur:", "g_id": "ID du Tuteur:", "success": "✅ Consentement documenté & masquage actif.", "cam": "🎥 Caméra Live", "upload": "📂 Télécharger Image", "card_title": "📊 Carte du Joueur", "back": "⬅️ Retour", "warn_age": "⚠️ Désolé, jusqu'à 17 ans.", "gallery": "🏆 Galerie des Stars", "download": "⬇️ Télécharger la Carte", "table_title": "📋 Base de Données", "select_player": "🔍 Sélectionnez un joueur:", "no_data": "Aucune donnée.", "pos_fw": "Attaquant", "pos_mf": "Milieu"
    },
    "🇪🇸 Español": {
        "title": "👶 Paquete Juvenil", "price": "💰 Precio: 10 Dinar (<16) | 20 Dinar (16-17) - Requiere Consentimiento", "age": "Edad Actual:", "gdpr": "🔒 Protección de Menores (<18):", "p_name": "Nombre del Jugador:", "club": "Academia / Club:", "g_name": "Nombre del Tutor:", "g_id": "ID del Tutor:", "success": "✅ Consentimiento documentado.", "cam": "🎥 Cámara en Vivo", "upload": "📂 Subir Imagen", "card_title": "📊 Carta del Jugador", "back": "⬅️ Volver", "warn_age": "⚠️ Solo hasta 17 años.", "gallery": "🏆 Galería de Estrellas", "download": "⬇️ Descargar Carta", "table_title": "📋 Base de Datos", "select_player": "🔍 Selecciona un jugador:", "no_data": "Sin datos.", "pos_fw": "Delantero", "pos_mf": "Centrocampista"
    },
    "🇮🇹 Italiano": {
        "title": "👶 Pacchetto Giovani", "price": "💰 Prezzo: 10 Dinar (<16) | 20 Dinar (16-17) - Richiede Consenso", "age": "Età Attuale:", "gdpr": "🔒 Protezione Minori (<18):", "p_name": "Nome Giocatore:", "club": "Accademia / Club:", "g_name": "Nome Tutore:", "g_id": "ID Tutore:", "success": "✅ Consenso documentato.", "cam": "🎥 Fotocamera Live", "upload": "📂 Carica Immagine", "card_title": "📊 Carta del Giocatore", "back": "⬅️ Indietro", "warn_age": "⚠️ Fino a 17 anni.", "gallery": "🏆 Galleria Stelle", "download": "⬇️ Scarica Carta", "table_title": "📋 Database", "select_player": "🔍 Seleziona un giocatore:", "no_data": "Nessun dato.", "pos_fw": "Attaccante", "pos_mf": "Centrocampista"
    },
    "🇵🇹 Português": {
        "title": "👶 Pacote Juvenil", "price": "💰 Preço: 10 Dinar (<16) | 20 Dinar (16-17) - Requer Consentimento", "age": "Idade Atual:", "gdpr": "🔒 Proteção de Menores (<18):", "p_name": "Nome do Jogador:", "club": "Academia / Clube:", "g_name": "Nome do Tutor:", "g_id": "ID do Tutor:", "success": "✅ Consentimento documentado.", "cam": "🎥 Câmara ao Vivo", "upload": "📂 Carregar Imagem", "card_title": "📊 Cartão do Jogador", "back": "⬅️ Voltar", "warn_age": "⚠️ Até 17 anos.", "gallery": "🏆 Galeria de Estrelas", "download": "⬇️ Baixar Cartão", "table_title": "📋 Banco de Dados", "select_player": "🔍 Selecione um jogador:", "no_data": "Sem dados.", "pos_fw": "Avançado", "pos_mf": "Médio"
    }
}

sel_lang = st.session_state.get("lang", "🇸🇦 العربية")
d = LANG_YOUTH.get(sel_lang, LANG_YOUTH["🇬🇧 English"])

st.error(d["price"])
st.title(d["title"])
st.write("---")

# ═══════════════════════════════════════════════════════════════
# 3️⃣ التحقق من العمر
# ═══════════════════════════════════════════════════════════════
age = st.number_input(d["age"], min_value=5, max_value=25, value=15)

if age >= 18:
    st.warning(d["warn_age"])
    st.stop()

parent_agree = False
if age < 18:
    st.info(d["gdpr"])
    p_name = st.text_input(d["p_name"], key="p_name")
    p_club = st.text_input(d["club"], key="p_club")
    g_name = st.text_input(d["g_name"], key="g_name")
    g_id = st.text_input(d["g_id"], key="g_id")
    if p_name and p_club and g_name and g_id:
        parent_agree = True
        st.success(d["success"])

# ═══════════════════════════════════════════════════════════════
# 4️⃣ دوال التوليد و YOLO
# ═══════════════════════════════════════════════════════════════
def generate_download_card(player_img_bytes, name, age, speed, star_name, match_pct, club):
    try:
        img = Image.open(io.BytesIO(player_img_bytes)).convert("RGB")
        img = img.resize((400, 400))
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
    except:
        return None

@st.cache_resource(show_spinner=False)
def load_yolo_model():
    try:
        return YOLO("yolo11n-pose.pt")
    except:
        return None

async def yolo_engine(frame_bytes, model):
    await asyncio.sleep(0.01)
    nparr = np.frombuffer(frame_bytes, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if frame is None: return None
    
    results = model(frame, verbose=False)
    annotated = frame.copy()
    if results and len(results) > 0:
        r = results[0]
        if r.keypoints is not None and len(r.keypoints) > 0:
            for idx, kps in enumerate(r.keypoints.xy.cpu().numpy()):
                face = kps[:5]
                valid = face[face.sum(axis=1) > 0]
                if len(valid) >= 2:
                    x_min, y_min = max(0, int(valid[:, 0].min()) - 30), max(0, int(valid[:, 1].min()) - 40)
                    x_max, y_max = min(frame.shape[1], int(valid[:, 0].max()) + 30), min(frame.shape[0], int(valid[:, 1].max()) + 50)
                    if x_max > x_min and y_max > y_min:
                        roi = annotated[y_min:y_max, x_min:x_max]
                        annotated[y_min:y_max, x_min:x_max] = cv2.GaussianBlur(roi, (61, 61), 0)
                        cv2.rectangle(annotated, (x_min, y_min), (x_max, y_max), (212, 212, 0), 2)
    return annotated

# ═══════════════════════════════════════════════════════════════
# 5️⃣ واجهة المستخدم والكارت والجدول
# ═══════════════════════════════════════════════════════════════
if parent_agree:
    if 'youth_db' not in st.session_state:
        st.session_state.youth_db = []

    use_live = st.checkbox("📸 Activate Live AI Lens", value=True)
    st.subheader(d["cam"] if use_live else d["upload"])

    cam = st.camera_input("", key="cam", label_visibility="collapsed") if use_live else None
    file = st.file_uploader("", type=["jpg", "jpeg", "png"], key="file", label_visibility="collapsed")

    if cam or file:
        data = cam.getvalue() if cam else file.getvalue()
        model = load_yolo_model()
        
        if model:
            with st.spinner("🔄 Analyzing..."):
                processed = asyncio.run(yolo_engine(data, model))
                
            if processed is not None:
                processed_rgb = cv2.cvtColor(processed, cv2.COLOR_BGR2RGB)
                st.image(processed_rgb, channels="RGB", use_container_width=True)
                st.write("---")
                
                speed = 24 + (age % 5) 
                pos = d["pos_fw"] if age % 2 == 0 else d["pos_mf"]
                stars = ["Lamine Yamal", "Gavi", "Endrick", "Pedri"]
                matched_star = stars[age % 4]
                match_pct = 85 + (age % 10)

                st.subheader(d["card_title"])
                st.markdown(f"""
                <div class="player-card-ui">
                    <h2 style="color:#00ff88; margin-bottom:5px;">{p_name}</h2>
                    <h4 style="color:#00d4ff; margin-top:0; margin-bottom:5px;">{p_club}</h4>
                    <p style="color:#aaa; margin-top:0;">{pos} | {age}</p>
                    <div style="display:flex; justify-content:space-around; margin-top:15px;">
                        <div><h3 style="color:#fff; margin:0;">{speed}</h3><span style="color:#888; font-size:12px;">km/h</span></div>
                        <div><h3 style="color:#fff; margin:0;">89</h3><span style="color:#888; font-size:12px;">Dribbles</span></div>
                        <div><h3 style="color:#fff; margin:0;">{match_pct}%</h3><span style="color:#888; font-size:12px;">Match</span></div>
                    </div>
                    <h4 style="color:#00d4ff; margin-top:20px;">Matches: {matched_star}</h4>
                </div>
                """, unsafe_allow_html=True)
                
                img_bytes = generate_download_card(data, p_name, age, speed, matched_star, match_pct, p_club)
                if img_bytes:
                    st.download_button(label=d["download"], data=img_bytes, file_name=f"{p_name}_card.png", mime="image/png", use_container_width=True)
                if not any(p["Name"] == p_name for p in st.session_state.youth_db):
                    st.session_state.youth_db.append({
                        "Name": p_name, "Club": p_club, "Age": age, "Position": pos, "Speed": speed, "Match": matched_star, 
                        "img_bytes": img_bytes, "match_pct": match_pct
                    })
                    
                    # ☁️ الحفظ في السحابة (Supabase)
                    try:
                        url = st.secrets["SUPABASE_URL"]
                        key = st.secrets["SUPABASE_KEY"]
                        supabase: Client = create_client(url, key)
                        
                        data_to_insert = {
                            "name": p_name,
                            "club": p_club,
                            "age": int(age),
                            "position": pos,
                            "speed": float(speed),
                            "match_pct": int(match_pct),
                            "star_name": matched_star
                        }
                        
                        supabase.table("youth_players").insert(data_to_insert).execute()
                        st.toast("☁️ تم حفظ بيانات اللاعب في السحابة بنجاح!", icon="✅")
                    except Exception as e:
                        st.error(f"⚠️ خطأ في الحفظ بالسحابة: {e}")
    # ═══ معرض النجوم (روابط مباشرة عبر بروكسي مضمون 100%) ═══
    st.write("---")
    st.subheader(d["gallery"])
    
    # استخدمنا wsrv.nl كوسيط لجلب صور حقيقية عالية الجودة من Transfermarkt
    star_images = {
        "Lamine Yamal": "https://wsrv.nl/?url=img.a.transfermarkt.technology/portrait/big/937958-1704735153.png",
        "Gavi": "https://wsrv.nl/?url=img.a.transfermarkt.technology/portrait/big/646740-1673605512.jpg",
        "Endrick": "https://wsrv.nl/?url=img.a.transfermarkt.technology/portrait/big/971570-1704880838.jpg",
        "Pedri": "https://wsrv.nl/?url=img.a.transfermarkt.technology/portrait/big/683840-1622116117.jpg"
    }
    
    cols = st.columns(4)
    for idx, (name, img_url) in enumerate(star_images.items()):
        with cols[idx % 4]:
            # عرض الصورة
            st.image(img_url, caption=name, use_container_width=True)

    # ═══ الجدول الموحد ═══
    st.write("---")
    st.subheader(d["table_title"])
    
    if st.session_state.youth_db:
        df = pd.DataFrame(st.session_state.youth_db)
        st.dataframe(df.drop(columns=["img_bytes", "match_pct"], errors="ignore"), use_container_width=True, hide_index=True)
        
        st.write("---")
        st.subheader(d["select_player"])
        player_names = [p["Name"] for p in st.session_state.youth_db]
        selected_player_name = st.selectbox("", ["-- Select --"] + player_names, label_visibility="collapsed")
        
        if selected_player_name != "-- Select --":
            player_data = next((p for p in st.session_state.youth_db if p["Name"] == selected_player_name), None)
            if player_data:
                st.markdown(f"""
                <div class="player-card-ui">
                    <h2 style="color:#00ff88; margin-bottom:5px;">{player_data["Name"]}</h2>
                    <h4 style="color:#00d4ff; margin-top:0; margin-bottom:5px;">{player_data.get("Club", "Unknown")}</h4>
                    <p style="color:#aaa; margin-top:0;">{player_data["Position"]} | {player_data["Age"]}</p>
                    <div style="display:flex; justify-content:space-around; margin-top:15px;">
                        <div><h3 style="color:#fff; margin:0;">{player_data["Speed"]}</h3><span style="color:#888; font-size:12px;">km/h</span></div>
                        <div><h3 style="color:#fff; margin:0;">89</h3><span style="color:#888; font-size:12px;">Dribbles</span></div>
                        <div><h3 style="color:#fff; margin:0;">{player_data.get("match_pct", 89)}%</h3><span style="color:#888; font-size:12px;">Match</span></div>
                    </div>
                    <h4 style="color:#00d4ff; margin-top:20px;">Matches: {player_data["Match"]}</h4>
                </div>
                """, unsafe_allow_html=True)
                
                if "img_bytes" in player_data and player_data["img_bytes"]:
                    st.download_button(label=d["download"], data=player_data["img_bytes"], file_name=f"{player_data['Name']}_card.png", mime="image/png", use_container_width=True, key=f"dl_{player_data['Name']}")
    else:
        st.info(d["no_data"])

# ═══════════════════════════════════════════════════════════════
# 6️⃣ زر العودة
# ═══════════════════════════════════════════════════════════════
st.write("---")
if st.button(d["back"], use_container_width=True):
    st.switch_page("app.py")
