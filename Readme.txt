"""
the following code was written for the University of Texas Southwestern for bioinformatics job coding challenge. 

Write a script in Perl or Python that parses the pileup file line-by-line, and will call a consensus base using two criteria: sequencing coverage and the proportion of consensus mismatches relative to the reference.  Call a consensus base if

(1) the sequencing coverage is greater than or equal to 5X, but less than 100X, and

(2) the percentage of consensus mismatches relative to the reference is greater than or equal to 80% of the total number of bases in the pile.

However, ignore bases whose sequencing quality score is below 40.  That is, do not use them to compute either the proportion of consensus mismatches, or the total coverage.

"""
