# Key reinstallation

## Objective
The objective of this challenge is to exploit the KRACK (Key Reinstallation Attack) vulnerability in the WPA2 protocol to recover an employee's login credentials without cracking the Wi-Fi passphrase.

## Tools
I used Wireshark, tshark and Python.

## Steps

After opening the capture in Wireshark, the first step was to find the MAC of the telephone and the KRACK attack. I applied the filter **eapol** for this purpose. I noticed that the victim's telephone was Apple_15:01:ef, because we can see the last packets were Message 3 and 4, without Messages 1 and 2.

<img width="870" height="274" alt="image" src="https://github.com/user-attachments/assets/30248c31-668c-415d-a20a-dd1b4bb96502" />

I found the MAC address of this phone:

<img width="510" height="130" alt="image" src="https://github.com/user-attachments/assets/7e5d8bc5-53c8-449d-ad1b-c10fbfff6849" />

Then, I applied the filter **wlan.ta == f0:18:98:15:01:ef** to isolate the packets from this MAC.

To see the PN sequences, I applied the Initialization Vector as a column, to better analyze how the PN rises and resets after the EAPOL Message 3, and then restarts.
We can notice there are 2 packets with the same PN, frames 148 and 331, with hex PN (0x000000000008).
In bash, with the command **tshark -r capture-1.pcap -Y "wlan.ta == f0:18:98:15:01:ef" -T fields -e frame.number -e wlan.ccmp.extiv -e frame.len -e data.data > frames.txt**, I exported the encrypted payloads. Analyzing the generated file "frames.txt", for every row we have the frame number, the PN, the length and the hexadecimal string "data.data".
We know that in frame 148, the bytes from 48 to -8 contain the initial text of expense-form.txt. Through the Python script, by computing the XOR between the two frames and the known plaintext, I saw the entire POST request with the credentials sent by the employee and the flag **netsec{ea5b7700e9fe31f78d52e11d46f88a21}**.

<img width="662" height="196" alt="image" src="https://github.com/user-attachments/assets/209e04f8-6c24-46ed-8b44-e2f7d9295658" />
