"""
NVIDIA NIM / AI Foundation Models API Client

This module provides integration with NVIDIA's hosted LLM endpoints
using OpenAI API standard client interface.
"""

import os
import re
import json
import logging
from typing import Dict, List, Tuple, Optional

logger = logging.getLogger(__name__)

# Default NVIDIA NIM model
DEFAULT_NVIDIA_MODEL = os.environ.get("NVIDIA_MODEL", "nvidia/nemotron-3.5-lightning-30b-a3b")
NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"

class NVIDIAClient:
    """
    Client interface for interacting with NVIDIA AI Foundation Models.
    """

    def __init__(self, api_key: Optional[str] = None, model: str = DEFAULT_NVIDIA_MODEL):
        """
        Initialize the NVIDIA API client.
        
        Args:
            api_key (str, optional): NVIDIA API key. If None, reads from NVIDIA_API_KEY or OPENAI_API_KEY.
            model (str): NVIDIA NIM model ID to use.
        """
        self.api_key = api_key or os.environ.get("NVIDIA_API_KEY") or os.environ.get("OPENAI_API_KEY")
        self.model = model
        self.client = None
        
        if self.api_key:
            try:
                from openai import OpenAI
                self.client = OpenAI(
                    base_url=NVIDIA_BASE_URL,
                    api_key=self.api_key
                )
                logger.info(f"Initialized NVIDIA AI Client with model: {self.model}")
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI client for NVIDIA: {str(e)}")
        else:
            logger.info("NVIDIA_API_KEY not found. NVIDIA AI features will fall back to rule-based NLP.")

    def is_available(self) -> bool:
        """Check if NVIDIA API client is configured and ready."""
        return self.client is not None

    def extract_skills_and_requirements(self, job_description: str) -> Optional[Dict]:
        """
        Extract structured skills and requirements from a job description using NVIDIA NIM LLM.
        
        Args:
            job_description (str): Raw text of the job description.
            
        Returns:
            dict or None: JSON structure with categorized skills and requirements, or None on failure.
        """
        if not self.is_available():
            return None

        prompt = f"""You are an expert technical recruiter and resume specialist.
Analyze the following job description and extract:
1. Technical and soft skills categorized into:
   - "Programming Languages"
   - "Frameworks & Libraries"
   - "Databases"
   - "Cloud & DevOps"
   - "Tools & Platforms"
   - "Methodologies"
   - "Soft Skills"
   - "Business & Analytics"
2. Key job requirements and expectations.

Return ONLY a valid JSON object matching this structure:
{{
  "skill_categories": {{
    "Programming Languages": ["Python", ...],
    "Frameworks & Libraries": [...],
    ...
  }},
  "matched_skills": ["Python", "Docker", ...],
  "matched_requirements": ["5+ years experience in Python", ...]
}}

Job Description:
{job_description}
"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a precise technical skill extractor that outputs ONLY valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                top_p=0.7,
                max_tokens=1500
            )

            raw_text = response.choices[0].message.content.strip()
            
            # Remove Markdown code blocks if present
            if raw_text.startswith("```"):
                raw_text = re.sub(r"^```(?:json)?\n?", "", raw_text)
                raw_text = re.sub(r"\n?```$", "", raw_text)

            data = json.loads(raw_text)
            logger.info(f"NVIDIA Model ({self.model}) successfully extracted skills and requirements.")
            return data

        except Exception as e:
            logger.warning(f"NVIDIA API skill extraction failed: {str(e)}. Falling back to local NLP.")
            return None

    def generate_tailored_summary(self, job_title: str, company: str, job_description: str, skills: List[str]) -> Optional[str]:
        """
        Generate a tailored professional summary for a CV based on job context.
        """
        if not self.is_available():
            return None

        prompt = f"""Write a compelling, 3-4 sentence professional summary for a resume tailored to the following role:
Role: {job_title} at {company}
Key Skills to Highlight: {', '.join(skills[:10])}
Job Description excerpt: {job_description[:1000]}

Return only the text of the professional summary.
"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional resume writer."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4,
                max_tokens=300
            )

            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.warning(f"NVIDIA API tailored summary generation failed: {str(e)}")
            return None
