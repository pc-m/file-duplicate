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

import argparse
import hashlib
import os
import sys


def list_files(base_dir):
    for root, _, files in os.walk(base_dir):
        for filename in files:
            yield os.path.abspath(os.path.join(root, filename))


def get_md5s_and_names(files):
    for filename in files:
        with open(filename, 'rb') as f:
            md5 = hashlib.md5()
            md5.update(f.read())
        yield md5.hexdigest(), filename


def get_non_unique_files(md5s_names):
    unique_md5s = set()
    for md5, name in md5s_names:
        if md5 not in unique_md5s:
            unique_md5s.add(md5)
        else:
            yield name


def show_non_unique_files(non_unique_files):
    for filename in non_unique_files:
        sys.stdout.write(filename + '\x00')


def find_duplicates(root):
    (show_non_unique_files
     (get_non_unique_files
      (get_md5s_and_names
       (list_files(root)))))


def _new_argument_parser():
    parser = argparse.ArgumentParser(
        'Finds file duplicate in a directory tree based on md5sum'
    )
    parser.add_argument(
        'root', nargs='?', help='Directory to scan', default=os.getcwd()
    )
    return parser


if __name__ == '__main__':
    parser = _new_argument_parser()
    args = parser.parse_args()
    root = args.root
    if os.path.isdir(root):
        find_duplicates(root)
    else:
        sys.exit(2)
