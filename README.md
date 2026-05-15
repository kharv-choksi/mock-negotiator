# Mock Negotiator

A lightweight web app built to help students and professionals practice difficult workplace conversations. Whether you are prepping for a salary negotiation or figuring out how to push back on a stubborn engineering lead, this tool uses Anthropic's Claude to roleplay the scenario with you. 

I originally built this as a side project to prepare for Product Management internship recruiting.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features
- **Dynamic Personas:** Choose who you are talking to (e.g., The Stingy Recruiter, The Skeptical VP of Product).
- **Custom Scenarios:** Define the exact context of the conversation before you start.
- **Realistic Pushback:** The AI is prompted specifically to not make it easy on you. It will push back, say no, and act like a real counterpart.
- **Session Memory:** Keeps track of the chat history so you can have a continuous back-and-forth conversation.

## Installation

You will need Python installed on your machine and an Anthropic API key.

1. Clone the repository:
    ```bash
    git clone [https://github.com/yourusername/mock-negotiator.git](https://github.com/yourusername/mock-negotiator.git)
    cd mock-negotiator
    ```

2. Create and activate a virtual environment (recommended to avoid dependency conflicts):
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required dependencies:
    ```bash
    pip install streamlit anthropic
    ```

## Usage

1. Start the application locally:
    ```bash
    python -m streamlit run app.py
    ```
    *(Note: using `python -m` helps avoid conflicts if you have Anaconda installed on your machine).*

2. The app will automatically open in your default web browser (usually at `localhost:8501`).
3. Grab an API key from your [Anthropic Console](https://console.anthropic.com/).
4. Paste the API key into the sidebar of the app.
5. Select your persona, type in your scenario, and start pitching.


## License
This project is open-source and available under the [MIT License](LICENSE).
