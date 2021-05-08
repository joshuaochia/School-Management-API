# School-Management-API

## Flow chart
<img src="https://user-images.githubusercontent.com/70097729/117541209-604fb300-b045-11eb-90b2-aecac2b82893.png" alt="Girl in a jacket" >


This project is open source - the sole purpose of this project is to showcase my skills on REST API for future clients. Also, the Project is tested and exceptions are handled using custom or built in Django Exceptions.Note: Loggings are already set up, after cloning this project. Create a "logs" directory inside the Project DIR

1. Clone the project, please refer to this link for instructions https://git-scm.com/book/en/v2/Git-Basics-Getting-a-Git-Repository               
   Clone url: https://github.com/joshuaochia/School-Management-API.git
   
2. After cloning the project, go the directory of School-Management-API/SchoolManagement_API using terminal - After that, run the project by typing "python manage.py runserver" 


## School-Management-API Apps

### School Features
- Edit or add a new employee for the school (Admin Access only)
- Edit or add policies for the school (Admin Access only)
- Add new or edit existing departments of the school (Admin Access only)
-  Add new or edit existing courses of the school (Admin Access only)
-  Add new or edit existing section of the school (Admin Access only)
-  Add new or edit existing subjectsof the school (Admin Access only)

### Students Features
- List, retrieve, put, or delete new students (Admin Access)
- Assign new subjects to students (Admin Access)
- If user is teacher:
   - Edit or add grades to students
   - Assign new assignments/projects for a particular handled subject
   - View handled students or subjects
   - Edit profile info
- If user is students:
   - View grades 
   - Pass assignments/project for a particular subject
   - View classmates for a particular subject
   - Edit profile info

### Finance Features
- If student:
   - Add payment (Deduct current balance) (HR Access)
   - View student tuition balance
- If employee:
   - Record Leave (HR Access) (Deduct salary)
   - Record a Overtime (HR Access) (Add salary)
   - View current salary



## Populator Feature
### Populate the DB first with fake data

Command:
   - python manage.py [avail custom command] [int(argument)] 

E.G. python manage.py policies 5

Avail custom command:
   1. policies 
   2. courses
   3. departments
   4. employees
   5. schedule
   6. section
   7. student
   8. subject

Int Argument: How many fake data you want to create


