# Refactoring and optimization

## Briefing

User genomic data contains a large amount of variants that we must process to be able to provide them with the most relevant information.
Each person has over 600k SNPs (Single Nucleotide Polymorphism) that we must weight and store separately for our system to work.

We have to us optimize and refactor the asynchronous task that we use to process our users genetic information.

## Instructions

In this folder you will find 3 files:

* models.py

    This file has the models used by the task.
    You don't have to do anything in this file and its purpose is to give you an insight of the amount of data each model can have.

* utils.py

    This file holds a few utilities that are used by the task.
    You don't have to do anything here either.

* task.py

    This is where the test is.
    Here there are a few functions and the file processing task.
    You have to refactor and optimize the code in this file.
    The asynchronous task that is being refereed is in this file and has the name `process_genome_file`.

* task.md

    This is an empty markdown file for you to write down your ideas and thoughts.
    After making changes to the code,
    please provide a short description of what you did,
    and why you chose to do it.
    If you have other comments on the test itself,
    you may leave them in the file as well.

The task works like this:
The genetic file is retrieved from amazon s3.
It's parsed, processed, saved and weighted.
Feel free to change this process order if you think it would optimize the process.

You can do anything you want to improve the overall code readability, ram usage, error handling, logging, speed of this process.
Remove code, add code, remove non-core features.
Anything.
This is where you show us how clean and maintainable you write code and how familiar you are with django and its ORM.

## Considerations

* Each user has over 600k SNPs in his snp file
* We have over 50k SNPs stored on our databases
* We match around 15k SNPs per user and that SNP match is saved on our databases
* The file that you are processing don't have any SNP associated with it before the processing

## Environment used

* Python 3.6
* Django 1.11
