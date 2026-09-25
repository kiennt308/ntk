#!/usr/bin/env python3
"""
PDF to Markdown MCP Server
===========================
High-performance Model Context Protocol (MCP) server for converting PDF documents
into clean, structured Markdown.

Supported conversion engines:
- `pymupdf4llm`: SOTA multi-column layout, LaTeX math formulas, tables, headings.
- `markitdown`: Microsoft MarkItDown engine.

Exposes 3 MCP Tools:
1. `convert_pdf_to_markdown`: Converts a PDF file and saves it to a `.md` file.
2. `read_pdf_as_markdown`: Converts a PDF in-memory and returns markdown content directly.
3. `batch_convert_pdfs`: Batch converts an entire directory of PDF files to Markdown.
"""

import os
import sys
import traceback
from typing import List, Optional

# Force UTF-8 on Windows stdio
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from mcp.server.mcpserver import MCPServer

# Initialize MCP Server
app = MCPServer("pdf-to-markdown")


def _convert_with_pymupdf(pdf_path: str, pages: Optional[List[int]] = None, extract_images: bool = False) -> str:
    import pymupdf4llm
    if pages:
        # 0-indexed in pymupdf4llm
        zero_indexed_pages = [p - 1 for p in pages if p > 0]
        md_text = pymupdf4llm.to_markdown(pdf_path, pages=zero_indexed_pages, write_images=extract_images)
    else:
        md_text = pymupdf4llm.to_markdown(pdf_path, write_images=extract_images)
    return md_text


def _convert_with_markitdown(pdf_path: str) -> str:
    from markitdown import MarkItDown
    md = MarkItDown()
    result = md.convert(pdf_path)
    return result.text_content


@app.tool()
def convert_pdf_to_markdown(
    pdf_path: str,
    output_md_path: Optional[str] = None,
    engine: str = "pymupdf4llm",
    extract_images: bool = False,
    pages: Optional[List[int]] = None
) -> str:
    """
    Convert a PDF file to a clean Markdown (.md) file.
    
    Args:
        pdf_path: Absolute or relative path to the source PDF file.
        output_md_path: Optional destination path for the markdown file. If omitted, uses <pdf_name>.md in the same directory.
        engine: Conversion engine to use ('pymupdf4llm' [default, best for papers & tables] or 'markitdown').
        extract_images: Whether to extract embedded images (default: False).
        pages: Optional list of 1-based page numbers to convert (e.g. [1, 2, 3]). If omitted, converts all pages.
        
    Returns:
        A confirmation message with output path, converted page count, character count, and preview snippet.
    """
    try:
        norm_pdf_path = os.path.abspath(pdf_path)
        if not os.path.exists(norm_pdf_path):
            return f"[ERROR] File not found at '{pdf_path}' (Resolved: '{norm_pdf_path}')"
            
        if not norm_pdf_path.lower().endswith(".pdf"):
            return f"[ERROR] File '{pdf_path}' is not a PDF file."

        if not output_md_path:
            base_name, _ = os.path.splitext(norm_pdf_path)
            norm_output_path = f"{base_name}.md"
        else:
            norm_output_path = os.path.abspath(output_md_path)

        os.makedirs(os.path.dirname(norm_output_path), exist_ok=True)

        if engine.lower() == "markitdown":
            md_content = _convert_with_markitdown(norm_pdf_path)
        else:
            md_content = _convert_with_pymupdf(norm_pdf_path, pages=pages, extract_images=extract_images)

        with open(norm_output_path, "w", encoding="utf-8") as f:
            f.write(md_content)

        char_count = len(md_content)
        word_count = len(md_content.split())
        line_count = len(md_content.splitlines())

        preview = md_content[:500] + ("..." if len(md_content) > 500 else "")

        return (
            f"Successfully converted PDF to Markdown!\n"
            f"- Source PDF    : {norm_pdf_path}\n"
            f"- Output File   : {norm_output_path}\n"
            f"- Engine Used   : {engine}\n"
            f"- Statistics    : {char_count:,} characters | {word_count:,} words | {line_count:,} lines\n\n"
            f"Preview (First 500 chars):\n"
            f"```markdown\n{preview}\n```"
        )
    except Exception as e:
        return f"[ERROR] PDF to Markdown conversion failed: {str(e)}\n\nTraceback:\n{traceback.format_exc()}"


