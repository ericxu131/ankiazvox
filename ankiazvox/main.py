import os
import base64
import time
import shutil
import yaml
import subprocess
from typing import Any, Optional, Dict, List
from pathlib import Path
from dotenv import load_dotenv

import requests
import azure.cognitiveservices.speech as speechsdk
from tqdm import tqdm
import click
from bs4 import BeautifulSoup

# --- Constants ---
DEFAULT_CONFIG_FILENAME = "azv_config.yaml"

# --- Core Logic Classes ---

class AnkiClient:
    """Wrapper for AnkiConnect API interactions."""
    
    def __init__(self, url: str):
        self.url = url
        self.version = 6

    def invoke(self, action: str, **params) -> Any:
        """Standard method to invoke AnkiConnect actions."""
        payload = {"action": action, "version": self.version, "params": params}
        try:
            response = requests.post(self.url, json=payload)
            response.raise_for_status()
            data = response.json()
            if data.get("error"):
                raise Exception(f"AnkiConnect Error: {data['error']}")
            return data.get("result")
        except Exception as e:
            click.secho(
                f"Error: Unable to connect to Anki. ({e})",
                fg="red",
            )
            return None


class AzureTTSManager:
    """Wrapper for Azure Cognitive Services Speech Synthesis with SSML support."""

    def __init__(self, key: str, region: str, voice: Optional[str] = None):
        self.speech_config = speechsdk.SpeechConfig(subscription=key, region=region)
        if voice:
            self.speech_config.speech_synthesis_voice_name = voice
        
        # Set output format to MP3
        self.speech_config.set_speech_synthesis_output_format(
            speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3
        )

    def speak(self, content: str, save_path: Path) -> bool:
        """Synthesize content (SSML or text) and save to MP3."""
        audio_config = speechsdk.audio.AudioOutputConfig(filename=str(save_path))
        synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=self.speech_config, audio_config=audio_config
        )
        
        if content.strip().startswith("<speak"):
            result = synthesizer.speak_ssml_async(content).get()
        else:
            result = synthesizer.speak_text_async(content).get()
            
        return result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted

    def get_voice_list(self, locale: Optional[str] = None) -> List[Any]:
        """Fetch list of available voices from Azure."""
        synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config, audio_config=None)
        result = synthesizer.get_voices_async(locale if locale else "").get()
        if result.reason == speechsdk.ResultReason.VoicesListRetrieved:
            return sorted(result.voices, key=lambda x: x.short_name)
        return []

    def list_voices(self, locale: Optional[str] = None):
        """Display available voices in terminal."""
        voices = self.get_voice_list(locale)
        if voices:
            click.echo(f"{'Voice Name':<40} | {'Gender':<10} | {'Locale':<10}")
            click.echo("-" * 65)
            for v in voices:
                gender = "Female" if v.gender == speechsdk.SynthesisVoiceGender.Female else "Male"
                click.echo(f"{v.short_name:<40} | {gender:<10} | {v.locale:<10}")


# --- Utilities ---

def wrap_ssml(text: str, voice: str, rate: str = "1.0", pitch: str = "0%") -> str:
    """
    Wraps plain text in an SSML envelope with prosody controls.
    Converts <br> tags into SSML break elements for natural pauses.
    """
    # Replace <br> or <br/> with a 400ms pause
    ssml_text = text.replace("<br>", '<break time="400ms"/>').replace("<br/>", '<break time="400ms"/>')
    
    return f"""
    <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'>
        <voice name='{voice}'>
            <prosody rate='{rate}' pitch='{pitch}'>
                {ssml_text}
            </prosody>
        </voice>
    </speak>
    """

def clean_html(raw_html: str) -> str:
    """Remove HTML tags except <br> and convert entities to plain text for TTS processing."""
    if not raw_html: return ""
    
    soup = BeautifulSoup(raw_html, "html.parser")
    for tag in soup.find_all(True):
        if tag.name != 'br':
            tag.unwrap()
            
    return str(soup)

