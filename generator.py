#!/usr/bin/env python3
"""
Secure version of TON assets generator with vulnerability fixes, by Yegor Pimenov
"""
"""
What I add:
Path Traversal (CWE-22)

Original issue: open(file) without path validation
Fix: Added validate_file_path() function with whitelist validation


Unsafe File Operations (CWE-73)

Original issue: Files opened without context managers, no encoding specified
Fix: All file operations now use with statements and explicit UTF-8 encoding


Input Validation (CWE-20)

Original issue: int(parts[0]) and bytearray.fromhex() without error handling
Fix: Comprehensive input validation with try-catch blocks


Base64 Decoding Vulnerabilities (CWE-20)

Original issue: base64.urlsafe_b64decode(a) without size validation
Fix: Added length checks and proper error handling



🟡 Medium Vulnerabilities Fixed:

YAML Bomb Protection (CWE-400)

Fix: Added file size limits (10MB max) and item count limits


Type Confusion (CWE-843)

Fix: Strict type checking for all data structures


Markdown Injection (CWE-79)

Fix: Added sanitize_markdown_string() function to escape special characters


Resource Exhaustion (CWE-400)

Fix: Added limits on string lengths, list sizes, and processing counts



🟢 Security Improvements Added:

Comprehensive logging for security events
Regex-based validation for addresses and URLs
Domain blacklisting for forbidden image sources
Safe error handling that doesn't leak sensitive information
Input sanitization for all external data
Resource limits to prevent DoS attacks
"""
import json
import yaml
import glob
import base64
import os
import logging
import re
from pathlib import Path
from typing import List, Dict, Any, Union, Optional

# Logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Safe import
try:
    from dexes import __get_stonfi_assets, __get_megaton_assets, __get_dedust_assets
except ImportError as e:
    logger.error(f"Failed to import dexes module: {e}")
    raise

# Constants
EXPLORER_JETTONS = "https://tonviewer.com/"
EXPLORER_ACCOUNTS = "https://tonviewer.com/"
EXPLORER_COLLECTIONS = "https://tonviewer.com/"
DEXES_FILE_NAME = "imported_from_dex.yaml"

# Security limits
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
MAX_ITEMS_COUNT = 50000
MAX_STRING_LENGTH = 1000
MAX_LIST_LENGTH = 100

# Allowed keys for jettons
ALLOWED_KEYS = {'symbol', 'name', 'address', 'description', 'image', 'social', 'websites', 'decimals', 'coinmarketcap', 'coingecko'}

# Validation patterns
ADDRESS_HEX_PATTERN = re.compile(r'^-?[0-9]+:[a-fA-F0-9]{64}$')
ADDRESS_BASE64_PATTERN = re.compile(r'^[A-Za-z0-9_-]{48}$')
URL_PATTERN = re.compile(r'^https?://[^\s<>"{}|\\^`\[\]]+$')
SAFE_STRING_PATTERN = re.compile(r'^[a-zA-Z0-9\s\-_.,:;!()\[\]&@#$%+=*/]+$')

# Forbidden domains
FORBIDDEN_DOMAINS = ['cache.tonapi.io']


class SecurityError(Exception):
    """Security-related exception"""
    pass


class ValidationError(Exception):
    """Data validation exception"""
    pass


def validate_file_path(filepath: str, allowed_dirs: List[str]) -> str:
    """Validate file path to prevent path traversal attacks"""
    try:
        # Normalize path
        normalized_path = os.path.normpath(filepath)
        
        # Check for dangerous sequences
        if '..' in normalized_path or normalized_path.startswith('/'):
            raise SecurityError(f"Dangerous path detected: {filepath}")
        
        # Get real path
        if os.path.exists(normalized_path):
            real_path = os.path.realpath(normalized_path)
        else:
            real_path = os.path.realpath(normalized_path)
        
        # Check if file is in allowed directory
        current_dir = os.path.realpath('.')
        for allowed_dir in allowed_dirs:
            allowed_path = os.path.realpath(os.path.join(current_dir, allowed_dir))
            if real_path.startswith(allowed_path):
                return normalized_path
        
        raise SecurityError(f"File '{filepath}' is outside allowed directories")
        
    except Exception as e:
        if isinstance(e, SecurityError):
            raise
        raise SecurityError(f"Path validation failed for '{filepath}': {e}")


