#!/usr/bin/env python3

import os
from pathlib import Path
import re
import shutil
import sys

__projectdir__ = Path(os.path.dirname(os.path.realpath(__file__)) + '')

sys.path.append(str(__projectdir__ / 'submodules/infrep/'))
from infrep_func import infrep_main

# Main Function:{{{1
def replacecommonsections(codelist, folder_commonsections, allextension = '.all'):
    """
        

    allextension needs to begin with a "." for it to work.
    """
    
    if not os.path.isdir(folder_commonsections):
        raise ValueError('The folder containing the common sections does not exist.')

    infreplist = []
    for filename_commonsection in os.listdir(folder_commonsections):
        fullfilename_commonsection = os.path.join(folder_commonsections, filename_commonsection)

        if not os.path.isfile(fullfilename_commonsection):
            raise ValueError('All the elements of the common section folder should be files.')

        # get text in filename
        with open(fullfilename_commonsection) as f:
            commonsection = f.read()
        if commonsection[-1] != '\n':
            commonsection = commonsection + '\n'
        commonsectionsplit = commonsection.split('\n')
        firstline = commonsectionsplit[0]
        lastline = commonsectionsplit[-2]

        extension = os.path.splitext(fullfilename_commonsection)[1]
        if extension == '.all':
            codelist_extension = codelist
        else:
            codelist_extension = [codefile for codefile in codelist if str(codefile).endswith(extension)]

        inputterm = re.compile(re.escape(firstline) + "(.*?)" + re.escape(lastline) + '\n', re.DOTALL)

        infreplist.append({'inputterm': inputterm, 'outputterm': commonsection, 'filenames': codelist_extension, 'inputmethod': 'recompiled'})

    infrep_main(infreplist)


# Test:{{{1
def commonsectiontest():
    if os.path.isdir(__projectdir__ / 'test'):
        shutil.rmtree(__projectdir__ / 'test')

    os.mkdir(__projectdir__ / 'test')
    os.mkdir(__projectdir__ / 'test/code')
    os.mkdir(__projectdir__ / 'test/commonsections')

    # create common section files
    with open(__projectdir__ / 'test/commonsections/code.txt', 'w+') as f:
        f.write('text_start.\n123\ntext_end.')
    with open(__projectdir__ / 'test/commonsections/code.all', 'w+') as f:
        f.write('all_start.\n234\nall_end.\n')

    # create code on which to do replace
    with open(__projectdir__ / 'test/code/file1.txt', 'w+') as f:
        f.write('text_start.\nabc\ntext_end.\ntext_start.\n123\ntext_end.\nall_start.\nbcd\nall_end.\n')
    with open(__projectdir__ / 'test/code/file2.other', 'w+') as f:
        f.write('text_start.\nabc\ntext_end.\nall_start.\nbcd\nall_end.\n')

    replacecommonsections([__projectdir__ / Path('test/code/file1.txt'), __projectdir__ / Path('test/code/file2.other')], __projectdir__ / 'test/commonsections', allextension = '.all')

    # verify done correctly
    with open(__projectdir__ / 'test/code/file1.txt') as f:
        text = f.read()
        if text != 'text_start.\n123\ntext_end.\ntext_start.\n123\ntext_end.\nall_start.\n234\nall_end.\n':
            print('File1 text:')
            print(text)
            raise ValueError('Bad match for file1.txt')
    with open(__projectdir__ / 'test/code/file2.other') as f:
        text = f.read()
        if text != 'text_start.\nabc\ntext_end.\nall_start.\n234\nall_end.\n':
            print('File2 text:')
            print(text)
            raise ValueError('Bad match for file2.txt')


