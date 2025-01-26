from markdown import markdown
from diagrams import Diagram
from gtts import gTTS
import os
import uuid
from langchain_ollama import ChatOllama
from .shared import convert_to_modality
from .tts import synthesize

class ContentDeliverer:
    def __init__(self, config):
        self.output_dir = config.get("output_dir", "outputs")
        os.makedirs(self.output_dir, exist_ok=True)
        
    def deliver(self, content: dict, modality: str) -> str:
        """Deliver content in specified format"""
        filename = f"{uuid.uuid4()}"
        
        if modality == "text":
            return self._save_text(content['explanation'], filename)
        elif modality == "visual":
            return self._generate_diagram(content, filename)
        elif modality == "audio":
            return self._generate_audio(content, filename)
        else:
            raise ValueError(f"Unsupported modality: {modality}")

    def _save_text(self, text: str, filename: str) -> str:
        """Save formatted text explanation"""
        path = f"{self.output_dir}/{filename}.md"
        with open(path, 'w') as f:
            f.write(markdown(text))
        return path

    def _generate_diagram(self, content: dict, filename: str) -> str:
        """Generate visual diagram from content"""
        diagram_path = f"{self.output_dir}/{filename}.png"
        with Diagram("", show=False, filename=diagram_path):
            # Diagram generation logic based on content
            pass
        return diagram_path

    def _generate_audio(self, content: dict, filename: str) -> str:
        """Generate audio explanation"""
        tts = gTTS(text=content['explanation'], lang='en')
        audio_path = f"{self.output_dir}/{filename}.mp3"
        tts.save(audio_path)
        return audio_path

def format_text(content: dict) -> str:
    """Format text output with proper styling"""
    return markdown(f"""
    # {content['title']}
    {content['explanation']}
    
    ## Quiz
    {content.get('quiz', '')}
    """)

def display_visual(diagram_spec: str) -> None:
    """Render visual diagrams"""
    Diagram("Learning Content", diagram_spec).render()

def play_audio(text: str) -> None:
    audio_file = synthesize(text)
    os.system(f"afplay {audio_file}")  # macOS only

def generate_diagram(explanation: str) -> str:
    """Generate diagram code from explanation"""
    llm = ChatOllama(model="llama3.2")
    prompt = f"""Convert this explanation into Mermaid.js diagram code:
    {explanation}
    """
    return llm.invoke(prompt).content 

def deliver_to_student(content: dict, modality: str = "text"):
    """Deliver content in specified format"""
    if modality == "text":
        print(f"\n📚 {content['title']}\n{content['body']}")
    elif modality == "audio":
        print("\n🔊 Audio content delivered")
    else:
        print("\n📦 Content package generated") 