def safe_load_yaml(filepath: str) -> Union[List, Dict, None]:
    """Safe YAML file loading with validation"""
    validated_path = validate_file_path(filepath, ['jettons', 'accounts', 'collections', '.'])
    
    try:
        # Check file size
        if os.path.exists(validated_path):
            file_size = os.path.getsize(validated_path)
            if file_size > MAX_FILE_SIZE:
                raise SecurityError(f"File '{filepath}' too large: {file_size} bytes")
        
        with open(validated_path, 'r', encoding='utf-8') as f:
            content = yaml.safe_load(f)
        
        # Validate structure
        if content is not None and not isinstance(content, (list, dict)):
            raise ValidationError(f"Invalid YAML structure in '{filepath}'")
        
        return content or []
        
    except yaml.YAMLError as e:
        raise ValidationError(f"YAML parsing error in '{filepath}': {e}")
    except (IOError, OSError) as e:
        raise ValidationError(f"File reading error '{filepath}': {e}")


def safe_write_json(filepath: str, data: Any) -> None:
    """Safe JSON file writing"""
    if isinstance(data, list) and len(data) > MAX_ITEMS_COUNT:
        raise SecurityError(f"Too many items to write: {len(data)}")
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, sort_keys=True, ensure_ascii=False)
        logger.info(f"Successfully wrote {filepath}")
    except (IOError, OSError) as e:
        raise ValidationError(f"Cannot write file '{filepath}': {e}")


def safe_write_yaml(filepath: str, data: Any) -> None:
    """Safe YAML file writing"""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=True)
        logger.info(f"Successfully wrote {filepath}")
    except (IOError, OSError) as e:
        raise ValidationError(f"Cannot write file '{filepath}': {e}")


def validate_string_field(value: Any, field_name: str, max_length: int = MAX_STRING_LENGTH) -> str:
    """Validate string field"""
    if not isinstance(value, str):
        raise ValidationError(f"Field '{field_name}' must be a string, got {type(value).__name__}")
    
    if len(value) > max_length:
        raise ValidationError(f"Field '{field_name}' too long: {len(value)} characters")
    
    # Check for dangerous characters
    if field_name in ['address', 'symbol'] and any(ord(char) < 32 for char in value):
        raise ValidationError(f"Field '{field_name}' contains control characters")
    
    return value.strip()


def validate_url(url: str) -> str:
    """Validate URL format and security"""
    if not isinstance(url, str):
        raise ValidationError("URL must be a string")
    
    url = url.strip()
    if not URL_PATTERN.match(url):
        raise ValidationError(f"Invalid URL format: {url}")
    
    # Check for forbidden domains
    for domain in FORBIDDEN_DOMAINS:
        if domain in url.lower():
            raise ValidationError(f"Forbidden domain in URL: {domain}")
    
    return url


def normalize_address(address: str, to_raw: bool) -> str:
    """Safe address normalization with validation"""
    if not isinstance(address, str):
        raise ValidationError("Address must be a string")
    
    address = address.strip()
    if not address:
        raise ValidationError("Address cannot be empty")
    
    try:
        if len(address) == 48 and ADDRESS_BASE64_PATTERN.match(address):
            # Base64 format
            try:
                raw = base64.urlsafe_b64decode(address + '==')  # Add padding
            except Exception as e:
                raise ValidationError(f"Invalid base64 address: {e}")
            
            if len(raw) < 34:
                raise ValidationError("Invalid base64 address length")
            
            workchain = raw[1]
            if workchain == 255:
                workchain = -1
            elif workchain > 127:
                workchain = workchain - 256
                
            addr = raw[2:34]
            
        elif ":" in address and ADDRESS_HEX_PATTERN.match(address):
            # Hex format
            parts = address.split(":")
            if len(parts) != 2:
                raise ValidationError(f"Invalid address format: {address}")
            
            try:
                workchain = int(parts[0])
                if workchain < -128 or workchain > 127:
                    raise ValidationError(f"Invalid workchain: {workchain}")
            except ValueError:
                raise ValidationError(f"Invalid workchain in address: {parts[0]}")
            
            try:
                addr = bytearray.fromhex(parts[1])
                if len(addr) != 32:
                    raise ValidationError("Address must be 32 bytes")
            except ValueError:
                raise ValidationError(f"Invalid hex in address: {parts[1]}")
                
        else:
            raise ValidationError(f"Invalid address format: {address}")
        
        # Return normalized address
        if to_raw:
            return f"{workchain}:{addr.hex()}"
        
        # Convert to base64
        if workchain == -1:
            workchain = 255
        
        human = bytearray(36)
        human[0] = 0x11
        human[1] = workchain & 0xFF
        human[2:34] = addr
        crc = crc16(human[:34])
        human[34:36] = crc
        
        return base64.urlsafe_b64encode(human).decode().rstrip('=')
        
    except ValidationError:
        raise
    except Exception as e:
        raise ValidationError(f"Address normalization failed: {e}")


