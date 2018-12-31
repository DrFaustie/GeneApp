# calculate_total_reputation rewritten to take advantage of Multiprocessing
- Previous implementation ran much slower because of the linear nature of which we worked on the genelist. Suppose we had a list of 300,000 genes, the previous code would simply iterate over each gene, perform all calculations, then create an object; all on one process.
- Our current implementation splits the genelist in n elements, feeding each list into a separate process, all working together to perform the necessary calculations and create objects in parallel time. This should result in much faster performance.
- Basic testing suggests iterating over 3,000,000 elements on one process takes around 5.5 seconds, while a multiprocess approach takes about 0.7.

# .iterator() should be usable on calculate_total_reputation
- genelist shouldn't need any caching, or to be queried more than once. .iterator() might be usable in other places in the code but unsure.

# Added error handling for calculate_total_reputation
- We raise some sort of warning if a UserGeneReputation object isn't created

# Reformatted task.py so datatypes and separate elements are more obvious.
- Style changes that break up ridiculously large statements

# Refactored all instances of .format, %s to fstrings.
- fstrings have a much faster performance than other methods and any loss of efficiency is unnecessary.

# General cleanup of print statements.
- Some were printing rather poor and broken English. Grammar and wording has been fixed to make them more descriptive and accurate.

# Refactored 'snp' variable to 'local_snp'.
- Having two variables that can only be distinguished by their case (Snp, snp) feels like extremely poor design. It may be obvious for those familiar - with the code, but can easily lead to misunderstandings; especially by new people coming in. 'local_snp' also acts a more descriptive label for the local variable, allowing us to keep the "Snp" model reference.

# Zygosities and Colors have been changed from Dicts of Tuples to Dicts of Dicts.
- Dicts of Dicts should improve lookup efficiency and be far easier to reference and understand in code.
- eg. zygosities["homozygous_major"]["reputation"] vs zygosities["homozygous_major"][2]
- I could not find a suitable name for "-/-" etc. elements. I've called them "hh" (Homozygous/Heterozygous) but someone with more understanding of biology could likely find a better one

# Added else statement to check_genotype_style
- check_genotype_style had no handling for a case where none of the if statements were met. Since we can assume that if none of them are met, the style is unknown, we simply change the last elif statement to an else statement. We could also optionally keep that statement and add a more explicit else statement, something like "DETECTION ERROR"

# Made sure all functions had an explicit return value
- Although it is not strictly necessary, it is good to visually document a "return None" on functions that do so as it makes our intention much clearer.

# Simplified deletion statement on #389
- Previous deletion statement was nonsensical. We created a backup, then deleted the backup if somehow our deletion on the initial file failed.

#Ideas

We could use multithreading to make reputation calculation faster

# Comments

This was a very fun task. Thinking about optimization was a big challenge, and, to be honest, this was my first ever implementation of Multiprocessing. I had to do a lot of research and experimentation to get the code to work properly, but in doing so I gained a lot of new knowledge about how python works at a base level, including its limitations.
