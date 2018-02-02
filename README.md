# coderbyte-challenges

This repository contains a small python script to scrape the CoderByte website.

The script extracts the name, original question text, my solution, and the 'difficulty' level (they are split up into 'easy', 'medium', and 'hard').

After extracting the data from the website, it creates a JSON file for each difficulty level which I can then access from my front-end site
similar to using a static API by using the following URL format:
`https://raw.githubusercontent.com/{username}/{repository}/master/{filename}`
