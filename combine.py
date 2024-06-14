import xml.etree.ElementTree as ET
import sys
import os

def collate_xml_reports(xml_files):
    # Initialize the aggregate data
    total_tests = 0
    total_failures = 0
    total_disabled = 0
    total_errors = 0
    total_time = 0.0
    timestamp = ''

    # Create the root element for the combined XML
    combined_testsuites = ET.Element('testsuites')

    for xml_file in xml_files:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        # Sum up the attributes in the testsuites tag
        total_tests += int(root.attrib.get('tests', 0))
        total_failures += int(root.attrib.get('failures', 0))
        total_errors += int(root.attrib.get('errors', 0))
        total_time += float(root.attrib.get('time', 0.0))
        timestamp = str(root.attrib.get('timestamp', ''))

        # Append each testsuite to the combined testsuites
        for testsuite in root.findall('testsuite'):
            combined_testsuites.append(testsuite)

    # Set the summed attributes on the combined testsuites element
    combined_testsuites.set('tests', str(total_tests))
    combined_testsuites.set('failures', str(total_failures))
    combined_testsuites.set('errors', str(total_errors))
    combined_testsuites.set('time', str(total_time))
    combined_testsuites.set('disabled', str(total_disabled))
    combined_testsuites.set('timestamp', timestamp)  # Just uses whatever the final timestamp was
    combined_testsuites.set('name', 'AllTests')  # General name

    # Create the combined XML tree and write to a file
    combined_tree = ET.ElementTree(combined_testsuites)
    combined_tree.write('combined_report.xml', encoding='utf-8', xml_declaration=True)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 combine.py <xml_file1> <xml_file2> ... <xml_filen>")
        sys.exit(1)

    xml_files = sys.argv[1:]

    # Check if all provided files exist
    for xml_file in xml_files:
        if not os.path.isfile(xml_file):
            print(f"Error: File {xml_file} does not exist.")
            sys.exit(1)

    collate_xml_reports(xml_files)
    print("Collation complete. Output written to 'combined_report.xml'")