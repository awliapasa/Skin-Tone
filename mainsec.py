import streamlit as st
from streamlit_option_menu import option_menu
from io import BytesIO
import cv2
import numpy as np
from PIL import Image, ImageDraw

def convert_color(image, from_format='RGB', to_format='BGR'):
    if from_format == 'RGB' and to_format == 'BGR':
        return cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    elif from_format == 'BGR' and to_format == 'RGB':
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image

def detect_face(image):
    """Deteksi wajah menggunakan Haar Cascade"""
    img_np = np.array(image)
    gray = cv2.cvtColor(convert_color(img_np, 'RGB', 'BGR'), cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.05,
        minNeighbors=5,
        minSize=(25,25)
    )
    if len(faces) > 0:
        print(len(faces))
        return faces[2]
    else:
        return None

def skinTone_detector(image_data):
    try:
        # Mengambil ROI
        width, height = img.size
        left = width // 4
        top = height // 4
        right = left + width // 2
        bottom = top + height // 2
        cropped_img = img.crop((left, top, right, bottom))

        # Konversi RGB ke HSV
        cropped_arr = np.array(cropped_img)
        hsv = cv2.cvtColor(cropped_arr, cv2.COLOR_RGB2HSV)
        
        hue = hsv[:, :, 0] * 2 # supaya jadi 0-360
        saturation = hsv[:, :, 1]
        value = hsv[:, :, 2]

        # filter hanya warna kulit
        valid_mask = (
            (hue >= 0) & (hue <= 50) & 
            (saturation >= 25) & (saturation <= 204) & 
            (value >= 51) & (value <= 255)
        )

        filtered_hue = hue[valid_mask]
        filtered_saturation = saturation[valid_mask]
        filtered_value = value[valid_mask]

        # Jika data terlalu sedikit, fallback ke semua pixel
        if len(filtered_hue) < 50:
            filtered_hue = hue.flatten()
            filtered_saturation = saturation.flatten()
            filtered_value = value.flatten()

        avg_h = np.median(filtered_hue)
        avg_s = np.median(filtered_saturation)
        avg_v = np.median(filtered_value)

        st.write(f"HSV rata-rata: H={avg_h:.2f}, S={avg_s:.2f}, V={avg_v:.2f}")

        if 0 <= avg_h <= 50 and 10 <= avg_s <= 60 and 80 <avg_v <= 255:
            return "FAIR"
        elif 10 <= avg_h <= 50 and 30 <= avg_s <= 90 and 70 <avg_v <= 240:
            return "LIGHT"
        elif 10 <= avg_h <= 40 and 50 <= avg_s <= 120 and 40 <avg_v <= 200:
            return "MEDIUM"
        elif 0 <= avg_h <= 30 and 60 <= avg_s <= 150 and 20 <avg_v <= 100:
            return "DARK"
        else:
            return "An Unknown Skin Tone"
    except Exception as e:
        st.error(f"Terjadi Kesalahan saat Mendeteksi: {e}")
        return "An Unknown Skin Tone"


st.markdown(
    """
    <style>
    .stApp {
        background-color: #FFF1F2;
    }
    h1, h2, h3, h4, h5, h6, p, div {
        color: #1B1E2E !important;
    }
    button {
        background-color: #FFC0CB !important;
        color: #1B1E2E !important;
        border: none !important;
    }
    button:hover {
        background-color: #FFB6C1 !important;
        color: #1B1E2E !important;
    }
    .stFileUploader div div {
        color: white !important; /* Change the "Drag and drop file here" text color */
    }
    </style>
    """,
    unsafe_allow_html=True
)
# inisialisasi session state
if "subpage" not in st.session_state:
    st.session_state.subpage = "main"

# fungsi untuk mengubah halaman
def go_to_upload():
    st.session_state.subpage = "upload"
def go_to_take_photo():
    st.session_state.subpage = "take_photo"
def go_back():
    st.session_state.subpage = "main"
def go_to_result():
    st.session_state.subpage = "result"

# navigasi sidebar
with st.sidebar:
    selected = option_menu('Skin Tone Detector',
                            ['Description Site',
                            'Detector Site', 'Developers Profile'],
                            default_index=0)

# halaman deskripsi
if(selected=='Description Site'):
    st.markdown("<h1 style='text-align: center;'>Type of Skin Tone</h1>", unsafe_allow_html=True)

    st.subheader('Fair Skin Tone')
    st.write ("Skin tone ini merupakan jenis warna kulit paling terang dan cenderung seperti putih. Orang dengan tipe kulit ini biasanya mudah terbakar ketika terpapar sinar matahari.")
    
    st.subheader('Light Skin Tone')
    st.write("Jika dibandingkan dengan pemilik warna kulit putih (fair), skin tone jenis light akan tampak lebih kuning atau keemasan. Namun, keduanya memiliki kesamaan, yaitu mudah terbakar ketika terkena sinar matahari. Namun, skin tone ini lebih tidak mudah terbakar seperti kulit putih.")
   
    st.subheader('Medium Skin Tone')
    st.write("""
    Skin tone jenis ini sering disebut sebagai warna sawo matang atau kuning langsat. Warna kulit satu ini merupakan skin tone yang dimiliki kebanyakan masyarakat Indonesia.
    Warna ini termasuk ke dalam warna kulit yang berada di antara gelap dan putih, namun lebih mendekati ke kulit putih. Walaupun begitu, warna skintone ini tidak pucat seperti kulit putih karena adanya pigmen kuning yang menjadikan warna kulit tampak lebih segar.
    """)
    
    st.subheader('Dark Skin Tone')
    st.write("Jenis warna kulit ini umumnya terlihat gelap, namun tidak sampai berwarna hitam. Skin tone ini merupakan warna kulit yang terjadi secara alami akibat pigmen melanin dan memiliki warna gelap. Warna kulit ini sering dianggap sebagai warna kulit yang eksotik.")

