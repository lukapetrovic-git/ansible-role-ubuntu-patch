import argparse
import re

arguments = argparse.ArgumentParser()
arguments.add_argument('-p','--apt-history-path', nargs=1, dest='apt_history_path', help='Path to the APT history log file', required=True) #, default='/var/log/apt/history.log')
arguments.add_argument('-u','--upgrade-string', nargs=1, dest='upgrade_string', help='String to filter on to filter upgraded packages', required=True) #, default='Upgrade: ')
arguments = arguments.parse_args()

def get_last_string_occurence(file_path: str, search_string: str) -> str:
  last_occurrence = None
  with open(file_path, 'r') as file:
      for line in file:
          if search_string in line:
              last_occurrence = line.strip()
  return last_occurrence

# not using removeprefix() for python 3.9 compatibility
def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text

upgraded_packages_string = get_last_string_occurence(arguments.apt_history_path[0],arguments.upgrade_string[0])
upgraded_packages_string = remove_prefix(upgraded_packages_string, arguments.upgrade_string[0])

# split the string on commas outside parentheses
upgraded_array = re.split(r',\s*(?![^()]*\))', upgraded_packages_string)

# extract the package name and the upgraded version from the parentheses
upgraded_packages_w_versions = []
for part in upgraded_array:
    match = re.match(r'([^:]+):[^()]+\(([^,]+),\s*([^,]+)\)', part)
    if match:
        package_name = match.group(1).strip()
        version = match.group(3).strip()
        upgraded_packages_w_versions.append(f"{package_name}={version}")

print(upgraded_packages_w_versions)