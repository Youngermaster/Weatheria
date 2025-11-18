#!/usr/bin/env python3
"""
Word Count MapReduce Example
Classic example to demonstrate basic MapReduce functionality

Usage:
    # Local mode
    python src/mapreduce/word_count.py data/raw/sample_text.txt
    
    # Hadoop mode
    python src/mapreduce/word_count.py -r hadoop hdfs:///input/sample_text.txt
"""

from mrjob.job import MRJob
import re

WORD_RE = re.compile(r"[\w']+")


class WordCount(MRJob):
    """
    Simple word count MapReduce job
    
    Input: Text file
    Output: word\tcount pairs
    """
    
    def mapper(self, _, line):
        """
        Emit each word with count of 1
        
        Args:
            _: Line number (ignored)
            line: Line of text
            
        Yields:
            (word, 1) for each word in the line
        """
        # Extract all words from the line
        for word in WORD_RE.findall(line):
            # Convert to lowercase for case-insensitive counting
            yield word.lower(), 1
    
    def reducer(self, word, counts):
        """
        Sum up counts for each word
        
        Args:
            word: The word
            counts: Iterator of counts (all 1s from mapper)
            
        Yields:
            (word, total_count)
        """
        yield word, sum(counts)


if __name__ == '__main__':
    WordCount.run()
