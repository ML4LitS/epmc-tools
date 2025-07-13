
import json
from xml_processor import XMLProcessor, ordered_labels

def test_xml_processing():
    xml_file_path = '/home/stirunag/work/github/JATX2JSON/test_data/PXD053361.xml'
    
    with open(xml_file_path, 'r', encoding='utf8') as f:
        xml_content = f.read()
        
    processor = XMLProcessor(sentenciser=True)
    
    print("Processing XML file...")
    data_temp = processor.process_full_text(xml_content)
    
    if data_temp:
        print("XML processing successful. Now processing JSON...")
        result = processor.process_json(data_temp, ordered_labels)
        
        if result:
            output_file_path = '/home/stirunag/work/github/JATX2JSON/test_output.json'
            print(f"JSON processing successful. Saving output to {output_file_path}...")
            with open(output_file_path, 'w', encoding='utf8') as f_out:
                json.dump(result, f_out, indent=2)
            print("Output saved successfully.")
        else:
            print("JSON processing failed.")
    else:
        print("XML processing failed.")

if __name__ == "__main__":
    test_xml_processing()
