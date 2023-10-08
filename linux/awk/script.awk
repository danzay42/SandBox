#!/usr/bin/env -S awk -f

BEGIN {
    print "start script"
}

{
    print "processing" $0
}

END {
    print "finish script"
}