"""Curated technical question bank for Upskill Pulse demo mode.

Each question is tagged with a `type`:
  - "Code Output"      What does this code / expression return?
  - "Error Prediction" Which raises an error / which fails?
  - "Concept"          Which statement about X is TRUE?
  - "Syntax"           Correct keyword / declaration / call signature.
  - "Comparison"       Difference between X and Y.
  - "Behavior"         What happens when [edge case]?
"""

BANK = {
    "python": [
        {"q": "What does `list.pop()` return when called without arguments on `[1,2,3]`?",
         "opts": ["1", "3", "None", "IndexError"], "c": 1, "t": "Code Output"},
        {"q": "What is the output of `print(type([]))`?",
         "opts": ["<class 'list'>", "<type 'list'>", "list", "<class 'array'>"], "c": 0, "t": "Code Output"},
        {"q": "Which will raise `TypeError`?",
         "opts": ["`'5' + '3'`", "`5 + 3`", "`'5' + 3`", "`[1] + [2]`"], "c": 2, "t": "Error Prediction"},
        {"q": "What does `{1,2,3} & {2,3,4}` return?",
         "opts": ["{1,2,3,4}", "{2,3}", "{1,4}", "{}"], "c": 1, "t": "Code Output"},
        {"q": "What is the default value of `dict.get('missing')`?",
         "opts": ["KeyError", "None", "0", "''"], "c": 1, "t": "Behavior"},
        {"q": "What does `[i*2 for i in range(3)]` produce?",
         "opts": ["[0,2,4]", "[2,4,6]", "[0,1,2]", "[1,2,3]"], "c": 0, "t": "Code Output"},
        {"q": "Which is mutable in Python?",
         "opts": ["tuple", "str", "frozenset", "list"], "c": 3, "t": "Concept"},
        {"q": "What does `len('Hello')` return?",
         "opts": ["4", "5", "6", "TypeError"], "c": 1, "t": "Code Output"},
        {"q": "`@staticmethod` on a class method means it:",
         "opts": ["Cannot access `self`", "Cannot access `cls`", "Both — no implicit first arg", "Must be private"], "c": 2, "t": "Concept"},
        {"q": "What does `a, *b = [1,2,3,4]` assign to `b`?",
         "opts": ["1", "[2,3,4]", "[1]", "[4]"], "c": 1, "t": "Syntax"},
    ],
    "javascript": [
        {"q": "What does `typeof null` return?",
         "opts": ["'null'", "'undefined'", "'object'", "'boolean'"], "c": 2, "t": "Code Output"},
        {"q": "Result of `[] + []` in JavaScript?",
         "opts": ["[]", "''", "0", "TypeError"], "c": 1, "t": "Code Output"},
        {"q": "What does `'5' == 5` evaluate to?",
         "opts": ["true", "false", "TypeError", "NaN"], "c": 0, "t": "Behavior"},
        {"q": "Which declares a block-scoped variable?",
         "opts": ["var", "let", "const", "Both let and const"], "c": 3, "t": "Syntax"},
        {"q": "What does `Promise.resolve(1).then(x => x+1)` resolve to?",
         "opts": ["1", "2", "Promise", "undefined"], "c": 1, "t": "Code Output"},
        {"q": "`Array.isArray({})` returns:",
         "opts": ["true", "false", "undefined", "TypeError"], "c": 1, "t": "Code Output"},
        {"q": "What does `0.1 + 0.2 === 0.3` evaluate to?",
         "opts": ["true", "false", "NaN", "RangeError"], "c": 1, "t": "Behavior"},
        {"q": "Result of `[1,2,3].map(parseInt)`?",
         "opts": ["[1,2,3]", "[1,NaN,NaN]", "[1,NaN,3]", "TypeError"], "c": 1, "t": "Code Output"},
        {"q": "`async function f() { return 1 }` — what does `f()` return?",
         "opts": ["1", "Promise<1>", "undefined", "Error"], "c": 1, "t": "Behavior"},
        {"q": "What does `Object.keys({a:1,b:2}).length` return?",
         "opts": ["0", "1", "2", "undefined"], "c": 2, "t": "Code Output"},
    ],
    "react": [
        {"q": "Which hook manages local state in a functional component?",
         "opts": ["useEffect", "useState", "useMemo", "useRef"], "c": 1, "t": "Concept"},
        {"q": "`useEffect(() => {...}, [])` — when does the effect run?",
         "opts": ["Every render", "Only on mount", "Only on unmount", "Never"], "c": 1, "t": "Behavior"},
        {"q": "What does `React.memo` do?",
         "opts": ["Caches API responses", "Skips re-render if props unchanged", "Stores state in memory", "Adds memoization to hooks"], "c": 1, "t": "Concept"},
        {"q": "Key prop on list items is required for:",
         "opts": ["Styling", "Event handling", "Efficient reconciliation", "Type safety"], "c": 2, "t": "Concept"},
        {"q": "`useRef(0)` — what happens when `.current` is mutated?",
         "opts": ["Triggers re-render", "Does NOT trigger re-render", "Throws error", "Resets to 0"], "c": 1, "t": "Behavior"},
        {"q": "Which is correct for updating state based on previous state?",
         "opts": ["`setN(n+1)`", "`setN(prev => prev+1)`", "`n = n+1`", "`this.state.n++`"], "c": 1, "t": "Syntax"},
        {"q": "What does `<Fragment>` or `<></>` do?",
         "opts": ["Renders nothing", "Groups children without adding DOM node", "Creates shadow DOM", "Lazy loads children"], "c": 1, "t": "Concept"},
    ],
    "java": [
        {"q": "Which collection does NOT allow duplicate elements?",
         "opts": ["ArrayList", "LinkedList", "HashSet", "Vector"], "c": 2, "t": "Concept"},
        {"q": "What is the parent class of all Java classes?",
         "opts": ["Class", "Object", "Parent", "Super"], "c": 1, "t": "Concept"},
        {"q": "`String` in Java is:",
         "opts": ["Mutable", "Immutable", "Primitive", "Interface"], "c": 1, "t": "Concept"},
        {"q": "Which keyword prevents method overriding?",
         "opts": ["static", "final", "const", "sealed"], "c": 1, "t": "Syntax"},
        {"q": "Result of `System.out.println(10 / 3)`?",
         "opts": ["3.33", "3", "3.0", "CompileError"], "c": 1, "t": "Code Output"},
        {"q": "Which is TRUE about `HashMap`?",
         "opts": ["Synchronized", "Ordered", "Allows one null key", "Thread-safe"], "c": 2, "t": "Concept"},
        {"q": "`interface` can contain:",
         "opts": ["Only abstract methods", "Default methods too (Java 8+)", "Constructors", "Static blocks only"], "c": 1, "t": "Concept"},
    ],
    "sql": [
        {"q": "Which SQL clause filters rows AFTER `GROUP BY`?",
         "opts": ["WHERE", "HAVING", "FILTER", "ON"], "c": 1, "t": "Syntax"},
        {"q": "`INNER JOIN` returns:",
         "opts": ["All rows from both tables", "Only matching rows from both", "All rows from left table", "All rows from right table"], "c": 1, "t": "Concept"},
        {"q": "What does `COUNT(*)` differ from `COUNT(column)`?",
         "opts": ["No difference", "`COUNT(*)` includes NULLs, `COUNT(column)` excludes them", "`COUNT(*)` is faster", "`COUNT(column)` includes NULLs"], "c": 1, "t": "Comparison"},
        {"q": "Which is NOT a valid aggregate function?",
         "opts": ["SUM", "AVG", "COUNT", "SORT"], "c": 3, "t": "Syntax"},
        {"q": "`PRIMARY KEY` implies:",
         "opts": ["NOT NULL + UNIQUE", "Only UNIQUE", "Only NOT NULL", "Foreign reference"], "c": 0, "t": "Concept"},
        {"q": "Which statement removes a table and all its data?",
         "opts": ["DELETE", "TRUNCATE", "DROP", "REMOVE"], "c": 2, "t": "Syntax"},
    ],
    "data structures": [
        {"q": "Time complexity of accessing element by index in an array?",
         "opts": ["O(1)", "O(n)", "O(log n)", "O(n log n)"], "c": 0, "t": "Concept"},
        {"q": "Which data structure uses LIFO order?",
         "opts": ["Queue", "Stack", "Heap", "Tree"], "c": 1, "t": "Concept"},
        {"q": "Average lookup time in a hash table?",
         "opts": ["O(1)", "O(n)", "O(log n)", "O(n²)"], "c": 0, "t": "Concept"},
        {"q": "Which is a balanced BST?",
         "opts": ["Binary Tree", "AVL Tree", "Trie", "Heap"], "c": 1, "t": "Concept"},
        {"q": "In a min-heap, the root is:",
         "opts": ["The largest element", "The smallest element", "Any element", "Always 0"], "c": 1, "t": "Concept"},
        {"q": "Time complexity of binary search on sorted array?",
         "opts": ["O(n)", "O(log n)", "O(1)", "O(n log n)"], "c": 1, "t": "Concept"},
    ],
    "algorithms": [
        {"q": "Worst-case time of QuickSort?",
         "opts": ["O(n log n)", "O(n²)", "O(n)", "O(log n)"], "c": 1, "t": "Concept"},
        {"q": "Which sorting algorithm is stable by default?",
         "opts": ["QuickSort", "HeapSort", "MergeSort", "SelectionSort"], "c": 2, "t": "Comparison"},
        {"q": "Dijkstra's algorithm is used for:",
         "opts": ["Sorting", "Shortest path in weighted graph", "BFS only", "Cycle detection"], "c": 1, "t": "Concept"},
        {"q": "Big-O of nested loops over N and M items?",
         "opts": ["O(N+M)", "O(N*M)", "O(max(N,M))", "O(log(N*M))"], "c": 1, "t": "Concept"},
        {"q": "Which algorithm uses divide-and-conquer?",
         "opts": ["Bubble Sort", "Merge Sort", "Insertion Sort", "Counting Sort"], "c": 1, "t": "Concept"},
    ],
    "git": [
        {"q": "Which command creates a new branch and switches to it?",
         "opts": ["`git branch new`", "`git checkout new`", "`git checkout -b new`", "`git switch new`"], "c": 2, "t": "Syntax"},
        {"q": "`git pull` is equivalent to:",
         "opts": ["`git fetch` + `git merge`", "`git push` + `git fetch`", "`git clone`", "`git reset`"], "c": 0, "t": "Comparison"},
        {"q": "Which undoes the last commit but keeps changes staged?",
         "opts": ["`git reset --hard HEAD~1`", "`git reset --soft HEAD~1`", "`git revert HEAD`", "`git checkout HEAD~1`"], "c": 1, "t": "Syntax"},
        {"q": "`.gitignore` affects:",
         "opts": ["Already-tracked files", "Untracked files only", "All files", "Remote files"], "c": 1, "t": "Behavior"},
        {"q": "`git rebase` vs `git merge`:",
         "opts": ["Identical", "Rebase rewrites history, merge preserves it", "Merge rewrites history", "Rebase is server-side only"], "c": 1, "t": "Comparison"},
    ],
    "docker": [
        {"q": "Which file defines a Docker image?",
         "opts": ["docker.yml", "Dockerfile", "docker-compose.yml", "image.json"], "c": 1, "t": "Syntax"},
        {"q": "`docker ps` shows:",
         "opts": ["All images", "Running containers", "All containers", "Docker processes"], "c": 1, "t": "Behavior"},
        {"q": "Which command builds an image from a Dockerfile?",
         "opts": ["`docker run`", "`docker build`", "`docker create`", "`docker make`"], "c": 1, "t": "Syntax"},
        {"q": "`EXPOSE 80` in Dockerfile does what?",
         "opts": ["Opens port 80 to host", "Documents the port the container listens on", "Blocks port 80", "Maps port 80 automatically"], "c": 1, "t": "Behavior"},
    ],
    "rest api": [
        {"q": "Which HTTP method is idempotent?",
         "opts": ["POST", "PATCH", "PUT", "CONNECT"], "c": 2, "t": "Concept"},
        {"q": "HTTP 201 means:",
         "opts": ["OK", "Created", "Accepted", "Moved"], "c": 1, "t": "Concept"},
        {"q": "Which status code indicates 'resource not found'?",
         "opts": ["400", "401", "403", "404"], "c": 3, "t": "Concept"},
        {"q": "REST stands for:",
         "opts": ["Remote State Transfer", "Representational State Transfer", "Resource Endpoint State Transport", "Request Event Stream Transfer"], "c": 1, "t": "Concept"},
        {"q": "Which header carries JSON body content-type?",
         "opts": ["`text/json`", "`application/json`", "`json/application`", "`content/json`"], "c": 1, "t": "Syntax"},
    ],
    "generic": [
        {"q": "Which is a compiled language?",
         "opts": ["Python", "JavaScript", "C++", "Ruby"], "c": 2, "t": "Concept"},
        {"q": "OOP stands for:",
         "opts": ["Object-Oriented Programming", "Open-Source Programming", "Operational Output Protocol", "Ordered Object Pattern"], "c": 0, "t": "Concept"},
        {"q": "Which is NOT a programming paradigm?",
         "opts": ["Functional", "Procedural", "Declarative", "Recursive"], "c": 3, "t": "Concept"},
        {"q": "Big-O notation describes:",
         "opts": ["Code length", "Algorithm's growth rate", "Memory address", "Compilation time"], "c": 1, "t": "Concept"},
        {"q": "Which protocol secures HTTP?",
         "opts": ["FTP", "TLS", "TCP", "UDP"], "c": 1, "t": "Concept"},
        {"q": "What does API stand for?",
         "opts": ["Application Protocol Interface", "Application Programming Interface", "Automated Program Integration", "Abstract Process Input"], "c": 1, "t": "Concept"},
        {"q": "Which is a NoSQL database?",
         "opts": ["MySQL", "PostgreSQL", "MongoDB", "Oracle"], "c": 2, "t": "Concept"},
        {"q": "A 'race condition' occurs when:",
         "opts": ["Code runs too fast", "Outcome depends on thread timing", "Functions compete for memory", "The CPU overheats"], "c": 1, "t": "Behavior"},
    ],
}


