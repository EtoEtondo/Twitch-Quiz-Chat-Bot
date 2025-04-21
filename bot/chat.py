#!/usr/bin/env python3

import socket
import threading
import time
import csv
import os

class ChatBot:
    def __init__(self, channel_name, oauth_token):
        self.CHANNEL = channel_name.lower()  # Monitored channel (always lowercase)
        self.OWNER = channel_name.lower()    # Account name (always lowercase)
        self.PASS = oauth_token              # Authentication token
        self.BOT = "Twitch-Quiz-Chat-Bot"
        
        self.answer_counts = {'a': 0, 'b': 0, 'c': 0, 'd': 0}
        self.total_answers = 0
        self.user_answers = set()
        self.is_reading_chat = True
        self.csv_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "webpy", "static", "answer_tmp.csv")
        self.forward_write = False # Flag to control writing to CSV after toggling off

        self.SERVER = "irc.twitch.tv"
        self.PORT = 6667
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Explicit socket creation

    def connect(self):
        try:
            self.irc.connect((self.SERVER, self.PORT))
            self.irc.send(f"PASS {self.PASS}\n".encode('utf-8'))
            self.irc.send(f"NICK {self.BOT}\n".encode('utf-8'))
            self.irc.send(f"JOIN #{self.CHANNEL}\n".encode('utf-8'))
            print(f"Successfully connected to Twitch channel: #{self.CHANNEL}")
        except socket.error as e:
            print(f"Error connecting to Twitch: {e}")
            # Consider adding retry logic here

    def handle_chat_input(self):
        while True:
            if self.is_reading_chat:
                if self.message and self.user not in self.user_answers:
                    answer = self.message.lower().strip()
                    if answer in self.answer_counts:
                        self.answer_counts[answer] += 1
                        self.total_answers += 1
                        self.user_answers.add(self.user)
                    self.message = "" # Reset message after processing
            else:
                if not self.forward_write:
                    self._write_results_to_csv()
                    self.forward_write = True
                # Reset counters and user list after writing
                self.answer_counts = {'a': 0, 'b': 0, 'c': 0, 'd': 0}
                self.total_answers = 0
                self.user_answers = set()
            time.sleep(0.1) # Small delay to reduce CPU usage

    def _write_results_to_csv(self):
        head = ["All", "A", "B", "C", "D"]
        data = [self.total_answers] + list(self.answer_counts.values())
        data_percentages = [100.0] + [round((count / self.total_answers) * 100, 2) if self.total_answers > 0 else 0.0 for count in self.answer_counts.values()]

        try:
            with open(self.csv_file_path, "w", newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(head)
                writer.writerow(data)
                if self.total_answers > 0:
                    writer.writerow([round(p, 2) for p in data_percentages]) # Round percentages for cleaner output
                print("Chat answer results written to CSV.")
        except Exception as e:
            print(f"Error writing to CSV file: {e}")

    def twitch_receive_loop(self):
        self._join_chat()
        self.irc.send("CAP REQ :twitch.tv/tags\r\n".encode('utf-8'))
        while True:
            try:
                readbuffer = self.irc.recv(1024).decode('utf-8')
                for line in readbuffer.split("\r\n"):
                    if not line:
                        continue
                    if "PING :tmi.twitch.tv" in line:
                        print(line)
                        self.irc.send("PONG :tmi.twitch.tv\r\n".encode('utf-8'))
                        print("PONG sent.")
                        continue
                    else:
                        try:
                            self.user = self._get_user(line)
                            self.message = self._get_message(line)
                            print(f"{self.user}: {self.message.strip()}")
                            if self.is_reading_chat:
                                print("Active: Checking Chat Input!")
                                self.forward_write = False
                            else:
                                print("Inactive: Chat input is being recorded for CSV.")
                        except Exception as e:
                            print(f"Error processing chat line: {e}")
            except socket.error as e:
                print(f"Socket error: {e}")
                # Consider adding reconnection logic with backoff
                time.sleep(10)
            except UnicodeDecodeError as e:
                print(f"Unicode decode error: {e}")
                # Handle potential encoding issues

    def _join_chat(self):
        loading = True
        while loading:
            try:
                readbuffer_join = self.irc.recv(1024).decode('utf-8')
                for line in readbuffer_join.split("\n")[:-1]:
                    print(line.strip())
                    if "End of /NAMES list" in line:
                        print(f'{self.BOT} running on #{self.CHANNEL}\'s channel!')
                        self._send_message("Hey everyone! You can answer the quiz by typing a, b, c, or d in the chat!")
                        loading = False
                        break
            except socket.error as e:
                print(f"Socket error during join: {e}")
                time.sleep(5) # Wait before retrying
            except UnicodeDecodeError as e:
                print(f"Unicode decode error during join: {e}")

    def _send_message(self, msg):
        message_temp = f"PRIVMSG #{self.CHANNEL} :{msg}"
        self.irc.send((message_temp + "\n").encode('utf-8'))
        print(f"<{self.BOT}>: {msg}")

    def _get_user(self, line):
        try:
            parts = line.split('!', 1)[0]
            return parts[1:] if parts.startswith(':') else parts
        except IndexError:
            return ""

    def _get_message(self, line):
        try:
            parts = line.split(':', 2)
            return parts[2] if len(parts) > 2 else ""
        except IndexError:
            return ""

    def toggle_chat_reading(self):
        while True:
            inp = input()
            if inp == "":
                self.is_reading_chat = not self.is_reading_chat
                print(f"Chat reading {'enabled' if self.is_reading_chat else 'disabled'}.")
                if not self.is_reading_chat:
                    self.forward_write = False # Prepare to write on next toggle
            time.sleep(0.1)

    def run(self):
        self.connect()
        twitch_thread = threading.Thread(target=self.twitch_receive_loop)
        answer_thread = threading.Thread(target=self.handle_chat_input)
        toggle_thread = threading.Thread(target=self.toggle_chat_reading)

        twitch_thread.daemon = True # Allow program to exit even if thread is blocked
        answer_thread.daemon = True
        toggle_thread.daemon = True

        twitch_thread.start()
        answer_thread.start()
        toggle_thread.start()

        # Keep the main thread alive to allow the others to run
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Bot shutting down.")
        finally:
            if self.irc:
                self.irc.close()

def main():
    # Replace with your actual Twitch username (lowercase) and OAuth token
    oauth_token = "oauth:YOUR_OAUTH_TOKEN"
    channel_name = "your_twitch_channel"
    chatbot = ChatBot(channel_name, oauth_token)
    chatbot.run()

if __name__ == '__main__':
    main()
