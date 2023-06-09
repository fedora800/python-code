import re

INPUT_FILE='C:\\mytmp\\file-downloads\\streamer-snip2.txt'
output_file='C:\\mytmp\\file-downloads\\parse_log_file.log'
skipped_file='C:\\mytmp\\file-downloads\\parse_log_skipped.log'

regex_testpattern = re.compile(r"EVENT.*RECV.*SOLACE>>  msgFix.*")

# Output file, where the matched loglines will be copied to
# output_filename = os.path.normpath(output_file)
# Overwrites the file, ensure we're starting out with a blank file
#with open(output_file, encoding='utf8', mode='w') as o_file:
o_file=open(output_file, encoding='utf8', mode='w')
s_file=open(skipped_file, encoding='utf8', mode='w')

# Open input file in 'read' mode
with open(INPUT_FILE, encoding='utf8', mode='r', errors='surrogateescape') as i_file:
    # Loop over each log f_line_rec
    #for f_line_rec in i_file:
    for f_line_num, f_line_rec in enumerate(i_file, 1) :
        # If log f_line_rec matches our regex, print to console, and output file
        if (regex_testpattern.search(f_line_rec)):
            print(f_line_num, ' ', f_line_rec.encode('utf-8', errors='surrogateescape'))
            o_file.write(str(f_line_rec.encode('utf-8', errors='surrogateescape')))
            o_file.write('\n')
        else :
            s_file.write(str(f_line_rec.encode('utf-8', errors='surrogateescape')))
            s_file.write('\n')

# need to check why b' and \n and put at start/end of each output line


