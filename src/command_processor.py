"""
THOR Agent - Enhanced Command Processor with Learning and Reflection
Supports multiple personas and advanced reasoning with Phi-4 Mini
"""

import whisper
import anthropic
import openai
import requests
import json
import re
import os
import io
import tempfile
from typing import Optional, Dict, Any, List
import asyncio
from mind.introspection_commands import MINDIntrospectionCommands
from loguru import logger


class EnhancedCommandProcessor:
    def __init__(self, llm_config: dict, memory_manager=None, mind_system=None):
        """Initialize enhanced command processor with memory, learning and MIND"""
        self.llm_config = llm_config
        self.memory = memory_manager
        self.mind = mind_system
        
        self.local_config = llm_config['providers']['local']
        self.remote_config = llm_config['providers']['remote']
        self.fallback_config = llm_config.get('providers', {}).get('fallback', {})
        self.routing_config = llm_config['routing']
        self.personas = llm_config.get('personas', {})
        
        # Initialize Whisper for STT
        try:
            model_size = llm_config.get('whisper_model', 'base')
            logger.info(f"Loading Whisper model: {model_size}")
            self.whisper_model = whisper.load_model(model_size)
            logger.info("Whisper model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load Whisper: {e}")
            self.whisper_model = None
            
        # Initialize LLM clients
        self._init_llm_clients()
        
        # Current session context
        self.current_persona = "assistant"
        self.conversation_history = []
        
        # Initialize MIND introspection commands
        if self.mind:
            self.introspection_commands = None  # Will be set by main app
        
    def _init_llm_clients(self):
        """Initialize all LLM clients"""
        # Anthropic client
        try:
            api_key = os.getenv('ANTHROPIC_API_KEY')
            if api_key:
                self.anthropic_client = anthropic.Anthropic(api_key=api_key)
                logger.info("Anthropic client initialized")
            else:
                self.anthropic_client = None
        except Exception as e:
            logger.error(f"Failed to initialize Anthropic client: {e}")
            self.anthropic_client = None
            
        # OpenAI client
        try:
            api_key = os.getenv('OPENAI_API_KEY')
            if api_key:
                self.openai_client = openai.OpenAI(api_key=api_key)
                logger.info("OpenAI client initialized")
            else:
                self.openai_client = None
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {e}")
            self.openai_client = None
            
    def _audio_to_text(self, audio_data: bytes) -> str:
        """Convert audio bytes to text using Whisper"""
        if not self.whisper_model:
            logger.error("Whisper model not available")
            return ""
            
        try:
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                temp_file.write(audio_data)
                temp_file_path = temp_file.name
                
            logger.info("Transcribing audio with Whisper...")
            result = self.whisper_model.transcribe(
                temp_file_path,
                language='de',
                fp16=False
            )
            
            text = result['text'].strip()
            logger.info(f"Transcription: '{text}'")
            
            os.unlink(temp_file_path)
            return text
            
        except Exception as e:
            logger.error(f"STT transcription failed: {e}")
            return ""
            
    def _determine_routing(self, text: str) -> str:
        """Determine which LLM to route to based on advanced patterns"""
        text_lower = text.lower()
        
        # Check for reflection/learning patterns
        if any(pattern in text_lower for pattern in self.routing_config.get('reflection_patterns', [])):
            return 'reflection'
            
        # Check for personal assistance patterns  
        if any(pattern in text_lower for pattern in self.routing_config.get('personal_patterns', [])):
            return 'personal'
            
        # Check for coding patterns
        if any(pattern in text_lower for pattern in self.routing_config.get('coding_patterns', [])):
            return 'coding'
            
        # Check for creative patterns
        if any(pattern in text_lower for pattern in self.routing_config.get('creative_patterns', [])):
            return 'creative'
            
        # Check for simple file operations
        if any(pattern in text_lower for pattern in self.routing_config.get('simple_patterns', [])):
            return 'simple'
            
        # Default to personal assistance
        return 'personal'
        
    async def _get_persona_context(self, routing_type: str) -> tuple[str, str]:
        """Get persona and system prompt based on routing"""
        persona_mapping = {
            'reflection': 'sparring_partner',
            'personal': 'assistant', 
            'coding': 'coder',
            'creative': 'sparring_partner',
            'simple': 'organizer'
        }
        
        persona = persona_mapping.get(routing_type, 'assistant')
        self.current_persona = persona
        
        persona_config = self.personas.get(persona, {})
        system_prompt = persona_config.get('prompt', '')
        
        # Add memory context if available
        if self.memory:
            memory_context = await self.memory.get_learning_context("")
            if memory_context:
                system_prompt += f"\n\nKontext aus früheren Interaktionen:\n{memory_context}"
                
        return persona, system_prompt
        
    async def _process_with_phi4_reasoning(self, text: str, routing_type: str) -> Optional[Dict]:
        """Process with Phi-4 Mini Reasoning using advanced prompting"""
        try:
            endpoint = self.local_config['endpoint']
            model = self.local_config['model']
            
            persona, system_prompt = await self._get_persona_context(routing_type)
            
            # Enhanced prompt with reasoning steps for Phi-4 Mini
            if routing_type == 'reflection':
                prompt = f"""<thinking>
Ich bin THOR, ein lernender KI-Assistent. Der Benutzer möchte eine Reflexion oder Analyse.

Befehl: "{text}"

Lass mich das analysieren:
1. Was genau wird von mir erwartet?
2. Welche Erkenntnisse kann ich aus bisherigen Interaktionen ziehen?
3. Wie kann ich dem Benutzer am besten helfen?
4. Welche Handlungsempfehlungen kann ich geben?

Systemkontext: {system_prompt}
</thinking>

{system_prompt}

Benutzer: "{text}"

Analysiere dies gründlich und gib eine durchdachte Antwort. Wenn es eine Dateioperation ist, antworte mit JSON.
Ansonsten gib eine reflektierte, hilfreiche Antwort."""
            
            elif routing_type == 'coding':
                prompt = f"""<thinking>
Ich bin THOR, der Coding-Assistent. Der Benutzer braucht Hilfe beim Programmieren.

Anfrage: "{text}"

Lass mich analysieren:
1. Handelt es sich um Code-Review, Debugging, oder neue Entwicklung?
2. Welche Programmiersprache oder Technologie ist betroffen?
3. Welche Best Practices sollte ich empfehlen?
4. Wie kann ich den Code verbessern?

Systemkontext: {system_prompt}
</thinking>

{system_prompt}

Benutzer: "{text}"

Analysiere die Coding-Anfrage und gib detaillierte, hilfreiche Antworten.
Bei Dateisystem-Operationen verwende JSON-Format."""
            
            elif routing_type == 'personal':
                prompt = f"""<thinking>
Ich bin THOR, der persönliche Assistent. Der Benutzer braucht Hilfe bei Organisation oder Aufgaben.

Anfrage: "{text}"

Lass mich analysieren:
1. Welche spezifische Aufgabe soll ich erledigen?
2. Welche Dateien oder Ordner sind betroffen?
3. Wie kann ich die Aufgabe am effizientesten ausführen?
4. Soll ich proaktive Verbesserungsvorschläge machen?

Systemkontext: {system_prompt}
</thinking>

{system_prompt}

Benutzer: "{text}"

Extrahiere die gewünschte Aktion und führe sie aus.
Für Dateisystem-Operationen antworte mit JSON:
{{"action": "copy|move|delete|list|create_folder|organize|cleanup", "source": ["datei"], "destination": "/pfad/"}}"""
            
            else:  # simple operations
                prompt = f"""<thinking>
Einfache Dateisystem-Operation erkannt.

Befehl: "{text}"

Analyse:
1. Welche Aktion? (kopiere=copy, verschiebe=move, lösche=delete, zeige=list, erstelle=create_folder)
2. Welche Dateien? (source)
3. Wohin? (destination)
4. Parameter oder Filter?
</thinking>

Extrahiere aus diesem deutschen Befehl die Dateisystem-Aktion:

Befehl: "{text}"

Antworte NUR mit validem JSON:
{{"action": "copy|move|delete|list|create_folder", "source": ["datei"], "destination": "/pfad/"}}"""

            payload = {
                "model": model,
                "messages": [
                    {"role": "system", "content": "Du bist THOR, ein intelligenter KI-Assistent mit Reasoning-Fähigkeiten."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": self.local_config.get('temperature', 0.1),
                "max_tokens": self.local_config.get('max_tokens', 1000)
            }
            
            logger.info(f"Sending request to Phi-4 ({routing_type}): {endpoint}")
            
            async with asyncio.timeout(15):  # 15 second timeout
                response = await asyncio.to_thread(
                    requests.post,
                    f"{endpoint}/chat/completions",
                    json=payload,
                    headers={"Content-Type": "application/json"}
                )
                
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content'].strip()
                
                # For simple operations, try to parse JSON
                if routing_type == 'simple':
                    try:
                        command = json.loads(content)
                        logger.info(f"Phi-4 JSON response: {command}")
                        return command
                    except json.JSONDecodeError:
                        # Extract JSON from response if wrapped in text
                        json_match = re.search(r'\{.*\}', content, re.DOTALL)
                        if json_match:
                            command = json.loads(json_match.group())
                            logger.info(f"Extracted JSON from Phi-4: {command}")
                            return command
                        else:
                            logger.error(f"Invalid JSON from Phi-4: {content}")
                            return None
                else:
                    # For other types, return as text response
                    logger.info(f"Phi-4 text response ({routing_type}): {content[:100]}...")
                    return {"type": "text_response", "content": content, "persona": persona}
            else:
                logger.error(f"Phi-4 request failed: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Phi-4 processing failed: {e}")
            return None
            
    async def _process_with_claude(self, text: str) -> Optional[Dict]:
        """Process command with Claude for complex commands"""
        if not self.anthropic_client:
            logger.error("Claude client not available")
            return None
            
        try:
            prompt = f"""Du bist THOR, ein intelligenter Dateisystem-Assistent.
Analysiere diesen deutschen Sprachbefehl und extrahiere die gewünschte Aktion.

Befehl: "{text}"

Antworte NUR mit einem validen JSON-Objekt im folgenden Format:
{{
  "action": "copy|move|delete|list|create_folder|search|rename|compress|extract|organize|cleanup",
  "source": ["datei1.txt", "datei2.txt"],
  "destination": "/ziel/pfad/",
  "parameters": {{"filter": "*.pdf", "recursive": true}}
}}

Wichtige Regeln:
- "source" ist immer ein Array, auch bei einer Datei
- Bei "list" oder "search" ist source der Suchpfad
- "destination" ist der Zielpfad
- "parameters" für zusätzliche Optionen wie Filter
- Erkenne deutsche Begriffe: kopiere=copy, verschiebe=move, lösche=delete, zeige/liste=list, erstelle=create_folder"""

            logger.info("Sending request to Claude...")
            
            message = await asyncio.to_thread(
                self.anthropic_client.messages.create,
                model=self.remote_config['model'],
                max_tokens=self.remote_config.get('max_tokens', 500),
                temperature=self.remote_config.get('temperature', 0.3),
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            content = message.content[0].text.strip()
            logger.info(f"Claude response: {content}")
            
            # Parse JSON response
            try:
                content = re.sub(r'```json\s*|\s*```', '', content)
                command = json.loads(content)
                logger.info(f"Parsed command from Claude: {command}")
                return command
                
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON from Claude: {content}")
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    try:
                        command = json.loads(json_match.group())
                        logger.info(f"Extracted JSON from Claude: {command}")
                        return command
                    except json.JSONDecodeError:
                        pass
                        
                logger.error("Could not parse command from Claude response")
                return None
                
        except Exception as e:
            logger.error(f"Claude processing failed: {e}")
            return None
            
    async def _process_with_openai_fallback(self, text: str) -> Optional[Dict]:
        """Fallback to OpenAI if other methods fail"""
        if not self.openai_client:
            logger.error("OpenAI client not available")
            return None
            
        try:
            logger.info("Using OpenAI as fallback...")
            
            response = await asyncio.to_thread(
                self.openai_client.chat.completions.create,
                model=self.fallback_config.get('model', 'gpt-4-turbo-preview'),
                messages=[
                    {"role": "system", "content": "Du bist THOR, ein Dateisystem-Assistent. Antworte nur mit JSON."},
                    {"role": "user", "content": f'Extrahiere Dateisystem-Befehl aus: "{text}" als JSON'}
                ],
                temperature=self.fallback_config.get('temperature', 0.3),
                max_tokens=self.fallback_config.get('max_tokens', 500),
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            command = json.loads(content)
            logger.info(f"OpenAI fallback response: {command}")
            return command
            
        except Exception as e:
            logger.error(f"OpenAI fallback failed: {e}")
            return None
            
    async def process(self, audio_data: bytes) -> Optional[Dict]:
        """
        Main processing pipeline with enhanced routing, learning and MIND consciousness
        """
        try:
            # Step 1: Speech to Text
            logger.info("Starting enhanced command processing pipeline...")
            text = self._audio_to_text(audio_data)
            
            if not text:
                logger.warning("No text extracted from audio")
                return None
                
            # Step 1.5: Check for MIND introspection commands
            if self.mind and self.introspection_commands:
                introspection_response = await self.introspection_commands.handle_introspection_command(text)
                if introspection_response:
                    # This is a consciousness/reflection command
                    return {
                        "type": "introspection_response",
                        "content": introspection_response,
                        "original_text": text
                    }
                
            # Step 2: Determine routing strategy
            routing_type = self._determine_routing(text)
            logger.info(f"Routing type determined: {routing_type}")
            
            # Step 3: Route to appropriate LLM with persona
            command = None
            
            # Try Phi-4 first for most operations
            if routing_type in ['simple', 'personal', 'coding', 'reflection']:
                command = await self._process_with_phi4_reasoning(text, routing_type)
                
            # Fallback to Claude for creative/complex tasks
            if not command and routing_type == 'creative':
                command = await self._process_with_claude(text)
                
            # Final fallback to OpenAI
            if not command:
                logger.info("Falling back to OpenAI...")
                command = await self._process_with_openai_fallback(text)
                
            # Store interaction in memory systems
            if self.memory and command:
                await self.memory.store_conversation(
                    user_input=text,
                    thor_response="Command processed",
                    command=command
                )
                
            # Store in MIND system
            if self.mind and command:
                await self.mind.process_experience(
                    event_type="processing",
                    content=f"Ich habe einen Befehl verarbeitet: '{text}' -> {command.get('action', 'unknown')}",
                    context={
                        "command_processing": True,
                        "routing_type": routing_type,
                        "success": command is not None,
                        "text_input": text
                    }
                )
                
            if command:
                if self._validate_command(command):
                    logger.info(f"Enhanced command processing successful: {command}")
                    return command
                else:
                    logger.error(f"Invalid command structure: {command}")
                    return None
            else:
                logger.error("No command extracted from text")
                return None
                
        except Exception as e:
            logger.error(f"Enhanced command processing pipeline failed: {e}")
            return None
            
    def _validate_command(self, command: Dict) -> bool:
        """Validate command structure"""
        try:
            # Handle text responses from reflection/coding
            if command.get('type') == 'text_response':
                return True
                
            required_fields = ['action']
            for field in required_fields:
                if field not in command:
                    logger.error(f"Missing required field: {field}")
                    return False
                    
            # Validate action
            valid_actions = [
                'copy', 'move', 'delete', 'list', 'create_folder', 'search', 
                'rename', 'compress', 'extract', 'organize', 'cleanup'
            ]
            if command['action'] not in valid_actions:
                logger.error(f"Invalid action: {command['action']}")
                return False
                
            # Ensure source is list
            if 'source' in command and not isinstance(command['source'], list):
                command['source'] = [command['source']]
                
            return True
            
        except Exception as e:
            logger.error(f"Command validation failed: {e}")
            return False


# Fallback for backward compatibility
class CommandProcessor(EnhancedCommandProcessor):
    """Backward compatible command processor"""
    
    def __init__(self, llm_config: dict):
        super().__init__(llm_config, memory_manager=None)


class MockCommandProcessor:
    """Mock processor for testing"""
    
    def __init__(self, llm_config: dict):
        self.llm_config = llm_config
        logger.info("Using Mock Command Processor")
        
    async def process(self, audio_data: bytes) -> Optional[Dict]:
        """Return a mock command"""
        return {
            "action": "list",
            "source": ["~/Downloads/"],
            "parameters": {"filter": "*"}
        }
