from get_profs_from_umd_directory import GET_PROFS_FROM_UMD_DIR
import json

def get_profs_list(school):
    if school == "UMD":
        umd_prof_finder = GET_PROFS_FROM_UMD_DIR()
        all_info = umd_prof_finder.extract_profs_information()
    
    return all_info

def main():
    all_info = get_profs_list("UMD")
    with open('faculty_data/umd_faculty_data.json', 'w') as json_file:
        json.dump(all_info, json_file, indent=4)

if __name__ == "__main__":
    main()
        