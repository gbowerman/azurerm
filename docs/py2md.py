'''py2md.py - Simple docs generator for Python code documented to Google docstring standard.'''
import argparse
import glob


def process_file(pyfile_name):
    '''Process a Python source file with Google style docstring comments.

    Reads file header comment, function definitions, function docstrings.
    Returns dictionary encapsulation for subsequent writing.

    Args:
        pyfile_name (str): file name to read.

    Returns:
        dictionary object containing summary comment, with a list of entries for each function.
    '''
    print('Processing file: ' + pyfile_name)

    # load the source file
    with open(pyfile_name) as fpyfile:
        pyfile_str = fpyfile.readlines()

    # meta-doc for a source file
    file_dict = {}

    # get file summary line at the top of the file
    if pyfile_str[0].startswith("'''"):
        file_dict['summary_comment'] = pyfile_str[0][:-1].strip("'")
    else:
        file_dict['summary_comment'] = pyfile_name

    file_dict['functions'] = []
    # find every function definition
    for line in pyfile_str:
        # process definition
        if line.startswith('def '):
            line_num = pyfile_str.index(line)
            fn_def = line[4:]
            fn_name = fn_def.split('(')[0]
            function_info = {'name': fn_name}
            if ')' not in fn_def:
                reached_end = False
                line_num += 1
                while reached_end is False:
                    next_line = pyfile_str[line_num]
                    if ')' in next_line:
                        reached_end = True
                    else:
                        line_num += 1
                    fn_def += next_line
            # get rid of trailing :\n
            fn_def_clean = fn_def.split(':')[0]
            function_info['definition'] = fn_def_clean
            # process docstring
            line_num += 1
            doc_line = pyfile_str[line_num]
            if doc_line.startswith("    '''"):
                comment_str = doc_line[7:]
                if "'''" not in comment_str:
                    reached_end = False
                    line_num += 1
                    while reached_end is False:
                        next_line = pyfile_str[line_num]
                        if "'''" in next_line:
                            reached_end = True
                        comment_str += next_line
                        line_num += 1
                # get rid of trailing '''\n
                comment_str_clean = comment_str.split("'''")[0]
                function_info['comments'] = comment_str_clean
            file_dict['functions'].append(function_info)
    return file_dict


def process_output(meta_file, outfile_name):
    '''Create a markdown format documentation file

    Args:
        meta_file (dict): Dictionary with documentation metadata.
        outfile_name (str): Markdown file to write to.
    '''

    # Markdown title line
    doc_str = '# ' + meta_file['header'] + '\n'

    # Document each meta-file
    for meta_doc in meta_file['modules']:
        doc_str += '## ' + meta_doc['summary_comment'] + '\n'
        for function_info in meta_doc['functions']:
            doc_str += '### ' + function_info['name'] + '\n'
            doc_str += function_info['definition'] + '\n\n'
            if 'comments' in function_info:
                doc_str += '```\n' + function_info['comments'] + '\n```\n\n'

    # write the markdown to file
    print('Writing file: ' + outfile_name)
    out_file = open(outfile_name, 'w')
    out_file.write(doc_str)
    out_file.close()


def main():
    '''Main routine.'''
    # validate command line arguments
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument('--sourcedir', '-s', required=True, action='store',
                            help='Source folder containing python files.')
    arg_parser.add_argument('--docfile', '-o', required=True, action='store',
                            help='Name of markdown file to write output to.')
    arg_parser.add_argument('--projectname', '-n', required=False, action='store',
                            help='Project name (optional, otherwise sourcedir will be used).')

    args = arg_parser.parse_args()

    source_dir = args.sourcedir
    doc_file = args.docfile
    proj_name = args.projectname
    if proj_name is None:
        proj_name = source_dir

    # main document dictionary
    meta_doc = {'header': proj_name + ' Technical Reference Guide'}
    meta_doc['modules'] = []

    # process each file
    for source_file in glob.glob(source_dir + '/*.py'):
        if '__' in source_file:
            print('Skipping: ' + source_file)
            continue
        file_meta_doc = process_file(source_file)
        meta_doc['modules'].append(file_meta_doc)

    # create output file
    process_output(meta_doc, doc_file)


if __name__ == "__main__":
    main()
