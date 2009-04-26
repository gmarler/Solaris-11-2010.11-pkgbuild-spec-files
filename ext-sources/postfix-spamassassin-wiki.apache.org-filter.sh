#!/bin/bash

# source: http://wiki.apache.org/spamassassin/IntegratedSpamdInPostfix
# changes: changed from /bin/sh to /bin/bash, logger remove -s, /usr/sbin/sendmail.postfix
# tom68@users.sourceforge.net

# filter.sh
#
# This script redirects mail flagged as spam to a separate account
# You must first create a user account named "spamvac" to hold the flagged mail

SENDMAIL="/usr/sbin/sendmail.postfix -i"
SPAMASSASSIN=/usr/bin/spamc
COMMAND="$SENDMAIL $@"
#If your SQL preferences set to "user"
USER=`echo $COMMAND | awk '{ print $NF }' | sed 's/@.*$//'`
#If your SQL preferences set to "user@domain"
#USER=`echo $COMMAND | awk '{ print $NF }'`

NEW_COMMAND=`echo $COMMAND | awk '{ $6 = "spamvac"; NF = 6; print }'`

    /usr/bin/logger -p mail.warning -t filter "filter.sh called with $*"
# Exit codes from <sysexits.h>
EX_TEMPFAIL=75
EX_UNAVAILABLE=69
umask 077

OUTPUT="`mktemp /tmp/mailfilter.XXXXXXXXXX`"

if [ "$?" != 0 ]; then
    /usr/bin/logger -p mail.warning -t filter "Unable to create temporary file."
    exit $EX_TEMPFAIL
fi

# Clean up when done or when aborting.
trap "rm -f $OUTPUT" EXIT TERM

$SPAMASSASSIN -x -E -u $USER > $OUTPUT
return="$?"
if [ "$return" = 1 ]; then
    $NEW_COMMAND < $OUTPUT
    exit $?
elif [ "$return" != 0 ]; then
    /usr/bin/logger -p mail.warning -t filter "Temporary SpamAssassin failure (spamc returned $return)"
    exit $EX_TEMPFAIL
fi

$SENDMAIL "$@" < $OUTPUT
exit $?

