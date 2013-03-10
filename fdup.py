#!/usr/bin/env python
# Copyright (c) 2012-2013, Pascal Cadotte Michaud
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 3. Neither the name Pascal Cadotte Michaud nor the names
#    of its contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


import os
import sys
import hashlib
from collections import defaultdict
from pprint import pprint


def list_files(base_dir):
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            yield os.path.join(root, file)


def get_md5s_and_names(files):
    for file in files:
        with open(file, 'rb') as f:
            md5 = hashlib.md5()
            md5.update(f.read())
        yield md5.hexdigest(), file


def get_md5s_map(md5s_and_names):
    md5s_map = defaultdict(list)
    for md5, name in md5s_and_names:
        md5s_map[md5].append(name)
    return md5s_map


def get_non_unique_files(md5s_map):
    for file_list in md5s_map.itervalues():
        if len(file_list) > 1:
            yield file_list


def show_non_unique_files(non_unique_file_list):
    for file_list in non_unique_file_list:
        pprint(file_list)


def find_duplicates(root):
    file_generator =  list_files(root)
    md5s_names_generator = get_md5s_and_names(file_generator)
    md5s_map = get_md5s_map(md5s_names_generator)
    non_unique_files = get_non_unique_files(md5s_map)
    show_non_unique_files(non_unique_files)


if __name__ == '__main__':
    root = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    if os.path.isdir(root):
        find_duplicates(root)
    sys.exit(2)