# halaman deteksi
if (selected=='Detector Site'):
    # halaman utama
    if st.session_state.subpage == "main":
        st.markdown("<h1 style='text-align: center;'>Skin Tone Detector</h1>", unsafe_allow_html=True)
        st.image("https://cdn.shopify.com/s/files/1/0269/7274/9917/files/SkinTone_finder_mobile_e496598c-4246-4a17-8a80-d7496eb29c59.jpg?v=1730999335")
        col1, col2 = st.columns(2, gap='medium')
        with col1:
            upload = st.button('Upload Photo', on_click=go_to_upload)
        with col2:
            photo = st.button('Take a Photo', on_click=go_to_take_photo)

    # halaman upload
    elif st.session_state.subpage == "upload":
        st.title('Please Upload your Photo')
        st.button('<-- Back', on_click=go_back, key='back_button_upload')
        uploaded_file = st.file_uploader('Upload your photo', type=['jpg', 'png', 'jpeg'], help="Pastikan foto menunjukkan wajah dengan jelas!") 

        if uploaded_file is not None:
            img = Image.open(uploaded_file)

            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            buffered = BytesIO()
            if uploaded_file.type in ['image/png', 'image/PNG']:
                img.save(buffered, format="PNG")
            else:
                img.save(buffered, format="JPEG", quality=95)

            buffered.seek(0)
            img = Image.open(buffered)
            img_np = np.array(img)

            face = detect_face(img)
            if face is not None:
                x, y, w, h = face
                img_with_box = img_np.copy()
                cv2.rectangle(img_with_box, (x, y), (x+w, y+h), (0, 255, 0), 2)
                img_with_box = convert_color(img_with_box, 'RGB', 'BGR')
                draw = ImageDraw.Draw(img)
                draw.rectangle([x, y, x+w, y+h], outline="green", width=3)
                st.image(convert_color(img_with_box, 'BGR', 'RGB'), caption='Wajah Terdeteksi', use_container_width=True, clamp=True, output_format="JPEG")
                
                if st.button('Analisis Skin Tone'):
                    st.session_state.result = skinTone_detector(uploaded_file)
                    go_to_result()
            else: 
                st.error("Wajah tidak terdeteksi. Upload foto dengan wajah jelas!")
                             
    elif st.session_state.subpage == "take_photo":
        st.title('Please Take a Photo')
        st.button('<-- Back', on_click=go_back, key='back_button_camera')
        # Simulasi pengambilan foto
        picture = st.camera_input("Take a picture")
        if picture:
            if picture:
                img = Image.open(picture)
                img_np = np.array(img)

                img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

                face_coords = detect_face(img)
                if face_coords is not None:
                    x, y, w, h = face_coords
                    img_with_box = img_bgr.copy()
                    cv2.rectangle(img_with_box, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    img_with_box_rgb = cv2.cvtColor(img_with_box, cv2.COLOR_BGR2RGB)
                    draw = ImageDraw.Draw(img)
                    draw.rectangle([x, y, x+w, y+h], outline="green", width=3)
                    st.image(img_with_box_rgb, caption="Wajah Terdeteksi", use_container_width=True)

                    if st.button('Analisis Skin Tone'):
                        st.session_state.result = skinTone_detector(picture)
                        go_to_result()
                else:
                    st.error("Wajah tidak terdeteksi. Pastikan wajah terlihat jelas!")
    
    # halaman hasil
    if st.session_state.subpage == "result":
        st.button('<-- Back', on_click=go_back, key='back_button_result')
        st.title('RESULT')
        st.text('Your skin tone is:')
        st.subheader(st.session_state.result)

        skin = st.session_state.result
        if skin == "An Unknown Skin Tone":
            st.warning("Please try again with clearer photo!")
        else:
            st.text('Your Color Palette Makeup Recommendation:')
            
            col1, col2, col3 = st.columns(3, gap='medium')
            with col1:
                st.image(f"images/{skin}/Blush/Blush.png", caption="Blush", use_container_width=True)
            with col2:
                st.image(f"images/{skin}/Foundation/Foundation.png", caption="Foundation", use_container_width=True)
            with col3:
                st.image(f"images/{skin}/Lipstick/Lipstick.png", caption="Lipstick", use_container_width=True)

if (selected == 'Developers Profile'):
    st.markdown("<h1 style='text-align: center;'>Meet the team!</h1>", unsafe_allow_html=True)
    st.image(f"images/Teams.jpg")
    st.text("1. Annisa Fawwaz Putriano - 2023105471")
    st.text("2. Michelle Hiu - 2023105488")
    st.text("3. Maizan Jamalina Yahnah - 2023105496")
    st.text("5. Najla Melinda Kiasati - 2023105534")
    st.text("6. Carissa Metta Wahyudi - 2023105506")
    st.text("7. Aulia Fasya - 2023105499")
