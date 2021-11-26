import argparse
import sys
from collections import Counter
from random import choices
from random import randint

def main(template_file,parameter_file,possible_parameters_file,size,weights_file,output_file):
	template_dict = {}
	parameter_dict = {}
	possible_parameters = {}
	parameter_numbers = {}

	with open(template_file) as f:
		template_list = f.read().splitlines() 
	
	#Creating the template dictionary and the parameter numbers dictionary
	for i in range(0,len(template_list)):
		splitted = template_list[i].split(' ')
		template_dict[splitted[0]] = splitted[1:]
		parameter_numbers[splitted[0]] = splitted[1:].count('*')

	with open(parameter_file) as f:
		parameter_list = f.read().splitlines()
		
	#Creating the parameter dictionary
	for i in range(0,len(parameter_list)):
		splitted = parameter_list[i].split(" ")
		parameter_dict[splitted[0]] = splitted[1]
	
	#Creating the possible parameters dictionary
	for i in range(1,len(template_list)+1):
		possible_parameters[i] = []
		
	with open(possible_parameters_file) as f:
		parameter_list = f.read().splitlines() 
	
	#Filling the possible parameters dictionary
	for i in range(0,len(parameter_list)):
		line_splitted = parameter_list[i].split()
		for j in range(1,len(line_splitted)):
			if(parameter_dict[line_splitted[j]] not in possible_parameters[int(line_splitted[0])]):
				possible_parameters[int(line_splitted[0])].append(parameter_dict[line_splitted[j]])
	
	#initialization of the population and the probabilities
	population = []
	for i in range(1,len(template_list)+1):
		population.append(i)
		
	with open(weights_file) as f:
		weights_list = f.read().splitlines()

	weights = []
	for i in range(0,len(weights_list)):
		weights.append(float(weights_list[i]))
	
	#Sample generation based on the probability distribution
	samples = choices(population, weights, k=size)

	output_message_list = []
	output_template_list =[]
	
	#Generation of new messages
	for i in range(0,len(samples)):
		template_id = samples[i]
		template_splitted = template_dict[str(template_id)]
		generated_message = ''
		
		for j in range(0,len(template_splitted)):
			if(template_splitted[j] == '*'):
				random = randint(0,len(possible_parameters[template_id])-1)
				if(generated_message != ''):
					generated_message = str(generated_message) + " " + possible_parameters[template_id][random]
				else:
					generated_message = possible_parameters[template_id][random]
			else:
				if(generated_message != ''):
					generated_message = str(generated_message) + " " + template_splitted[j]
				else:
					generated_message = template_splitted[j]
				
		output_message_list.append(generated_message)
	
	#Writing the messages to the output file
	with open(output_file, 'w') as filehandle:
		for item in output_message_list:
			filehandle.write('%s\n' % item)



def commandline_input_handler():
	parser = argparse.ArgumentParser(description=(
		"This script generates log messages\n"
		"\tpython log_generator.py -t \"template_dictionary_example.txt\" -p \"parameter_dictionary_example.txt\" -pp \"possible_parameters_example.txt\" n- 100"),
		formatter_class=argparse.RawDescriptionHelpFormatter
	)

	parser.add_argument("-t", "--template_dictionary", 	help="The file that contains the templates", required=True, default=None)
	parser.add_argument("-p", "--parameter_dictionary", 	help="The file that contains the parameters", required=True, default=None)
	parser.add_argument("-pp", "--possible_parameter", 	help="The file that contains the possible parameters for each template", required=True, default=None)
	parser.add_argument("-n", "--number", 	help="The number of the messages to be generated", required=True, default=None)
	parser.add_argument("-w", "--probability_weights", 	help="The probability of each template", required=True, default=None)
	parser.add_argument("-o", "--output", help="Output file", required=True, default=None)

	args = vars(parser.parse_args())
	
	main(args['template_dictionary'],args['parameter_dictionary'],args['possible_parameter'],int(args['number']),args['probability_weights'],args['output'])
  
if __name__ == '__main__':
   if len(sys.argv) > 1:
      commandline_input_handler()
   else:
      print('No input arguments given. Use -h or --help to see help!')