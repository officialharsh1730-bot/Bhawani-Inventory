import streamlit as st
import pandas as pd

# पेज की सेटिंग
st.set_page_config(page_title="Bhawani Enterprises Stock", layout="wide")

st.title("🏢 Bhawani Enterprises - Stock Manager")
st.write("HPL, ACP, MDF, Acrylic और CNC कटिंग स्टॉक का हिसाब")

# डेटाबेस लोड करने का फंक्शन
def load_data():
    return pd.read_csv("inventory.csv")

# डेटाबेस सेव करने का फंक्शन
def save_data(df):
    df.to_csv("inventory.csv", index=False)

df = load_data()

# --- सेक्शन 1: लो-स्टॉक अलर्ट ---
st.subheader("⚠️ Low Stock Alert (ये माल खत्म होने वाला है)")
low_stock = df[df['Quantity'] <= df['Threshold']]
if not low_stock.empty:
    st.error("नीचे दी गई शीट्स का स्टॉक कम हो गया है, कृपया ऑर्डर करें!")
    st.dataframe(low_stock)
else:
    st.success("सारा स्टॉक बिल्कुल सही मात्रा में उपलब्ध है।")

st.markdown("---")

# --- सेक्शन 2: स्टॉक अपडेट करें (In / Out) ---
st.subheader("🔄 Update Stock (माल आया या कटा/बिका)")

col1, col2, col3 = st.columns(3)

with col1:
    selected_material = st.selectbox("Material चुनें", df['Material'].unique())
    filtered_brands = df[df['Material'] == selected_material]['Brand'].unique()
    selected_brand = st.selectbox("Brand चुनें", filtered_brands)

with col2:
    filtered_sizes = df[(df['Material'] == selected_material) & (df['Brand'] == selected_brand)]['Size'].unique()
    selected_size = st.selectbox("Size चुनें", filtered_sizes)
    action = st.radio("क्या करना है?", ["Out (कटा/बिका)", "In (नया माल आया)"])

with col3:
    qty_change = st.number_input("कितनी शीट?", min_value=1, step=1)
    
    if st.button("Update Stock"):
        index = df[(df['Material'] == selected_material) & 
                   (df['Brand'] == selected_brand) & 
                   (df['Size'] == selected_size)].index[0]
        
        if action == "In (नया माल आया)":
            df.at[index, 'Quantity'] += qty_change
            st.success(f"✅ स्टॉक में {qty_change} शीट जोड़ दी गईं!")
        else:
            if df.at[index, 'Quantity'] >= qty_change:
                df.at[index, 'Quantity'] -= qty_change
                st.success(f"✅ स्टॉक से {qty_change} शीट कम कर दी गईं!")
            else:
                st.error("❌ स्टॉक में इतनी शीट नहीं हैं!")
        
        save_data(df)
        st.rerun() 

st.markdown("---")

# --- सेक्शन 3: पूरा स्टॉक देखें ---
st.subheader("📦 All Available Stock (पूरा स्टॉक)")
st.dataframe(df, use_container_width=True)