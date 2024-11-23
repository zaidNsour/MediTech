# MediTech

The Medical Test Management System is a API designed to simplify medical test processes and enhance the patient experience. This system allows patients to view, manage, and interpret their medical test results, schedule appointments, and access critical healthcare-related information.


## Features

- **Authentication**: Secure login and registration for users.

- **Display Medical Test Results**: Patients can view their test results.

- **Interpret Results**: Provides AI powered, easy-to-understand interpretations of test results.

- **Patient-Specific Appointments**: View appointments tailored to each patient.

- **Schedule Appointments**: implify the process of scheduling medical appointments.
  
- **Request to Cancel Appointment**: Allows patients to cancel their appointments if needed.

- **Profile Management**: Add or update personal and medical profile information.
  
- **Test Information**: Access detailed information about various medical tests.

- **Help and Support**: Users can find assistance and support for using the platform.

- **FAQs**: View common questions and their answers for a better understanding of the platform.

 - **Notifications**: Receive notifications about appointments, updates, and other alerts.

 - **Reset Account via Email**: Reset password securely through email.

 - **Verify User**: Ensure user verification for secure access.

  - **Admin Dashboard**: Admins have access to a powerful dashboard to manage users, appointments, and test data.


## Tech Stack
- Backend: Flask (Python)
- Database: SQLite
- Authentication: Flask-Login
- 

## Python Version
  This project requires Python 3.12.7


## Getting Started

Step 1. Clone the repository:
```bash
git clone https://github.com/zaidNsour/MediTech.git
```


Step 2. Navigate into the project directory:
```bash
cd MediTech
```


Step 3. Install the required dependencies:
 ```bash
   pip install -r requirements.txt
```


Step 4. Set up the following environment variables:
```bash
  export SECRET_KEY=your-secret-key
  export EMAIL_USER=your-email@example.com
  export EMAIL_PASS=your-email-password
```

Step 5. Run the app:
```bash
  flask run
```

## Contributing
 If you'd like to contribute to the project, follow these steps:
 
1- Fork the repository.

2- Create a new branch: 

```bash
git checkout -b feature/new-feature
```

3- Make your changes and commit them:

```bash
git commit -m 'Add new feature'
```

4- Push to the branch: 

```bash
git push origin feature/new-feature
```

5- Submit a pull request.

## License
This project is licensed under the MIT License.
