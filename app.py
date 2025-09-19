# app.py
import streamlit as st
import io

from utils.pdf_utils import extract_text_from_pdf_bytes, extract_tables_from_pdf_bytes
from utils.excel_utils import extract_from_excel_bytes
from utils.metrics_utils import find_key_metrics_in_text
from utils.prompt_utils import build_prompt_from_document
from utils.ollama_client import query_ollama

st.set_page_config(page_title="Document Q&A Assistant", layout="wide")
st.title("📊 Document Q&A Assistant")

with st.sidebar:
    st.header("Upload documents")
    uploaded_files = st.file_uploader(
        "Upload PDF(s) or Excel (.xlsx). You can upload multiple files.",
        accept_multiple_files=True,
        type=["pdf", "xlsx", "xls"]
    )

    st.markdown("---")
    st.write("Ollama settings")
    ollama_model = st.text_input("Model name (as pulled to Ollama)", value="tinyllama:latest")
    ollama_base = st.text_input("Ollama generate endpoint", value="http://localhost:11434/api/generate")
    # show_raw = st.checkbox("Show raw extracted text", value=False)
    # show_prompt = st.checkbox("Show prompt sent to model", value=False)
    st.markdown("## Notes")
    st.caption("Make sure `ollama serve` is running and the model is pulled (e.g. `ollama pull tinyllama`). Default port: 11434.")

if uploaded_files:
    all_text = []
    all_tables = []
    all_excel = {}

    # Process each uploaded file
    for f in uploaded_files:
        fname = f.name.lower()
        b = f.read()
        
        if fname.endswith(".pdf"):
            st.info(f"📄 Processing PDF: {f.name}")
            try:
                text = extract_text_from_pdf_bytes(b)
                tables = extract_tables_from_pdf_bytes(b)
                all_text.append(text)
                all_tables.extend(tables)
                st.success(f"PDF processed: {len(text)} characters extracted")
            except Exception as e:
                st.error(f"❌ Error processing PDF {f.name}: {str(e)}")
                
        elif fname.endswith((".xlsx", ".xls")):
            st.info(f"Processing Excel: {f.name}")
            try:
                sheets = extract_from_excel_bytes(b)
                sheets_processed = 0
                
                for sname, df in sheets.items():
                    key = f"{f.name}::{sname}"
                    all_excel[key] = df
                    sheets_processed += 1

                
                
            except Exception as e:
                st.error(f"❌ Error processing Excel {f.name}: {str(e)}")

    # Combine PDF text
    doc_text = "\n\n".join(all_text)
    
    # Find key metrics (only for PDFs with text)
    key_metrics = find_key_metrics_in_text(doc_text) if doc_text.strip() else {}

    

    # Show Excel data
    if all_excel:
        for name, df in all_excel.items():
            # Parse filename and sheet name
            if "::" in name:
                filename, sheet_name = name.split("::", 1)
            else:
                filename, sheet_name = name, "Unknown"
                
            with st.expander(f"📁 {filename} → 📋 {sheet_name} ({df.shape[0]} rows × {df.shape[1]} cols)"):
                if not df.empty:
                    st.write(f"**Columns:** {', '.join(df.columns.tolist())}")
                    st.dataframe(df.head(10), use_container_width=True)
                else:
                    st.warning("⚠️ This sheet is empty")

    # Show PDF tables
    if all_tables:
        st.write("📄 **PDF Tables Detected:**")
        for i, df in enumerate(all_tables[:3]):  # Show first 3 tables
            with st.expander(f"Table {i+1} ({df.shape[0]} rows × {df.shape[1]} cols)"):
                st.dataframe(df.head(10), use_container_width=True)

    # Show raw text if requested
    # if show_raw and doc_text.strip():
    #     with st.expander("📝 Raw PDF Text"):
    #         st.text_area("Extracted text", value=doc_text[:10000], height=300)

    # Show key metrics if found
    if key_metrics:
        with st.expander("📊 Key Metrics Found"):
            st.json(key_metrics)

    # Q&A Section
    st.markdown("---")
    st.subheader("Ask a Question About Your Documents")
    
    # Show what data is available
    data_summary = []
    if all_excel:
        data_summary.append(f"📊 {len(all_excel)} Excel sheet(s)")
    if doc_text.strip():
        data_summary.append(f"📄 PDF content ({len(doc_text):,} chars)")
    if all_tables:
        data_summary.append(f"📋 {len(all_tables)} PDF table(s)")
    
   
    
    question = st.text_input("Enter your question:", key="q1", placeholder="e.g., What is the title? What columns are in the Excel file?")
    
    if st.button("Get Answer", type="primary"):
        if not question.strip():
            st.error("Please enter a question.")
        else:
            # Show what we're processing
            with st.status("Processing your question...", expanded=False) as status:
                st.write("Building context from documents...")
                
                # Build the prompt
                prompt = build_prompt_from_document(doc_text, all_tables, all_excel, question)
                
                st.write("Sending to AI model...")
                
                # Show prompt in debug mode
                # if show_prompt:
                #     st.text_area("🔍 Full prompt sent to model:", prompt, height=300)
                
                status.update(label="🤖 Waiting for AI response...", state="running")
                
                try:
                    # Query the model
                    reply = query_ollama(prompt, model=ollama_model, ollama_url=ollama_base)
                    status.update(label="✅ Response received!", state="complete")
                    
                except Exception as e:
                    status.update(label="Error occurred", state="error")
                    st.error(f"Could not reach Ollama: {str(e)}")
                    reply = None
            
            # Show the answer
            if reply:
                st.markdown("### Answer:")
                
                # Clean up the response if it's echoing the question
                if reply.strip().lower().startswith('question:') or reply.strip() == question:
                    st.warning("The model seems to be echoing the question. This might indicate:")
                    st.write("- The prompt is too complex")
                    st.write("- The model needs more context") 
                    st.write("- Try a simpler question first")
                    
                    # if show_prompt:
                    #     st.write("**Enable 'Show prompt sent to model' to debug**")
                else:
                    st.markdown(reply)

else:
    st.info("Upload at least one PDF or Excel file using the left sidebar to begin.")
    
    