def crc16(data: bytes) -> bytes:
    """Calculate CRC16 for address"""
    POLY = 0x1021
    reg = 0
    message = bytes(data) + bytes(2)

    for byte in message:
        mask = 0x80
        while mask > 0:
            reg <<= 1
            if byte & mask:
                reg += 1
            mask >>= 1
            if reg > 0xffff:
                reg &= 0xffff
                reg ^= POLY
    
    return bytes([reg // 256, reg % 256])


def validate_jetton(jetton: Dict[str, Any]) -> None:
    """Validate jetton data"""
    if not isinstance(jetton, dict):
        raise ValidationError("Jetton must be a dictionary")
    
    # Check for invalid keys
    invalid_keys = set(jetton.keys()) - ALLOWED_KEYS
    if invalid_keys:
        raise ValidationError(f"Invalid keys {invalid_keys} in jetton {jetton.get('name', 'unknown')}")
    
    # Check required fields
    required_fields = {'name', 'symbol', 'address'}
    missing_fields = required_fields - set(jetton.keys())
    if missing_fields:
        raise ValidationError(f"Missing required fields {missing_fields} in jetton {jetton.get('name', 'unknown')}")
    
    # Validate string fields
    for field in ['symbol', 'name', 'address', 'description', 'coinmarketcap', 'coingecko']:
        if field in jetton:
            jetton[field] = validate_string_field(jetton[field], field)
    
    # Validate URL fields
    if 'image' in jetton:
        jetton['image'] = validate_url(jetton['image'])
    
    # Validate URL lists
    for field in ['social', 'websites']:
        if field in jetton:
            if not isinstance(jetton[field], list):
                raise ValidationError(f"Field '{field}' must be a list in jetton {jetton['name']}")
            
            if len(jetton[field]) > MAX_LIST_LENGTH:
                raise ValidationError(f"Too many items in '{field}' for jetton {jetton['name']}")
            
            validated_urls = []
            for url in jetton[field]:
                validated_urls.append(validate_url(url))
            jetton[field] = validated_urls
    
    # Validate decimals
    if 'decimals' in jetton:
        try:
            decimals = int(jetton['decimals'])
            if decimals < 0 or decimals > 30:
                raise ValidationError(f"Invalid decimals value: {decimals}")
            jetton['decimals'] = decimals
        except (ValueError, TypeError):
            raise ValidationError(f"Decimals must be an integer in jetton {jetton['name']}")


def sanitize_markdown_string(text: str) -> str:
    """Sanitize string for safe Markdown output"""
    if not isinstance(text, str):
        return str(text)
    
    # Remove or escape potentially dangerous characters
    text = text.replace('[', '\\[').replace(']', '\\]')
    text = text.replace('(', '\\(').replace(')', '\\)')
    text = text.replace('|', '\\|')
    
    return text


def collect_all_dexes():
    """Collect assets from DEXes with security validation"""
    logger.info("Starting DEX asset collection")
    
    try:
        # Load existing jettons
        temp = []
        jetton_files = glob.glob("jettons/*.yaml")
        
        # Validate glob results
        validated_files = []
        for file in jetton_files:
            try:
                validated_path = validate_file_path(file, ['jettons'])
                if not file.endswith(DEXES_FILE_NAME):
                    validated_files.append(validated_path)
            except SecurityError as e:
                logger.warning(f"Skipping suspicious file {file}: {e}")
                continue
        
        for file in sorted(validated_files):
            try:
                content = safe_load_yaml(file)
                if content:
                    temp.append(content)
            except (ValidationError, SecurityError) as e:
                logger.error(f"Error loading {file}: {e}")
                continue
        
        # Process jettons
        jettons = []
        for item in temp:
            if isinstance(item, list):
                jettons.extend(item)
            elif isinstance(item, dict):
                jettons.append(item)
        
        # Build existing addresses set
        existing_addresses = set()
        for jetton in jettons:
            try:
                normalized_addr = normalize_address(jetton["address"], True)
                existing_addresses.add(normalized_addr)
            except (ValidationError, KeyError) as e:
                logger.warning(f"Invalid jetton address: {e}")
                continue
        
        # Get DEX assets
        try:
            assets = __get_dedust_assets() + __get_stonfi_assets() + __get_megaton_assets()
        except Exception as e:
            logger.error(f"Failed to get DEX assets: {e}")
            return
        
        # Process new assets
        new_assets = {}
        for asset in assets:
            try:
                normalized_addr = normalize_address(asset.address, True)
                if normalized_addr not in existing_addresses:
                    new_assets[normalized_addr] = {
                        'name': validate_string_field(asset.name, 'name'),
                        'address': normalized_addr,
                        'symbol': validate_string_field(asset.symbol, 'symbol')
                    }
            except (ValidationError, AttributeError) as e:
                logger.warning(f"Invalid DEX asset: {e}")
                continue
        
        # Save new assets
        if new_assets:
            sorted_assets = sorted(new_assets.values(), key=lambda x: x['symbol'])
            safe_write_yaml(f"jettons/{DEXES_FILE_NAME}", sorted_assets)
            logger.info(f"Saved {len(new_assets)} new DEX assets")
        else:
            logger.info("No new DEX assets found")
            
    except Exception as e:
        logger.error(f"Error in collect_all_dexes: {e}")
        raise


def merge_jettons():
    """Merge and validate all jetton files"""
    logger.info("Starting jetton merge")
    
    try:
        # Load all jetton files
        jetton_files = glob.glob("jettons/*.yaml")
        validated_files = []
        
        for file in jetton_files:
            try:
                validated_path = validate_file_path(file, ['jettons'])
                validated_files.append(validated_path)
            except SecurityError as e:
                logger.warning(f"Skipping suspicious file {file}: {e}")
                continue
        
        all_jettons = []
        for file in sorted(validated_files):
            try:
                content = safe_load_yaml(file)
                if isinstance(content, list):
                    all_jettons.extend(content)
                elif isinstance(content, dict):
                    all_jettons.append(content)
            except (ValidationError, SecurityError) as e:
                logger.error(f"Error loading {file}: {e}")
                continue
        
        # Validate and normalize jettons
        processed_jettons = []
        seen_addresses = {}
        
        for jetton in all_jettons:
            try:
                validate_jetton(jetton)
                
                # Normalize address
                jetton["address"] = normalize_address(jetton["address"], True)
                
                # Check for duplicates
                if jetton["address"] in seen_addresses:
                    logger.warning(f"Duplicate address: {jetton['name']} and {seen_addresses[jetton['address']]}")
                    continue
                
                seen_addresses[jetton["address"]] = jetton["name"]
                processed_jettons.append(jetton)
                
            except ValidationError as e:
                logger.error(f"Invalid jetton: {e}")
                continue
        
        # Sort and save
        processed_jettons.sort(key=lambda x: x.get('symbol', '').lower())
        safe_write_json('jettons.json', processed_jettons)
        
        logger.info(f"Processed {len(processed_jettons)} jettons")
        return [(j.get('name', 'unknown'), j.get('address', 'unknown')) for j in processed_jettons]
        
    except Exception as e:
        logger.error(f"Error in merge_jettons: {e}")
        raise


def merge_accounts():
    """Merge and validate account files"""
    logger.info("Starting account merge")
    
    try:
        # Main page accounts
        main_page = []
        main_files = ['accounts/infrastructure.yaml', 'accounts/defi.yaml', 'accounts/celebrities.yaml']
        
        all_accounts = []
        
        # Process main files
        for file in main_files:
            try:
                if os.path.exists(file):
                    accounts = safe_load_yaml(file)
                    if isinstance(accounts, list):
                        main_page.extend([(acc.get('name', 'unknown'), acc.get('address', 'unknown')) for acc in accounts])
                        all_accounts.extend(accounts)
            except (ValidationError, SecurityError) as e:
                logger.error(f"Error loading {file}: {e}")
                continue
        
        # Process other account files
        other_files = ['accounts/givers.yaml', 'accounts/custodians.yaml', 'accounts/bridges.yaml', 
                      'accounts/validators.yaml', 'accounts/scammers.yaml', 'accounts/notcoin.yaml', 'accounts/dapps.yaml']
        
        for file in other_files:
            try:
                if os.path.exists(file):
                    accounts = safe_load_yaml(file)
                    if isinstance(accounts, list):
                        all_accounts.extend(accounts)
            except (ValidationError, SecurityError) as e:
                logger.error(f"Error loading {file}: {e}")
                continue
        
        # Validate and normalize accounts
        processed_accounts = []
        for account in all_accounts:
            try:
                if not isinstance(account, dict):
                    continue
                
                if 'address' in account:
                    account['address'] = normalize_address(account['address'], True)
                
                if 'name' in account:
                    account['name'] = validate_string_field(account['name'], 'name')
                
                processed_accounts.append(account)
                
            except ValidationError as e:
                logger.warning(f"Invalid account: {e}")
                continue
        
        # Save accounts
        safe_write_json('accounts.json', processed_accounts)
        
        logger.info(f"Processed {len(processed_accounts)} accounts")
        return main_page
        
    except Exception as e:
        logger.error(f"Error in merge_accounts: {e}")
        raise


def merge_collections():
    """Merge and validate collection files"""
    logger.info("Starting collection merge")
    
    try:
        collection_files = glob.glob("collections/*.yaml")
        validated_files = []
        
        for file in collection_files:
            try:
                validated_path = validate_file_path(file, ['collections'])
                validated_files.append(validated_path)
            except SecurityError as e:
                logger.warning(f"Skipping suspicious file {file}: {e}")
                continue
        
        all_collections = []
        for file in sorted(validated_files):
            try:
                content = safe_load_yaml(file)
                if isinstance(content, list):
                    all_collections.extend(content)
                elif isinstance(content, dict):
                    all_collections.append(content)
            except (ValidationError, SecurityError) as e:
                logger.error(f"Error loading {file}: {e}")
                continue
        
        # Validate and normalize collections
        processed_collections = []
        for collection in all_collections:
            try:
                if not isinstance(collection, dict):
                    continue
                
                if 'address' in collection:
                    collection['address'] = normalize_address(collection['address'], True)
                
                if 'name' in collection:
                    collection['name'] = validate_string_field(collection['name'], 'name')
                
                processed_collections.append(collection)
                
            except ValidationError as e:
                logger.warning(f"Invalid collection: {e}")
                continue
        
        # Save collections
        safe_write_json('collections.json', processed_collections)
        
        logger.info(f"Processed {len(processed_collections)} collections")
        return [(c.get('name', 'unknown'), c.get('address', 'unknown')) for c in processed_collections]
        
    except Exception as e:
        logger.error(f"Error in merge_collections: {e}")
        raise


def generate_readme(accounts: List[tuple], collections: List[tuple]) -> None:
    """Generate README.md with sanitized content"""
    logger.info("Generating README.md")
    
    try:
        # Read template safely
        template_path = validate_file_path("readme.md.template", ['.'])
        
        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()
        
        # Generate account links with sanitization
        accounts_md = []
        for name, address in accounts:
            safe_name = sanitize_markdown_string(name)
            try:
                safe_address_user = normalize_address(address, False)
                safe_address_raw = normalize_address(address, True)
                link = f"[{safe_name}]({EXPLORER_ACCOUNTS}{safe_address_user}) | {safe_address_raw}"
                accounts_md.append(link)
            except ValidationError as e:
                logger.warning(f"Invalid account address for {name}: {e}")
                continue
        
        # Generate collection links with sanitization
        collections_md = []
        for name, address in collections:
            safe_name = sanitize_markdown_string(name)
            try:
                safe_address_user = normalize_address(address, False)
                safe_address_raw = normalize_address(address, True)
                link = f"[{safe_name}]({EXPLORER_COLLECTIONS}{safe_address_user}) | {safe_address_raw}"
                collections_md.append(link)
            except ValidationError as e:
                logger.warning(f"Invalid collection address for {name}: {e}")
                continue
        
        # Fill template
        readme_content = template % ('\n'.join(accounts_md), '\n'.join(collections_md))
        
        # Write README
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        logger.info("README.md generated successfully")
        
    except Exception as e:
        logger.error(f"Error generating README: {e}")
        raise


def main():
    """Main function with comprehensive error handling"""
    logger.info("Starting secure TON asset processing")
    
    try:
        # Check for YAML files in root
        root_yaml_files = glob.glob("*.yaml")
        if root_yaml_files:
            raise SecurityError("YAML files found in root directory. Please move to jettons/ or collections/")
        
        # Process all asset types
        collect_all_dexes()
        jettons = merge_jettons()
        collections = merge_collections()
        accounts = merge_accounts()
        
        # Generate README
        generate_readme(accounts, collections)
        
        logger.info("Processing completed successfully")
        logger.info(f"Total processed: {len(jettons)} jettons, {len(accounts)} accounts, {len(collections)} collections")
        
    except (SecurityError, ValidationError) as e:
        logger.error(f"Processing failed: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise


if __name__ == '__main__':
    main()
