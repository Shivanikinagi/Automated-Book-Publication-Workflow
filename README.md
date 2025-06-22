Automated Book Publication Workflow

Overview

This project implements an automated book publication pipeline that fetches, processes, and refines chapters from a web source. It integrates web scraping, AI-driven text paraphrasing, human-in-the-loop review, and content versioning to produce polished, customized outputs.

Features
Web Scraping: Extracts chapter text from a specified URL using Playwright and saves screenshots.
AI Paraphrasing: Uses an LLM to rephrase content based on user instructions (e.g., "make it simple").
Human Review: Supports iterative human feedback with edit prompts and example instructions.
Content Versioning: Stores versions in ChromaDB and retrieves the best match using an RL search algorithm.
Seamless Workflow: Ensures smooth content flow between agents via an agentic API.

Tech Stack
Python: Core development language.
Playwright: For web scraping and screenshot capture.
LLM: For AI-driven paraphrasing and review.
ChromaDB: For content storage and versioning.
RL Search Algorithm: For intelligent version retrieval.

Usage
Run the pipeline to scrape a chapter from a URL (e.g., Wikisource).
Provide an AI instruction (e.g., "make it simple") for paraphrasing.
Review and edit the output during human-in-the-loop iterations.
Store and retrieve versions from ChromaDB based on query relevance.

Setup

pip install -r requirements.txt
python main.py

Demo : https://youtu.be/WyM2Kei_Y-8