@app.tool()
def read_pdf_as_markdown(
    pdf_path: str,
    engine: str = "pymupdf4llm",
    pages: Optional[List[int]] = None,
    max_characters: int = 50000
) -> str:
    """
    Read and convert a PDF file directly into Markdown text in-memory for instant analysis.
    
    Args:
        pdf_path: Absolute or relative path to the source PDF file.
        engine: Conversion engine ('pymupdf4llm' [default] or 'markitdown').
        pages: Optional list of 1-based page numbers to convert (e.g. [1, 2]).
        max_characters: Maximum characters to return to avoid exceeding context window (default: 50,000).
        
    Returns:
        The markdown text content of the PDF.
    """
    try:
        norm_pdf_path = os.path.abspath(pdf_path)
        if not os.path.exists(norm_pdf_path):
            return f"[ERROR] File not found at '{pdf_path}'"

        if engine.lower() == "markitdown":
            md_content = _convert_with_markitdown(norm_pdf_path)
        else:
            md_content = _convert_with_pymupdf(norm_pdf_path, pages=pages, extract_images=False)

        total_chars = len(md_content)
        if total_chars > max_characters:
            truncated_md = md_content[:max_characters]
            return (
                f"{truncated_md}\n\n"
                f"---\n"
                f"[Output truncated at {max_characters:,} / {total_chars:,} characters. "
                f"Specify `pages` or call `convert_pdf_to_markdown` to save the full document.]"
            )
        return md_content
    except Exception as e:
        return f"[ERROR] Reading PDF as Markdown failed: {str(e)}"


@app.tool()
def batch_convert_pdfs(
    folder_path: str,
    output_folder: Optional[str] = None,
    engine: str = "pymupdf4llm",
    recursive: bool = False
) -> str:
    """
    Batch convert all PDF files in a directory to Markdown (.md) files.
    
    Args:
        folder_path: Directory path containing PDF files.
        output_folder: Optional destination directory for .md files. If omitted, saves alongside original PDFs.
        engine: Conversion engine ('pymupdf4llm' [default] or 'markitdown').
        recursive: Whether to search subdirectories recursively (default: False).
        
    Returns:
        A detailed summary report of all converted files.
    """
    try:
        norm_folder = os.path.abspath(folder_path)
        if not os.path.isdir(norm_folder):
            return f"[ERROR] Directory '{folder_path}' does not exist."

        pdf_files = []
        if recursive:
            for root, _, files in os.walk(norm_folder):
                for file in files:
                    if file.lower().endswith(".pdf"):
                        pdf_files.append(os.path.join(root, file))
        else:
            for file in os.listdir(norm_folder):
                if file.lower().endswith(".pdf"):
                    pdf_files.append(os.path.join(norm_folder, file))

        if not pdf_files:
            return f"No PDF files found in '{norm_folder}'."

        if output_folder:
            out_dir = os.path.abspath(output_folder)
            os.makedirs(out_dir, exist_ok=True)
        else:
            out_dir = None

        converted_list = []
        failed_list = []

        for pdf_f in pdf_files:
            try:
                base_name = os.path.splitext(os.path.basename(pdf_f))[0]
                if out_dir:
                    target_md = os.path.join(out_dir, f"{base_name}.md")
                else:
                    target_md = os.path.join(os.path.dirname(pdf_f), f"{base_name}.md")

                if engine.lower() == "markitdown":
                    content = _convert_with_markitdown(pdf_f)
                else:
                    content = _convert_with_pymupdf(pdf_f)

                with open(target_md, "w", encoding="utf-8") as f:
                    f.write(content)

                converted_list.append((pdf_f, target_md, len(content)))
            except Exception as e_conv:
                failed_list.append((pdf_f, str(e_conv)))

        report = [
            f"BATCH PDF CONVERSION COMPLETED",
            f"- Source Folder    : {norm_folder}",
            f"- Output Folder    : {out_dir if out_dir else 'Same as source files'}",
            f"- Total PDFs Found : {len(pdf_files)}",
            f"- Successful       : {len(converted_list)}",
            f"- Failed           : {len(failed_list)}",
            "",
            "Converted Files:"
        ]
        for src, dst, sz in converted_list:
            report.append(f"  - {os.path.basename(src)} -> {os.path.basename(dst)} ({sz:,} chars)")

        if failed_list:
            report.append("\nFailed Files:")
            for src, err in failed_list:
                report.append(f"  - {os.path.basename(src)}: {err}")

        return "\n".join(report)
    except Exception as e:
        return f"[ERROR] Batch conversion failed: {str(e)}"


if __name__ == "__main__":
    app.run()
