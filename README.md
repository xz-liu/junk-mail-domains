# Junk Mail Domains

A curated list of junk email domains maintained for use with **Power Automate** to forcefully block spam.

## Motivation

Outlook's native spam filtering often creates more problems than it solves. This project exists to address three specific failures in the Outlook ecosystem:

1. **Aggressive False Positives:** Important notifications frequently land in the Junk folder, getting lost among actual spam.
2. **Rule Bypass:** As soon as Outlook marks an item as "Junk," **it stops processing user-defined rules.** This renders your carefully crafted sorting rules useless for any email Outlook unilaterally decides is spam.
3. **Manual Triage Fatigue:** Users are forced to manually sift through a pile of garbage in the Junk folder every day just to ensure they haven't missed a critical notification.

### The Objective

The goal of this list is to **hard-block** obvious garbage domains before they even reach the Junk folder. By filtering out true spam at the source, the Junk folder stays clean enough to serve as a **"Secondary Inbox"**—a reliable place for legitimate-but-noisy notifications that doesn't require daily deep-cleaning.

## Repository Structure

This repository contains a Python script to manage and generate the blocklists.

* `generate_fuckoff_lists.py`: The main logic script. It reads the raw source, removes duplicate domains, and generates the output files.
* `raw_junk_email_domains.json`: The source file containing the raw list of domains.
* `fuckoff.json`: The clean, deduplicated list for production use.
* `fuckoff_debug.json`: The deduplicated list with `proton.me` appended to test Power Automate flows without waiting for actual spam.

## Usage

Run the script to update the lists after adding new domains to the raw JSON file:

```bash
python3 generate_fuckoff_lists.py

```