def load_config(config_path: Optional[str] = None) -> Dict[str, str]:
    """Load configuration from YAML or .env file."""
    config = {
        "ANKI_CONNECT_URL": "http://127.0.0.1:8765",
        "AZURE_SPEECH_KEY": "",
        "AZURE_SPEECH_REGION": "",
        "DEFAULT_VOICE": ""
    }
    target_path = Path(config_path) if config_path else Path.cwd() / DEFAULT_CONFIG_FILENAME
    
    if not target_path.exists() and not config_path:
        for alt in ["azv_config.yml", ".env"]:
            if (Path.cwd() / alt).exists():
                target_path = Path.cwd() / alt
                break

    if target_path.exists():
        if target_path.suffix.lower() in [".yaml", ".yml"]:
            with open(target_path, "r", encoding="utf-8") as f:
                yaml_data = yaml.safe_load(f)
                if yaml_data: config.update(yaml_data)
        elif target_path.name == ".env" or target_path.suffix == "":
            load_dotenv(dotenv_path=target_path)
            config["ANKI_CONNECT_URL"] = os.getenv("ANKI_CONNECT_URL", config["ANKI_CONNECT_URL"])
            config["AZURE_SPEECH_KEY"] = os.getenv("AZURE_SPEECH_KEY", "")
            config["AZURE_SPEECH_REGION"] = os.getenv("AZURE_SPEECH_REGION", "")
            config["DEFAULT_VOICE"] = os.getenv("DEFAULT_VOICE", "")
    return config

def play_audio(file_path: Path):
    """Play audio file using system player."""
    try:
        if os.name == 'nt': os.startfile(file_path)
        elif os.uname().sysname == 'Darwin': subprocess.run(['afplay', str(file_path)], check=True)
        else: subprocess.run(['ffplay', '-nodisp', '-autoexit', str(file_path)], check=True)
    except Exception: pass

def parse_field_mapping(mapping_str: str) -> Dict[str, str]:
    """Parses 's1:t1;s2:t2' into {'s1': 't1', 's2': 't2'}."""
    mapping = {}
    parts = mapping_str.split(";")
    for part in parts:
        if ":" in part:
            s, t = part.split(":", 1)
            mapping[s.strip()] = t.strip()
    return mapping

# --- CLI Command Group ---

@click.group()
def cli():
    """AnkiVox CLI: Professional Anki TTS Synchronization Tool."""
    pass

@cli.command()
def init():
    """Interactively initialize the azv_config.yaml file."""
    config_path = Path.cwd() / DEFAULT_CONFIG_FILENAME
    if config_path.exists():
        if not click.confirm(f"'{DEFAULT_CONFIG_FILENAME}' already exists. Overwrite?"):
            click.echo("Initialization aborted.")
            return

    click.secho("--- AnkiVox Configuration Setup ---", fg="cyan", bold=True)
    
    key = click.prompt("Enter your Azure Speech Key", type=str)
    region = click.prompt("Enter your Azure Speech Region (e.g., eastus)", type=str)
    anki_url = click.prompt("Enter AnkiConnect URL", default="http://127.0.0.1:8765", type=str)
    
    click.echo("\nPopular Voices:")
    click.echo("1. en-US-AndrewNeural (Male, English)")
    click.echo("2. en-US-AvaNeural (Female, English)")
    click.echo("3. zh-CN-XiaoxiaoNeural (Female, Chinese)")
    click.echo("4. Custom / Skip")
    
    voice_choice = click.prompt("Select a default voice", default="4", type=str)
    
    default_voice = ""
    if voice_choice == "1": default_voice = "en-US-AndrewNeural"
    elif voice_choice == "2": default_voice = "en-US-AvaNeural"
    elif voice_choice == "3": default_voice = "zh-CN-XiaoxiaoNeural"
    else:
        default_voice = click.prompt("Enter custom voice name (or leave empty)", default="", show_default=False)

    config_data = {
        "AZURE_SPEECH_KEY": key.strip(),
        "AZURE_SPEECH_REGION": region.strip(),
        "ANKI_CONNECT_URL": anki_url.strip(),
        "DEFAULT_VOICE": default_voice.strip()
    }

    with open(config_path, "w", encoding="utf-8") as f:
        yaml.dump(config_data, f, default_flow_style=False, sort_keys=False)
    
    click.secho(f"\nSuccess! Configuration saved to {DEFAULT_CONFIG_FILENAME}", fg="green")
    click.echo("You can now run 'azv list-voices' to verify your connection.")

@cli.command()
@click.option("--config", type=click.Path(exists=True), help="Path to config file")
@click.option("--voice", "-v", help="Specific Azure voice name")
@click.option("--locale", "-l", help="Sample all voices in a specific locale")
@click.option("--text", "-t", default="Sample text.", help="Text to synthesize")
@click.option("--rate", default="1.0", help="Speech rate (e.g., 0.8)")
@click.option("--pitch", default="0%", help="Pitch (e.g., +10%)")
@click.option("--out-dir", "-o", default="samples", help="Output directory")
@click.option("--play", is_flag=True, default=False, help="Play audio immediately")
def sample(config, voice, locale, text, rate, pitch, out_dir, play):
    """Generate sample audio files with SSML support."""
    if not voice and not locale:
        click.secho("Error: Provide either --voice or --locale.", fg="red")
        return
    cfg = load_config(config)
    tts = AzureTTSManager(cfg.get("AZURE_SPEECH_KEY"), cfg.get("AZURE_SPEECH_REGION"))
    out_path = Path(out_dir)
    out_path.mkdir(exist_ok=True)
    
    voices = [voice] if voice else [v.short_name for v in tts.get_voice_list(locale)]
    click.echo(f"Generating {len(voices)} samples...")
    for v_name in tqdm(voices):
        file_path = out_path / f"{v_name}.mp3"
        tts.speech_config.speech_synthesis_voice_name = v_name
        content = wrap_ssml(text, v_name, rate=rate, pitch=pitch) if (rate != "1.0" or pitch != "0%") else text
        if tts.speak(content, file_path) and play and len(voices) == 1:
            play_audio(file_path)

