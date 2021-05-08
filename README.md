# School-Management-API

## Flow chart
<img src="https://user-images.githubusercontent.com/70097729/117541209-604fb300-b045-11eb-90b2-aecac2b82893.png" alt="" >


This project is open source - the sole purpose of this project is to showcase my skills on REST API for future clients. Also, the Project is tested and exceptions are handled using custom or built in Django Exceptions.Note: Loggings are already set up, after cloning this project. Create a "logs" directory inside the Project DIR

1. Clone the project, please refer to this link for instructions https://git-scm.com/book/en/v2/Git-Basics-Getting-a-Git-Repository               
   Clone url: https://github.com/joshuaochia/School-Management-API.git
   
2. After cloning the project, go the directory of School-Management-API/SchoolManagement_API using terminal - After that, run the project by typing "python manage.py runserver" 


## School-Management-API Apps

### School Features

<img src="https://user-images.githubusercontent.com/70097729/117542340-ca1e8b80-b04a-11eb-8ef5-cda0b049b32c.png" alt="" >

- Create employees for the school (Admin Access)
- Edit or add policies (Admin Access)
- Add or edit existing departments (Admin Access)
- Create or edit existing courses (Admin Access)
- Add or edit existing section (Admin Access)
- Create or edit existing subjects (Admin Access)

### Students Features

<img src="https://user-images.githubusercontent.com/70097729/117542446-474a0080-b04b-11eb-80d8-b21dc0371349.png" alt="" >

- List, retrieve, put, post, or delete new students (Admin Access)
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

<img src="https://user-images.githubusercontent.com/70097729/117542478-60eb4800-b04b-11eb-9707-b854c3bb019d.png" alt="" >

- If student:
   - Add payment (Deduct current balance) (HR Access)
   - View student tuition balance
- If employee:
   - Record Leave (HR Access) (Deduct salary)
   - Record a Overtime (HR Access) (Add salary)
   - View current salary



## Populator Feature
### Populate the DB first with fake data

<img src="https://user-images.githubusercontent.com/70097729/117542756-6eed9880-b04c-11eb-9c39-c4eaf100ad58.png" alt="" >

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


