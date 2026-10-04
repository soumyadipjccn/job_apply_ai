import unittest
from unittest.mock import MagicMock
import os
import sys

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.nvidia_client import NVIDIAClient

class TestNVIDIAClient(unittest.TestCase):
    def setUp(self):
        self.client = NVIDIAClient(api_key="mock_key")
        self.client.client = MagicMock()

    def test_extract_skills_empty_response(self):
        # Mock empty content returned from OpenAI client
        mock_choice = MagicMock()
        mock_choice.message.content = ""
        mock_response = MagicMock()
        mock_response.choices = [mock_choice]
        self.client.client.chat.completions.create.return_value = mock_response

        result = self.client.extract_skills_and_requirements("Job description text")
        self.assertIsNone(result)

    def test_extract_skills_none_content(self):
        mock_choice = MagicMock()
        mock_choice.message.content = None
        mock_response = MagicMock()
        mock_response.choices = [mock_choice]
        self.client.client.chat.completions.create.return_value = mock_response

        result = self.client.extract_skills_and_requirements("Job description text")
        self.assertIsNone(result)

    def test_extract_skills_valid_json(self):
        mock_choice = MagicMock()
        mock_choice.message.content = '{"matched_skills": ["Python"], "matched_requirements": [], "skill_categories": {}}'
        mock_response = MagicMock()
        mock_response.choices = [mock_choice]
        self.client.client.chat.completions.create.return_value = mock_response

        result = self.client.extract_skills_and_requirements("Job description text")
        self.assertEqual(result, {"matched_skills": ["Python"], "matched_requirements": [], "skill_categories": {}})

    def test_extract_skills_markdown_wrapped_json(self):
        mock_choice = MagicMock()
        mock_choice.message.content = '''Here is the requested JSON extraction:
```json
{
  "matched_skills": ["Python", "Docker"],
  "matched_requirements": ["5+ years experience"],
  "skill_categories": {"Programming Languages": ["Python"]}
}
```'''
        mock_response = MagicMock()
        mock_response.choices = [mock_choice]
        self.client.client.chat.completions.create.return_value = mock_response

        result = self.client.extract_skills_and_requirements("Job description text")
        self.assertIsNotNone(result)
        self.assertEqual(result["matched_skills"], ["Python", "Docker"])

    def test_generate_summary_empty_response(self):
        mock_choice = MagicMock()
        mock_choice.message.content = ""
        mock_response = MagicMock()
        mock_response.choices = [mock_choice]
        self.client.client.chat.completions.create.return_value = mock_response

        result = self.client.generate_tailored_summary("Software Engineer", "Acme", "Job description", ["Python"])
        self.assertIsNone(result)

    def test_generate_summary_valid_response(self):
        mock_choice = MagicMock()
        mock_choice.message.content = "Experienced software engineer with strong Python skills."
        mock_response = MagicMock()
        mock_response.choices = [mock_choice]
        self.client.client.chat.completions.create.return_value = mock_response

        result = self.client.generate_tailored_summary("Software Engineer", "Acme", "Job description", ["Python"])
        self.assertEqual(result, "Experienced software engineer with strong Python skills.")

if __name__ == "__main__":
    unittest.main()
