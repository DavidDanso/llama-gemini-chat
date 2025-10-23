import requests
import streamlit as st

# ===============================
# Utility functions
# ===============================
def call_api(endpoint: str, payload: dict):
    """Generic API caller with flexible response handling."""
    try:
        response = requests.post(endpoint, json=payload, timeout=120)
        response.raise_for_status()
        data = response.json()
        output = data.get("output")

        # Handle if output is dict or string
        if isinstance(output, dict):
            return output.get("content", "")
        elif isinstance(output, str):
            return output
        else:
            return ""

    except requests.exceptions.RequestException as e:
        st.error(f"❌ API request failed: {e}")
    except (ValueError, KeyError, AttributeError):
        st.error("❌ Unexpected response format from the server.")

    return None



def get_essay(topic: str):
    """Fetch essay from Gemini endpoint."""
    return call_api(
        "http://localhost:8000/essay/invoke",
        {"input": {"topic": topic}}
    )


def get_poem(topic: str):
    """Fetch poem from Ollama endpoint."""
    return call_api(
        "http://localhost:8000/poem/invoke",
        {"input": {"topic": topic}}
    )


# ===============================
# Streamlit UI
# ===============================
st.set_page_config(
    page_title="LangChain Writer ✍️",
    page_icon="🧠",
    layout="centered"
)

st.title("🧠 LangChain Writer")
st.markdown("Generate creative content powered by **Gemini** and **LLAMA2 APIs**.")

# Tabs for better UX
tab1, tab2 = st.tabs(["📝 Essay Generator", "🎭 Poem Generator"])

with tab1:
    st.subheader("Generate an Essay")
    essay_topic = st.text_input("Enter a topic for your essay:")
    if st.button("Generate Essay", use_container_width=True):
        if essay_topic.strip():
            with st.spinner("Generating your essay... ✍️"):
                essay = get_essay(essay_topic)
                if essay:
                    st.success("✅ Essay generated successfully!")
                    st.markdown(f"### 🧾 Result:\n{essay}")
        else:
            st.warning("⚠️ Please enter a topic before generating.")

with tab2:
    st.subheader("Generate a Poem")
    poem_topic = st.text_input("Enter a theme for your poem:")
    if st.button("Generate Poem", use_container_width=True):
        if poem_topic.strip():
            with st.spinner("Creating your poem... 🎨"):
                poem = get_poem(poem_topic)
                if poem:
                    st.success("✅ Poem generated successfully!")
                    st.markdown(f"### 🎶 Result:\n{poem}")
        else:
            st.warning("⚠️ Please enter a theme before generating.")

# Footer
st.markdown("---")
st.caption("Built with ❤️ using Streamlit + LangChain + LLAMA2")
