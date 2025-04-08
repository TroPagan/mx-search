
import streamlit as st
import json

st.set_page_config(page_title="Modulex Sign Family Search Tool", layout="wide")
st.title("📘 Modulex Sign Family Search Tool")
st.write("Search preloaded Modulex product codes by size, family, and location.")

@st.cache_data
def load_data():
    with open("modulex_data.json") as f:
        return json.load(f)

data = load_data()

size_query = st.text_input("Search size (partial OK)", "")
families = ["Any"] + sorted(set(d["family"] for d in data))
locations = ["Any", "Interior", "Exterior"]

family_filter = st.selectbox("Filter by Family", families)
location_filter = st.selectbox("Filter by Location", locations)

filtered = []
for item in data:
    if size_query.lower() not in item["size"].lower():
        continue
    if family_filter != "Any" and item["family"] != family_filter:
        continue
    if location_filter != "Any" and item["location"] != location_filter:
        continue
    filtered.append(item)

st.markdown(f"### 🔍 Results: {len(filtered)} match{'es' if len(filtered)!=1 else ''}")
for item in filtered:
    st.write(f"**{item['code']}** — {item['size']} — {item['family']} — {item['location']}")
