# srt-translate-OpenAI-API
Configurable Python-based .srt subtitle translator utilizing the OpenAI API.

## Install

To use this script, you first need to clone the repository and install the required Python dependencies.

```bash
git clone https://github.com/FlyingFathead/srt-translate-OpenAI-API.git
cd srt-translate-OpenAI-API
pip install -r requirements.txt
```

## Usage

After installing the necessary dependencies, you can run the script using:

```bash
python translate_srt.py path/to/your/file.srt
```

Make sure to replace `path/to/your/file.srt` with the actual path to your subtitle file.

## Configuration

Before running the script, you need to set up your OpenAI API key. You can do this by setting an environment variable `OPENAI_API_KEY` or by placing it in a file named `api_token.txt` in the same directory as the script.

## Changes

- v0.09 - clarity for term preview
- v0.08 - preview printout during translation
- v0.07 - unique block marker
- v0.06 - block counting
- v0.05 - additional error handling
- v0.04 - option to add in additional information for the model
- v0.03 - initial commit

## About

By [FlyingFathead](https://github.com/FlyingFathead) (w/ digital ghost code from ChaosWhisperer)
