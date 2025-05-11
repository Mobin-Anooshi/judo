import json
import os
import traceback

def determine_winner(match, next_matches):
    # If the match has only one participant, they are the winner
    if len(match) == 1:
        if isinstance(match[0], dict) and "name" in match[0]:
            return match[0]["name"]
        return None  # If no name key, return None
    
    # If winner key exists, return it
    for entry in match:
        if isinstance(entry, dict) and "winner" in entry:
            return entry["winner"]
    
    # Find participants present in the next rounds
    current_participants = []
    for entry in match:
        if isinstance(entry, dict) and "name" in entry:
            current_participants.append(entry["name"])
        else:
            return None  # If any entry lacks name, return None
    
    for next_match in next_matches:
        for participant in next_match:
            if isinstance(participant, dict) and "name" in participant:
                participant_name = participant["name"]
                if participant_name in current_participants:
                    return participant_name
    
    # If none are in the next rounds, assume the first participant is the winner
    return current_participants[0] if current_participants else None

def process_repechage(repechage_data):
    # Copy data to avoid modifying the original
    repechage = repechage_data.copy()
    
    # Process round 1-4 if it exists
    if "round 1-4" in repechage:
        round_1_4 = repechage["round 1-4"]
        next_matches = round_1_4[4:] if len(round_1_4) > 4 else []
        next_matches += repechage.get("round 1-2", [])
        
        for i, match in enumerate(round_1_4):
            if not any(isinstance(entry, dict) and "winner" in entry for entry in match):
                winner = determine_winner(match, next_matches[i:] if i < len(next_matches) else [])
                if winner:
                    match.append({"winner": winner})
    
    # Process round 1-2
    if "round 1-2" in repechage:
        round_1_2 = repechage["round 1-2"]
        for i, match in enumerate(round_1_2):
            if len(match) > 1:
                next_matches = round_1_2[i+1:] if i+1 < len(round_1_2) else []
                if not any(isinstance(entry, dict) and "winner" in entry for entry in match):
                    winner = determine_winner(match, next_matches)
                    if winner:
                        match.append({"winner": winner})
        
        # Find final winners (two matches before the last two in round 1-2)
        final_winners = []
        if len(round_1_2) >= 4:  # Ensure there are enough matches
            for match in round_1_2[-4:-2]:
                winner = determine_winner(match, round_1_2[-2:])
                if winner:
                    final_winners.append(winner)
        repechage["final_winners"] = final_winners
    
    return repechage

def process_pool_or_semi(round_data):
    # Copy data to avoid modifying the original
    round_data_copy = round_data.copy()
    
    if "round 1-1" in round_data_copy:
        round_1_1 = round_data_copy["round 1-1"]
        if round_1_1 and len(round_1_1) > 0:
            final_winner_entry = round_1_1[-1]
            if (isinstance(final_winner_entry, list) and len(final_winner_entry) > 0 and
                isinstance(final_winner_entry[0], dict) and "name" in final_winner_entry[0]):
                final_winner = final_winner_entry[0]["name"]
                round_data_copy["final_winner"] = final_winner
                round_data_copy["round 1-1"] = round_1_1[:-1]
    
    return round_data_copy

def process_round_structure(round_data):
    # Copy data to avoid modifying the original
    round_data_copy = round_data.copy()
    
    if "round 1-1" in round_data_copy:
        round_1_1 = round_data_copy["round 1-1"]
        if len(round_1_1) == 2:
            # Check if the second match exists and has the expected structure
            if (isinstance(round_1_1[1], list) and len(round_1_1[1]) > 0 and
                isinstance(round_1_1[1][0], dict) and "name" in round_1_1[1][0]):
                winner_name = round_1_1[1][0]["name"]
                round_1_1[0].append({"winner": winner_name})
                round_1_1.pop(1)
                round_data_copy["final_winner"] = winner_name
    
    return round_data_copy

def process_tournament_data(input_json):
    # Copy input data
    output_json = input_json.copy()
    
    # Check JSON structure (POOL/REPECHAGE or ROUND)
    has_pool_structure = any(key.startswith("POOL") or key in ["REPECHAGE", "SEMI-FINALS"] for key in output_json.keys())
    has_round_structure = any(key.startswith("ROUND") for key in output_json.keys())
    
    if has_pool_structure:
        # Process POOL/REPECHAGE structure
        for stage in output_json.keys():
            if stage == "REPECHAGE":
                output_json["REPECHAGE"] = process_repechage(output_json["REPECHAGE"])
            else:
                # For POOLs and SEMI-FINALS
                output_json[stage] = process_pool_or_semi(output_json[stage])
    
    elif has_round_structure:
        # Process ROUND structure
        for round_name in output_json.keys():
            output_json[round_name] = process_round_structure(output_json[round_name])
    
    return output_json

def process_tournament_folder(input_folder, output_folder):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Initialize log data
    log_data = {
        "successful_files": [],
        "failed_files": []
    }
    
    # Traverse all subfolders and files
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.endswith(".json"):
                input_file_path = os.path.join(root, file)
                # Create output path preserving folder structure
                relative_path = os.path.relpath(root, input_folder)
                output_subfolder = os.path.join(output_folder, relative_path)
                if not os.path.exists(output_subfolder):
                    os.makedirs(output_subfolder)
                output_file_path = os.path.join(output_subfolder, f"{file}")
                
                try:
                    with open(input_file_path, 'r', encoding='utf-8') as file:
                        input_data = json.load(file)
                    
                    processed_data = process_tournament_data(input_data)
                    
                    with open(output_file_path, 'w', encoding='utf-8') as file:
                        json.dump(processed_data, file, ensure_ascii=False, indent=4)
                    
                    log_data["successful_files"].append({
                        "input_file": input_file_path,
                        "output_file": output_file_path
                    })
                    print(f"File {input_file_path} processed successfully and saved to {output_file_path}.")
                
                except FileNotFoundError:
                    log_data["failed_files"].append({
                        "file": input_file_path,
                        "error": "File not found",
                        "function": "process_tournament_folder"
                    })
                    print(f"File {input_file_path} not found.")
                except json.JSONDecodeError:
                    log_data["failed_files"].append({
                        "file": input_file_path,
                        "error": "Invalid JSON structure",
                        "function": "process_tournament_folder"
                    })
                    print(f"Error reading file {input_file_path}: Invalid JSON structure.")
                except Exception as e:
                    log_data["failed_files"].append({
                        "file": input_file_path,
                        "error": str(e),
                        "function": traceback.extract_tb(e.__traceback__)[-1].name
                    })
                    print(f"An error occurred while processing {input_file_path}: {str(e)}")
    
    # Save log file
    log_file_path = os.path.join(output_folder, "processing_log.json")
    with open(log_file_path, 'w', encoding='utf-8') as log_file:
        json.dump(log_data, log_file, ensure_ascii=False, indent=4)
    
    print(f"Processing log saved to {log_file_path}.")

# Example usage
if __name__ == "__main__":
    input_folder = "tests"  # Input folder (can be changed)
    output_folder = "BBBBBB"  # Output folder
    process_tournament_folder(input_folder, output_folder)


# import os
# import shutil

# # مسیر پوشه‌ای که می‌خوای داخلش جستجو کنی
# base_path = '/home/mobin/Desktop/mr.abdollahi/tests'  # این رو به مسیر واقعی تغییر بده

# for name in os.listdir(base_path):
#     full_path = os.path.join(base_path, name)
#     if os.path.isdir(full_path) and name.endswith('2019'):
#         print(f"Deleting folder: {full_path}")
#         shutil.rmtree(full_path)