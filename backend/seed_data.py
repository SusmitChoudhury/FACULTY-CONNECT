import os
import re
import zlib
from datetime import datetime, timezone, timedelta
from database import db_session, init_db, engine
from models import (
    Base, Student, Teacher, Section, Subject, CourseOutcome, Unit, Topic,
    TeacherSubject, TeacherSection, Doubt, DoubtStudentSupport, FacultyAnswer,
    AIResponse, FacultyAvailability, Appointment, Notification, Announcement,
    Bookmark, StudentFeedback
)

def extract_pdf_text_streams(pdf_path):
    """Decompresses and extracts PDF text streams using standard zlib."""
    with open(pdf_path, 'rb') as f:
        content = f.read()
    
    stream_pattern = re.compile(rb'stream[\r\n]+(.*?)[\r\n]+endstream', re.DOTALL)
    streams = stream_pattern.findall(content)
    
    all_text = []
    for s in streams:
        data = None
        try:
            data = zlib.decompress(s)
        except Exception:
            try:
                data = zlib.decompress(s, -15)
            except Exception:
                data = s
        
        if data:
            ops = re.findall(rb'(\(.*?\)\s*Tj|\[.*?\]\s*TJ)', data)
            for op in ops:
                if op.endswith(b'Tj'):
                    m = re.match(rb'\((.*?)\)\s*Tj', op)
                    if m:
                        try:
                            t = m.group(1).decode('utf-8', errors='ignore')
                            t = t.replace(r'\(', '(').replace(r'\)', ')')
                            all_text.append(t)
                        except Exception:
                            pass
                elif op.endswith(b'TJ'):
                    m = re.match(rb'\[(.*?)\]\s*TJ', op)
                    if m:
                        subparts = re.findall(rb'\((.*?)\)', m.group(1))
                        line = ''.join([sp.decode('utf-8', errors='ignore').replace(r'\(', '(').replace(r'\)', ')') for sp in subparts])
                        all_text.append(line)
    return '\n'.join(all_text)


