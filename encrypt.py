import os
from cryptography.fernet import Fernet
from tqdm import tqdm
from termcolor import colored

class DirectoryEncryptor:
    def __init__(self, key_file_path):
        if os.path.exists(key_file_path):
            with open(key_file_path, 'rb') as file:
                self.key = file.read()
        else:
            self.key = Fernet.generate_key()
            with open(key_file_path, 'wb') as file:
                file.write(self.key)
        self.fernet = Fernet(self.key)

    def encrypt_directory(self, directory_path):
        for dirpath, dirnames, filenames in os.walk(directory_path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                with open(filepath, 'rb') as file:
                    original = file.read()
                encrypted = self.fernet.encrypt(original)
                with open(filepath, 'wb') as encrypted_file:
                    encrypted_file.write(encrypted)
                progress_bar = tqdm(desc=colored('Encrypting', 'red', attrs=['bold']), unit='file')
                progress_bar.set_postfix(file=filename)
                progress_bar.update()
                progress_bar.close()

        print(colored('\nEncryption complete', 'red', attrs=['bold']))

    def decrypt_directory(self, directory_path):
        for dirpath, dirnames, filenames in os.walk(directory_path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                with open(filepath, 'rb') as encrypted_file:
                    encrypted = encrypted_file.read()
                decrypted = self.fernet.decrypt(encrypted)
                with open(filepath, 'wb') as decrypted_file:
                    decrypted_file.write(decrypted)
                progress_bar = tqdm(desc=colored('Decrypting', 'red', attrs=['bold']), unit='file')
                progress_bar.set_postfix(file=filename)
                progress_bar.update()
                progress_bar.close()

        print(colored('\nDecryption complete', 'red', attrs=['bold']))

key_file_path = input(colored('Enter the path to the key file: ', 'red', attrs=['bold']))
directory_path = input(colored('Enter the path to the directory to encrypt/decrypt: ', 'red', attrs=['bold']))

directory_encryptor = DirectoryEncryptor(key_file_path)

directory_encryptor.encrypt_directory(directory_path)

directory_encryptor.decrypt_directory(directory_path)
