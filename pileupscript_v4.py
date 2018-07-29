# !/usr/bin/env python

import sys
import argparse


"""
main() defines the arguments that are taken in from command line. 

"""
class Pileup(object):   
	def __init__(self, input_data, i, k, j, ref_count, alt_count, alt_allele, ref_allele, ref_check):
		self.i = i 
		self.k = k
		self.j = j
		self.ref_count = ref_count
		self.alt_count = alt_count
		self.alt_allele = alt_allele
		self.ref_allele = ref_allele
		self.ref_check = ref_check
		self.bq = []
		self.input_data = input_data
		self.pileup_len = len(self.input_data[4])
				
	def read_depth_eval(self):
		"""
		read_depth_eval() is called by main() for each new line of pileup file. First it evaluates read depth. 
		"""
		
		noChange = True
		if int(self.input_data[3]) > 4 and int(self.input_data[3]) < 100:				
			self.j = self.k = 0
			while self.k < int(self.input_data[3]):
				self.pileup_quality_eval()
				self.k += 1
			
			if 'Y' in self.bq:
				if (self.alt_count*100/(self.alt_count+self.ref_count)) > 79:
					self.ref_check = (self.input_data[0], self.input_data[1], self.alt_allele)
					return "\t".join(x for x in (self.input_data[0], self.input_data[1], self.alt_allele.upper()))
					noChange = False
			
		if noChange:
			self.ref_check = (self.input_data[0], self.input_data[1], self.input_data[2])
			return "\t".join(x for x in (self.input_data[0], self.input_data[1], self.input_data[2].upper()))
		
	def pileup_quality_eval(self):
		"""
		pileup_quality_eval() is called by read_depth_eval() for each position of the quality string.  
		"""
		self.base_call_counter_adjust()
		if (ord(self.input_data[5][self.k]))-33 > 39:							 
			self.bq.append('Y')
			self.consensus()
		else:
			self.bq.append('N')
		self.j += 1
		
	
	def base_call_counter_adjust(self):
		if self.input_data[4][self.j] == "^":								
			self.j += 2
					
		elif self.input_data[4][self.j] == "$":
			self.j += 1
			
		elif self.input_data[4][self.j] == "+" or self.input_data[4][self.j] == "-":
			self.j = self.j + int(self.input_data[4][self.j+1]) + 1
			
	def consensus(self):
		"""
		consensus() is called only by 
		"""
				
		if self.input_data[4][self.j] != "." and self.input_data[4][self.j] != ",":
			self.alt_count += 1
			self.alt_allele = self.input_data[4][self.j]		
			
		elif self.input_data[4][self.j] == "." or self.input_data[4][self.j] == ",":
			self.ref_count += 1
			self.ref_allele = self.input_data[2]
			
		else:
			self.ref_allele = self.input_data[2]
			

def main():
	"""
	The main() takes in arguments of input file name and output file name from terminal. This function parses each line of the pileup file, and outputs a consensus to a file.
	"""
	
	parser=argparse.ArgumentParser(description="Script to parse sequence pileup and output a consensus")
	parser.add_argument("-in",help="txt input file" ,dest="input", type=str, required=True)
	parser.add_argument("-out",help="txt output filename" ,dest="output", type=str, required=True)
	args=parser.parse_args()
	
	fileinp = open(args.input,'r')
	input_data = []
																		
	i = j = k = 0
	alt_count = 0
	ref_count = 0
	alt_allele = []
	ref_allele = []
	ref_check = []
	
	fileout = open(args.output, 'w')

	for line in fileinp:
		data = line.strip("\n").split("\t")		
		pileup = Pileup(data, i, k, j, ref_count, alt_count, alt_allele, ref_allele, ref_check)
		con = pileup.read_depth_eval()
		fileout.write(con + "\n")
		
	fileinp.close()
	fileout.close()
	print("\n\n","END OF PILEUP FILE PROCESSING")
	

if __name__=="__main__":
	main() 