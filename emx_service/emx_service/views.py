"""Webcall views dealing with all backend functionality"""
import html
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Reverses signs if a sign is passed in, otherwise copies inital_value
def reverseOrEquals(initial_value, compare_value):
    if compare_value == ">":
        return "<"
    elif compare_value == "<":
        return ">"
    elif compare_value == "=":
        return initial_value
    else:
        raise Exception("Unknown values")

# Solves logical switch puzzle
def puzzleSolver(puzzle_items):
    solution_response = {}
    slots = ["X"]

    # Skip first 2 lines as they are the question asked and ABCD
    # First, walk through each set and collect discovred value
    for y in range(2, len(puzzle_items)):
        did_append = False
        for x in range(1, len(puzzle_items[y])):
            if puzzle_items[y][x] == "<":
                did_append = True
                slots.append("<")
                break
            elif puzzle_items[y][x] == ">":
                did_append = True
                slots.append(">")
                break
        if did_append == False:
            slots.append("=")


    # Second walk though each set and creat new final lists based on the inverse if previous values and extracted ones
    for y in range(2, len(puzzle_items)):
        key = ""
        final_list = []
        for x in range(len(puzzle_items[y])):
            if x == 0:
                key = puzzle_items[y][x]
            elif x == y - 1:
                final_list.append("=")
            elif puzzle_items[y][x] == "-":
                final_list.append(reverseOrEquals(slots[y - 1], slots[x]))
            elif puzzle_items[y][x] == ">":
                final_list.append(">")
            elif puzzle_items[y][x] == "<":
                final_list.append("<")
            elif puzzle_items[y][x] == "=":
                final_list.append("=")
        solution_response[key] = "".join(final_list)


    # Nicley format string in concat map format
    return_string = " ABCD"
    for response in solution_response:
        return_string += "\n{}{}".format(response, solution_response[response])
    return return_string


@csrf_exempt
def EmxPoll(request):
    question = request.GET.get('q')
    description = request.GET.get('d')
    if question == "Ping":
        return HttpResponse("OK")
    elif question == "Status":
        return HttpResponse("Yes, I'm a U.S. Citizen")
    elif question == "Phone":
        return HttpResponse("Cell: (818) 632-5149")
    elif question == "Degree":
        return HttpResponse("Bachelors Degree in Computer Science and Philosophy from the University of California: San Diego")
    elif question == "Name":
        return HttpResponse("Samson Tse")
    elif question == "Resume":
        return HttpResponse("Resume link: https://www.dropbox.com/s/wuoi6tmlz86y27j/samson_resume_2021.pdf?dl=0 || Cover Letter Link: https://www.dropbox.com/s/l0qe1b0yciazq5u/samson_cover_letter_2021.pdf?dl=0")
    elif question == "Years":
        return HttpResponse("I have 5 years of experience with Software Engineering")
    elif question == "Position":
        return HttpResponse("Appying for a Principal Software Engineer Role")
    elif question == "Referrer":
        return HttpResponse("Hacker News/Indeed")
    elif question == "Email Address":
        return HttpResponse("samsonsmtse@gmail.com")
    elif question == "Source":
        return HttpResponse("https://github.com/ChillBroYo/emx")
    elif question == "Puzzle":

        # Split the puzzle into new lines, discard the last new line and pipe it into the solver
        puzzle_items = description.split("\n")
        puzzle_items.pop()
        return HttpResponse(puzzleSolver(puzzle_items))

    return HttpResponse("Unknown Question")

