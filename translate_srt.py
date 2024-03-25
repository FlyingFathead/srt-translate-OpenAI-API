# translate_srt.py
# v0.04
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# https://github.com/FlyingFathead/srt-translate-OpenAI-API
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import openai
import pysrt
import sys
import os
import configparser

# Initialize and read the configuration
config = configparser.ConfigParser()
config.read('config.ini')

# Function to read the OpenAI API key securely
def get_api_key():
    prefer_env = config.getboolean('DEFAULT', 'PreferEnvForAPIKey', fallback=True)

    if prefer_env:
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key is not None:
            return api_key

    try:
        with open('api_token.txt', 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        if not prefer_env:
            api_key = os.getenv('OPENAI_API_KEY')
            if api_key is not None:
                return api_key

        print("The OPENAI_API_KEY environment variable is not set, and `api_token.txt` was not found.")
        print("Please set either one and adjust `config.ini` if needed for the preferred load order.")
        sys.exit(1)

def get_config(section, option, prompt_message, is_int=False):
    if section not in config or option not in config[section]:
        print(prompt_message)
        value = input().strip()
        if not section in config:
            config.add_section(section)
        config.set(section, option, value)
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        return int(value) if is_int else value
    return int(config[section][option]) if is_int else config[section][option]

# Check for the correct usage and provide feedback if needed
if len(sys.argv) != 2:
    print("Usage: python translate_srt.py path/to/your/file.srt")
    sys.exit(1)

input_file_path = sys.argv[1]

# Load your .srt file
subs = pysrt.open(input_file_path)

# Retrieve the OpenAI API key
openai.api_key = get_api_key()

# Retrieve various configurations
default_translation_language = get_config('Translation', 'DefaultLanguage', "Please enter the default translation language code (e.g., 'es' for Spanish):")
additional_info = get_config('Translation', 'AdditionalInfo', "Enter any additional info for translation context (leave blank if none):", is_int=False)
block_size = get_config('Settings', 'BlockSize', "Please enter the number of subtitles to process at once (e.g., 10):", is_int=True)
model = get_config('Settings', 'Model', "Please enter the model to use (e.g., 'gpt-3.5-turbo-0125'):")
temperature = get_config('Settings', 'Temperature', "Please enter the temperature to use for translation (e.g., 0.3):", is_int=False)
max_tokens = get_config('Settings', 'MaxTokens', "Please enter the max tokens to use for translation (e.g., 1024):", is_int=True)

# Function to translate blocks of subtitles with context-specific information
def translate_block(block):
    combined_text = ' '.join([sub.text for sub in block])
    if additional_info:
        prompt_text = f"{additional_info} Translate this into {default_translation_language}: {combined_text}"
    else:
        prompt_text = f"Translate this into {default_translation_language}: {combined_text}"
    response = openai.Completion.create(
        model=model,
        prompt=prompt_text,
        temperature=float(temperature),
        max_tokens=max_tokens
    )
    return response.choices[0].text.strip().split('  ')  # Assuming double space as a separator for block translations

# Process subtitles in blocks
for i in range(0, len(subs), block_size):
    block = subs[i:i + block_size]
    translated_block = translate_block(block)
    
    # Update the subtitles with their translations
    for j, sub in enumerate(block):
        if j < len(translated_block):
            sub.text = translated_block[j]

# Determine the output file name based on the input
output_file_path = input_file_path.replace('.srt', '_translated.srt')

# Save the translated subtitles
subs.save(output_file_path)

print(f"Translation done!")
print(f"Translated subtitles saved to: {output_file_path}")