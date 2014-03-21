#!/bin/bash

VERSION=$1
COMPARE=$2
GALFIT="../exec/galfitm-"$VERSION

function compare {
    if ! diff -q $1 $2 > /dev/null ; then
	echo "${2} differs from ${1}"
    fi
}

function test_galfitm {
    INFEEDME=$1
    TEST=$2
    # run galfit and record results
    echo "Testing $GALFIT $INFEEDME"
    OUTFEEDME=${INFEEDME}.$VERSION
    OUTPUT=${INFEEDME/feedme/output}.$VERSION
    OUTLOG=${INFEEDME/feedme/log}.$VERSION
    rm -f galfit.01 fit.log
    $GALFIT $INFEEDME &> $OUTPUT
    mv -f galfit.01 $OUTFEEDME &> /dev/null
    mv -f fit.log $OUTLOG &> /dev/null
    if [ $? -ne 0 ] ; then
	echo "$GALFIT $INFEEDME : FAILED TO RUN"
    fi
    # compare results with previous
    if [ "$TEST" = "" ] ; then
	PREVFEEDMES=`ls -t ${INFEEDME}.* 2> /dev/null`
	TEST=`${PREVFEEDMES}| grep -v ${OUTFEEDME} | head -1`
    else
	TEST=${INFEEDME}.$TEST
    fi
    if [ "$TEST" = "" ] ; then
	echo "No previous output to compare to!"
    else
	compare ${TEST/feedme/log} $OUTLOG
	compare $TEST $OUTFEEDME
	compare ${TEST/feedme/output} $OUTPUT
    fi
}


# Simple tests

FEEDME_LIST=`ls simple/*feedme | grep -v many`
for FEEDME in $FEEDME_LIST
do
    test_galfitm $FEEDME $COMPARE
done
