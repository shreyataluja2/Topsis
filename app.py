import streamlit as st
import pandas as pd
from topsis_angad import run_topsis
import os
import tempfile

st.set_page_config(page_title="TOPSIS Calculator", page_icon="📊", layout="wide")

st.title("📊 TOPSIS Calculator")
st.markdown("**Technique for Order Preference by Similarity to Ideal Solution**")
st.markdown("---")

# Sidebar for inputs
with st.sidebar:
    st.header("⚙️ Configuration")
    
    uploaded_file = st.file_uploader("Upload CSV File", type=['csv'])
    
    weights_input = st.text_input("Weights (comma-separated)", placeholder="2.3,1.7,3.1,0.9,2.6")
    
    impacts_input = st.text_input("Impacts (comma-separated)", placeholder="+,-,+,-,+")
    
    calculate_btn = st.button("🚀 Calculate TOPSIS", type="primary")

# Main content area
col1, col2 = st.columns(2)

with col1:
    st.subheader("📥 Input Data")
    if uploaded_file is not None:
        try:
            df_input = pd.read_csv(uploaded_file)
            st.dataframe(df_input, width='stretch')
        except Exception as e:
            st.error(f"Error reading file: {e}")
    else:
        st.info("Please upload a CSV file to get started")

with col2:
    st.subheader("📤 TOPSIS Results")
    
    if calculate_btn:
        if uploaded_file is None:
            st.error("Please upload a CSV file")
        elif not weights_input:
            st.error("Please enter weights")
        elif not impacts_input:
            st.error("Please enter impacts")
        else:
            try:
                # Create temporary files
                with tempfile.NamedTemporaryFile(delete=False, suffix='.csv', mode='wb') as tmp_input:
                    tmp_input.write(uploaded_file.getvalue())
                    input_path = tmp_input.name
                
                with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp_output:
                    output_path = tmp_output.name
                
                # Run TOPSIS
                run_topsis(input_path, weights_input, impacts_input, output_path)
                
                # Read and display results
                df_result = pd.read_csv(output_path)
                st.dataframe(df_result, width='stretch')
                
                # Download button
                csv = df_result.to_csv(index=False)
                st.download_button(
                    label="⬇️ Download Results",
                    data=csv,
                    file_name="topsis_results.csv",
                    mime="text/csv"
                )
                
                # Success message
                st.success("✅ TOPSIS calculation completed successfully!")
                
                # Clean up temp files
                os.unlink(input_path)
                os.unlink(output_path)
                
            except Exception as e:
                st.error(f"Error: {e}")

# Footer
st.markdown("---")
st.markdown("**Author:** Angad Singh Madhok (102313005)")
st.markdown("[GitHub Repository](https://github.com/angad2803/TOPSIS-Data-Science)")
