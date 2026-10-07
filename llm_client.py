"""
LLM Client Module
Handles communication with OpenAI or Anthropic APIs
"""

import os
import json
from typing import List, Dict, Optional
from dotenv import load_dotenv

load_dotenv()


class LLMClient:
    """Unified client for LLM providers"""
    
    def __init__(self, provider: str = None, model: str = None):
        self.provider = provider or os.getenv('LLM_PROVIDER', 'openai')
        self.model = model or os.getenv('LLM_MODEL', 'gpt-4-turbo-preview')
        
        if self.provider == 'openai':
            import openai
            self.client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        elif self.provider == 'anthropic':
            import anthropic
            self.client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
    
    def chat_completion(self, messages: List[Dict[str, str]], temperature: float = 0.1) -> str:
        """
        Get chat completion from LLM
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature (0-1)
            
        Returns:
            Response content as string
        """
        if self.provider == 'openai':
            return self._openai_completion(messages, temperature)
        elif self.provider == 'anthropic':
            return self._anthropic_completion(messages, temperature)
    
    def _openai_completion(self, messages: List[Dict[str, str]], temperature: float) -> str:
        """OpenAI completion"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            response_format={"type": "json_object"} if "json" in messages[0].get('content', '').lower() else None
        )
        return response.choices[0].message.content
    
    def _anthropic_completion(self, messages: List[Dict[str, str]], temperature: float) -> str:
        """Anthropic completion"""
        # Convert messages format
        system_msg = next((m['content'] for m in messages if m['role'] == 'system'), None)
        user_messages = [m for m in messages if m['role'] != 'system']
        
        response = self.client.messages.create(
            model=self.model if 'claude' in self.model else 'claude-3-opus-20240229',
            max_tokens=4096,
            temperature=temperature,
            system=system_msg,
            messages=user_messages
        )
        return response.content[0].text
    
    def extract_json(self, text: str) -> dict:
        """
        Extract JSON from LLM response
        Handles markdown code blocks and other formatting
        """
        text = text.strip()
        
        # Remove markdown code blocks
        if text.startswith('```'):
            lines = text.split('\n')
            text = '\n'.join(lines[1:-1]) if len(lines) > 2 else text
            text = text.replace('```json', '').replace('```', '')
        
        # Try to parse JSON
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            # Try to find JSON object in text
            start = text.find('{')
            end = text.rfind('}') + 1
            if start != -1 and end != 0:
                return json.loads(text[start:end])
            
            # Try to find JSON array
            start = text.find('[')
            end = text.rfind(']') + 1
            if start != -1 and end != 0:
                return json.loads(text[start:end])
            
            raise ValueError("Could not extract valid JSON from response")


# Global instance
_llm_client = None


def get_llm_client() -> LLMClient:
    """Get or create LLM client singleton"""
    global _llm_client
    if _llm_client is None:
        _llm_client = LLMClient()
    return _llm_client
