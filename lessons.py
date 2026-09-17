VIDEOS = {
    # full CS50P lectures 
    "lecture0": {"title": "CS50P Lecture 0 - Functions, Variables", "url": "https://youtu.be/JP7ITIXGpHk", "file": None},
    "lecture1": {"title": "CS50P Lecture 1 - Conditionals", "url": "https://youtu.be/_b6NgY_pMdw", "file": None},
    "lecture2": {"title": "CS50P Lecture 2 - Loops", "url": "https://youtu.be/-7xg8pGcP6w", "file": None},
    "lecture3": {"title": "CS50P Lecture 3 - Exceptions", "url": "https://youtu.be/LW7g1169v7w", "file": None},
    "lecture4": {"title": "CS50P Lecture 4 - Libraries", "url": "https://youtu.be/MztLZWibctI", "file": None},
    # CS50P shorts
    "functions": {"title": "Functions - CS50P Shorts", "url": "https://youtu.be/lGS6O47debI", "file": None},
    "variables": {"title": "Variables - CS50P Shorts", "url": "https://youtu.be/ylhcZZ7O3Tk", "file": None},
    "return_values": {"title": "Return Values - CS50P Shorts", "url": "https://youtu.be/AetGXMcNU3M", "file": None},
    "string_methods": {"title": "String Methods - CS50P Shorts", "url": "https://youtu.be/f4_ZPwvKF5g", "file": None},
    "conditionals": {"title": "Conditionals - CS50P Shorts", "url": "https://youtu.be/vGr1tvjqWs0", "file": None},
    "boolean_expressions": {"title": "Boolean Expressions - CS50P Shorts", "url": "https://youtu.be/51BNn5Ojupw", "file": None},
    "while_loops": {"title": "While Loops - CS50P Shorts", "url": "https://youtu.be/CYobbeiGgp8", "file": None},
    "for_loops": {"title": "For Loops - CS50P Shorts", "url": "https://youtu.be/iTRBRXOMzeM", "file": None},
    "lists": {"title": "Lists - CS50P Shorts", "url": "https://youtu.be/xdpABsJZQYU", "file": None},
    "dictionaries": {"title": "Dictionaries - CS50P Shorts", "url": "https://youtu.be/yPyFlO8G6rw", "file": None},
    "handling_exceptions": {"title": "Handling Exceptions - CS50P Shorts", "url": "https://youtu.be/wjWMOYLNK_E", "file": None},
    "raising_exceptions": {"title": "Raising Exceptions - CS50P Shorts", "url": "https://youtu.be/BltXeMM96DA", "file": None},
    "random": {"title": "random - CS50P Shorts", "url": "https://youtu.be/yec-UUauUV8", "file": None},
    "creating_modules_packages": {"title": "Creating Modules and Packages - CS50P Shorts", "url": "https://youtu.be/imrloYMePL0", "file": None},
}
LESSONS = {
    1: {
        "title": "Functions and Variables",
        "videos": ["lecture0", "functions", "variables", "return_values"],
        "steps": [
            {"type": "teach", "text":
             "💬 *Lesson 1: Functions and Variables* (CS50P Week 0)\n\n"
             "A *function* is an action Python already knows. *print* shows text:\n\n"
             "print(\"hello, world\")\n\n"
             "Text in quotes is a *string*. What goes inside ( ) is an *argument*."},
            {"type": "video", "video": "functions",
             "text": "📺 Watch this short video first (about 5 minutes), then we'll practise:"},
            {"type": "question",
             "text": "Write this on paper:\n\nprint(\"hello,\", \"Ada\")\n\n"
                     "When print gets two arguments, it puts a space between them.\n"
                     "What does it show? Type it exactly.",
             "answers": ["hello, Ada", "\"hello, Ada\""],
             "wrong": {"hello,ada": "print adds a *space* between its arguments. Where does it go?",
                       "hello, \"ada\"": "The quotes aren't shown - they only mark where the text starts and ends.",
                       "\"hello,\", \"ada\"": "That's the code. What appears on the screen when it runs?"},
             "hint": "Write hello, then one space, then Ada. No quotes.",
             "video": "functions"},
            {"type": "teach", "text":
             "A *variable* is a labelled box that holds a value.\n\n"
             "name = input(\"What's your name? \")\n"
             "print(\"hello,\", name)\n\n"
             "*input* waits for the user to type. Whatever they type goes into the box *name*."},
            {"type": "choice",
             "text": "The user types Ada. What does this print?\n\n"
                     "name = input(\"What's your name? \")\n"
                     "print(\"hello, name\")",
             "options": [("hello, name", "hello, name"), ("hello, ada", "hello, Ada"), ("error", "an error")],
             "answer": "hello, name",
             "wrong": {"hello, ada": "The famous trap! 🎯\n\n\"hello, name\" is all inside the quotes, so *name* is just text.\n\n"
                                     "To use the box, take it out of the quotes:\nprint(\"hello,\", name)",
                       "error": "No error - Python happily prints the text inside the quotes, exactly as written."},
             "video": "variables"},
            {"type": "teach", "text":
             "Tidy what the user typed with *methods*:\n\n"
             "name = input(\"Name? \").strip().title()\n\n"
             "*strip()* removes spaces from both ends.\n"
             "*title()* Capitalises The First Letter Of Each Word.\n\n"
             "An *f-string* puts a variable inside text:\n"
             "print(f\"hello, {name}\")"},
            {"type": "choice",
             "text": "The user types:   ada lovelace   (with spaces around it)\n\n"
                     "name = input(\"Name? \").strip().title()\n\n"
                     "What is in the box *name* now?",
             "options": [("title", "Ada Lovelace"), ("lower", "ada lovelace"), ("upper", "ADA LOVELACE")],
             "answer": "title",
             "wrong": {"lower": "title() changes it: it capitalises the first letter of *each word*.",
                       "upper": "That would be upper(). title() only capitalises the first letter of each word."},
             "video": "string_methods"},
            {"type": "teach", "text":
             "⚠️ *input always gives you text.*\n\n"
             "x = input(\"x? \")   ← user types 1\n"
             "y = input(\"y? \")   ← user types 2\n"
             "print(x + y)\n\n"
             "This prints *12*, because + on text *joins* it.\n\n"
             "The fix is *int*, which turns text into a whole number:\n"
             "x = int(input(\"x? \"))"},
            {"type": "question",
             "text": "Now with int:\n\n"
                     "x = int(input(\"x? \"))   ← user types 1\n"
                     "y = int(input(\"y? \"))   ← user types 2\n"
                     "print(x + y)\n\n"
                     "What prints?",
             "answers": ["3"],
             "wrong": {"12": "That's what happens *without* int(). Here int turns \"1\" into the number 1, so + adds.",
                       "1 2": "print(x + y) prints one thing: the result of x + y."},
             "hint": "int turns the text into numbers. So this is 1 + 2.",
             "video": "variables"},
            {"type": "teach", "text":
             "Make your own function with *def*:\n\n"
             "def square(n):\n"
             "    return n * n\n\n"
             "print(square(3))\n\n"
             "*n* is a parameter: it holds whatever is passed in, here 3.\n"
             "*return* hands the result back, so this prints 9."},
            {"type": "video", "video": "return_values",
             "text": "📺 Optional: this short explains return values another way."},
            {"type": "question",
             "text": "Trace it on paper:\n\n"
                     "def square(n):\n"
                     "    return n * n\n\n"
                     "x = square(4)\n"
                     "print(x + 1)\n\n"
                     "What prints?",
             "answers": ["17"],
             "wrong": {"16": "square(4) gives 16 and stores it in x. But then we print x + 1.",
                       "5": "square(4) returns 4 * 4, not 4. What's in x?",
                       "9": "This time n is 4, not 3."},
             "hint": "First work out square(4) = 4 * 4. Put that in box x. Then add 1.",
             "video": "return_values"},
            {"type": "paper",
             "text": "🎉 Final task for Lesson 1.\n\n"
                     "On paper, write a program that:\n"
                     "1. defines a function *double(n)* that returns n * 2\n"
                     "2. asks the user for a number and turns it into an int, stored in *x*\n"
                     "3. prints double(x)\n\n"
                     "📷 Photograph it (dark pen, good light, camera straight above)\n"
                     "- or just type your code instead.",
             "patterns": [r"def\s+double\s*\(\s*n\s*\)\s*:",
                          r"return\s+(n\s*\*\s*2|2\s*\*\s*n|n\s*\+\s*n)",
                          r"x\s*=\s*int\s*\(\s*input\s*\(",
                          r"print\s*\(\s*double\s*\(\s*x\s*\)\s*\)"],
             "pattern_hints": ["Start the function with:  def double(n):",
                               "Inside it, send the answer back:  return n * 2",
                               "Get the number:  x = int(input(\"Number? \"))",
                               "Show the result:  print(double(x))"],
             "video": "functions"},
        ],
    },
    2: {
        "title": "Conditionals",
        "videos": ["lecture1", "conditionals", "boolean_expressions"],
        "steps": [
            {"type": "teach", "text":
             "🔀 *Lesson 2: Conditionals* (CS50P Week 1)\n\n"
             "Programs choose with *if*:\n\n"
             "if x < y:\n"
             "    print(\"x is less than y\")\n"
             "elif x > y:\n"
             "    print(\"x is greater than y\")\n"
             "else:\n"
             "    print(\"x is equal to y\")\n\n"
             "Note the colons : and the indented lines."},
            {"type": "video", "video": "conditionals",
             "text": "📺 Watch this short video first, then we'll practise:"},
            {"type": "question",
             "text": "Trace it with x = 5 and y = 5. What prints?",
             "answers": ["x is equal to y"],
             "wrong": {"x is less than y": "Is 5 < 5? No - equal isn't less. Python moves on to elif.",
                       "x is greater than y": "Is 5 > 5? No. Both tests are False, so else runs."},
             "hint": "Check each test in order. If none is True, the else part runs.",
             "video": "conditionals"},
            {"type": "teach", "text":
             "Comparisons:\n\n"
             "==  equal        !=  not equal\n"
             "<   less         >   greater\n"
             "<=  at most      >=  at least\n\n"
             "*One* = puts a value in a box. *Two* == compares.\n\n"
             "Copy this table onto paper."},
            {"type": "question",
             "text": "Fill in the blank so it prints \"even\" when n is 4:\n\n"
                     "if n % 2 ___ 0:\n"
                     "    print(\"even\")\n\n"
                     "(% gives the remainder: 4 % 2 is 0.)\n\n"
                     "Type just the missing symbol.",
             "answers": ["=="],
             "wrong": {"=": "One = puts a value in a box. To *compare*, you need two: ==",
                       "===": "Python uses exactly two equals signs: ==",
                       "!=": "That means 'not equal'. We want the remainder to *be* 0."},
             "hint": "You want to test whether the remainder *equals* 0. Two equals signs.",
             "video": "conditionals"},
            {"type": "teach", "text":
             "Join tests with *and* / *or*:\n\n"
             "if score >= 90 and score <= 100:\n"
             "    print(\"A\")\n\n"
             "*and* - both sides must be True.\n"
             "*or* - at least one side must be True."},
            {"type": "choice",
             "text": "score = 95. Which test is True?\n\n"
                     "A) score > 90 and score < 95\n"
                     "B) score < 90 or score > 94\n"
                     "C) score == 90 or score == 100",
             "options": [("a", "A"), ("b", "B"), ("c", "C")],
             "answer": "b",
             "wrong": {"a": "*and* needs both sides True. Is 95 < 95? No - so A is False.",
                       "c": "95 is neither 90 nor 100, so both sides are False. *or* needs at least one True."},
             "video": "boolean_expressions"},
            {"type": "teach", "text":
             "*match* compares one value against several:\n\n"
             "match name:\n"
             "    case \"Harry\" | \"Hermione\" | \"Ron\":\n"
             "        print(\"Gryffindor\")\n"
             "    case \"Draco\":\n"
             "        print(\"Slytherin\")\n"
             "    case _:\n"
             "        print(\"Who?\")\n\n"
             "| means \"or\". *case _* catches everything else."},
            {"type": "question",
             "text": "Using that program, what prints if name is \"Luna\"?",
             "answers": ["Who?", "who"],
             "wrong": {"gryffindor": "Luna isn't one of Harry, Hermione or Ron. Check the next case.",
                       "slytherin": "Luna isn't Draco either. What catches everything else?",
                       "nothing": "case _ catches anything the other cases didn't match."},
             "hint": "Neither case matches Luna, so the last case, case _, runs.",
             "video": "conditionals"},
            {"type": "paper",
             "text": "🎉 Final task for Lesson 2.\n\n"
                     "On paper, write a program that:\n"
                     "1. asks for an age and stores it as an int in *age*\n"
                     "2. if age is 18 or more, prints \"adult\"\n"
                     "3. otherwise prints \"minor\"\n\n"
                     "Don't forget the colons and indentation!\n"
                     "📷 Photograph it - or just type your code instead.",
             "patterns": [r"age\s*=\s*int\s*\(\s*input\s*\(",
                          r"if\s+(age\s*>=\s*18|18\s*<=\s*age|age\s*>\s*17)\s*:",
                          r"print\s*\(\s*[\"']adult[\"']\s*\)",
                          r"else\s*:",
                          r"print\s*\(\s*[\"']minor[\"']\s*\)"],
             "pattern_hints": ["Line 1:  age = int(input(\"Age? \"))",
                               "The test needs a colon:  if age >= 18:",
                               "Inside the if:  print(\"adult\")",
                               "Then:  else:  (with a colon)",
                               "Inside the else:  print(\"minor\")"],
             "video": "conditionals"},
        ],
    },
    3: {
        "title": "Loops",
        "videos": ["lecture2", "while_loops", "for_loops", "lists", "dictionaries"],
        "steps": [
            {"type": "teach", "text":
             "🔁 *Lesson 3: Loops* (CS50P Week 2)\n\n"
             "A *while* loop repeats as long as its test is True:\n\n"
             "i = 0\n"
             "while i < 3:\n"
             "    print(\"meow\")\n"
             "    i += 1\n\n"
             "*i += 1* is short for i = i + 1."},
            {"type": "video", "video": "while_loops",
             "text": "📺 Watch this short video first, then we'll practise:"},
            {"type": "question",
             "text": "How many times does it print meow?\n\nTrace the box i on paper: 0, 1, ...",
             "answers": ["3", "three"],
             "wrong": {"4": "When i reaches 3, is 3 < 3? No - the loop stops before a 4th meow.",
                       "2": "Count again: i = 0, 1 and 2 all pass the test.",
                       "forever": "It would, without i += 1. Here i grows by 1 each time."},
             "hint": "Write i = 0, 1, 2, 3 on paper. For each one, is i < 3?",
             "video": "while_loops"},
            {"type": "choice",
             "text": "What happens if we delete the line  i += 1 ?",
             "options": [("3 times", "prints 3 times"), ("nothing", "prints nothing"), ("forever", "never stops")],
             "answer": "forever",
             "wrong": {"3 times": "Without i += 1, i stays 0 - and 0 < 3 is True every single time.",
                       "nothing": "0 < 3 is True, so it prints... and i never changes."},
             "video": "while_loops"},
            {"type": "teach", "text":
             "A *for* loop is shorter:\n\n"
             "for _ in range(3):\n"
             "    print(\"meow\")\n\n"
             "*range(3)* gives 0, 1, 2 - three numbers, starting at 0.\n"
             "*_* means \"I don't need the number\"."},
            {"type": "question",
             "text": "for i in range(4):\n"
                     "    print(i)\n\n"
                     "Type the numbers it prints, e.g. `1 2 3`",
             "answers": ["0 1 2 3", "0123", "0,1,2,3", "0, 1, 2, 3"],
             "wrong": {"1 2 3 4": "range starts at 0, not 1.",
                       "0 1 2 3 4": "range(4) stops *before* 4. It gives four numbers."},
             "hint": "range(4) gives four numbers, starting at 0.",
             "video": "for_loops"},
            {"type": "teach", "text":
             "A *list* holds many values in order:\n\n"
             "students = [\"Hermione\", \"Harry\", \"Ron\"]\n"
             "for student in students:\n"
             "    print(student)\n\n"
             "Positions count from 0: students[0] is \"Hermione\".\n"
             "*len(students)* is how many items: 3."},
            {"type": "question",
             "text": "students = [\"Hermione\", \"Harry\", \"Ron\"]\n"
                     "print(students[1])\n"
                     "print(len(students))\n\n"
                     "Type both things it prints, e.g. `Ada 5`",
             "answers": ["Harry 3", "harry, 3", "harry,3"],
             "wrong": {"hermione 3": "Lists count from 0. students[0] is Hermione, so students[1] is...",
                       "harry 2": "len counts every item: Hermione, Harry, Ron.",
                       "hermione 2": "Two things to check: positions start at 0, and len counts every item."},
             "hint": "Number them: 0 Hermione, 1 Harry, 2 Ron. How many are there?",
             "video": "lists"},
            {"type": "teach", "text":
             "A *dictionary* pairs *keys* with *values*:\n\n"
             "houses = {\"Harry\": \"Gryffindor\", \"Draco\": \"Slytherin\"}\n"
             "print(houses[\"Draco\"])\n\n"
             "This prints Slytherin. You look things up by key, not by position."},
            {"type": "question",
             "text": "houses = {\"Harry\": \"Gryffindor\", \"Draco\": \"Slytherin\"}\n"
                     "houses[\"Luna\"] = \"Ravenclaw\"\n"
                     "print(len(houses))\n\n"
                     "What prints?",
             "answers": ["3", "three"],
             "wrong": {"2": "The middle line *adds* a new key, Luna. Count the keys now."},
             "hint": "Count the keys after the middle line: Harry, Draco, and...",
             "video": "dictionaries"},
            {"type": "paper",
             "text": "🎉 Final task for Lesson 3.\n\n"
                     "On paper, write a program that uses a *for* loop and *range* to print\n"
                     "#\n#\n#\n"
                     "(a # on three lines).\n\n"
                     "📷 Photograph it - or just type your code instead.",
             "patterns": [r"for\s*\w+\s+in\s+range\s*\(\s*3\s*\)\s*:",   # \s* not \s+: "for _" often reads as "for_"
                          r"print\s*\(\s*[\"']#[\"']\s*\)"],
             "pattern_hints": ["Start the loop with:  for _ in range(3):",
                               "Inside the loop (indented):  print(\"#\")"],
             "video": "for_loops"},
        ],
    },
    4: {
        "title": "Exceptions",
        "videos": ["lecture3", "handling_exceptions", "raising_exceptions"],
        "steps": [
            {"type": "teach", "text":
             "⚠️ *Lesson 4: Exceptions* (CS50P Week 3)\n\n"
             "Some errors only happen while the program runs:\n\n"
             "x = int(input(\"What's x? \"))\n\n"
             "If the user types *cat*, int can't turn it into a number, so Python stops with a *ValueError*."},
            {"type": "video", "video": "handling_exceptions",
             "text": "📺 Watch this short video first, then we'll practise:"},
            {"type": "question",
             "text": "The program runs  x = int(input(\"x? \"))\n\n"
                     "Which of these inputs make it crash?\n\n"
                     "A) 42\nB) cat\nC) -7\nD) 3.5\n\n"
                     "Type the letters, e.g. `A C`",
             "answers": ["B D", "BD", "B, D", "B,D", "D B"],
             "wrong": {"b": "One more: int(\"3.5\") fails too - int only accepts whole numbers.",
                       "d": "One more: cat isn't a number at all.",
                       "b c": "-7 is a whole number, so int handles it fine. Look at D again.",
                       "b c d": "-7 is a whole number, so int handles it fine."},
             "hint": "int accepts whole numbers only, positive or negative.",
             "video": "handling_exceptions"},
            {"type": "teach", "text":
             "Catch the error with *try* and *except*:\n\n"
             "try:\n"
             "    x = int(input(\"What's x? \"))\n"
             "except ValueError:\n"
             "    print(\"x is not an integer\")\n"
             "else:\n"
             "    print(f\"x is {x}\")\n\n"
             "*else* runs only if nothing went wrong in try."},
            {"type": "choice",
             "text": "The user types cat. What prints?",
             "options": [("not an integer", "x is not an integer"), ("x is cat", "x is cat"), ("both", "both lines")],
             "answer": "not an integer",
             "wrong": {"x is cat": "int(\"cat\") fails *inside* try, so Python jumps to except. else never runs.",
                       "both": "else only runs when try had *no* error."},
             "video": "handling_exceptions"},
            {"type": "teach", "text":
             "Keep asking until the input is good:\n\n"
             "while True:\n"
             "    try:\n"
             "        x = int(input(\"What's x? \"))\n"
             "    except ValueError:\n"
             "        print(\"x is not an integer\")\n"
             "    else:\n"
             "        break\n\n"
             "*break* leaves the loop."},
            {"type": "question",
             "text": "The user types: cat, then dog, then 7.\n\n"
                     "How many times does it print \"x is not an integer\"?",
             "answers": ["2", "two"],
             "wrong": {"3": "The third input, 7, works - so else runs and break ends the loop.",
                       "1": "Both cat and dog fail. Count again.",
                       "0": "cat and dog both fail inside try, so except runs for each."},
             "hint": "Go through each input: does int() work on it?",
             "video": "handling_exceptions"},
            {"type": "teach", "text":
             "Put it in a function, and use *pass* to stay quiet on errors:\n\n"
             "def get_int(prompt):\n"
             "    while True:\n"
             "        try:\n"
             "            return int(input(prompt))\n"
             "        except ValueError:\n"
             "            pass\n\n"
             "*pass* means \"do nothing\", so the loop simply asks again."},
            {"type": "paper",
             "text": "🎉 Final task for Lesson 4.\n\n"
                     "On paper, write a program that:\n"
                     "1. tries  x = int(input(\"x? \"))\n"
                     "2. on a ValueError, prints \"not a number\"\n"
                     "3. otherwise prints x\n\n"
                     "📷 Photograph it - or just type your code instead.",
             "patterns": [r"try\s*:",
                          r"x\s*=\s*int\s*\(\s*input\s*\(",
                          r"except\s+ValueError\s*:",
                          r"print\s*\(\s*[\"']not a number[\"']\s*\)",
                          r"print\s*\(\s*(x|f[\"'][^\"']*\{\s*x\s*\}[^\"']*[\"'])\s*\)"],
             "pattern_hints": ["Start with:  try:",
                               "Inside try:  x = int(input(\"x? \"))",
                               "Catch it:  except ValueError:",
                               "Inside except:  print(\"not a number\")",
                               "Then:  else:  and inside it  print(x)"],
             "video": "handling_exceptions"},
        ],
    },
    5: {
        "title": "Libraries",
        "videos": ["lecture4", "random", "creating_modules_packages"],
        "steps": [
            {"type": "teach", "text":
             "📚 *Lesson 5: Libraries* (CS50P Week 4)\n\n"
             "A *library* is code someone already wrote. Load it with *import*:\n\n"
             "import random\n"
             "coin = random.choice([\"heads\", \"tails\"])\n"
             "print(coin)\n\n"
             "*random.choice* picks one item at random."},
            {"type": "video", "video": "random",
             "text": "📺 Watch this short video first, then we'll practise:"},
            {"type": "choice",
             "text": "Can you know in advance what print(coin) shows?",
             "options": [("heads", "always heads"), ("tails", "always tails"), ("either", "heads or tails")],
             "answer": "either",
             "wrong": {"heads": "choice picks at *random*. Run it again and it may change.",
                       "tails": "choice picks at *random*. Run it again and it may change."},
             "video": "random"},
            {"type": "teach", "text":
             "More from random:\n\n"
             "random.randint(1, 10)\n"
             "gives a whole number from 1 to 10 - *including* both 1 and 10.\n\n"
             "random.shuffle(cards)\n"
             "mixes up a list."},
            {"type": "question",
             "text": "Which numbers could random.randint(1, 3) give?\n\n"
                     "0   1   2   3   4\n\n"
                     "Type all that are possible, e.g. `0 4`",
             "answers": ["1 2 3", "123", "1,2,3", "1, 2, 3"],
             "wrong": {"1 2": "randint includes the last number too.",
                       "0 1 2": "randint(1, 3) starts at 1 - and it includes 3.",
                       "0 1 2 3": "It starts at 1, not 0.",
                       "2": "Any of the numbers from 1 to 3 is possible, including both ends."},
             "hint": "randint(1, 3) means from 1 to 3, and both ends count.",
             "video": "random"},
            {"type": "teach", "text":
             "Import just one function with *from*:\n\n"
             "from random import choice\n"
             "coin = choice([\"heads\", \"tails\"])\n\n"
             "Now you write choice(...) instead of random.choice(...)."},
            {"type": "choice",
             "text": "After  from random import choice  which line works?\n\n"
                     "A) choice([1, 2])\n"
                     "B) random.choice([1, 2])",
             "options": [("a", "A only"), ("b", "B only"), ("both", "both work")],
             "answer": "a",
             "wrong": {"b": "from random import choice only brings in *choice*. The name random isn't loaded, so B gives an error.",
                       "both": "The name random itself isn't loaded by  from random import choice , so B gives an error."},
             "video": "creating_modules_packages"},
            {"type": "teach", "text":
             "Python comes with many libraries:\n\n"
             "import statistics\n"
             "print(statistics.mean([100, 90]))\n\n"
             "This prints 95, the average.\n\n"
             "You can make your own too: save functions in *sayings.py*, then write *import sayings* in another file."},
            {"type": "question",
             "text": "import statistics\n"
                     "print(statistics.mean([2, 4, 6]))\n\n"
                     "What prints?",
             "answers": ["4", "4.0"],
             "wrong": {"12": "That's the total. mean is the average: the total divided by how many numbers.",
                       "6": "6 is the biggest. mean is the average."},
             "hint": "Add them up, then divide by how many numbers there are.",
             "video": "random"},
            {"type": "paper",
             "text": "🎉 Final task for Lesson 5.\n\n"
                     "On paper, write a dice program that:\n"
                     "1. imports random\n"
                     "2. stores a random whole number from 1 to 6 in *roll*\n"
                     "3. prints roll\n\n"
                     "📷 Photograph it - or just type your code instead.",
             "patterns": [r"import\s+random|from\s+random\s+import\s+randint",
                          r"roll\s*=\s*(random\s*\.\s*)?randint\s*\(\s*1\s*,\s*6\s*\)",
                          r"print\s*\(\s*roll\s*\)"],
             "pattern_hints": ["Line 1:  import random",
                               "Line 2:  roll = random.randint(1, 6)",
                               "Line 3:  print(roll)"],
             "video": "random"},
        ],
    },
}
