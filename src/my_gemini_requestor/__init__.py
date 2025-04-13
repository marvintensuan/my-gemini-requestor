import os
from pathlib import Path
import re

from google import genai
from google.genai import types


class GeminiRequestor:
    """
    Handles sending a prompt and file to the Gemini API and storing the response.

    Attributes:
        prompt (str): The prompt string to be sent.
        file_path (Path | None): Optional file path of the document to attach.
        file_mime_type (str): MIME type of the file. Default is 'application/pdf'.
        model (str): Gemini model to use. Default is 'gemini-1.5-flash'.
        client (genai.Client): An instance of the Gemini API client.
    """

    def __init__(
        self,
        prompt: str = "",
        file_path: Path | None = None,
        file_mime_type: str = "application/pdf",
        model: str = "gemini-1.5-flash",
        client: genai.Client | None = None,
    ) -> None:
        self.prompt = prompt
        self.file_path = file_path
        self.file_mime_type = file_mime_type
        self.model = model
        self._response: types.GenerateContentResponse | None = None

        if client:
            self.client = client
        else:
            api_key = os.environ.get("GEMINI_API_KEY")
            if not api_key:
                raise ValueError("GEMINI_API_KEY environment variable is not set.")
            try:
                self.client = genai.Client(api_key=api_key)
            except Exception as e:
                raise RuntimeError("Failed to initialize Gemini client.") from e

    @property
    def response(self) -> str:
        """
        Returns the parsed JSON-like response content from Gemini.

        Raises:
            NotYetRequestedError: If no request has been made yet.
        """
        if self._response is None:
            raise NotYetRequestedError(
                "No valid response at the moment. Have you tried to `send_request`?"
            )

        if self._response is None:
            raise NotYetRequestedError()

        if isinstance(self._response, types.GenerateContentResponse):
            pattern = r"```json(?:[a-zA-Z0-9]*\n)?(.*?)```"
            match = re.findall(pattern, self._response.text, re.DOTALL)
            return match[0] if match else self._response.text
        return str(self._response)

    def send_request(self) -> None:
        """
        Sends the prompt and optional file to the Gemini model and stores the response.

        Raises:
            FileNotFoundError: If the specified file path does not exist.
            RuntimeError: If the request fails for any reason.
        """
        parts = [self.prompt]

        if self.file_path:
            if not self.file_path.exists():
                raise FileNotFoundError(f"File not found: {self.file_path}")
            file_part = types.Part.from_bytes(
                data=self.file_path.read_bytes(), mime_type=self.file_mime_type
            )
            parts.append(file_part)

        try:
            self._response = self.client.models.generate_content(
                model=self.model, contents=parts
            )
        except Exception as e:
            raise RuntimeError("Failed to send request to Gemini.") from e


class NotYetRequestedError(Exception):
    """Raised when `.response` is accessed before `send_request()` has been called."""

    def __init__(self, message=None) -> None:
        default_message = "No valid response. Did you forget to call `send_request()`?"
        super().__init__(message or default_message)
