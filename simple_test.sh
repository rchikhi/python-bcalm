#!/bin/bash
DIR=`pwd`
mkdir -p scratch 
cd scratch
python $DIR/main.py $DIR/tests/lambda.input.dot output.dot
diff output.dot $DIR/tests/lambda.groundtruth.dot > /dev/null
var=$?
if [ $var -eq 0 ]
then
    echo  PASSED
else
    echo  FAILED
fi


