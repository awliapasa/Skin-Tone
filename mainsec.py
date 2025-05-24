import streamlit as st
from streamlit_option_menu import option_menu
import numpy as np
from PIL import Image

def skinTone_detector(image_data):
    img = Image.open(image_data).convert("RGB")
    img = img.resize((200, 200))

    # Mengambil ROI
    width, height = img.size
    left = width // 4
    top = height // 4
    right = left + width // 2
    bottom = top + height // 2
    cropped_img = img.crop((left, top, right, bottom))

    # Konversi RGB ke HSV
    cropped_arr = np.array(cropped_img) / 255.0
    r, g, b = cropped_arr[:, :, 0], cropped_arr[:, :, 1], cropped_arr[:, :, 2]
    cmax = np.max(cropped_arr, axis=2)
    cmin = np.min(cropped_arr, axis=2)
    d = cmax-cmin

    hue = np.zeros_like(cmax)
    with np.errstate(divide='ignore', invalid='ignore'):
        mask_r = (cmax == r) & (d != 0)
        mask_g = (cmax == g) & (d != 0) 
        mask_b = (cmax == b) & (d != 0)
 
        hue[mask_r] = (((g - b) / d) % 6)[mask_r]
        hue[mask_g] = (((b - r) / d) + 2)[mask_g]
        hue[mask_b] = (((r - g) / d) + 4)[mask_b]
    
    hue *= 60
    hue = np.nan_to_num(hue)

    saturation = np.where(cmax == 0, 0, d / cmax)
    value = cmax

    avg_h = np.median(hue)
    avg_s = np.median(saturation) * 255
    avg_v = np.median(value) * 255

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
                            'Detector Site'],
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
        st.button('<-- Back', on_click=go_back)
        uploaded_file = st.file_uploader('Upload your photo', type=['jpg', 'png', 'jpeg'])
        if uploaded_file is not None:
            # Menampilkan gambar yang diupload
            st.image(uploaded_file, caption='Uploaded Image', use_container_width=True)
            st.write("")
            st.write("Classifying...")
            # Menampilkan hasil klasifikasi
            st.session_state.result = skinTone_detector(uploaded_file)
            st.button('See Result', on_click=go_to_result)
    
    elif st.session_state.subpage == "take_photo":
        st.title('Please Take a Photo')
        st.button('<-- Back', on_click=go_back)
        # Simulasi pengambilan foto
        picture = st.camera_input("Take a picture")
        if picture is not None:
            # Menampilkan gambar yang diambil
            st.image(picture, caption='Captured Image', use_container_width=True)
            st.write("")
            st.write("Classifying...")
            # Menampilkan hasil klasifikasi
            st.session_state.result = skinTone_detector(picture)
            st.button('See Result', on_click=go_to_result)
    
    # halaman hasil
    if st.session_state.subpage == "result":
        st.button('<-- Back', on_click=go_back)
        st.title('RESULT')
        st.text('Your skin tone is:')
        st.subheader(st.session_state.result)

        skin = st.session_state.result
        if skin == "An Unknown Skin Tone":
            st.warning("Please try again with clearer photo!")
        else:
            st.image(f"images/{skin}.jpg", caption=f"{st.session_state.result} Skin Tone", use_container_width=True)
            st.text('Your Color Palette Makeup Recommendation:')
            
            col1, col2, col3 = st.columns(3, gap='medium')
            with col1:
                st.image(f"images/{skin}/Blush/Blush.jpg", caption="Blush", use_container_width=True)
            with col2:
                st.image(f"images/{skin}/Foundation/Foundation.jpg", caption="Foundation", use_container_width=True)
            with col3:
                st.image(f"images/{skin}/Lipstick/Lipstick.jpg", caption="Lipstick", use_container_width=True)


