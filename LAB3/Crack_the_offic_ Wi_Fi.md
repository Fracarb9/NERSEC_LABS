# Crack the office Wi-Fi

## Objective
The objective of this lab is to recover the passphrase, decrypt the traffic, and find the flag "netsec{...}" from a capture by a sniffer on channel 6 next to the Acme's office.
We know that the office network **Acme-WiFi** uses WPA2-Personal (PSK), and the Acme's IT policy states that the Wi-Fi passphrase is always "Acme" followed by six digits.

## Tools
For this lab I use "hcxpcapngtool" + "hashcat -m 22000" (mask attack, "-a 3"). "hcxpcapngtool" was used for extract the handshake from the capture file, while "hashcat" was used for try the mask attack (brute-force)

## Steps
After installing the tools, I used the bash command: **hcxpcapngtool -o hash.22000 capture-1.pcap**, where I extracted the handshake from the capture "capture-1". The command created the file "hash.2000".
Next, I used the command **hashcat -m 22000 -a 3 hash.22000 Acme?d?d?d?d?d?d** for a brute-force attack, throght which I could find the passphrase.
I found 2 different passphrases:

<img width="665" height="84" alt="image" src="https://github.com/user-attachments/assets/5a77ceae-8f7f-4fc6-a016-28fff4ceddff" />

I chose the **Acme856402** because there are 2 client with this one.

In wireshark, **Preferences --> Protocols --> IEEE 802.11 --> Decryption keys** I added the decryption key in the format (wpa-pwd, passphrase:SSID)

<img width="577" height="441" alt="image" src="https://github.com/user-attachments/assets/fd3e3cb7-87ea-452d-a36b-5d619f2ce05e" />

Afterwards, I applied the filter "htt.request", selected the "POST" request from the packets, and followed the HTTP stream.

<img width="1073" height="443" alt="image" src="https://github.com/user-attachments/assets/eb0ba5d2-3832-4589-a11b-c49e4ad19d8c" />

Here I found the NetSec string:

<img width="604" height="252" alt="image" src="https://github.com/user-attachments/assets/05e5657b-a104-4bdf-aeb4-05543e956d56" />

And the challenge is solved:

<img width="671" height="204" alt="image" src="https://github.com/user-attachments/assets/cbf5d702-628c-475b-96df-0024e99ba223" />