TOPIC_ALIASES = {
    "python":          ["python", "py", "django", "flask", "pandas"],
    "javascript":      ["javascript", "js", "node", "nodejs", "typescript", "ts", "es6"],
    "react":           ["react", "reactjs", "jsx", "hooks", "nextjs", "next"],
    "java":            ["java", "spring", "jvm", "kotlin"],
    "sql":             ["sql", "mysql", "postgres", "postgresql", "database", "db"],
    "data structures": ["data structure", "ds", "array", "linked list", "tree", "graph", "heap", "stack", "queue"],
    "algorithms":      ["algorithm", "algo", "sort", "search", "complexity", "big o", "dynamic programming", "dp"],
    "git":             ["git", "github", "version control", "branch", "commit"],
    "docker":          ["docker", "container", "kubernetes", "k8s"],
    "rest api":        ["rest", "api", "http", "endpoint"],
}


def match_topics(user_topics):
    matched = set()
    joined = " ".join(user_topics).lower()
    for category, keywords in TOPIC_ALIASES.items():
        if any(kw in joined for kw in keywords):
            matched.add(category)
    return list(matched) if matched else ["generic"]


def generate_questions(user_topics, count):
    import random
    categories = match_topics(user_topics)
    pool = []
    for cat in categories:
        for item in BANK.get(cat, []):
            pool.append({
                "question": item["q"],
                "options":  item["opts"],
                "correct":  item["c"],
                "topic":    cat.title(),
                "type":     item["t"],
            })
    if len(pool) < count:
        for item in BANK["generic"]:
            pool.append({
                "question": item["q"],
                "options":  item["opts"],
                "correct":  item["c"],
                "topic":    "General Tech",
                "type":     item["t"],
            })
    random.shuffle(pool)
    return pool[:count]
