"""
Encryption Helper - Compatible with C# EncryptionHelper

AES-256-CBC encryption with PKCS7 padding, matching the C# implementation.
"""

import json
import base64
from typing import Type
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend


class EncryptionHelper:
    """
    AES encryption helper compatible with the C# EncryptionHelper class.
    Uses AES-256-CBC with PKCS7 padding.
    """
    
    # AES requires a 16-byte IV (Initialization Vector) - matching C# implementation
    _IV = bytes(16)  # 16 zero bytes
    _ENCRYPTION_KEY = "G7r8f5Tj2Qw1Xv3ZyU9KpL6oM4nBc7Es"
    
    @classmethod
    def encrypt(cls, data) -> str:
        """
        Encrypt any object by serializing to JSON first.
        
        Args:
            data: Any JSON-serializable object
            
        Returns:
            Base64-encoded encrypted string
        """
        # Serialize the object to JSON string
        json_str = json.dumps(data)
        json_bytes = json_str.encode('utf-8')
        
        # Apply PKCS7 padding
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(json_bytes) + padder.finalize()
        
        # Create cipher and encrypt
        cipher = Cipher(
            algorithms.AES(cls._ENCRYPTION_KEY.encode('utf-8')),
            modes.CBC(cls._IV),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        encrypted = encryptor.update(padded_data) + encryptor.finalize()
        
        # Return as base64
        return base64.b64encode(encrypted).decode('utf-8')
    
    @classmethod
    def decrypt(cls, encrypted_data: str, return_type: Type = None):
        """
        Decrypt an encrypted string and optionally deserialize to a specific type.
        
        Args:
            encrypted_data: Base64-encoded encrypted string
            return_type: Optional type to deserialize to. If None or str, returns string.
            
        Returns:
            Decrypted and deserialized object
        """
        try:
            # Decode from base64
            encrypted_bytes = base64.b64decode(encrypted_data)
            
            # Create cipher and decrypt
            cipher = Cipher(
                algorithms.AES(cls._ENCRYPTION_KEY.encode('utf-8')),
                modes.CBC(cls._IV),
                backend=default_backend()
            )
            decryptor = cipher.decryptor()
            decrypted_padded = decryptor.update(encrypted_bytes) + decryptor.finalize()
            
            # Remove PKCS7 padding
            unpadder = padding.PKCS7(128).unpadder()
            decrypted = unpadder.update(decrypted_padded) + unpadder.finalize()
            
            # Convert to string
            json_str = decrypted.decode('utf-8')
            
            # Check if the decrypted value has extra quotes (matching C# behavior)
            if json_str.startswith('"') and json_str.endswith('"'):
                json_str = json_str[1:-1]
            
            # If return_type is str or None, return the plain string
            if return_type is None or return_type == str:
                return json_str
            
            # Otherwise deserialize to the specified type
            return json.loads(json_str)
            
        except Exception as e:
            print(f"Decryption failed: {e}")
            raise
