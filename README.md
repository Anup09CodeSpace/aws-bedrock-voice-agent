# aws-bedrock-voice-agent

A voice-enabled hotel agent built on AWS Bedrock with DynamoDB-backed demo tools for guest profiles and reservation management.

## Overview

This project includes a sample voice agent architecture that can:
- handle interruptible speech interactions
- call hotel-specific tools for guest lookup and reservation updates
- store guest and reservation data in DynamoDB
- parse and display conversation logs via a Streamlit utility

## Repository Structure

- `hotel-agent.py` - core voice agent logic and tool processing for hotel guest/reservation workflows
- `db-setup.py` - DynamoDB table creation and demo seed data for `Hotel_Guests` and `Hotel_Reservations`
- `app.py` - Streamlit app for parsing and inspecting assistant logs
- `requirements.txt` - Python dependencies for the project

## Prerequisites

- Python 3.10+ (or compatible)
- AWS credentials configured with access to Bedrock and DynamoDB
- AWS region set, e.g. `us-east-1`
- `pyaudio` may require platform-specific audio dependencies

## Installation

1. Create and activate a Python virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   If `requirements.txt` is empty, install packages manually:

   ```bash
   pip install boto3 pyaudio streamlit streamlit-autorefresh aws-sdk-bedrock-runtime
   ```

## Setup

1. Ensure AWS credentials are available in your environment.
2. Run the database setup script to create tables and seed demo data:

   ```bash
   python db-setup.py
   ```

## Usage

- `hotel-agent.py` is the main voice agent implementation.
- `app.py` can be used to inspect log files and visualize recent assistant events.

Run the Streamlit viewer in one terminal:

```bash
streamlit run app.py
```

Then run the agent in another terminal and stream logs into `assistant.log`:

```bash
PYTHONBUFFERED=1 python hotel-agent.py --debug >>assistant.log 2>&1
```

## Notes

- Replace any dummy AWS credentials in `hotel-agent.py` with your actual AWS credentials.   `Line 1255 - 1257`
- Replace the dummy region value in `db-setup.py` with your actual AWS region name.
`Line 9`
- Update `requirements.txt` with the exact dependencies you need for your Bedrock runtime environment.
- Confirm the DynamoDB region and table names match your AWS account configuration.

