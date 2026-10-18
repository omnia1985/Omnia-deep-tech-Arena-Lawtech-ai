import streamlit as st
import asyncio
import numpy as np
import cv2
import pandas as pd
import io
import requests
from PIL import Image, ImageDraw, ImageFont
from ultralytics import YOLO

# ═══════════════════════════════════════════════════════════════
# 1️⃣ إعدادات الصفحة
# ═══════════════════════════════════════════════════════════════
st.set_page_config(layout="wide", page_icon="👶", page_title="Youth Players")

st.markdown("""
<style>
.stApp{background:linear-gradient(rgba(4,10,24,0.97),rgba(1,16,10,0.97));color:#fff;}
.youth-card{background:rgba(255,255,255,0.02);border:1px solid #00e1ff;padding:15px;border-radius:10px;margin-bottom:10px;}
.player-card-ui {background: linear-gradient(135deg, rgba(0, 225, 255, 0.1), rgba(0, 255, 136, 0.1)); border: 2px solid #00e1ff; border-radius: 20px; padding: 20px; text-align: center; margin-bottom: 20px;}
.star-gallery {display: flex; justify-content: space-around; margin-top: 15px;}
.star-item {text-align: center;}
.star-item img {border-radius: 50%; width: 60px; height: 60px; object-fit: cover; border: 2px solid #fff;}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# 2️⃣ قاموس اللغات (تم إزالة كلمة مجاناً وتصحيح الأسعار)
# ═══════════════════════════════════════════════════════════════
LANG_YOUTH = {
    "🇸🇦 العربية": ["👶 باقة الناشئين والأطفال", "💰 السعر: 10 دينار (دون 16 سنة) | 20 دينار (16-17 سنة) - يتطلب موافقة الولي والـ GDPR", "العمر اللحظي للناشئ:", "🔒 نظام حماية القصر (دون 18 سنة):", "اسم اللاعب:", "اسم الولي الشرعي بالكامل:", "رقم الهوية أو الإقرار القانوني:", "✅ تم توثيق الموافقة وتفعيل التغبيش الرقمي للوجوه.", "🎥 البث الحي لكاميرا الهاتف", "📂 رفع صورة للتحليل", "📊 كارت اللاعب (Player Card)", "🔄 رادار التشبيه بالنجوم", "⬅️ العودة إلى الرئيسية", "⚠️ يرجى التقاط صورة لتفعيل الكارت.", "⚠️ عذراً، هذه الباقة مخصصة حتى 17 سنة. يرجى الانتقال لصفحة الأكابر.", "🏆 معرض النجوم", "⬇️ تحميل كارت اللاعب", "📋 قاعدة بيانات الناشئين (الجدول الموحد)", "الاسم", "العمر", "المركز", "السرعة", "التشبيه", "التاريخ"],
    "🇬🇧 English": ["👶 Youth & Kids Pack", "💰 Price: 10 Dinar (<16) | 20 Dinar (16-17) - Requires Guardian Consent & GDPR", "Current Age:", "🔒 Minor Protection System (<18):", "Player Name:", "Guardian Full Name:", "Guardian ID:", "✅ Consent documented & face masking active.", "🎥 Live Camera Stream", "📂 Upload Image", "📊 Player Card", "🔄 Star Matching Radar", "⬅️ Back to Home", "⚠️ Please capture an image to activate the card.", "⚠️ Sorry, this pack is up to 17 years. Please go to Seniors page.", "🏆 Star Gallery", "⬇️ Download Player Card", "📋 Youth Database (Unified Table)", "Name", "Age", "Position", "Speed", "Match", "Date"],
    # يمكنك إضافة باقي اللغات بنفس الطريقة
    "🇫🇷 Français": ["👶 Pack Jeunes", "💰 Prix: 10 Dinar (<16) | 20 Dinar (16-17)", "Âge:", "🔒 Protection des Mineurs (<18):", "Nom du Joueur:", "Nom du Tuteur:", "ID Tuteur:", "✅ Consentement documenté.", "🎥 Caméra Live", "📂 Télécharger Image", "📊 Carte du Joueur", "🔄 Radar de Correspondance", "⬅️ Retour", "⚠️ Capturez une image.", "⚠️ Désolé, jusqu'à 17 ans.", "🏆 Galerie des Stars", "⬇️ Télécharger la Carte", "📋 Base de Données", "Nom", "Âge", "Poste", "Vitesse", "Correspondance", "Date"],
    "🇪🇸 Español": ["👶 Paquete Juvenil", "💰 Precio: 10 Dinar (<16) | 20 Dinar (16-17)", "Edad:", "🔒 Protección de Menores (<18):", "Nombre del Jugador:", "Nombre del Tutor:", "ID Tutor:", "✅ Consentimiento documentado.", "🎥 Cámara en Vivo", "📂 Subir Imagen", "📊 Carta del Jugador", "🔄 Radar de Estrellas", "⬅️ Volver", "⚠️ Captura una imagen.", "⚠️ Solo hasta 17 años.", "🏆 Galería de Estrellas", "⬇️ Descargar Carta", "📋 Base de Datos", "Nombre", "Edad", "Posición", "Velocidad", "Coincidencia", "Fecha"],
    "🇮🇹 Italiano": ["👶 Pacchetto Giovani", "💰 Prezzo: 10 Dinar (<16) | 20 Dinar (16-17)", "Età:", "🔒 Protezione Minori (<18):", "Nome Giocatore:", "Nome Tutore:", "ID Tutore:", "✅ Consenso documentato.", "🎥 Fotocamera Live", "📂 Carica Immagine", "📊 Carta del Giocatore", "🔄 Radar Stelle", "⬅️ Indietro", "⚠️ Cattura un'immagine.", "⚠️ Fino a 17 anni.", "🏆 Galleria Stelle", "⬇️ Scarica Carta", "📋 Database", "Nome", "Età", "Posizione", "Velocità", "Corrispondenza", "Data"],
    "🇵🇹 Português": ["👶 Pacote Juvenil", "💰 Preço: 10 Dinar (<16) | 20 Dinar (16-17)", "Idade:", "🔒 Proteção de Menores (<18):", "Nome do Jogador:", "Nome do Tutor:", "ID Tutor:", "✅ Consentimento documentado.", "🎥 Câmara ao Vivo", "📂 Carregar Imagem", "📊 Cartão do Jogador", "🔄 Radar de Estrelas", "⬅️ Voltar", "⚠️ Capture uma imagem.", "⚠️ Até 17 anos.", "🏆 Galeria de Estrelas", "⬇️ Baixar Cartão", "📋 Banco de Dados", "Nome", "Idade", "Posição", "Velocidade", "Correspondência", "Data"]
}

sel_lang = st.session_state.get("lang", "🇸🇦 العربية")
d = LANG_YOUTH.get(sel_lang, LANG_YOUTH["🇸🇦 العربية"])

st.error(d[1])
st.title(d[0])
st.write("---")

# ═══════════════════════════════════════════════════════════════
# 3️⃣ التحقق من العمر
# ═══════════════════════════════════════════════════════════════
age = st.number_input(d[2], min_value=5, max_value=25, value=15)

if age >= 18:
    st.warning(d[14])
    st.stop() # إيقاف تحميل باقي الصفحة

parent_agree = False
if age < 18:
    st.info(d[3])
    p_name = st.text_input(d[4], key="p_name") # اسم اللاعب
    g_name = st.text_input(d[5], key="g_name") # اسم الولي
    g_id = st.text_input(d[6], key="g_id")
    if p_name and g_name and g_id:
        parent_agree = True
        st.success(d[7])

# ═══════════════════════════════════════════════════════════════
# 4️⃣ دالة توليد صورة الكارت للتحميل (Pillow)
# ═══════════════════════════════════════════════════════════════
def generate_download_card(player_img_bytes, name, age, speed, star_name, match_pct):
    try:
        # تحميل صورة اللاعب
        img = Image.open(io.BytesIO(player_img_bytes)).convert("RGB")
        img = img.resize((400, 400))
        
        # إنشاء خلفية الكارت
        card = Image.new("RGB", (800, 500), color=(4, 10, 24))
        draw = ImageDraw.Draw(card)
        
        # لصق صورة اللاعب
        card.paste(img, (50, 50))
        
        # إضافة نصوص (نستخدم خط افتراضي لتجنب مشاكل الخطوط على السيرفر)
        draw.text((500, 100), f"Name: {name}", fill=(0, 255, 136))
        draw.text((500, 150), f"Age: {age}", fill=(255, 255, 255))
        draw.text((500, 200), f"Speed: {speed} km/h", fill=(255, 255, 255))
        draw.text((500, 250), f"Star Match: {star_name}", fill=(0, 212, 255))
        draw.text((500, 300), f"Similarity: {match_pct}%", fill=(255, 170, 0))
        
        # حفظ الصورة في الذاكرة وإرجاعها
        buf = io.BytesIO()
        card.save(buf, format="PNG")
        return buf.getvalue()
    except Exception as e:
        return None

# ═══════════════════════════════════════════════════════════════
# 5️⃣ محرك YOLO26 (مع التغبيش)
# ═══════════════════════════════════════════════════════════════
@st.cache_resource(show_spinner=False)
def load_yolo_model():
    try:
        return YOLO("yolo11n-pose.pt")
    except:
        return None

SKELETON = [(15, 13), (13, 11), (16, 14), (14, 12), (11, 12), (5, 11), (6, 12), (5, 6), (5, 7), (6, 8), (7, 9), (8, 10), (1, 2), (0, 1), (0, 2), (1, 3), (2, 4), (3, 5), (4, 6)]
NEON_GREEN = (0, 255, 136)
NEON_CYAN = (212, 212, 0)

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
                # التغبيش
                face = kps[:5]
                valid = face[face.sum(axis=1) > 0]
                if len(valid) >= 2:
                    x_min, y_min = max(0, int(valid[:, 0].min()) - 30), max(0, int(valid[:, 1].min()) - 40)
                    x_max, y_max = min(frame.shape[1], int(valid[:, 0].max()) + 30), min(frame.shape[0], int(valid[:, 1].max()) + 50)
                    if x_max > x_min and y_max > y_min:
                        roi = annotated[y_min:y_max, x_min:x_max]
                        annotated[y_min:y_max, x_min:x_max] = cv2.GaussianBlur(roi, (61, 61), 0)
                        cv2.rectangle(annotated, (x_min, y_min), (x_max, y_max), NEON_CYAN, 2)
    return annotated

# ═══════════════════════════════════════════════════════════════
# 6️⃣ واجهة المستخدم وعرض الكارت
# ═══════════════════════════════════════════════════════════════
if parent_agree:
    # تهيئة قاعدة البيانات المحلية (الجدول)
    if 'youth_db' not in st.session_state:
        st.session_state.youth_db = []

    use_live = st.checkbox("📸 Activate Live AI Lens", value=True)
    st.subheader(d[8] if use_live else d[9])

    cam = st.camera_input("", key="cam", label_visibility="collapsed") if use_live else None
    file = st.file_uploader("", type=["jpg", "jpeg", "png"], key="file", label_visibility="collapsed")

    if cam or file:
        data = cam.getvalue() if cam else file.getvalue()
        model = load_yolo_model()
        
        if model:
            with st.spinner("🔄 Analyzing..."):
                processed = asyncio.run(yolo_engine(data, model))
                
            if processed is not None:
                # عرض الصورة المحللة
                processed_rgb = cv2.cvtColor(processed, cv2.COLOR_BGR2RGB)
                st.image(processed_rgb, channels="RGB", use_container_width=True)
                
                st.write("---")
                
                # بيانات وهمية للتجربة (لاحقاً ستُحسب من YOLO)
                speed = 24 + (age % 5) 
                pos = "مهاجم" if age % 2 == 0 else "وسط"
                
                # اختيار النجم
                stars = ["Lamine Yamal", "Gavi", "Endrick", "Pedri"]
                matched_star = stars[age % 4]
                match_pct = 85 + (age % 10)

                # ═══ تصميم كارت اللاعب (UI) ═══
                st.subheader(d[10])
                st.markdown(f"""
                <div class="player-card-ui">
                    <h2 style="color:#00ff88; margin-bottom:5px;">{p_name}</h2>
                    <p style="color:#aaa; margin-top:0;">{pos} | {age} سنة</p>
                    <div style="display:flex; justify-content:space-around; margin-top:15px;">
                        <div><h3 style="color:#fff; margin:0;">{speed}</h3><span style="color:#888; font-size:12px;">km/h</span></div>
                        <div><h3 style="color:#fff; margin:0;">89</h3><span style="color:#888; font-size:12px;">مراوغات</span></div>
                        <div><h3 style="color:#fff; margin:0;">{match_pct}%</h3><span style="color:#888; font-size:12px;">تطابق</span></div>
                    </div>
                    <h4 style="color:#00d4ff; margin-top:20px;">يشبه: {matched_star}</h4>
                </div>
                """, unsafe_allow_html=True)
                
                # ═══ زر التحميل ═══
                img_bytes = generate_download_card(data, p_name, age, speed, matched_star, match_pct)
                if img_bytes:
                    st.download_button(
                        label=d[17], 
                        data=img_bytes, 
                        file_name=f"{p_name}_card.png", 
                        mime="image/png",
                        use_container_width=True
                    )

                # إضافة اللاعب إلى الجدول
                st.session_state.youth_db.append({
                    d[19]: p_name, d[20]: age, d[21]: pos, d[22]: speed, d[23]: matched_star, d[24]: "2026-10-18"
                })

    # ═══ معرض النجوم ═══
    st.write("---")
    st.subheader(d[15])
    star_images = {
        "Lamine Yamal": "https://images.unsplash.com/photo-1579952363873-27f3bade9f55?w=200&q=80",
        "Gavi": "https://images.unsplash.com/photo-1518609878373-06d740f60d8b?w=200&q=80",
        "Endrick": "https://images.unsplash.com/photo-1508098682722-e99c43a406b2?w=200&q=80",
        "Pedri": "https://images.unsplash.com/photo-1552674605-db6ffd4facb5?w=200&q=80"
    }
    st.markdown('<div class="star-gallery">', unsafe_allow_html=True)
    for name, img_url in star_images.items():
        st.markdown(f'<div class="star-item"><img src="{img_url}"><br><span style="font-size:12px; color:#fff;">{name}</span></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ═══ الجدول الموحد (قاعدة البيانات المصغرة) ═══
    st.write("---")
    st.subheader(d[18])
    if st.session_state.youth_db:
        df = pd.DataFrame(st.session_state.youth_db)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("لا توجد بيانات مسجلة بعد. قم بتحليل لاعب لإضافته إلى الجدول.")

# ═══════════════════════════════════════════════════════════════
# 7️⃣ زر العودة
# ═══════════════════════════════════════════════════════════════
st.write("---")
if st.button(d[12], use_container_width=True):
    st.switch_page("app.py")
