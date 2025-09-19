def build_prompt_from_document(doc_text, tables=None, excel_data=None, question="", max_chars=3000):
    """
    Build a focused prompt for TinyLlama with proper Excel handling
    """
    
    prompt_parts = [
        "Answer the question using the provided document data.",
        ""
    ]
    
    # Handle Excel files first (they're usually more structured)
    if excel_data and len(excel_data) > 0:
        prompt_parts.extend([
            "EXCEL DATA:",
            "-" * 30
        ])
        
        for sheet_key, df in excel_data.items():
            # Parse the sheet key: "filename.xlsx::SheetName"
            if "::" in sheet_key:
                filename, sheet_name = sheet_key.split("::", 1)
            else:
                filename = sheet_key
                sheet_name = "Sheet1"
            
            prompt_parts.append(f"File: {filename}")
            prompt_parts.append(f"Sheet: {sheet_name}")
            
            if df.empty:
                prompt_parts.append("(This sheet is empty)")
            else:
                prompt_parts.append(f"Size: {len(df)} rows, {len(df.columns)} columns")
                
                # Show column names
                if len(df.columns) > 0:
                    columns_str = ", ".join(df.columns.astype(str).tolist()[:10])  # Max 10 columns
                    if len(df.columns) > 10:
                        columns_str += f"... (+{len(df.columns)-10} more)"
                    prompt_parts.append(f"Columns: {columns_str}")
                
                # Show sample data (first 3 rows only)
                if len(df) > 0:
                    try:
                        sample = df.head(3).to_string(index=False, max_cols=6)
                        if len(sample) < 500:  # Only if not too long
                            prompt_parts.append("Sample data:")
                            prompt_parts.append(sample)
                    except:
                        prompt_parts.append("(Data preview unavailable)")
            
            prompt_parts.append("")  # Empty line between sheets
        
        prompt_parts.append("-" * 30)
        prompt_parts.append("")
    
    # Handle PDF text content
    if doc_text and doc_text.strip():
        # Truncate if too long
        text_content = doc_text.strip()
        if len(text_content) > max_chars:
            text_content = text_content[:max_chars] + "\n[...text truncated...]"
        
        prompt_parts.extend([
            "PDF TEXT CONTENT:",
            "-" * 30,
            text_content,
            "-" * 30,
            ""
        ])
    
    # Handle PDF tables (only first one to keep prompt short)
    if tables and len(tables) > 0:
        table = tables[0]  # Only first table
        if not table.empty:
            prompt_parts.extend([
                "PDF TABLE:",
                "-" * 30
            ])
            
            try:
                table_str = table.head(3).to_string(index=False)
                if len(table_str) < 400:  # Only if not too long
                    prompt_parts.append(table_str)
                else:
                    prompt_parts.append(f"Table with {len(table)} rows and {len(table.columns)} columns")
                    prompt_parts.append("Columns: " + ", ".join(table.columns.tolist()[:5]))
            except:
                prompt_parts.append("Table data unavailable")
            
            prompt_parts.extend(["-" * 30, ""])
    
    # Add the question and clear instructions
    prompt_parts.extend([
        f"QUESTION: {question}",
        "",
        "Please provide a direct answer based on the data above. If the information is not available, say so clearly.",
        "",
        "ANSWER:"
    ])
    
    return "\n".join(prompt_parts)