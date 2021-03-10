import os
from pikepdf import Pdf
from os import listdir
from os.path import isfile, join

def convert_bytes(num):
    """
    this function will convert bytes to MB... GB... etc
    :param num:
    :return:
    """
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0

def file_size(file_path):
    """
    this function will return the file size
    :param file_path:
    :return:
    """
    if os.path.isfile(file_path):
        file_info = os.stat(file_path)
        return convert_bytes(file_info.st_size)


def get_size(file_path):
    """
    this function will return the file size in bytes
    :param file_path:
    :return:
    """
    if os.path.isfile(file_path):
        file_info = os.stat(file_path)
        return file_info.st_size


def merge_files(input_path, list_files, output_file):
    """
    this function will merge pdf files
    :param string, list, string:
    :return:
    """
    pdf = Pdf.new()
    version = pdf.pdf_version
    for _file in list_files:
        src = Pdf.open(input_path + _file)
        pdf.pages.extend(src.pages)
    pdf.save(output_file, min_version=version)

max_size_file = input("Please type maximum size file in MB (default is 10) : ")
if max_size_file is None or len(max_size_file) == 0:
    max_size_file = 10 * 1024 * 1024
else:
    max_size_file = int(max_size_file) * 1024 * 1024

path = input("Please type input folder (default is .) : ")
if path is None or len(path) == 0:
    input_path = '.'
else:
    input_path = ''.join(['./', path, '/'])

folder_output = input("Please type the output folder (default is output) : ")
if folder_output is None or len(folder_output) == 0:
    folder_output = 'output'

if not os.path.isdir('./'+folder_output):
    try:
        os.mkdir('./'+folder_output)
    except OSError:
        print("Creation of the directory %s failed" % folder_output)
    else:
        print("Successfully created the directory %s " % folder_output)

filename = input("Please type the output filename (default is OUTPUT_: ")
if filename is None or len(filename) == 0:
    filename = 'OUTPUT_'

onlyfiles = [f for f in listdir(input_path) if isfile(join(input_path, f)) and f.endswith(".pdf")]
onlyfiles.sort()

counter = 0
accumulator = 0
join_files = []

do_it = False

print('Please wait!')

for index, file in enumerate(onlyfiles):
    # file_path = r"categories_test.csv"
    file_path = file
    size_file = get_size(input_path+file_path)
    # This line is create to limit size files
    # Files needs to be lower than max_size_file (in bytes)
    if accumulator+size_file < max_size_file:
        print(index, file, len(onlyfiles))
        join_files.append(file)
        accumulator += size_file
        do_it = True
    else:
        counter += 1
        output_file = ''.join([folder_output, "/", filename.upper(), str(counter), ".pdf"])
        print("*** MERGE FILES ***", output_file)
        merge_files(input_path, join_files, output_file)
        accumulator = 0
        join_files = []
        do_it = False
if do_it:
    counter += 1
    output_file = ''.join([folder_output, "/", filename.upper(), str(counter), ".pdf"])
    print("*** MERGE FILES ***", output_file)
    merge_files(input_path, join_files, output_file)

print('DID IT!')