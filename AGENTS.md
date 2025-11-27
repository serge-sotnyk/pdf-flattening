# Project Description

This repository contains a command-line utility for converting PDFs into a one-image-per-page format. Its main purpose is to ensure that no sensitive personal information remains in anonymized documents. Such information may appear to be hidden by overlays (usually dark rectangles) but can technically still exist within the PDF.

## Stack

* Python 3.13
* **uv** as the package manager
* **uvx** as the client-side execution method
* **pypdfium2** as the PDF-processing library with a permissive license

## Code style
- All comments and messages in code and documentation should be in English, even if user used another language in messages. Exception: if it is part of feature or user asks for it directly.
- Don't write obvious comments in the code in tutorial style. Only explanations for non-standard solutions.
- Use python 3.13 features, annotate types: List[str] -> list[str], Dict[str, str]->dict[str, str], Optional[int]->int|None, Tuple->tuple
- Use the best practices for architecture and code organization. DRY, SOLID, KISS, YAGNI, etc.
- Don't write code that is not asked by user.
- Try to use existing code and libraries if possible.

## Development
- Use MCP context7 for up-to-date knowledge about libraries/frameworks.
