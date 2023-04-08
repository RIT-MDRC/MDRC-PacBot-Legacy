# AutoRobo
### Written by Michael Elia
### Last updated: 2023-04-06

## Description

Facilitates running the Pacbot server and client code provided by HarvardURC.

## Setup

- You must have Python 3.10 or later installed
- In order to properly set up the git submodules in this folder, you must run `git submodule update --init --recursive` from the root of the repository

If pygame complains about no display device:

- Install and run VcXsrv on windows
  - Multiple displays
  - Start no client
  - Default display 0
- Set the DISPLAY environment variable to `<<your local IP>>:0`

