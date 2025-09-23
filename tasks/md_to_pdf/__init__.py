#region generated meta
import typing
class Inputs(typing.TypedDict):
    md_content: str | None
    md_file_path: str | None
    output_filename: str
    save_path: str | None
    title: str | None
    author: str | None
    css_style: str | None
class Outputs(typing.TypedDict):
    pdf_path: str
    status: str
    file_size: float
#endregion

import os
import markdown
from weasyprint import HTML, CSS

def main(params: Inputs, context) -> Outputs:
    """
    Convert Markdown content to PDF format

    Args:
        params: Input parameters containing markdown content/file and options
        context: OOMOL context object

    Returns:
        Output dictionary with PDF path, status and file size
    """
    try:
        # Get markdown content
        md_content = ""
        if params.get("md_content"):
            md_content = params["md_content"]
        elif params.get("md_file_path"):
            if not os.path.exists(params["md_file_path"]):
                raise ValueError(f"Markdown file not found: {params['md_file_path']}")
            with open(params["md_file_path"], 'r', encoding='utf-8') as f:
                md_content = f.read()
        else:
            raise ValueError("Either md_content or md_file_path must be provided")

        if not md_content.strip():
            raise ValueError("Markdown content cannot be empty")

        # Configure markdown extensions
        extensions = [
            'codehilite',
            'tables',
            'toc',
            'fenced_code',
            'nl2br'
        ]

        extension_configs = {
            'codehilite': {
                'css_class': 'highlight',
                'use_pygments': True,
                'noclasses': True,
            }
        }

        # Convert markdown to HTML
        md = markdown.Markdown(
            extensions=extensions,
            extension_configs=extension_configs
        )
        html_content = md.convert(md_content)

        # Default CSS styles
        default_css = """
        @page {
            margin: 2cm;
            @bottom-center {
                content: counter(page);
            }
        }

        body {
            font-family: 'DejaVu Sans', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: none;
        }

        h1, h2, h3, h4, h5, h6 {
            color: #2c3e50;
            margin-top: 2em;
            margin-bottom: 0.5em;
        }

        h1 { font-size: 2.5em; border-bottom: 3px solid #3498db; padding-bottom: 0.3em; }
        h2 { font-size: 2em; border-bottom: 2px solid #3498db; padding-bottom: 0.3em; }
        h3 { font-size: 1.5em; }
        h4 { font-size: 1.2em; }

        p { margin: 1em 0; }

        code {
            background-color: #f8f9fa;
            padding: 0.2em 0.4em;
            border-radius: 3px;
            font-family: 'DejaVu Sans Mono', 'Courier New', monospace;
            font-size: 0.9em;
        }

        pre {
            background-color: #f8f9fa;
            padding: 1em;
            border-radius: 5px;
            overflow-x: auto;
            border-left: 4px solid #3498db;
        }

        pre code {
            background-color: transparent;
            padding: 0;
        }

        blockquote {
            border-left: 4px solid #bdc3c7;
            margin: 1em 0;
            padding: 0 1em;
            color: #7f8c8d;
        }

        table {
            border-collapse: collapse;
            width: 100%;
            margin: 1em 0;
        }

        th, td {
            border: 1px solid #bdc3c7;
            padding: 0.5em;
            text-align: left;
        }

        th {
            background-color: #ecf0f1;
            font-weight: bold;
        }

        ul, ol {
            margin: 1em 0;
            padding-left: 2em;
        }

        li {
            margin: 0.5em 0;
        }

        a {
            color: #3498db;
            text-decoration: none;
        }

        a:hover {
            text-decoration: underline;
        }

        .highlight {
            background-color: #f8f9fa;
            padding: 0.1em;
            border-radius: 3px;
        }
        """

        # Combine default CSS with custom CSS
        final_css = default_css
        if params.get("css_style"):
            final_css += "\n" + params["css_style"]

        # Create complete HTML document
        title = params.get("title", "Document")
        author = params.get("author", "")

        full_html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{title}</title>
            <meta name="author" content="{author}">
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """

        # Determine output path
        output_filename = params.get("output_filename", "document")
        if not output_filename.endswith('.pdf'):
            output_filename += '.pdf'

        if params.get("save_path"):
            pdf_path = params["save_path"]
            if not pdf_path.endswith('.pdf'):
                pdf_path = os.path.join(pdf_path, output_filename)
        else:
            # Save to oomol-storage if no specific path provided
            storage_path = "/oomol-driver/oomol-storage"
            os.makedirs(storage_path, exist_ok=True)
            pdf_path = os.path.join(storage_path, output_filename)

        # Ensure directory exists
        os.makedirs(os.path.dirname(pdf_path), exist_ok=True)

        # Convert HTML to PDF
        try:
            html_doc = HTML(string=full_html)
            css_doc = CSS(string=final_css)
            html_doc.write_pdf(pdf_path, stylesheets=[css_doc])
        except Exception as pdf_error:
            # Fallback: try without CSS
            try:
                html_doc = HTML(string=full_html)
                html_doc.write_pdf(pdf_path)
            except Exception as fallback_error:
                raise ValueError(f"PDF generation failed: {pdf_error}; Fallback also failed: {fallback_error}")

        # Get file size
        file_size = os.path.getsize(pdf_path)

        return {
            "pdf_path": pdf_path,
            "status": f"Successfully converted Markdown to PDF: {pdf_path}",
            "file_size": file_size
        }

    except Exception as e:
        error_msg = f"Error converting Markdown to PDF: {str(e)}"
        # Still return a valid response structure even on error
        return {
            "pdf_path": "",
            "status": error_msg,
            "file_size": 0
        }