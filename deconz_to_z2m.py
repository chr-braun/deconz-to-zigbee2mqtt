
#!/usr/bin/env python3
"""
deCONZ to Zigbee2MQTT Migration Tool

This tool facilitates the migration of devices and configurations from deCONZ 
to Zigbee2MQTT by extracting network parameters and device information from 
the deCONZ database and generating a valid configuration.yaml file.
"""

import os
import sqlite3
import yaml
import random
import logging
import re
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple, Union

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)


class DeconzMigrationError(Exception):
    """Custom exception for deCONZ migration errors."""
    pass


class DeconzToZ2MMigrator:
    """Main class for handling deCONZ to Zigbee2MQTT migration."""
    
    DEFAULT_DB_PATH = Path.home() / ".local/share/deCONZ/zll.db"
    VALID_CHANNELS = range(11, 27)  # Zigbee channels 11-26
    
    def __init__(self):
        """Initialize the migrator."""
        self.db_path: Optional[Path] = None
        self.devices: List[Tuple[Any, ...]] = []
        
    def find_database(self) -> Path:
        """
        Find the deCONZ database file.
        
        Returns:
            Path: Path to the deCONZ database file
            
        Raises:
            DeconzMigrationError: If database file cannot be found
        """
        if self.DEFAULT_DB_PATH.exists():
            logger.info(f"Found deCONZ database at default location: {self.DEFAULT_DB_PATH}")
            return self.DEFAULT_DB_PATH
            
        while True:
            try:
                path_input = input("Enter path to zll.db: ").strip()
                if not path_input:
                    continue
                    
                db_path = Path(path_input)
                if db_path.exists() and db_path.is_file():
                    logger.info(f"Database found at: {db_path}")
                    return db_path
                else:
                    logger.error(f"File not found: {db_path}")
                    
            except KeyboardInterrupt:
                logger.info("Operation cancelled by user")
                raise DeconzMigrationError("Database location input cancelled")
    
    def validate_hex_string(self, hex_str: str, expected_length: int) -> bool:
        """
        Validate a hexadecimal string.
        
        Args:
            hex_str: The hex string to validate
            expected_length: Expected length in characters
            
        Returns:
            bool: True if valid, False otherwise
        """
        # Remove 0x prefix if present
        clean_hex = hex_str.lower().replace('0x', '')
        
        # Check length and format
        if len(clean_hex) != expected_length:
            return False
            
        return bool(re.match(r'^[0-9a-f]+$', clean_hex))
    
    def validate_channel(self, channel_str: str) -> bool:
        """
        Validate Zigbee channel number.
        
        Args:
            channel_str: Channel as string
            
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            channel = int(channel_str)
            return channel in self.VALID_CHANNELS
        except ValueError:
            return False
    
    def prompt_with_validation(self, prompt_text: str, default: Optional[str] = None, 
                              validator=None, error_msg: str = "Invalid input") -> str:
        """
        Prompt user for input with validation.
        
        Args:
            prompt_text: The prompt message
            default: Default value if user provides empty input
            validator: Function to validate input
            error_msg: Error message for invalid input
            
        Returns:
            str: Validated user input
        """
        while True:
            try:
                if default:
                    user_input = input(f"{prompt_text} [{default}]: ").strip()
                    value = user_input if user_input else default
                else:
                    value = input(f"{prompt_text}: ").strip()
                    
                if not value:
                    if default:
                        return default
                    logger.error("Input cannot be empty")
                    continue
                    
                if validator and not validator(value):
                    logger.error(error_msg)
                    continue
                    
                return value
                
            except KeyboardInterrupt:
                logger.info("Operation cancelled by user")
                raise DeconzMigrationError("User input cancelled")
    
    def generate_random_hex(self, byte_count: int) -> str:
        """
        Generate random hexadecimal string.
        
        Args:
            byte_count: Number of bytes to generate
            
        Returns:
            str: Random hex string
        """
        return ''.join(random.choices('0123456789abcdef', k=byte_count * 2))
    
    def read_devices_from_db(self, db_path: Path) -> List[Tuple[Any, ...]]:
        """
        Read device information from deCONZ database.
        
        Args:
            db_path: Path to the database file
            
        Returns:
            List[Tuple[Any, ...]]: List of device records
            
        Raises:
            DeconzMigrationError: If database cannot be read
        """
        try:
            with sqlite3.connect(str(db_path)) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM devices")
                devices = cursor.fetchall()
                
            logger.info(f"Found {len(devices)} devices in database")
            return devices
            
        except sqlite3.Error as e:
            error_msg = f"Failed to read database: {e}"
            logger.error(error_msg)
            raise DeconzMigrationError(error_msg)
    
    def build_zigbee2mqtt_config(self, devices: List[Tuple[Any, ...]], channel: str, 
                                pan_id: str, ext_pan_id: str, network_key: str,
                                mqtt_server: str = "mqtt://localhost", 
                                mqtt_base_topic: str = "zigbee2mqtt") -> Dict[str, Any]:
        """
        Build Zigbee2MQTT configuration dictionary.
        
        Args:
            devices: List of device records
            channel: Zigbee channel
            pan_id: PAN ID
            ext_pan_id: Extended PAN ID  
            network_key: Network encryption key
            mqtt_server: MQTT server URL
            mqtt_base_topic: MQTT base topic
            
        Returns:
            Dict[str, Any]: Configuration dictionary
        """
        # Clean hex values (remove 0x prefix if present)
        clean_pan_id = pan_id.replace('0x', '')
        clean_ext_pan_id = ext_pan_id.replace('0x', '')
        clean_network_key = network_key.replace('0x', '')
        
        config = {
            'mqtt': {
                'base_topic': mqtt_base_topic,
                'server': mqtt_server
            },
            'serial': {
                'port': '/dev/ttyACM0'
            },
            'advanced': {
                'pan_id': f"0x{clean_pan_id}",
                'extended_pan_id': f"0x{clean_ext_pan_id}", 
                'network_key': f"[{', '.join(f'0x{clean_network_key[i:i+2]}' for i in range(0, len(clean_network_key), 2))}]",
                'channel': int(channel)
            },
            'devices': []
        }
        
        # Add devices to config
        for device in devices:
            if not device:  # Skip empty tuples
                continue
                
            device_id = str(device[0]) if len(device) > 0 else "unknown"
            device_name = (
                str(device[1]) if len(device) > 1 and device[1] 
                else f"device_{device_id}"
            )
            
            device_config = {
                'id': device_id,
                'name': device_name
            }
            config['devices'].append(device_config)
        
        return config
    
    def save_config(self, config: Dict[str, Any], filename: str = "configuration.yaml") -> None:
        """
        Save configuration to YAML file.
        
        Args:
            config: Configuration dictionary
            filename: Output filename
            
        Raises:
            DeconzMigrationError: If file cannot be written
        """
        try:
            output_path = Path(filename)
            with output_path.open('w', encoding='utf-8') as f:
                yaml.dump(config, f, sort_keys=False, default_flow_style=False, 
                         allow_unicode=True, indent=2)
            
            logger.info(f"Configuration saved to: {output_path.absolute()}")
            
        except (OSError, yaml.YAMLError) as e:
            error_msg = f"Failed to save configuration: {e}"
            logger.error(error_msg)
            raise DeconzMigrationError(error_msg)
    
    def run_migration(self) -> None:
        """
        Run the complete migration process.
        
        Raises:
            DeconzMigrationError: If migration fails
        """
        try:
            logger.info("=== deCONZ to Zigbee2MQTT Migration Tool ===")
            
            # Find and read database
            self.db_path = self.find_database()
            self.devices = self.read_devices_from_db(self.db_path)
            
            if not self.devices:
                logger.warning("No devices found in database")
            
            # Get network configuration
            channel = self.prompt_with_validation(
                "Zigbee Channel (11-26)", "15",
                self.validate_channel,
                "Invalid channel. Must be between 11 and 26"
            )
            
            pan_id = self.prompt_with_validation(
                "PAN-ID (e.g., 0x1A63)", "0x1A63",
                lambda x: self.validate_hex_string(x, 4),
                "Invalid PAN-ID. Must be 4 hex characters (e.g., 0x1A63)"
            )
            
            ext_pan_id = self.prompt_with_validation(
                "Extended PAN ID (16 hex characters)", self.generate_random_hex(8),
                lambda x: self.validate_hex_string(x, 16),
                "Invalid Extended PAN ID. Must be 16 hex characters"
            )
            
            network_key = self.prompt_with_validation(
                "Network Key (32 hex characters)", self.generate_random_hex(16),
                lambda x: self.validate_hex_string(x, 32),
                "Invalid Network Key. Must be 32 hex characters"
            )
            
            # Get MQTT configuration
            mqtt_server = self.prompt_with_validation(
                "MQTT Server", "mqtt://localhost"
            )
            
            mqtt_base_topic = self.prompt_with_validation(
                "MQTT Base Topic", "zigbee2mqtt"
            )
            
            # Build configuration
            config = self.build_zigbee2mqtt_config(
                self.devices, channel, pan_id, ext_pan_id, network_key,
                mqtt_server, mqtt_base_topic
            )
            
            # Handle output
            dry_run_input = self.prompt_with_validation(
                "Dry-run mode (preview only)? [y/N]", "N"
            )
            
            is_dry_run = dry_run_input.lower() in ('y', 'yes')
            
            if is_dry_run:
                logger.info("=== Configuration Preview ===")
                print(yaml.dump(config, sort_keys=False, default_flow_style=False, 
                               allow_unicode=True, indent=2))
            else:
                self.save_config(config)
                
        except (KeyboardInterrupt, EOFError):
            logger.info("Migration cancelled by user")
        except DeconzMigrationError as e:
            logger.error(f"Migration failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise DeconzMigrationError(f"Unexpected error: {e}")


def main():
    """
    Main entry point for the migration tool.
    """
    try:
        migrator = DeconzToZ2MMigrator()
        migrator.run_migration()
    except DeconzMigrationError:
        exit(1)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        exit(1)


if __name__ == "__main__":
    main()
