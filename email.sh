#!/bin/bash

# Define the base directory
base_dir="email_assistant"

# Create the base directory
mkdir -p $base_dir

# Create subdirectories
mkdir -p $base_dir/agents
mkdir -p $base_dir/core
mkdir -p $base_dir/utils

# Create files in the agents directory
touch $base_dir/agents/__init__.py
touch $base_dir/agents/filtering_agent.py
touch $base_dir/agents/summarization_agent.py
touch $base_dir/agents/response_agent.py
touch $base_dir/agents/human_review_agent.py

# Create files in the core directory
touch $base_dir/core/__init__.py
touch $base_dir/core/email_ingestion.py
touch $base_dir/core/email_sender.py
touch $base_dir/core/state.py
touch $base_dir/core/supervisor.py

# Create files in the utils directory
touch $base_dir/utils/__init__.py
touch $base_dir/utils/logger.py

# Create other files in the base directory
touch $base_dir/sample_emails.json
touch $base_dir/config.py
touch $base_dir/main.py
touch $base_dir/requirements.txt
touch $base_dir/README.md

echo "File tree created successfully."
