#!/usr/bin/python
# Copyright (c) TurnKey GNU/Linux - http://www.turnkeylinux.org
#
# This file is part of AutoVersion
#
# AutoVersion is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 3 of the License, or (at your
# option) any later version.

"""Map git commits to auto-versions and vice versa

Arguments:

  <commit> := any revision supported by git (e.g., commit ids, tags, refs, etc.)

Options:

  -r --reverse		map version to git commit

Example usage:

  autoversion HEAD                      # print latest version
  autoversion -r v1.0                   # print commit of version v1.0
  autoversion $(git-rev-list --all)     # print all versions

"""
import os
import re
import sys
import help
import getopt

import autoversion

@help.usage(__doc__)
def usage():
    print >> sys.stderr, "Syntax: %s <commit> [ ... ]" % sys.argv[0]
    print >> sys.stderr, "Syntax: %s -r <version> [ ... ]" % sys.argv[0]

def fatal(s):
    print >> sys.stderr, "error: " + str(s)
    sys.exit(1)

def resolve_committish(git, committish):
    # skip expensive git-rev-parse if given a full commit id
    if re.match('[0-9a-f]{40}$', committish):
        return committish

    commit = git.rev_parse(committish)
    if commit is None:
        fatal("invalid committish `%s'" % committish)
    return commit

def main():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], 'rh', ['reverse'])
    except getopt.GetoptError, e:
        usage(e)

    opt_reverse = False
    for opt, val in opts:
        if opt == '-h':
            usage()

        if opt in ('-r', '--reverse'):
            opt_reverse = True

    if not args:
        usage()

    av = autoversion.Autoversion(os.getcwd(), precache=len(args) > 1)

    for arg in args:
        if opt_reverse:
            print av.version2commit(arg)
        else:
            print av.commit2version(resolve_committish(av.git, arg))

if __name__=="__main__":
    main()

