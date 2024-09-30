import argparse
import json
import os
import time
from googletrans import Translator  # Ensure googletrans is installed
from termcolor import colored  # Ensure termcolor is installed
import re

# Load the replacement dictionary from replace.json
def load_replacement_dict(replace_file='replace.json'):
    if os.path.exists(replace_file):
        with open(replace_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

# Function to replace words based on the replacement dictionary
def custom_replace(text, replacement_dict):
    for key, value in replacement_dict.items():
        text = text.replace(key, value)
    return text

# Display the welcome banner
def display_welcome():
    welcome_text = """
    ███╗░░██╗░██████╗███████╗
    ████╗░██║██╔════╝██╔════╝
    ██╔██╗██║╚█████╗░█████╗░░
    ██║╚████║░╚═══██╗██╔══╝░░
    ██║░╚███║██████╔╝██║░░░░░
    ╚═╝░░╚══╝╚═════╝░╚═╝░░░░░
    RPG MAKER MV TRANSLATOR
    """
    print(colored(welcome_text, "green"))

# Display translation progress
def display_progress(file_name, current, total):
    print(f"Translating file: {file_name} ({current}/{total})")

# Clean invisible characters
def clean_text(text):
    return text.replace("\u200b", "").strip() if text else text

# Extract translatable text while skipping \HURUF[ANGKA] patterns like \c[8] or \n[1]
def extract_translatable_text(text):
    # Use regex to capture escape sequences and other parts
    parts = re.split(r'(\\[A-Za-z]+\[\d+\])', text)  # Adjusted to capture sequences like \c[8] or \n[1]
    return parts

# Improved text wrapping for dialog boxes
def wrap_text(text, max_len):
    words = text.split()
    lines = []
    line = ""
    
    for word in words:
        if len(line) + len(word) + 1 > max_len:
            lines.append(line)
            line = word
        else:
            line += " " + word if line else word
    
    if line:
        lines.append(line)
    
    return "\n".join(lines)

# Translate a sentence, skipping \HURUF[ANGKA] patterns
def translate_sentence(tr, text, replacement_dict, dst='en', verbose=False, max_retries=10, retry_delay=3):
    if text is None:
        with open('failed_translations.log', 'a') as log_file:
            log_file.write(f"Skipped None text\n")
        return text

    text = clean_text(text)
    parts = extract_translatable_text(text)
    translated_parts = []
    
    for part in parts:
        # Skip any part matching \HURUF[ANGKA], e.g. \C[1], \N[123]
        if re.match(r'(\\[A-Za-z]+\[\d+\])', part):
            translated_parts.append(part)  # Skip these parts without translation
        else:
            for attempt in range(max_retries):
                try:
                    if part.strip():
                        print(colored(f"+ {part}", "blue"))
                        translation = tr.translate(part, dest=dst).text
                        translated_text = custom_replace(translation, replacement_dict)
                        print(colored(f"= {translated_text}", "green"))
                        translated_parts.append(translated_text)
                    else:
                        translated_parts.append(part)
                    break
                except Exception as e:
                    time.sleep(retry_delay)
                    if verbose:
                        print(f"Attempt {attempt + 1} failed: {e}")
            else:
                with open('failed_translations.log', 'a') as log_file:
                    log_file.write(f"Failed to translate: {part}\n")
                translated_parts.append(part)

    return ''.join(translated_parts)

# File translation logic with error logging
def translate_file(file_path, tr, replacement_dict, dst='en', verbose=False, max_len=40):
    with open(file_path, 'r', encoding='utf-8-sig') as datafile:
        data = json.load(datafile)

    def translate_text(text):
        translated = translate_sentence(tr, text, replacement_dict, dst=dst, verbose=verbose)
        if translated:
            return wrap_text(translated, max_len)
        return text

    total_translated = 0

    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict) and 'list' in item:
                for command in item['list']:
                    if command['code'] == 401:
                        command['parameters'][0] = translate_text(command['parameters'][0])
                        total_translated += 1

    elif isinstance(data, dict) and "events" in data:
        for event in data['events']:
            if event is not None and 'pages' in event:
                for page in event['pages']:
                    if page is not None and 'list' in page:
                        for command in page['list']:
                            if command['code'] == 401:
                                command['parameters'][0] = translate_text(command['parameters'][0])
                                total_translated += 1

    return data, total_translated

# Main function
def main(input_folder, dst_lang, verbose=False, max_len=40):
    tr = Translator()
    replacement_dict = load_replacement_dict()
    translated_files = 0
    total_strings = 0
    dest_folder = input_folder + '_' + dst_lang

    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    files = [f for f in os.listdir(input_folder) if f.endswith('.json')]
    total_files = len(files)

    for index, file in enumerate(files):
        file_path = os.path.join(input_folder, file)
        start_time = time.time()

        print(f"Translating : {file_path} ({index+1}/{total_files})")
        
        translated_data, translated_strings = translate_file(file_path, tr, replacement_dict, dst=dst_lang, verbose=verbose, max_len=max_len)

        end_time = time.time()
        time_taken = end_time - start_time
        percentage_complete = ((index + 1) / total_files) * 100

        new_file = os.path.join(dest_folder, file)
        with open(new_file, 'w', encoding='utf-8') as f:
            json.dump(translated_data, f, indent=4, ensure_ascii=False)

        print(colored(f"Completed-{file}. (Time: {time_taken:.2f} seconds)", "green"))
        print(colored(f"Total translated strings in this file: {translated_strings}", "blue"))
        
        display_progress(file, index + 1, total_files)
        print(f"Progress: {percentage_complete:.2f}%\n")

        translated_files += 1
        total_strings += translated_strings

    print(colored(f"\nTranslation complete! {translated_files} files and {total_strings} strings translated.", "green"))

# Command-line arguments setup
if __name__ == '__main__':
    display_welcome()

    ap = argparse.ArgumentParser(description="NSF Translation Tool")
    ap.add_argument("-dl", "--dest_lang", type=str, required=True, help="Destination language for translation")
    ap.add_argument("-m", "--max_len", type=int, default=40, help="Maximum length of text lines (default: 40)")
    ap.add_argument("-v", "--verbose", action="store_true", default=False, help="Increase output verbosity")

    args = ap.parse_args()
    main(input_folder="dialogs", dst_lang=args.dest_lang, verbose=args.verbose, max_len=args.max_len)
