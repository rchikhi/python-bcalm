#!/bin/bash
mkdir -p scratch 
cd scratch
python ../main.py ../tests/lambda.input.dot output.dot
diff output.dot ../tests/lambda.groundtruth.dot > /dev/null
var=$?
if [ $var -eq 0 ]
then
    echo  PASSED
else
    echo  FAILED
fi


