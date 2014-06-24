def main():
	with open('types.txt', 'r') as inputfile, open('output.txt', 'w') as output:
		for line in inputfile:
			line = line.strip().strip(',').strip("'")
			line = "('" + line + "', '" + line + "'), "
			output.write(line)
#('py', 'Python')
if __name__ == '__main__':
	main()