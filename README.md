# Gradescope Java Marker

An automated pipeline for setting up a Gradescope Java autograder.

## Setup
+ Copy your test suite into src/test/java/gradescope
+ Ensure that all your test classes include `package gradescope;` at the top
+ Zip all the contents of the repository
+ Upload the zip to Gradescope as the autograder

## How it works
When the autograder is built, after the initial docker image is loaded, setup.sh is run. This file installs all required dependencies, including curl, zip, unzip, sdkman, java, gradle and python3. This typically takes 1-2 minutes to run.

When a student submits their code, run\_autograder is run. This program starts off by moving student code into the gradle project (specifically into src/main/java/gradescope), and prepends `package gradescope;` to all of their java files. Gradle is run via the gradlew wrapper, and all the test cases are executed. The Gradle `test` task has been modified such that a cleaned version of the results are stored in results.txt. This simply stores the test case names, classes, results and exception information. Once the task is completed, make\_result.py is run, which processes results.txt and produces results.json, which conforms to the Gradescope specification. This file is then moved to autograder/results/, and all the temporary files are deleted.

Students are then presented with all the public test cases and their score. If they have failed any test case(s), those test cases will show the JUnit stacktrace, with the first line stating the error message.

If a submission does not compile, the output from the gradle compileJava task is saved to output.txt, which is processed by make_results.py. The resulting json file then contains the compiler output under the "output" attribute, and has a score of 0.

## Test case format
Test case score and visibility is all set through the naming of test cases. The format of a test case name is as follows: `<name>_[Score<score>]_[Hidden]`. Note that the score and hidden values are optional, with the default being score=1 and hidden=false. Example test cases include `test1()`, which has (name=test1, score=1, hidden=false), `test2_Score4()`, which has (name=test2, score=4, hidden=false), `test3_Hidden()`, which has (name=test3, score=1, hidden=true), and `test4_Score10_Hidden()`, which has (name=test4, score=10, hidden=true).

## Notes
+ Currently packages are not supported (everything must be in default package)
+ Sample I/O test cases have been provided for Hello World
+ Currently students can only submit Java code (everything else is ignored)