@cli.command()
@click.option("--config", type=click.Path(exists=True), help="Path to config")
@click.option("--query", "-q", required=True, help='Anki query, e.g., "deck:Default"')
@click.option("--source", "-s", help="Source field")
@click.option("--target", "-t", help="Target field")
@click.option("--fields", "-f", help="Field mapping e.g., 'Front:Audio;Back:BackAudio'")
@click.option("--voice", "-v", help="Azure voice name")
@click.option("--rate", default="1.0", help="Speech rate")
@click.option("--pitch", default="0%", help="Pitch adjustment")
@click.option("--overwrite", is_flag=True, default=False, help="Overwrite existing audio")
@click.option("--yes", "-y", is_flag=True, default=False, help="Skip confirmation")
def sync(config, query, source, target, fields, voice, rate, pitch, overwrite, yes):
    """Sync Anki notes with multi-field mapping and SSML support."""
    cfg = load_config(config)
    anki = AnkiClient(cfg.get("ANKI_CONNECT_URL"))
    
    field_map = parse_field_mapping(fields) if fields else {}
    if source and target:
        field_map[source] = target
    
    if not field_map:
        click.secho("Error: Must provide --source/--target or --fields.", fg="red")
        return

    tts_key, tts_region = cfg.get("AZURE_SPEECH_KEY"), cfg.get("AZURE_SPEECH_REGION")
    default_voice = voice or cfg.get("DEFAULT_VOICE")
    if not tts_key or not tts_region:
        click.secho("Error: Missing Azure credentials. Run 'azv init' to set them up.", fg="red")
        return

    tts = AzureTTSManager(tts_key, tts_region, default_voice)
    temp_path = Path("temp_audios")
    
    try:
        click.echo(f"Searching: {query}...")
        note_ids = anki.invoke("findNotes", query=query)
        if not note_ids: return
        notes_data = anki.invoke("notesInfo", notes=note_ids)
        
        tasks = []
        for note in notes_data:
            note_fields = note.get("fields", {})
            for src, tgt in field_map.items():
                if src in note_fields and tgt in note_fields:
                    val = note_fields.get(tgt, {}).get("value", "").strip()
                    if val and not overwrite: continue
                    txt = clean_html(note_fields.get(src, {}).get("value", ""))
                    if txt: tasks.append((note["noteId"], src, tgt, txt))

        if not tasks:
            click.secho("No notes require sync.", fg="yellow")
            return

        click.secho(f"Sync Preview: {len(tasks)} audio files to generate.", fg="cyan", bold=True)
        if not yes and not click.confirm("Proceed?"): return

        temp_path.mkdir(exist_ok=True)
        for nid, s_fld, t_fld, txt in tqdm(tasks, desc="Syncing"):
            fname = f"azv_{s_fld}_{nid}.mp3"
            l_file = temp_path / fname
            if "<br" in txt or rate != "1.0" or pitch != "0%":
                input_content = wrap_ssml(txt, default_voice, rate=rate, pitch=pitch)
            else:
                input_content = txt
            
            if tts.speak(input_content, l_file):
                with open(l_file, "rb") as f:
                    b64 = base64.b64encode(f.read()).decode("utf-8")
                anki.invoke("storeMediaFile", filename=fname, data=b64)
                anki.invoke("updateNoteFields", note={"id": nid, "fields": {t_fld: f"[sound:{fname}]"}})
                time.sleep(0.05)
        click.secho(f"Done! {len(tasks)} files synced.", fg="green")
    finally:
        if temp_path.exists(): shutil.rmtree(temp_path)

@cli.command()
@click.option("--config", type=click.Path(exists=True), help="Path to config")
@click.option("--locale", "-l", help="Locale filter")
def list_voices(config, locale):
    """List available Azure TTS voices."""
    cfg = load_config(config)
    tts = AzureTTSManager(cfg.get("AZURE_SPEECH_KEY"), cfg.get("AZURE_SPEECH_REGION"))
    tts.list_voices(locale)

if __name__ == "__main__":
    cli()