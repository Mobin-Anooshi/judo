import json
import os
import traceback

def determine_winner(match, next_matches):
    if len(match) == 1:
        if isinstance(match[0], dict) and "name" in match[0]:
            return match[0]["name"]
        return None
    for entry in match:
        if isinstance(entry, dict) and "winner" in entry:
            return entry["winner"]
    current_participants = [entry["name"] for entry in match if isinstance(entry, dict) and "name" in entry]
    if not current_participants:
        return None
    for next_match in next_matches:
        for participant in next_match:
            if isinstance(participant, dict) and "name" in participant:
                if participant["name"] in current_participants:
                    return participant["name"]
    return current_participants[0] if current_participants else None

def process_repechage(repechage_data):
    repechage = repechage_data.copy()
    for round_name, matches in list(repechage.items()):
        if round_name.startswith("round"):
            if not isinstance(matches, list):
                continue
            for i, match in enumerate(matches):
                if len(match) > 1:
                    next_matches = matches[i+1:] if i+1 < len(matches) else []
                    if not any(isinstance(entry, dict) and "winner" in entry for entry in match):
                        winner = determine_winner(match, next_matches)
                        if winner:
                            match.append({"winner": winner})
            final_winners = []
            if len(matches) >= 2:
                last_match = matches[-1]
                if len(last_match) == 1 and isinstance(last_match[0], dict) and "name" in last_match[0]:
                    final_winners.append(last_match[0]["name"])
            repechage["final_winners"] = final_winners if final_winners else []
    return repechage

def process_pool_or_semi(round_data):
    round_data_copy = round_data.copy()
    for round_name, matches in list(round_data_copy.items()):
        if round_name.startswith("round"):
            if not isinstance(matches, list):
                continue
            for i, match in enumerate(matches):
                if len(match) > 1:
                    next_matches = matches[i+1:] if i+1 < len(matches) else []
                    if not any(isinstance(entry, dict) and "winner" in entry for entry in match):
                        winner = determine_winner(match, next_matches)
                        if winner:
                            match.append({"winner": winner})
            final_winners = []
            if len(matches) >= 2:
                last_matches = matches[-2:] if len(matches) >= 2 else matches
                for match in last_matches:
                    if isinstance(match, list) and len(match) == 1 and isinstance(match[0], dict) and "name" in match[0]:
                        final_winners.append(match[0]["name"])
                    elif isinstance(match, list) and len(match) > 1 and any(isinstance(entry, dict) and "winner" in entry for entry in match):
                        for entry in match:
                            if isinstance(entry, dict) and "winner" in entry:
                                final_winners.append(entry["winner"])
            if final_winners:
                round_data_copy["final_winners"] = list(dict.fromkeys(final_winners))
                round_data_copy[round_name] = matches[:-len(final_winners)] if len(final_winners) <= len(matches) else []
    return round_data_copy

def process_round_structure(round_data):
    round_data_copy = round_data.copy()
    if "round 1-1" in round_data_copy:
        round_1_1 = round_data_copy["round 1-1"]
        if len(round_1_1) == 2:
            if (isinstance(round_1_1[1], list) and len(round_1_1[1]) > 0 and
                isinstance(round_1_1[1][0], dict) and "name" in round_1_1[1][0]):
                winner_name = round_1_1[1][0]["name"]
                round_1_1[0].append({"winner": winner_name})
                round_1_1.pop(1)
                round_data_copy["final_winner"] = winner_name
    return round_data_copy

def process_tournament_data(input_json):
    output_json = input_json.copy()
    has_pool_structure = any(key.startswith("POOL") or key in ["REPECHAGE", "SEMI-FINALS", "FINALS"] for key in output_json.keys())
    has_round_structure = any(key.startswith("ROUND") for key in output_json.keys())
    if has_pool_structure:
        for stage in list(output_json.keys()):
            if stage == "REPECHAGE":
                output_json["REPECHAGE"] = process_repechage(output_json["REPECHAGE"])
            else:
                output_json[stage] = process_pool_or_semi(output_json[stage])
    elif has_round_structure:
        for round_name in list(output_json.keys()):
            output_json[round_name] = process_round_structure(output_json[round_name])
    return output_json

def process_tournament_folder(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    log_data = {"successful_files": [], "failed_files": []}
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.endswith(".json"):
                input_file_path = os.path.join(root, file)
                relative_path = os.path.relpath(root, input_folder)
                output_subfolder = os.path.join(output_folder, relative_path)
                if not os.path.exists(output_subfolder):
                    os.makedirs(output_subfolder)
                output_file_path = os.path.join(output_subfolder, f"processed_{file}")
                try:
                    with open(input_file_path, 'r', encoding='utf-8') as file:
                        input_data = json.load(file)
                    processed_data = process_tournament_data(input_data)
                    with open(output_file_path, 'w', encoding='utf-8') as file:
                        json.dump(processed_data, file, ensure_ascii=False, indent=4)
                    log_data["successful_files"].append({"input_file": input_file_path, "output_file": output_file_path})
                    print(f"File {input_file_path} processed successfully and saved to {output_file_path}.")
                except FileNotFoundError:
                    log_data["failed_files"].append({"file": input_file_path, "error": "File not found", "function": "process_tournament_folder"})
                    print(f"File {input_file_path} not found.")
                except json.JSONDecodeError:
                    log_data["failed_files"].append({"file": input_file_path, "error": "Invalid JSON structure", "function": "process_tournament_folder"})
                    print(f"Error reading file {input_file_path}: Invalid JSON structure.")
                except Exception as e:
                    log_data["failed_files"].append({"file": input_file_path, "error": str(e), "function": traceback.extract_tb(e.__traceback__)[-1].name})
                    print(f"An error occurred while processing {input_file_path}: {str(e)}")
    log_file_path = os.path.join(output_folder, "processing_log.json")
    with open(log_file_path, 'w', encoding='utf-8') as log_file:
        json.dump(log_data, log_file, ensure_ascii=False, indent=4)
    print(f"Processing log saved to {log_file_path}.")

if __name__ == "__main__":
    input_folder = "test"
    output_folder = "export-test-3"
    process_tournament_folder(input_folder, output_folder)