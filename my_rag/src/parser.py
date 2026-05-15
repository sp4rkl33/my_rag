from pypdf import PdfReader
from pathlib import Path
from typing import Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DocumentParser:
    @staticmethod
    def parse_pdf(file_path: str) -> Optional[str]:
        try:
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n\n"
            return text.strip()
        except Exception as e:
            logger.error(f"Failed to parse PDF {file_path}: {e}")
            return None

    @staticmethod
    def parse_text(file_path: str) -> Optional[str]:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except UnicodeDecodeError:
            try:
                with open(file_path, 'r', encoding='latin-1') as f:
                    return f.read().strip()
            except Exception as e:
                logger.error(f"Failed to parse text file {file_path}: {e}")
                return None
        except Exception as e:
            logger.error(f"Failed to parse text file {file_path}: {e}")
            return None

    @staticmethod
    def parse_markdown(file_path: str) -> Optional[str]:
        return DocumentParser.parse_text(file_path)

    @staticmethod
    def parse(file_path: str) -> Optional[str]:
        path = Path(file_path)
        suffix = path.suffix.lower()

        if suffix == '.pdf':
            return DocumentParser.parse_pdf(file_path)
        elif suffix in ['.txt', '.text']:
            return DocumentParser.parse_text(file_path)
        elif suffix in ['.md', '.markdown']:
            return DocumentParser.parse_markdown(file_path)
        else:
            logger.warning(f"Unsupported file type: {suffix} for {file_path}")
            return None