def seed_database(reset=True):
    """Initializes tables and populates verified syllabus data and demonstration state."""
    session = db_session()
    if reset:
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)

    # 1. Sections
    section_names = ["K22DF", "K22GF", "K22SE", "K23AA", "K23AB"]
    for s_name in section_names:
        sec = Section(name=s_name, department="Computer Science & Engineering")
        session.add(sec)
    session.commit()

    # 2. Subjects from Syllabus Directory
    # We will populate the 7 real LPU subjects
    subjects_spec = [
        {
            "code": "INT335",
            "title": "Design Thinking",
            "credits": 2,
            "lecture_hours": "L:2 T:0 P:0",
            "textbooks": "1. Change by Design by Tim Brown, Harper\n2. Design Thinking for Dummies by Christian Muller-Roterberg, Wiley",
            "cos": [
                ("CO1", "Explain the core principles of human-centered design frameworks and differentiate iterative workflows from traditional linear engineering pipelines."),
                ("CO2", "Apply primary qualitative research and field observation methods to identify user requirements and customer environmental needs."),
                ("CO3", "Analyze unstructured user data and qualitative insights to formulate clear, actionable design challenge frameworks."),
                ("CO4", "Apply divergent thinking tools, ideation strategies, and screening techniques to systematically prioritize alternative design solutions."),
                ("CO5", "Demonstrate prototyping concepts by planning low-fidelity layouts and structural interaction paths for applications."),
                ("CO6", "Analyze user validation data, feedback matrices, and customer journey graphs to identify operational design bottlenecks.")
            ],
            "units": [
                {
                    "unit_number": "Unit I",
                    "title": "Foundations of Learning, Creativity and Design Thinking",
                    "topics": [
                        ("Learning and Creative Thinking", "Brain Processing Dynamics: Focused and Diffuse Modes, Learning Frameworks and VARK Model, Functional Fixedness and Cognitive Blocks, Creativity, Invention and Innovation"),
                        ("Foundations of Design Thinking", "History and Evolution of Design Thinking, Stanford d.school Design Thinking Framework, IDEO Human-Centred Design Framework, Global Case Studies of Successful and Failed Designs")
                    ]
                },
                {
                    "unit_number": "Unit II",
                    "title": "Empathy, Observation and Problem Identification",
                    "topics": [
                        ("User Empathy and Research Methods", "Computational Empathy in Software Engineering, Qualitative and Quantitative User Research, Field Observation and AEIOU Framework, User Interviews and Inquiry Techniques"),
                        ("User Needs and Problem Identification", "Explicit and Implicit User Needs, User Pain Points and Problem Identification, User Personas and Target Archetypes, Empathy Mapping and User Insights")
                    ]
                },
                {
                    "unit_number": "Unit III",
                    "title": "Ideation and Creative Problem Solving",
                    "topics": [
                        ("Divergent Thinking and Idea Generation", "Convergent and Divergent Thinking, Brainstorming and Idea Generation, SCAMPER Technique, Mind Mapping and Reverse Thinking"),
                        ("Idea Evaluation and Selection", "Idea Organisation and Clustering, Feasibility and Relevance Analysis, Idea Screening Matrices, Idea Selection and Prioritisation")
                    ]
                },
                {
                    "unit_number": "Unit IV",
                    "title": "Product Design and Prototyping",
                    "topics": [
                        ("Prototyping and Rapid Learning", "Prototyping Philosophy and Rapid Learning, Low-Fidelity and High-Fidelity Prototypes, Paper Prototyping for Digital Products, Storyboarding User Interactions"),
                        ("Wireframing and Minimum Viable Product", "Fundamentals of Digital Wireframing, Wireframing Rules and Conventions, User Flows and Core Product Features, Minimum Viable Product (MVP)")
                    ]
                },
                {
                    "unit_number": "Unit V",
                    "title": "Testing, Validation and Customer Experience",
                    "topics": [
                        ("User Testing and Design Validation", "Principles of Neutral User Testing, Task Scenarios and User Testing, Show Don't Tell Testing Approach, Feedback Capture Matrix"),
                        ("Customer Experience and Usability", "Customer Experience and Journey Mapping, User Touchpoints and Pain Points, Software Usability and Navigation, Accessibility in Digital Products")
                    ]
                },
                {
                    "unit_number": "Unit VI",
                    "title": "Innovation Project, Re-Design and Product Presentation",
                    "topics": [
                        ("Design Iteration and Product Re-Design", "Principles of Design Iteration, User Feedback Analysis, Design Refactoring and Re-Design, Strategic Pivoting and Continuous Improvement"),
                        ("Product Presentation and Design Communication", "High-Impact Product Presentation, NABC Model, Elevator Pitching and Product Communication, Technical Design Case Study and Final Project Presentation")
                    ]
                }
            ]
        },
        {
            "code": "CSE316",
            "title": "Operating Systems",
            "credits": 3,
            "lecture_hours": "L:3 T:0 P:0",
            "textbooks": "1. Operating System Concepts by Abraham Silberschatz, Peter B. Galvin, Greg Gagne, Wiley\n2. Design of the Unix Operating System by Maurice J. Bach, Pearson",
            "cos": [
                ("CO1", "Recall OS structure, functions, evolution, and process management."),
                ("CO2", "Apply CPU scheduling algorithms to optimize process execution."),
                ("CO3", "Analyze synchronization mechanisms and classical problems for efficient multi-threaded execution."),
                ("CO4", "Analyze deadlock conditions and handling techniques."),
                ("CO5", "Apply memory management techniques such as paging, segmentation, and virtual memory."),
                ("CO6", "Apply disk scheduling, inter-process communication methods.")
            ],
            "units": [
                {
                    "unit_number": "Unit I",
                    "title": "Introduction to Operating System & Process Management",
                    "topics": [
                        ("OS Meaning and Structures", "Supervisor & User Mode, Simple Batch Systems, Multiprogramming, Multiprocessing, Multitasking, Parallel, Distributed and RTOS, OS structure, System calls, Functions and Evolution"),
                        ("Process Management", "PCB, Operations on Processes, Co-operating and Independent Processes, Process states, Life cycle")
                    ]
                },
                {
                    "unit_number": "Unit II",
                    "title": "CPU Scheduling",
                    "topics": [
                        ("CPU Scheduling Principles & Algorithms", "Types of Scheduling, Preemptive and Non-preemptive, Dispatcher, First Come First Serve (FCFS), Shortest Job First (SJF), Round Robin (Time Quantum), Priority Scheduling, Multi Level Feedback Queue"),
                        ("Advanced Scheduling", "Multiprocessor scheduling, Real time scheduling, Thread scheduling")
                    ]
                },
                {
                    "unit_number": "Unit III",
                    "title": "Process Synchronization & Threads",
                    "topics": [
                        ("Process Synchronization Mechanisms", "Critical Section Problem, Semaphores, Precedence graph, Monitors, Dining Philosopher Problem, Reader-Writer Problem, Producer-Consumer problem, Classical solutions, Hardware primitives"),
                        ("Threads", "Multithreading Models, Scheduler activations, Threaded program examples")
                    ]
                },
                {
                    "unit_number": "Unit IV",
                    "title": "Deadlock & Protection/Security",
                    "topics": [
                        ("Deadlock Handling", "Deadlock Characterization, Deadlock Prevention, Deadlock Avoidance (Banker's Algorithm), Detection and Recovery, Starvation"),
                        ("Protection and Security", "Buffer overflow, Trapdoors, Backdoors, Authentication, Access matrix, System threats")
                    ]
                },
                {
                    "unit_number": "Unit V",
                    "title": "Memory Management",
                    "topics": [
                        ("Address Spaces and Allocation", "Logical & Physical Address Space, Swapping, Contiguous Memory Allocation, Fragmentation (Internal & External)"),
                        ("Paging and Virtual Memory", "Paging, Segmentation, Multi-level Paging, Page Fault Interrupts, Demand Paging, Page Replacement Algorithms (FIFO, LRU, Optimal)")
                    ]
                },
                {
                    "unit_number": "Unit VI",
                    "title": "File & Device Management, IPC",
                    "topics": [
                        ("File System Management", "File Concepts, Access Methods, Directory Structure, File System Mounting and Sharing, Free-Space Management"),
                        ("Device Management & Disk Scheduling", "Direct Access Storage Devices, Disk scheduling methods (FCFS, SSTF, SCAN, C-SCAN, LOOK)"),
                        ("Inter-Process Communication", "Pipes, Shared memory, FIFOs, Message queues")
                    ]
                }
            ]
        },
        {
            "code": "CSM228",
            "title": "Data Structures",
            "credits": 4,
            "lecture_hours": "L:3 T:0 P:2",
            "textbooks": "1. Data Structures and Algorithm Analysis in Java by Mark Allen Weiss, Pearson\n2. Introduction to Algorithms by Cormen, Leiserson, Rivest, Stein, MIT Press",
            "cos": [
                ("CO1", "Describe the process to find efficiency of algorithms using asymptotic notations."),
                ("CO2", "Illustrate the importance of Queue in context of problem solving."),
                ("CO3", "Differentiate HashTable and HashMap in context of writing efficient programs."),
                ("CO4", "Identify the appropriateness of HashSet and tree in problem solving."),
                ("CO5", "Analyze the effectiveness of Priority queue and Heap Data Structures."),
                ("CO6", "Use Graph and various techniques in real-world problem solving.")
            ],
            "units": [
                {
                    "unit_number": "Unit I",
                    "title": "Complexity Analysis & Stacks",
                    "topics": [
                        ("Asymptotic Analysis", "Time-Space trade off, Big O notation, Omega Notation, Theta Notation"),
                        ("Stacks and Applications", "Implementing a Stack, Parenthesis Matching Problem, File Versioning System")
                    ]
                },
                {
                    "unit_number": "Unit II",
                    "title": "Queues and Variations",
                    "topics": [
                        ("Queues Fundamentals", "Queue ADT, Implement Stack using Queues, Ticket Booking System, Palindromic String Problem, Duplicate Parenthesis")
                    ]
                },
                {
                    "unit_number": "Unit III",
                    "title": "HashTables and HashMaps",
                    "topics": [
                        ("Hash Tables Design", "Hash Functions, Collision Resolution, Dictionary Implementation"),
                        ("HashMaps Applications", "Symmetric Pairs Problem, Asymmetric Pairs, First Unique Character Problem")
                    ]
                },
                {
                    "unit_number": "Unit IV",
                    "title": "HashSets and Binary Search Trees",
                    "topics": [
                        ("HashSets", "Array of Contiguous Integers, Pair with a Given Sum, Itinerary from Tickets"),
                        ("Binary Trees & BST", "Linear vs Non-linear, Tree Traversals (DFS & BFS), BST Insertion, Deletion, Lowest Common Ancestor, Balanced BSTs")
                    ]
                },
                {
                    "unit_number": "Unit V",
                    "title": "Priority Queues and Heaps",
                    "topics": [
                        ("Priority Queues ADT", "Implementation using LinkedList and ArrayList"),
                        ("Heaps", "Binary Heaps, Heapify, Heap Sort, Merge K Sorted Lists, Median of Integer Stream")
                    ]
                },
                {
                    "unit_number": "Unit VI",
                    "title": "Graphs and Graph Algorithms",
                    "topics": [
                        ("Graph Representations", "Adjacency Matrix, Adjacency List, Edge List"),
                        ("Graph Algorithms", "Depth-First Search (DFS), Breadth-First Search (BFS), Dijkstra's Shortest Path Algorithm")
                    ]
                }
            ]
        },
        {
            "code": "CSM229",
            "title": "Programming in Java",
            "credits": 4,
            "lecture_hours": "L:3 T:0 P:2",
            "textbooks": "1. Java: The Complete Reference by Herbert Schildt, McGraw Hill\n2. Effective Java by Joshua Bloch, Addison-Wesley",
            "cos": [
                ("CO1", "Use basic constructs of Java programming to solve real-world problems."),
                ("CO2", "Apply Object-oriented programming principles to write efficient and reusable codes."),
                ("CO3", "Understand abstract classes, interfaces and Lambda expressions."),
                ("CO4", "Develop robust Java applications handling runtime environment issues."),
                ("CO5", "Use predefined Java libraries and in-built data structures."),
                ("CO6", "Understand database connection and manage transactions using JDBC.")
            ],
            "units": [
                {
                    "unit_number": "Unit I",
                    "title": "Java Fundamentals",
                    "topics": [
                        ("JDK and Core Syntax", "Installation of JDK, Compiling and Executing via CLI and IDE, Data Types, Variables, Operators, Working with Arrays and Strings")
                    ]
                },
                {
                    "unit_number": "Unit II",
                    "title": "Control Structures, Methods and Lambdas",
                    "topics": [
                        ("Basic I/O & Loops", "Console I/O, Conditional Statements, Loop Optimization"),
                        ("Methods and Lambdas", "Method Overloading, Internal Functions, Defining and Using Lambda Expressions")
                    ]
                },
                {
                    "unit_number": "Unit III",
                    "title": "Object-Oriented Programming & Encapsulation",
                    "topics": [
                        ("Classes and Objects", "Modelling real-life problems, Constructors, this, final and static keywords"),
                        ("Abstraction & Encapsulation", "Private access modifiers, Getters and Setters")
                    ]
                },
                {
                    "unit_number": "Unit IV",
                    "title": "Inheritance and Polymorphism",
                    "topics": [
                        ("Inheritance & Method Overriding", "Subclasses, Superclasses, Dynamic Polymorphism, Composition vs Inheritance"),
                        ("Abstract Classes & Interfaces", "Defining Abstract Classes, Interface Default/Static methods, Anonymous Classes")
                    ]
                },
                {
                    "unit_number": "Unit V",
                    "title": "Collections & Exception Handling",
                    "topics": [
                        ("ArrayList & LinkedList", "Structure, Basic Operations, Iterators, Performance comparison"),
                        ("Exception Handling", "Propagation, Try-Catch-Finally, Multi-catch, Try-with-resources, Custom Exceptions")
                    ]
                },
                {
                    "unit_number": "Unit VI",
                    "title": "Stream API, Serialization & JDBC",
                    "topics": [
                        ("Stream API", "Intermediate and Terminal operations on Streams"),
                        ("Serialization and JDBC", "Object Serialization, JDBC Architecture, Executing SQL Statements")
                    ]
                }
            ]
        },
        {
            "code": "MTH401",
            "title": "Discrete Mathematics",
            "credits": 4,
            "lecture_hours": "L:3 T:1 P:0",
            "textbooks": "1. Discrete Mathematics and Its Applications by Kenneth H. Rosen, McGraw Hill\n2. Higher Engineering Mathematics by B. V. Ramana, McGraw Hill",
            "cos": [
                ("CO1", "Understand methods for constructing and validating logical proofs."),
                ("CO2", "Explain recursive techniques for solving problems in combinatorics."),
                ("CO3", "Apply equivalence and partial order relation properties on graphs."),
                ("CO4", "Understand graph-theoretic concepts and applications."),
                ("CO5", "Apply planar graphs, Euler's formula, graph coloring and trees."),
                ("CO6", "Compute linear congruences using the Euclidean algorithm.")
            ],
            "units": [
                {
                    "unit_number": "Unit I",
                    "title": "Logic and Proofs",
                    "topics": [
                        ("Propositional Logic", "Propositional equivalences, Quantifiers, Direct proof, Contraposition, Contradiction, Counterexamples")
                    ]
                },
                {
                    "unit_number": "Unit II",
                    "title": "Recurrence Relations",
                    "topics": [
                        ("Recurrence Modelling", "Homogeneous linear recurrence with constant coefficients, Method of inverse operator, Generating functions")
                    ]
                },
                {
                    "unit_number": "Unit III",
                    "title": "Counting Principles & Relations",
                    "topics": [
                        ("Combinatorics & Relations", "Inclusion-Exclusion, Pigeonhole Principle, Equivalence Relations, Partial Order Relations, Hasse Diagrams, Lattices")
                    ]
                },
                {
                    "unit_number": "Unit IV",
                    "title": "Graph Theory I",
                    "topics": [
                        ("Graph Basics", "Special graphs (cycle, bipartite), Adjacency & Incidence matrices, Graph isomorphism, Shortest path (Dijkstra's)")
                    ]
                },
                {
                    "unit_number": "Unit V",
                    "title": "Graph Theory II",
                    "topics": [
                        ("Planar Graphs & Trees", "Planar graphs, Euler's formula, Graph coloring and Chromatic number, Spanning trees")
                    ]
                },
                {
                    "unit_number": "Unit VI",
                    "title": "Number Theory & Cryptography",
                    "topics": [
                        ("Divisibility & Congruence", "Modular arithmetic, Primes, GCD/LCM, Euclidean Algorithm, Bezout's Lemma, Chinese Remainder Theorem, Fermat's Little Theorem")
                    ]
                }
            ]
        },
        {
            "code": "CSE325",
            "title": "Operating Systems Laboratory",
            "credits": 1,
            "lecture_hours": "L:0 T:0 P:2",
            "textbooks": "1. Beginning Linux Programming by Neil Mathew & Richard Stones, Wiley\n2. Operating Systems: Internals and Design Principles by William Stallings, Pearson",
            "cos": [
                ("CO1", "Understand Linux command-line tools and system utilities to manage users and packages."),
                ("CO2", "Apply automation scripts using Bash shell scripting."),
                ("CO3", "Use low-level file operations with OS system calls."),
                ("CO4", "Contrast process creation using fork and exec."),
                ("CO5", "Demonstrate multithreading and synchronization with POSIX threads."),
                ("CO6", "Apply inter-process communication mechanisms using pipes and shared memory.")
            ],
            "units": [
                {
                    "unit_number": "Unit I",
                    "title": "Linux Ecosystem & Shell Scripting",
                    "topics": [
                        ("Linux Command Line & Scripting", "User/group management, package management, bash variables, loops, conditionals, arrays, functions")
                    ]
                },
                {
                    "unit_number": "Unit II",
                    "title": "System Calls & Process Management",
                    "topics": [
                        ("System Calls and Fork", "open, read, write, close, lseek, process creation using fork(), exec(), orphan and zombie processes")
                    ]
                },
                {
                    "unit_number": "Unit III",
                    "title": "Threads & Inter-Process Communication",
                    "topics": [
                        ("POSIX Threads & IPC", "pthread creation and termination, mutex locks, semaphores, pipes, shared memory")
                    ]
                }
            ]
        },
        {
            "code": "CSM216",
            "title": "Python Project",
            "credits": 2,
            "lecture_hours": "L:0 T:0 P:3",
            "textbooks": "1. Pearson Python Programming by S. Sridhar, Pearson\n2. Core Python Programming by Dr. R. Nageswara Rao, Dreamtech Press",
            "cos": [
                ("CO1", "Define Python language syntax including control statements and functions."),
                ("CO2", "Classify numpy, pandas and matplotlib modules for data analysis."),
                ("CO3", "Apply tkinter module to build GUI applications."),
                ("CO4", "Compare performance of linear and binary search."),
                ("CO5", "Design pygame modules for computer graphics and sound."),
                ("CO6", "Construct real-world projects using Python.")
            ],
            "units": [
                {
                    "unit_number": "Unit I",
                    "title": "Core Python & Algorithmic Thinking",
                    "topics": [
                        ("Basic Syntax and Logic", "Control flow, loops, data structures, random module, Number Guessing System project")
                    ]
                },
                {
                    "unit_number": "Unit II",
                    "title": "GUI Development & Pygame Foundations",
                    "topics": [
                        ("Tkinter & Pygame", "Tkinter widgets, geometry managers, event binding, Pygame surfaces, tic-tac-toe project")
                    ]
                },
                {
                    "unit_number": "Unit III",
                    "title": "Data Science & Algorithm Performance",
                    "topics": [
                        ("Data Science Stack", "Numpy arrays, Pandas Dataframe, Matplotlib visualizations, Searching algorithm performance analyzer")
                    ]
                }
            ]
        }
    ]

    subject_entities = {}
    for spec in subjects_spec:
        subj = Subject(
            code=spec["code"],
            title=spec["title"],
            credits=spec["credits"],
            lecture_hours=spec["lecture_hours"],
            textbooks=spec["textbooks"]
        )
        session.add(subj)
        session.flush()
        subject_entities[spec["code"]] = subj

        # Add COs
        for co_code, co_desc in spec["cos"]:
            co = CourseOutcome(subject_id=subj.id, co_code=co_code, description=co_desc)
            session.add(co)

        # Add Units & Topics
        for u_spec in spec["units"]:
            unit = Unit(
                subject_id=subj.id,
                unit_number=u_spec["unit_number"],
                title=u_spec["title"]
            )
            session.add(unit)
            session.flush()

            for top_title, top_sub in u_spec["topics"]:
                topic = Topic(
                    unit_id=unit.id,
                    title=top_title,
                    subtopics=top_sub
                )
                session.add(topic)
    session.commit()

    # 3. Faculty Members (Secure Password Hashes)
    teachers_spec = [
        {
            "name": "Dr. Rajesh Sharma",
            "email": "dr.rajesh@lpu.co.in",
            "password": "faculty123", # Hashed securely
            "department": "Department of Computer Science & Engineering",
            "cabin_location": "Block 34, Cabin 601",
            "phone": "+91 98141 12345",
            "bio": "Lead Professor for INT335 Design Thinking. Specializes in Human-Centered Design and Innovation Frameworks.",
            "subjects": ["INT335"],
            "sections": ["K22DF", "K22GF", "K22SE"]
        },
        {
            "name": "Dr. Harpreet Kaur",
            "email": "dr.harpreet@lpu.co.in",
            "password": "faculty123",
            "department": "Department of Computer Science & Engineering",
            "cabin_location": "Block 38, Cabin 402",
            "phone": "+91 98722 54321",
            "bio": "Senior Associate Professor for Operating Systems. Research interests in Kernel Architectures and Real-Time Systems.",
            "subjects": ["CSE316", "CSE325"],
            "sections": ["K22DF", "K22GF", "K23AA"]
        },
        {
            "name": "Prof. Amit Verma",
            "email": "prof.verma@lpu.co.in",
            "password": "faculty123",
            "department": "Department of Computer Science & Engineering",
            "cabin_location": "Block 34, Cabin 405",
            "phone": "+91 98888 67890",
            "bio": "Faculty in Data Structures & Java Systems. Passionate about asymptotic algorithm optimizations and clean OOP design.",
            "subjects": ["CSM228", "CSM229"],
            "sections": ["K22DF", "K22SE", "K23AB"]
        },
        {
            "name": "Dr. Neha Gupta",
            "email": "dr.neha@lpu.co.in",
            "password": "faculty123",
            "department": "Department of Mathematics",
            "cabin_location": "Block 36, Cabin 201",
            "phone": "+91 99155 33445",
            "bio": "Associate Professor for Discrete Mathematics and Cryptographic Number Theory.",
            "subjects": ["MTH401"],
            "sections": ["K22DF", "K22GF", "K22SE", "K23AA"]
        },
        {
            "name": "Prof. Gurpreet Singh",
            "email": "prof.singh@lpu.co.in",
            "password": "faculty123",
            "department": "Department of Computer Science & Engineering",
            "cabin_location": "Block 34, Cabin 312",
            "phone": "+91 97800 11223",
            "bio": "Mentor for Python Capstone Projects and Data Analysis applications.",
            "subjects": ["CSM216"],
            "sections": ["K22DF", "K23AB"]
        }
    ]

    teacher_entities = {}
    for t_spec in teachers_spec:
        teacher = Teacher(
            name=t_spec["name"],
            email=t_spec["email"],
            department=t_spec["department"],
            cabin_location=t_spec["cabin_location"],
            phone=t_spec["phone"],
            bio=t_spec["bio"]
        )
        teacher.set_password(t_spec["password"])
        session.add(teacher)
        session.flush()
        teacher_entities[t_spec["email"]] = teacher

        # Assign subjects
        for s_code in t_spec["subjects"]:
            if s_code in subject_entities:
                ts = TeacherSubject(teacher_id=teacher.id, subject_id=subject_entities[s_code].id)
                session.add(ts)

        # Assign sections
        for sec_name in t_spec["sections"]:
            tsec = TeacherSection(teacher_id=teacher.id, section_name=sec_name)
            session.add(tsec)
    session.commit()

    # 4. Students
    students_spec = [
        {"name": "Aman Choudhary", "section": "K22DF"},
        {"name": "Priya Sharma", "section": "K22DF"},
        {"name": "Rohan Patel", "section": "K22GF"},
        {"name": "Ananya Sen", "section": "K22SE"},
        {"name": "Kavya Iyer", "section": "K22DF"},
        {"name": "Vikram Reddy", "section": "K23AA"}
    ]
    student_entities = {}
    for s_spec in students_spec:
        st = Student(name=s_spec["name"], section=s_spec["section"])
        session.add(st)
        session.flush()
        student_entities[s_spec["name"]] = st
    session.commit()

    # 5. Faculty Availability Schedules
    now = datetime.now(timezone.utc)
    availabilities = [
        # Dr. Rajesh Sharma (INT335)
        {"teacher": teacher_entities["dr.rajesh@lpu.co.in"], "day": "Monday", "start": "02:00 PM", "end": "03:30 PM", "loc": "Block 34, Cabin 601", "max": 4, "inst": "Bring your low-fidelity prototype sketches and empathy research logs."},
        {"teacher": teacher_entities["dr.rajesh@lpu.co.in"], "day": "Wednesday", "start": "11:00 AM", "end": "12:30 PM", "loc": "Block 34, Cabin 601", "max": 4, "inst": "Group discussions on user testing matrices."},
        {"teacher": teacher_entities["dr.rajesh@lpu.co.in"], "day": "Friday", "start": "03:00 PM", "end": "04:30 PM", "loc": "Block 34, Cabin 601", "max": 3, "inst": "Reviewing P09 Project deck & presentation pitch."},

        # Dr. Harpreet Kaur (CSE316, CSE325)
        {"teacher": teacher_entities["dr.harpreet@lpu.co.in"], "day": "Tuesday", "start": "10:00 AM", "end": "11:30 AM", "loc": "Block 38, Cabin 402", "max": 3, "inst": "Bring your CPU scheduling Gantt chart exercises or synchronization questions."},
        {"teacher": teacher_entities["dr.harpreet@lpu.co.in"], "day": "Thursday", "start": "02:30 PM", "end": "04:00 PM", "loc": "Block 38, Cabin 402", "max": 3, "inst": "Linux system call bugs or deadlock detection practice."},

        # Prof. Amit Verma (CSM228, CSM229)
        {"teacher": teacher_entities["prof.verma@lpu.co.in"], "day": "Monday", "start": "10:30 AM", "end": "12:00 PM", "loc": "Block 34, Cabin 405", "max": 3, "inst": "Java OOP and BST traversal code reviews."},
        {"teacher": teacher_entities["prof.verma@lpu.co.in"], "day": "Thursday", "start": "11:00 AM", "end": "12:30 PM", "loc": "Block 34, Cabin 405", "max": 3, "inst": "Graph representation and Dijkstra algorithm traces."},

        # Dr. Neha Gupta (MTH401)
        {"teacher": teacher_entities["dr.neha@lpu.co.in"], "day": "Wednesday", "start": "01:30 PM", "end": "03:00 PM", "loc": "Block 36, Cabin 201", "max": 4, "inst": "Bring step-by-step mathematical proofs or recurrence relation attempts."}
    ]

    for av in availabilities:
        fa = FacultyAvailability(
            teacher_id=av["teacher"].id,
            day_of_week=av["day"],
            start_time=av["start"],
            end_time=av["end"],
            location=av["loc"],
            max_bookings=av["max"],
            instructions=av["inst"],
            is_active=True
        )
        session.add(fa)
    session.commit()

    # 6. Sample Doubts, +1 Repeated Questions, Faculty Answers, and AI Answers
    os_subj = subject_entities["CSE316"]
    os_unit2 = [u for u in os_subj.units if "Unit II" in u.unit_number][0]
    os_topic_cpu = os_unit2.topics[0]

    dt_subj = subject_entities["INT335"]
    dt_unit2 = [u for u in dt_subj.units if "Unit II" in u.unit_number][0]
    dt_topic_empathy = dt_unit2.topics[0]

    java_subj = subject_entities["CSM229"]
    java_unit4 = [u for u in java_subj.units if "Unit IV" in u.unit_number][0]
    java_topic_inh = java_unit4.topics[0]

    math_subj = subject_entities["MTH401"]
    math_unit6 = [u for u in math_subj.units if "Unit VI" in u.unit_number][0]
    math_topic_num = math_unit6.topics[0]

    # Doubt 1: Round Robin scheduling (High repeat count +1 with Faculty Answer)
    d1 = Doubt(
        student_id=student_entities["Aman Choudhary"].id,
        student_name="Aman Choudhary",
        section="K22DF",
        subject_id=os_subj.id,
        unit_id=os_unit2.id,
        topic_id=os_topic_cpu.id,
        teaching_date="2026-11-10",
        category="Conceptual Doubt",
        question_text="Why does Round Robin scheduling use a time quantum, and what happens if the time quantum is chosen to be extremely large or extremely small?",
        status="Faculty Answered",
        duplicate_count=4, # 4 students have this exact doubt!
        created_at=now - timedelta(days=2, hours=5),
        response_deadline=now - timedelta(days=2, hours=2)
    )
    session.add(d1)
    session.flush()

    # +1 supporters
    for s_name in ["Priya Sharma", "Kavya Iyer", "Rohan Patel"]:
        sup = DoubtStudentSupport(
            doubt_id=d1.id,
            student_name=s_name,
            student_section="K22DF" if s_name != "Rohan Patel" else "K22GF",
            created_at=now - timedelta(days=2, hours=3)
        )
        session.add(sup)

    # Faculty Answer by Dr. Harpreet Kaur
    fa1 = FacultyAnswer(
        doubt_id=d1.id,
        teacher_id=teacher_entities["dr.harpreet@lpu.co.in"].id,
        teacher_name="Dr. Harpreet Kaur",
        answer_text=(
            "Excellent question, Aman and class!\n\n"
            "In Round Robin (RR), the **Time Quantum (q)** is the maximum time slice a process gets before CPU preemption.\n\n"
            "1. **If q is extremely large (q → ∞):** RR degrades directly into First-Come, First-Served (FCFS). Interactive processes will experience severe latency.\n"
            "2. **If q is extremely small (q → 0):** While it simulates processor sharing, the context-switch overhead dominates CPU utilization, wasting throughput on kernel state-saving.\n\n"
            "**Standard Practice:** Silberschatz Chapter 5 specifies that 80% of CPU bursts should be shorter than the chosen time quantum (typically between 10ms and 100ms)."
        ),
        created_at=now - timedelta(days=2, hours=1)
    )
    session.add(fa1)

    # Student feedback on Doubt 1
    session.add(StudentFeedback(doubt_id=d1.id, student_name="Aman Choudhary", resolved=True, feedback_text="Understood completely, helped a lot for CA1!"))
    session.add(StudentFeedback(doubt_id=d1.id, student_name="Priya Sharma", resolved=True, feedback_text="Clear explanation about the 80% rule."))

    # Doubt 2: Design Thinking AEIOU Framework (Answered by AI after 3-hour timer, verified by Faculty)
    d2 = Doubt(
        student_id=student_entities["Priya Sharma"].id,
        student_name="Priya Sharma",
        section="K22DF",
        subject_id=dt_subj.id,
        unit_id=dt_unit2.id,
        topic_id=dt_topic_empathy.id,
        teaching_date="2026-11-12",
        category="Lecture Clarification",
        question_text="How should our group apply the AEIOU framework during field observations for our INT335 Project P09 on faculty-student communication?",
        status="Faculty Verified",
        duplicate_count=2,
        created_at=now - timedelta(days=1, hours=6),
        response_deadline=now - timedelta(days=1, hours=3)
    )
    session.add(d2)
    session.flush()

    session.add(DoubtStudentSupport(doubt_id=d2.id, student_name="Aman Choudhary", student_section="K22DF", created_at=now - timedelta(days=1, hours=4)))

    # AI Response generated automatically when 3 hours passed
    ai_resp2 = AIResponse(
        doubt_id=d2.id,
        model_name="FacultyConnect-Academic-Engine",
        response_text=(
            "### Applying AEIOU in INT335 Innovation Project P09\n\n"
            "The **AEIOU Framework** organizes observational ethnographic data into five distinct lenses:\n\n"
            "- **A – Activities:** Observe actions students take when seeking help (e.g., checking cabin doors, messaging CRs on WhatsApp, wandering corridors).\n"
            "- **E – Environments:** The physical cabin spaces, lecture hall exits, and digital spaces (UMS, group chats).\n"
            "- **I – Interactions:** Communication between student-to-teacher, student-to-CR, and peer-to-peer.\n"
            "- **O – Objects:** Noticeboards, consultation slips, syllabus PDFs, lecture notes, mobile phones.\n"
            "- **U – Users:** Students with urgent doubts, faculty with grading deadlines, class representatives acting as intermediaries.\n\n"
            "**Key Takeaway:** Use these five categories to fill your Empathy Map before converging on the problem statement."
        ),
        confidence_score=0.96,
        faculty_quality_status="Correct",
        faculty_feedback_notes="Accurate application to the INT335 curriculum and project domain."
    )
    session.add(ai_resp2)

    # Faculty verified answer from Dr. Rajesh Sharma
    fa2 = FacultyAnswer(
        doubt_id=d2.id,
        teacher_id=teacher_entities["dr.rajesh@lpu.co.in"].id,
        teacher_name="Dr. Rajesh Sharma",
        answer_text="The AI guidance above is spot-on for Project P09! During your presentations, ensure you present photos or observation logs mapping each of the 5 letters.",
        created_at=now - timedelta(days=1, hours=1)
    )
    session.add(fa2)

    # Doubt 3: Pending Question awaiting response (Recently submitted)
    d3 = Doubt(
        student_id=student_entities["Rohan Patel"].id,
        student_name="Rohan Patel",
        section="K22GF",
        subject_id=java_subj.id,
        unit_id=java_unit4.id,
        topic_id=java_topic_inh.id,
        teaching_date="2026-11-16",
        category="Conceptual Doubt",
        question_text="Why does Java prohibit multiple inheritance with classes but allow multiple inheritance of interfaces?",
        status="Pending",
        duplicate_count=1,
        created_at=now - timedelta(minutes=45),
        response_deadline=now + timedelta(hours=2, minutes=15) # Still 2h 15m left on the 3-hour timer!
    )
    session.add(d3)
    session.flush()

    # Doubt 4: Discrete Math Euclidean Algorithm
    d4 = Doubt(
        student_id=student_entities["Ananya Sen"].id,
        student_name="Ananya Sen",
        section="K22SE",
        subject_id=math_subj.id,
        unit_id=math_unit6.id,
        topic_id=math_topic_num.id,
        teaching_date="2026-11-14",
        category="Numerical Problem",
        question_text="How do we use Bezout's identity to find the multiplicative inverse of a modulo m when gcd(a,m) = 1?",
        status="AI Answered",
        duplicate_count=3,
        created_at=now - timedelta(hours=5),
        response_deadline=now - timedelta(hours=2) # 3-hour timer completed!
    )
    session.add(d4)
    session.flush()

    session.add(DoubtStudentSupport(doubt_id=d4.id, student_name="Vikram Reddy", student_section="K23AA", created_at=now - timedelta(hours=3)))
    session.add(DoubtStudentSupport(doubt_id=d4.id, student_name="Kavya Iyer", student_section="K22DF", created_at=now - timedelta(hours=2)))

    ai_resp4 = AIResponse(
        doubt_id=d4.id,
        model_name="FacultyConnect-Academic-Engine (3-Hour Fallback)",
        response_text=(
            "### Modular Multiplicative Inverse via Bezout's Identity\n\n"
            "According to Bezout's identity, if $\\gcd(a, m) = 1$, there exist integers $x$ and $y$ such that:\n"
            "$$a \\cdot x + m \\cdot y = 1$$\n\n"
            "Taking both sides modulo $m$:\n"
            "$$(a \\cdot x + m \\cdot y) \\equiv 1 \\pmod m$$\n"
            "$$a \\cdot x \\equiv 1 \\pmod m$$\n\n"
            "Hence, the integer $x$ obtained via the **Extended Euclidean Algorithm** is the modular multiplicative inverse of $a$ modulo $m$ (written as $a^{-1} \\pmod m$).\n\n"
            "**Example:** Find inverse of $7 \\pmod{26}$:\n"
            "1. $26 = 3 \\cdot 7 + 5$\n"
            "2. $7 = 1 \\cdot 5 + 2$\n"
            "3. $5 = 2 \\cdot 2 + 1$\n"
            "Back-substituting yields $1 = 5 - 2(7 - 5) = 3(26 - 3 \\cdot 7) - 2 \\cdot 7 = 3(26) - 11(7)$.\n"
            "Thus, $-11 \\equiv 15 \\pmod{26}$. So $7^{-1} \\equiv 15 \\pmod{26}$."
        ),
        confidence_score=0.98,
        faculty_quality_status="Pending"
    )
    session.add(ai_resp4)

    # 7. Sample Appointments
    app1 = Appointment(
        teacher_id=teacher_entities["dr.rajesh@lpu.co.in"].id,
        student_id=student_entities["Aman Choudhary"].id,
        student_name="Aman Choudhary",
        student_section="K22DF",
        subject_id=dt_subj.id,
        appointment_date="2026-11-20",
        time_slot="02:00 PM - 02:45 PM",
        location="Block 34, Cabin 601",
        reason="Consultation regarding INT335 Project P09 design thinking validation metrics.",
        status="Accepted",
        teacher_notes="Approved. Please bring your wireframes and testing feedback sheet.",
        created_at=now - timedelta(days=1)
    )
    session.add(app1)

    app2 = Appointment(
        teacher_id=teacher_entities["dr.harpreet@lpu.co.in"].id,
        student_id=student_entities["Priya Sharma"].id,
        student_name="Priya Sharma",
        student_section="K22DF",
        subject_id=os_subj.id,
        appointment_date="2026-11-21",
        time_slot="10:00 AM - 10:45 AM",
        location="Block 38, Cabin 402",
        reason="Doubt regarding banker's algorithm safety algorithm code implementation.",
        status="Pending",
        created_at=now - timedelta(hours=4)
    )
    session.add(app2)

    # 8. Sample Notifications
    notifs = [
        Notification(
            recipient_type="student",
            student_name="Aman Choudhary",
            title="Appointment Confirmed",
            message="Dr. Rajesh Sharma accepted your appointment for Friday, 20 Nov at 02:00 PM.",
            notification_type="appointment_update",
            link_id=app1.id,
            is_read=False
        ),
        Notification(
            recipient_type="student",
            student_name="Aman Choudhary",
            title="Faculty Answer Received",
            message="Dr. Harpreet Kaur posted an official answer on Round Robin Scheduling.",
            notification_type="faculty_answer",
            link_id=d1.id,
            is_read=True
        ),
        Notification(
            recipient_type="teacher",
            teacher_id=teacher_entities["dr.harpreet@lpu.co.in"].id,
            title="New Consultation Request",
            message="Priya Sharma (K22DF) requested an appointment for CSE316 on Nov 21.",
            notification_type="appointment_update",
            link_id=app2.id,
            is_read=False
        ),
        Notification(
            recipient_type="teacher",
            teacher_id=teacher_entities["prof.verma@lpu.co.in"].id,
            title="New Student Doubt (K22GF)",
            message="Rohan Patel submitted a doubt on Java Inheritance. Response deadline in 2 hours.",
            notification_type="doubt_update",
            link_id=d3.id,
            is_read=False
        )
    ]
    for n in notifs:
        session.add(n)

    # 9. Announcements
    ann1 = Announcement(
        teacher_id=teacher_entities["dr.rajesh@lpu.co.in"].id,
        teacher_name="Dr. Rajesh Sharma",
        subject_id=dt_subj.id,
        target_section="All",
        title="INT335 Group Project Evaluation P09 Guidelines",
        content="All student innovation groups must ensure their working prototype demonstrates all 5 stages of Design Thinking: Empathy, Define, Ideate, Prototype, and Test. Cabins will be open for pre-evaluation checks this Wednesday.",
        priority="Important",
        created_at=now - timedelta(days=3)
    )
    session.add(ann1)

    ann2 = Announcement(
        teacher_id=teacher_entities["dr.harpreet@lpu.co.in"].id,
        teacher_name="Dr. Harpreet Kaur",
        subject_id=os_subj.id,
        target_section="K22DF",
        title="CPU Scheduling Practice Problems Uploaded",
        content="Please attempt the Round Robin and Multilevel Feedback Queue numerical problems before our next lecture session.",
        priority="Normal",
        created_at=now - timedelta(days=1)
    )
    session.add(ann2)

    # 10. Bookmark
    bm = Bookmark(student_name="Aman Choudhary", doubt_id=d1.id)
    session.add(bm)

    session.commit()
    session.close()
    print("Database successfully initialized and seeded with official syllabus & demonstration records.")

if __name__ == '__main__':
    seed_database(reset=True)
