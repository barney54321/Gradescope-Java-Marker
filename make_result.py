import json

def format_name(val):
    val = val.replace("()", "")
    spl = val.split("_")
    name = spl[0]
    score = 1
    hidden = False

    if len(spl) == 3:
        # Both score and hidden
        score = int(spl[1].replace("Score", ""))
        hidden = True

    if len(spl) == 2:
        # Could either be hidden or score
        if spl[1] == "Hidden":
            hidden = True
        else:
            score = int(spl[1].replace("Score", ""))

    return (name, score, hidden)

class Test:
    def __init__(self, line):
        self.line = line
        split = line.split("|")

        if len(split) == 3:
            # Success
            self.result = "Pass"
            self.name, self.score, self.hidden = format_name(split[0])
            self.output = "Pass"
        else:
            self.result = "Fail"
            self.name, self.score, self.hidden = format_name(split[0])

            out = split[3] + "\n"

            i = 0
            for part in split[4].replace("[", "").replace("]", "").split(", "):
                i += 1
                out += part + "\n"

                if i > 10:
                    break

            self.output = out

result = {}

tests = []
passed = 0
score = 0
max_score = 0
failed = False
compiler_output = ""

try:
    with open("/autograder/source/results.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            test = Test(line)
            tests.append(test)
            max_score += test.score
            if test.result == "Pass":
                passed += 1
                score += test.score
except FileNotFoundError as e:
    # No results
    failed = True
    with open("/autograder/source/compiler.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            compiler_output = compiler_output + line + "\n"
    max_score = 100

tests.sort(key=lambda x: x.name)

if not failed:
    result["output"] = "Passed " + str(passed) + " out of " + str(len(tests)) + " test cases. Score: " + str(score) + "/" + str(max_score)
else:
    result["output"] = "Your code did not compile: \n:" + compiler_output
    result["score"] = 0

test_results = []

for test in tests:
    obj = {}

    if test.result == "Pass":
        obj["score"] = test.score
    else:
        obj["score"] = 0

    obj["max_score"] = test.score

    obj["output"] = test.output

    obj["name"] = test.name

    if test.hidden:
        obj["visibility"] = "after_published"
    else:
        obj["visibility"] = "visible"

    test_results.append(obj)

if len(test_results) > 0:
    result["tests"] = test_results

json_string = json.dumps(result, indent=4)
json_file = open("/autograder/source/results.json", "w")
json_file.write(json_string)
json_file.close()