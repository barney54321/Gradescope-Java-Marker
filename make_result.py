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
            self.output = split[3] + "\n" + split[4]

result = {}

tests = []
passed = 0
score = 0
max_score = 0

with open("results.txt", "r") as f:
    lines = f.readlines()
    for line in lines:
        test = Test(line)
        tests.append(test)
        max_score += test.score
        if test.result == "Pass":
            passed += 1
            score += test.score

tests.sort(key=lambda x: x.name)

result["output"] = "Passed " + str(passed) + " out of " + str(len(tests)) + " test cases. Score: " + str(score) + "/" + str(max_score)

test_results = []

for test in tests:
    obj = {}

    if test.result == "Pass":
        obj["score"] = test.score
    else:
        obj["score"] = 0

    obj["max_score"] = test.score

    obj["output"] = test.output

    if test.hidden:
        obj["visibility"] = "after_published"
    else:
        obj["visibility"] = "visible"

    test_results.append(obj)

result["tests"] = test_results

json_string = json.dumps(result, indent=4)
json_file = open("results.json", "w")
json_file.write(json_string)
json_file.close()