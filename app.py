import subprocess
import re
from flask import Flask, request, jsonify
import json  
import requests
import os
from urllib.parse import urlparse, parse_qs

solidity_file_path = './test_evm_api.sol'
  
app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True)

# Contract Report route
@app.route('/contract_report', methods=['POST'])
def contract_report():
    solidity_file_path = request.args.get('file_path', default='', type=str)
    # return jsonify({
    #     'file_path':solidity_file_path
    # })

    # Download the file
    solidity_file_path = download_file(solidity_file_path)
    if not solidity_file_path:
        return jsonify({'error': 'Failed to download file'}), 500


    if not solidity_file_path:
        return jsonify({'error': 'No file path provided'}), 400

    fileVersion = extract_solc_version(solidity_file_path)
    if fileVersion['status'] is False:
        return jsonify(fileVersion)

    # use version
    fileVersion = fileVersion['version']
    setUpVersion = set_solc_version(fileVersion)

    # if not installed then install new version
    if setUpVersion is None:
        install_solc_version(fileVersion)
        setUpVersion = set_solc_version(fileVersion)
    
    # Run slither 
    output = run_slither(solidity_file_path)
    print( 'Run Slither method =>  ', output )
    return jsonify({
        'status':True,
        'report':output,
        'message':'Successfully get report of file named: ' + solidity_file_path
    })






# Run slither command
def run_slither(file_path):
    """Run Slither on the given Solidity file and print the output."""
    command = f"slither {file_path} "
    try:
        output = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(' Final Report => ', output.stderr)
        return output.stderr
    except subprocess.CalledProcessError as e:
        return e.stderr


# download file through URL
def download_file(url):
    """Download a file from a URL and save it locally."""
    
    try:
        parsed_url = urlparse(url)
        file_name = os.path.basename(parsed_url.path)
        
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(file_name, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return file_name
    except Exception as e:
        print(f"Error downloading file: {e}")
        return None


# Extract file version
def extract_solc_version(file_path):
    """Extract the Solidity version from the pragma directive in the file."""
    command = f"powershell -Command \"(Select-String -Path '{file_path}' -Pattern 'pragma solidity').Line -replace '.*pragma solidity (.*);.*', '$1'\""
    try:
        output = subprocess.check_output(command, shell=True, text=True)
        if len(output) == 1: 
            return {'status':False, 'message':'File not contain pragma version only file with pragma version can process!'}

        solidity_version = output.strip()
        solidity_version = find_compatible_version(solidity_version)
        print( 'Version => ', solidity_version )
        return {
            'status':True, 
            'version': solidity_version
        }
    except Exception as e:
        return {'status':False, 'message':str(e)}




#  Set system solc version 
def set_solc_version(version):
    """Set the Solidity compiler version using solc-select."""
    try:
        subprocess.run(f"solc-select use {version}", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(f"Solidity compiler version set to {version}")
        return True 
    except subprocess.CalledProcessError as e:
        print(f"Error setting Solidity compiler version: {e.stderr}")
        return None
    except Exception as e:
        return False

def install_solc_version(version):
    try:
        subprocess.run(f"solc-select install {version}", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(f"Solidity compiler version ({version}) installed ")
        return True 
    except subprocess.CalledProcessError as e:
        print(f"Error installing Solidity compiler version: {e.stderr}")
        return False
    except Exception as e:
        return False

def  find_compatible_version( version_text ):
    ver = version_text.split('<')
    ver = ver[0].replace('>=', '')
    ver = ver.replace(' ', '')
    return ver

