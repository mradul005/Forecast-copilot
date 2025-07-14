import streamlit as st
import pandas as pd
import openai
import os

# Set your OpenAI API key
openai.api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")

st.title("📊 Forecast Copilot")

st.write("Upload a forecast CSV and select a product to understand forecast variance.")

# Upload CSV
uploaded_file = st.file_uploader("Upload your forecast CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("📄 Preview of Uploaded Data:")
    st.dataframe(df.head())

    # Select product
    product_options = df["Product"].unique()
    selected_product = st.selectbox("Select Product", product_options)

    # Filter data for selected product
    product_df = df[df["Product"] == selected_product]

    # Convert to string for prompt
    data_str = product_df.to_string(index=False)

    # Prompt
    prompt = f"""
You are a demand planning expert. Based on the following forecast and actual sales data with events and promotions,
generate 3–5 business-friendly insights explaining why forecasts differed from actuals.

Data:
{data_str}

Return your answer as clear bullet points.
"""

    if st.button("Generate Forecast Insights"):
        with st.spinner("🧠 Thinking..."):
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3
                )
                explanation = response['choices'][0]['message']['content']
                st.markdown("### 🧠 Forecast Explanation:")
                st.markdown(explanation)
            except Exception as e:
                st.error(f"Error: {str(e)}")
