#!/bin/bash

VERSION=$1
COMPARE=$2
TESTNAME=$3
GALFIT="../exec/galfitm-"$VERSION

function compare {
    if ! diff -q $1 $2 > /dev/null ; then
	echo "BAD?: ${2} differs from ${1}"
    else
	echo "GOOD: ${2} identical to ${1}"
    fi
}

function test_galfitm {
    INFEEDME=$1
    TEST=$2
    # run galfit and record results
    echo; echo "Testing $GALFIT $INFEEDME"
    OUTFEEDME=${INFEEDME}.$VERSION
    OUTPUTFULL=${INFEEDME/feedme/outputfull}.$VERSION
    OUTPUT=${INFEEDME/feedme/output}.$VERSION
    OUTLOG=${INFEEDME/feedme/log}.$VERSION
    rm -f */*.galfit.01 fit.log
    $GALFIT $INFEEDME &> $OUTPUTFULL
    cat $OUTPUTFULL | tail -10 &> $OUTPUT
    mv -f */*.galfit.01 $OUTFEEDME &> /dev/null
    mv -f fit.log $OUTLOG &> /dev/null
    if [ $? -ne 0 ] ; then
	echo "BAD?: failed to run $GALFIT $INFEEDME"
    fi
    # compare results with previous
    if [ "$TEST" = "" ] ; then
	TEST=`ls ${INFEEDME}.*.* | sort -t. -k 3,3n -k 4,4n -k 5,5n -k 6,6n -k 7,7n -k 8,8n -k 9,9n | grep -v ${OUTFEEDME} | tail -1`
    else
	TEST=${INFEEDME}.$TEST
    fi
    if [ "$TEST" = "" ] ; then
	echo "BAD?: no previous output to compare to"
    else
	compare ${TEST/feedme/log} $OUTLOG
	compare $TEST $OUTFEEDME
	compare ${TEST/feedme/output} $OUTPUT
    fi
}


# Simple tests

FEEDME_LIST=`ls simple/*${TESTNAME}*feedme | grep -v many`
for FEEDME in $FEEDME_LIST
do
    test_galfitm $FEEDME $COMPARE 2> /dev/null
done


# Wrapping tests

FEEDME_LIST=`ls wrapping/*${TESTNAME}*feedme`
for FEEDME in $FEEDME_LIST
do
    test_galfitm $FEEDME $COMPARE 2> /dev/null
done
