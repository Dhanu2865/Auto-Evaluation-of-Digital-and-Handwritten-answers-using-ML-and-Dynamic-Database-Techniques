from database import Base, engine, SessionLocal
from models import Topic, Question, ReferenceAnswer

Base.metadata.create_all(bind=engine)
db = SessionLocal()

topics_data = {
    "Programming Knowledge QP": [
        (
            "What is a compiler?",2,
            "compiler, source code, machine code",
            "A compiler is a program that translates high-level source code into machine code. It processes the entire program at once and reports errors after compilation.The generated machine code can be executed multiple times without recompilation.Compilers improve execution speed by converting code into optimized low-level instructions.Examples include GCC and Java compiler."
        ),
        (
            "What is an interpreter?",2,
            "interpreter, line by line",
            "An interpreter is a program that translates and executes code line by line.It executes each instruction immediately without generating separate machine code.Errors are reported one line at a time during execution.Interpreters are easier for debugging but slower than compilers.Examples include Python and JavaScript interpreters."
        ),
        (
            "Explain variables",2,
            "variables, memory, data storage",
            "Variables are named memory locations used to store data values.They allow programs to store, modify, and retrieve data during execution.Each variable has a data type that determines the kind of data it can hold.Variables improve code readability and flexibility.They play a key role in dynamic program behavior."
        ),
        (
            "What is a loop?",2,
            "loop, iteration",
            "A loop is a control structure used to repeat a block of code multiple times.It helps reduce code duplication and improves efficiency.Loops execute until a specified condition becomes false.Common types include for, while, and do-while loops.Loops are widely used for iteration and automation."
        ),
        (
            "What is recursion?",2,
            "recursion, function call",
            "Recursion is a programming technique where a function calls itself.It solves complex problems by breaking them into smaller subproblems.A base condition is required to stop infinite recursion.Recursion is useful for problems like factorial and tree traversal.It improves clarity but may consume more memory."
        ),
        (
            "Explain data types",2,
            "data types, integer, float",
            "Data types define the type of data a variable can store.They determine memory allocation and valid operations on data.Common data types include integer, float, character, and boolean.Data types help prevent errors and ensure program correctness.They improve code reliability and efficiency."
        ),
        (
            "What is debugging?",2,
            "debugging, error fixing",
            "Debugging is the process of identifying and fixing errors in a program.It helps ensure that the program runs correctly and efficiently.Debugging tools allow step-by-step execution and inspection of variables.It improves software quality and reliability.Debugging is a crucial phase of software development."
        ),
        (
            "Explain algorithm",2,
            "algorithm, steps",
            "An algorithm is a step-by-step procedure used to solve a problem.It provides a clear sequence of instructions to achieve a desired outcome.Algorithms are independent of programming languages.They help analyze time and space complexity.Efficient algorithms improve program performance."
        ),
        (
            "What is syntax?",2,
            "syntax, grammar",
            "Syntax refers to the set of rules that define the structure of a program.It determines how statements and expressions are written in a language.Incorrect syntax leads to compilation or runtime errors.Syntax varies between programming languages.Following syntax rules ensures correct program execution."
        ),
        (
            "What is runtime error?",2,
            "runtime error, execution",
            "A runtime error occurs during program execution.It happens when the program encounters an unexpected condition.Examples include division by zero and invalid memory access.Runtime errors are not detected during compilation. Proper exception handling can prevent runtime failures."
        )
    ],

    "Operating Systems": [
        (
            "What is an operating system?",2,
            "operating system, resource management",
            "An operating system is system software that manages computer hardware and software resources. "
            "It acts as an interface between users and hardware. "
            "The OS controls memory, CPU, storage, and input-output devices. "
            "It enables multitasking and process management. "
            "Examples include Windows, Linux, and macOS."
        ),
        (
            "Explain process",2,
            "process, execution",
            "A process is a program in execution. "
            "It includes program code, data, and execution state. "
            "Each process has its own memory space. "
            "Processes enable multitasking in an operating system. "
            "The OS manages processes using scheduling algorithms."
        ),
        (
            "Explain thread",2,
            "thread, lightweight process",
            "A thread is the smallest unit of execution within a process. "
            "Threads share the same memory space of a process. "
            "They improve application performance through parallelism. "
            "Threads are called lightweight processes. "
            "Multithreading enhances responsiveness and efficiency."
        ),
        (
            "What is deadlock?",2,
            "deadlock, resource waiting",
            "Deadlock is a situation where processes wait indefinitely for resources. "
            "It occurs when circular dependency exists among processes. "
            "Deadlock leads to system halt if not handled. "
            "Necessary conditions include mutual exclusion and hold-and-wait. "
            "Deadlock prevention techniques are used to avoid it."
        ),
        (
            "What is scheduling?",2,
            "scheduling, CPU",
            "Scheduling is the process of selecting a process for CPU execution. "
            "It ensures fair and efficient CPU utilization. "
            "Scheduling algorithms decide execution order. "
            "Examples include FCFS and Round Robin. "
            "Scheduling improves system throughput and response time."
        ),
        (
            "Explain paging",2,
            "paging, memory",
            "Paging is a memory management technique. "
            "It divides memory into fixed-size pages. "
            "Paging avoids external fragmentation. "
            "Pages are mapped to frames in physical memory. "
            "It improves efficient memory utilization."
        ),
        (
            "What is virtual memory?",2,
            "virtual memory, disk",
            "Virtual memory allows execution of programs larger than physical memory. "
            "It uses disk space as an extension of RAM. "
            "Only required pages are loaded into memory. "
            "This improves system performance. "
            "Virtual memory provides memory abstraction."
        ),
        (
            "Explain semaphore",2,
            "semaphore, synchronization",
            "A semaphore is a synchronization mechanism. "
            "It controls access to shared resources. "
            "Semaphores prevent race conditions. "
            "They are used in concurrent programming. "
            "Binary and counting semaphores are common types."
        ),
        (
            "What is context switching?",2,
            "context switching",
            "Context switching is the process of saving and restoring process state. "
            "It allows the CPU to switch between processes. "
            "Context switching enables multitasking. "
            "It involves overhead but improves responsiveness. "
            "The OS handles context switching efficiently."
        ),
        (
            "What is kernel?",2,
            "kernel, core",
            "The kernel is the core component of an operating system. "
            "It manages system resources and hardware interaction. "
            "The kernel handles process, memory, and device management. "
            "It runs in privileged mode. "
            "All system operations depend on the kernel."
        )
    ],
    "OOPS Concepts": [
        (
            "Explain OOPS concepts",2,
            "encapsulation, inheritance, polymorphism, abstraction",
            "Object-Oriented Programming System is a paradigm that structures programs using objects and classes. "
            "It focuses on modeling real-world entities through data and behavior. "
            "The core ideas help in achieving modular, reusable, and maintainable code. "
            "Programs become easier to extend and manage. "
            "OOPS is widely used in modern software development."
        ),
        (
            "What is a class?",2,
            "class, blueprint",
            "A class is a blueprint or template used to create objects. "
            "It defines properties and methods that objects will have. "
            "Classes help organize code logically. "
            "They support reusability and abstraction. "
            "Objects are instances of a class."
        ),
        (
            "What is an object?",2,
            "object, instance",
            "An object is an instance of a class. "
            "It represents a real-world entity in a program. "
            "Objects contain data and methods to operate on that data. "
            "They interact with other objects. "
            "Objects form the foundation of object-oriented programming."
        ),
        (
            "Explain encapsulation",2,
            "encapsulation, data hiding",
            "Encapsulation is the technique of wrapping data and methods into a single unit. "
            "It restricts direct access to internal data. "
            "Encapsulation improves data security. "
            "It prevents unintended modification of data. "
            "Access is provided through controlled methods."
        ),
        (
            "Explain inheritance",2,
            "inheritance, reuse",
            "Inheritance allows one class to acquire properties of another class. "
            "It promotes code reusability and reduces redundancy. "
            "The child class extends the functionality of the parent class. "
            "Inheritance supports hierarchical classification. "
            "It simplifies maintenance of large systems."
        ),
        (
            "Explain polymorphism",2,
            "polymorphism, many forms",
            "Polymorphism allows a method to take multiple forms. "
            "It enables the same operation to behave differently. "
            "Polymorphism is achieved through method overloading and overriding. "
            "It increases flexibility in programs. "
            "It supports dynamic behavior at runtime."
        ),
        (
            "Explain abstraction",2,
            "abstraction, hide details",
            "Abstraction hides complex implementation details. "
            "It shows only essential features to the user. "
            "Abstraction reduces complexity in software design. "
            "It is implemented using abstract classes and interfaces. "
            "It improves system clarity and maintainability."
        ),
        (
            "What is constructor?",2,
            "constructor, initialization",
            "A constructor is a special method used to initialize objects. "
            "It is automatically called when an object is created. "
            "Constructors assign initial values to data members. "
            "They have the same name as the class. "
            "Constructors improve object initialization."
        ),
        (
            "What is interface?",2,
            "interface, contract",
            "An interface defines a contract for classes to implement. "
            "It contains method declarations without implementation. "
            "Interfaces support multiple inheritance. "
            "They promote loose coupling. "
            "Interfaces enhance flexibility and scalability."
        ),
        (
            "What is method overloading?",2,
            "overloading, same name",
            "Method overloading allows multiple methods with the same name. "
            "Methods differ by parameter type or count. "
            "It improves code readability. "
            "Overloading provides compile-time polymorphism. "
            "It simplifies method usage."
        )
    ],
    "DBMS Questions": [
        (
            "What is DBMS?",2,
            "dbms, database",
            "DBMS stands for Database Management System. "
            "It is software used to create and manage databases. "
            "DBMS provides efficient data storage and retrieval. "
            "It ensures data security and integrity. "
            "Examples include MySQL and Oracle."
        ),
        (
            "What is a table?",2,
            "table, rows, columns",
            "A table stores data in rows and columns. "
            "Each row represents a record. "
            "Each column represents an attribute. "
            "Tables organize data efficiently. "
            "They form the basic structure of a database."
        ),
        (
            "What is a primary key?",2,
            "primary key, unique",
            "A primary key uniquely identifies a record in a table. "
            "It cannot contain duplicate or null values. "
            "Primary keys ensure data integrity. "
            "They improve data retrieval speed. "
            "Each table can have only one primary key."
        ),
        (
            "What is foreign key?",2,
            "foreign key, relation",
            "A foreign key establishes a relationship between tables. "
            "It refers to the primary key of another table. "
            "Foreign keys maintain referential integrity. "
            "They prevent invalid data insertion. "
            "They support relational database design."
        ),
        (
            "What is normalization?",2,
            "normalization, redundancy",
            "Normalization is the process of organizing data efficiently. "
            "It reduces data redundancy. "
            "Normalization improves data integrity. "
            "It divides tables into smaller related tables. "
            "Normal forms define normalization rules."
        ),
        (
            "Explain SQL",2,
            "sql, query",
            "SQL stands for Structured Query Language. "
            "It is used to interact with databases. "
            "SQL allows data insertion, retrieval, and modification. "
            "It supports database creation and management. "
            "SQL is widely used in relational databases."
        ),
        (
            "What is index?",2,
            "index, performance",
            "An index improves data retrieval speed. "
            "It creates a fast lookup structure. "
            "Indexes reduce query execution time. "
            "They consume additional storage. "
            "Indexes are used on frequently searched columns."
        ),
        (
            "What is transaction?",2,
            "transaction, ACID",
            "A transaction is a sequence of database operations. "
            "It must follow ACID properties. "
            "Transactions ensure data consistency. "
            "They either complete fully or rollback. "
            "Transactions are essential for reliability."
        ),
        (
            "What is join?",2,
            "join, combine tables",
            "A join combines records from multiple tables. "
            "It is based on related columns. "
            "Joins retrieve meaningful combined data. "
            "Types include inner and outer joins. "
            "Joins support relational queries."
        ),
        (
            "What is view?",2,
            "view, virtual table",
            "A view is a virtual table based on a query. "
            "It does not store data physically. "
            "Views simplify complex queries. "
            "They enhance security by restricting access. "
            "Views improve data abstraction."
        )
    ]
}


for topic_name, questions in topics_data.items():

    topic = db.query(Topic).filter(Topic.name == topic_name).first()
    if not topic:
        topic = Topic(name=topic_name)
        db.add(topic)
        db.commit()
        db.refresh(topic)

    for q_text, max_marks, key_concepts, answer_text in questions:

        existing_q = db.query(Question).filter(
            Question.question_text == q_text,
            Question.topic_id == topic.id
        ).first()

        if existing_q:
            continue

        question = Question(
            topic_id=topic.id,
            question_text=q_text,
            max_marks=2
        )
        db.add(question)
        db.commit()
        db.refresh(question)

        reference = ReferenceAnswer(
            question_id=question.id,
            answer_text=answer_text,
            key_concepts=key_concepts,
            source_type="teacher"
        )

        db.add(reference)
        db.commit()

db.close()
print("✅ Database seeded with 5 topics and 50 questions successfully!")