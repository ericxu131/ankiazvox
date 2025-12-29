# **ankiazvox**

**ankiazvox** is a professional-grade CLI tool that synchronizes Anki notes with high-quality Azure Neural TTS audio. By leveraging cloud-based Neural voices, it automates text extraction, sanitization, and card updates via AnkiConnect, transforming text-only decks into immersive audio-visual learning tools.

## **✨ New in v0.5.0**

* **azv init**: An interactive onboarding setup that walks you through connecting your Azure account and setting your preferred default voice.  
* **Field Mapping**: Efficiency-focused syncing that processes multiple fields simultaneously via the \--fields flag (e.g., Word:Audio;Sent:SentAudio).  
* **Prosody Control**: Fine-tune the listening experience with \--rate and \--pitch flags, allowing you to slow down complex phrases or adjust tone for clarity.  
* **SSML Support**: Enhanced processing that preserves natural phrasing by converting `<br>` to pauses and providing full support for raw SSML input fields.

## **🚀 Installation**

### **1\. Prerequisites**

* **Anki Desktop**: Must be running with the [AnkiConnect](https://ankiweb.net/shared/info/2055492159) add-on installed and configured.  
* **Azure Speech Service**: An active subscription key and region from the Azure portal (Azure offers a generous free tier for speech services).

### **2\. Setup & Configuration**

Install the package and run the initializer to create your azv\_config.yaml file:

```
pip install ankiazvox  
azv init
```

## **🛠 Usage**

### **1\. Synchronize Audio (sync)**

The sync command generates audio for notes that match a specific Anki search query. It handles the batch processing of voice synthesis and media management automatically.

**Basic Single-Field Sync:**

Sync text from "Front" and save audio tag to "Audio"  
```
azv sync -q "deck:English::Vocabulary" -s "Front" -t "Audio"
```

**Advanced Multi-Field Sync with Prosody:**

Process Word and Sentence fields at 85% speed with a slight pitch increase
```  
azv sync -q "deck:JP::Grammar" -f "Word:WordAud;Sent:SentAud" --rate 0.85 --pitch +5%
```

| Option | Short | Description |
| :---- | :---- | :---- |
| \--query | \-q | Anki search query (standard Anki search syntax) |
| \--fields | \-f | Key-value mapping: source1:target1;source2:target2 |
| \--source | \-s | Name of the field containing source text |
| \--target | \-t | Name of the field to store the \[sound:...\] tag |
| \--rate |  | Synthesis speed (1.0 is normal; 0.8 is 80% speed) |
| \--pitch |  | Pitch adjustment (e.g., \+10% or \-5%) |
| \--voice | \-v | Override the default neural voice for this session |
| \--overwrite |  | If set, replaces existing audio in the target field |
| \--yes | \-y | Skips the confirmation preview and starts immediately |

### **2\. Sample & List Voices**

Before running a large sync, it is recommended to sample voices to find the best fit for your language material.

Preview a voice at a slower speed to check clarity  
```
azv sample --voice en-US-AndrewNeural --text "The quick brown fox" --rate 0.8 --play
```

List all Japanese neural voices to find a specific dialect or tone  
```
azv list-voices --locale ja-JP
```

## **📝 Formatting & SSML**

* **HTML Sanitization**: The tool cleans up Anki's internal HTML (like `<div>` and `<span>`) to ensure the TTS engine only reads the text.  
* **Smart Pauses**: It preserves line breaks by converting `<br>` tags into 400ms SSML pauses, which helps in separating sentences or definitions.  
* **Raw SSML**: For advanced users, if a field's content starts with the `<speak>` tag, **ankiazvox** treats it as raw SSML. This allows you to manually insert custom breaks, emphasis, or phoneme corrections directly into your Anki notes.

## **🤝 Contributing**

Contributions are welcome\! Whether it's a bug fix, a new feature, or an improvement to the documentation, feel free to open an issue or submit a Pull Request on GitHub.

## **📄 License**

This project is open-source and released under the **MIT License**.