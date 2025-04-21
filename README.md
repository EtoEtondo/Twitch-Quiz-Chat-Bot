# Twitch Quiz Chat Bot

Easy Twitch Chat-Bot for quizzing with or against community via chat.

## About

This project was conceived to create engaging new streaming content for special streamers and events. At its core is an interactive quiz, allowing for the integration of custom questions.

However, the central feature of this project lies in its seamless integration with the Twitch live stream chat. To grasp the concept, consider the interactive quizzes popularized by the German YouTubers [PietSmiet](https://www.youtube.com/watch?v=jiFptUKaWGY). For further details or inquiries, feel free to reach out to us.

## Installing and Preparation

First, you need to `git clone` this project. Also checkout your Python 3, a suitable code editor to run and modify the chatbot and
for the website component, ensure you have a compatible web browser and install the [Flask](https://flask.palletsprojects.com/en/2.0.x/installation/#install-flask) microframework.

## Usage

To utilize the quiz with Twitch chat integration, you need to launch the chatbot script. Before doing so, ensure you have updated the username and OAuth key within the script. Then, navigate to the project's `bot/` directory in your terminal and execute the `chat.py`:

```bash
cd bot/
python3 chat.py
```

This script must remain running to continuously monitor the Twitch chat. To terminate the script, press `Ctrl + C` (or `Cmd + C` on macOS) in your terminal.

The quiz requires interaction with your Twitch chat. At various points, you'll want to review the answer submissions from your audience. To facilitate this, the script allows you to toggle the chat reading process on or off by pressing **Enter** in the terminal. Each toggle will provide textual feedback in the terminal indicating the current reading status. When toggled off, the script writes the collected chat responses to a `.csv` file, which is subsequently read by the web application.

Thereupon, you need to inform Flask about your web application and then run the Python web server script. Navigate to the `webpy/` directory in your terminal and execute the following commands:

```bash
cd webpy/
export FLASK_APP=web
export FLASK_ENV=development
flask run
```

This will launch the website locally, accessible via `localhost:5000` in your web browser.

Upon pressing the "Start" button on the website, the first quiz question will be displayed. You can customize these questions by editing the `quiz.js` file. After participants submit their answers in the chat and you confirm, the website will reveal the correct answer (or indicate if the submitted answer was incorrect) alongside the collective choices made by the chat. The +/- buttons located at the bottom of the website interface allow you to distribute points to participating teams. The methodology for awarding points is flexible and depends on your preferred game rules – have fun experimenting!

## Improvements and Contributions

If you have any suggestions on how to streamline the process or enhance the project's functionality, please do not hesitate to contact us. We are also open to discussions regarding potential game rules and detailed explanations for their implementation.

Our initial attempts involved developing the website entirely with JavaScript. However, we encountered challenges in efficiently reading the `.csv` file, which ultimately led us to adopt Python for the web application component.
