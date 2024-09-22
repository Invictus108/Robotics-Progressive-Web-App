# Robotics Team Organizer - A Flask Progressive Web App

This **Flask Progressive Web App** is designed to help small robotics teams stay organized by keeping detailed records, managing team tasks, and tracking important information. The app is fully customizable and allows teams to download it as an app for their iOS, Android, or Windows 11 devices.

## Key Features

- **Progressive Web App (PWA)**: 
  - This app is designed as a Progressive Web App, which means users can install it directly onto their devices (iOS, Android, or Windows 11) for a native app-like experience. 
  - Learn more about Progressive Web Apps [here](https://support.google.com/chrome/answer/9658361?hl=en&co=GENIE.Platform%3DDesktop).
  
- **Flask and SQLite3 Backend**: 
  - The app uses Flask as its web framework and SQLite3 as the database to store user and team information securely.

## Multi-Page Features

The app offers a wide range of features tailored to robotics teams, including:

- **Individual Logins**: Each team member has their own login, providing a personalized dashboard.
- **Admin Control Panel**: A special admin panel to manage team settings, users, and more.
- **Score Keeping Page**: A dedicated page for keeping track of scores during practice sessions.
- **Game Records**: A page where game outcomes and performance stats are recorded.
- **Team Agenda**: A shared team agenda that all members can view and follow.
- **Personal Agenda**: Each user has their own personal to-do list that is unique to their login.
- **Calendar**: A calendar to keep track of important team events, meetings, and deadlines.
- **Team Roster**: View and manage a roster of all team members.
- **Part Request Form**: Submit part requests for team approval, streamlining team inventory management.

## Admin Approval System

- **Form Submissions**: All form submissions, aside from the personal to-do list, must go through admin approval, ensuring accountability and consistency.

## Customizing the App

Personalizing the app for your own team is simple and only requires a few steps:

1. **Change the Team Name**:
   - In the `layout.html` file located in the `templates` folder, replace **"Ridgebots"** with your team’s name.
   
2. **Add Your Team Logo or Photo**:
   - Customize the **index** page by adding a fun team photo or your team’s logo to make the app feel more personal.

3. **Admin Account Setup**:
   - Log in using the default admin credentials: 
     - **Username**: `admin`
     - **Password**: `admin`
   - Once logged in, make sure to change the password to secure the admin account.

## Hosting the App

One of the easiest ways to host this application is through **PythonAnywhere**. It provides a free hosting solution for small projects like this. 

- Watch this helpful video tutorial on deploying Flask apps on PythonAnywhere: [How to Deploy Flask Apps on PythonAnywhere](https://www.youtube.com/watch?v=M4sxSoRZLtI).

## Tools and Technologies

- **Flask**: A lightweight Python web framework used for handling routing and user interaction.
- **SQLite3**: A simple and efficient database for managing user data, team records, and agenda items.
- **Progressive Web App (PWA)**: Allows users to install the app on their devices for easy access without needing a dedicated app store.

## Credits

- Special thanks to the **CS50 Finance** template for providing the foundation for this project.
- This app was inspired by the need to create an organizational tool tailored specifically for small robotics teams.

