# **ankiazvox**

**ankiazvox** is a professional CLI tool designed to synchronize Anki notes with high-quality neural audio powered by Azure Cognitive Services. It automates the process of fetching text, stripping HTML, generating speech, and updating your Anki cards.

## **✨ Features**

* **Neural TTS**: Uses Azure's state-of-the-art Neural voices for natural, human-like speech.  
* **HTML Sanitization**: Automatically strips HTML tags (like \<br/\>, \<div\>) from your Anki fields to ensure clean speech synthesis.  
* **Overwrite Protection**: Smartly skips notes that already have audio to save API quota, with an optional \--overwrite flag.  
* **Seamless Integration**: Automatically uploads audio to Anki's media folder and updates the \[sound:...\] tags via AnkiConnect.  
* **Voice Explorer**: Built-in command to list and filter available Azure voices by locale.  
* **Auto-Cleanup**: Automatically removes temporary audio files after synchronization is complete.  
* **Flexible CLI**: Built with Click for a smooth command-line experience.

## **🚀 Installation**

### **1\. Prerequisites**

* **Anki Desktop** with the [AnkiConnect](https://ankiweb.net/shared/info/2055492159) add-on installed.  
* An **Azure Speech Service** subscription (Key and Region).

### **2\. Install via pip**

```
pip install ankiazvox
```

### **3\. Install from Source**

```
git clone https://github.com/ericxu131/ankiazvox.git
cd ankiazvox  
pip install .
```

## **⚙️ Configuration**

Create a .env file in your working directory (or specify one via \--env):

```
# AnkiConnect Settings  
ANKI_CONNECT_URL=http://127.0.0.1:8765

# Azure Speech Settings  
AZURE_SPEECH_KEY=your_azure_api_key  
AZURE_SPEECH_REGION=your_service_region (e.g., eastus)

# Default Voice Configuration  
DEFAULT_VOICE=en-US-AvaMultilingualNeural
```

## **🛠 Usage**

You can use the azv alias or the full ankiazvox command.

### **1\. Synchronize Audio (sync)**

Sync notes from a deck. By default, it **skips** fields that already contain audio data.

azv sync \--query "deck:English" \--source "Front" \--target "Audio"

**Force overwrite** existing audio and limit to 5 notes:

azv sync \-q "tag:review" \-s "Word" \-t "Sound" \--overwrite \--limit 5

| Option | Short | Description |
| :---- | :---- | :---- |
| \--query | \-q | Anki search query (e.g., deck:Default) |
| \--source | \-s | Field name containing the text to synthesize |
| \--target | \-t | Field name where the \[sound:...\] tag will be saved |
| \--overwrite |  | Force update the target field even if it has a value |
| \--voice | \-v | Override the default Azure voice |
| \--limit |  | Max number of notes to process |
| \--env |  | Path to a specific .env file |

### **2\. List Voices (list-voices)**

Explore available neural voices:

```
azv list-voices --locale zh-CN
```

## **🤝 Contributing**

1. Fork the Project  
2. Create your Feature Branch (git checkout \-b feature/AmazingFeature)  
3. Commit your Changes (git commit \-m 'Add some AmazingFeature')  
4. Push to the Branch (git push origin feature/AmazingFeature)  
5. Open a Pull Request

## **📄 License**

Distributed under the **MIT License**.

## **👤 Author**

Eric Xu \- xulihua2006@gmail.com  
Project Link: https://github.com/ericxu131/ankiazvox