# GCP AI Code Reviewer

An AI-powered code review web application built using **Google Cloud Platform, Firebase, and Gemini AI**.

The application allows developers to paste code into a web interface and receive **automated AI feedback on bugs, security issues, and potential improvements**.

This project demonstrates how **Generative AI models can be integrated with cloud services to automate developer workflows like code review**.

---

## Demo

Paste your code → Click **Review Code** → Receive AI-generated feedback.

Example suggestions include:

- Bug detection
- Security vulnerabilities
- Performance improvements
- Best practice recommendations

---

## Architecture

```
User Browser
      │
      ▼
Firebase Hosting (Frontend UI)
      │
      ▼
Cloud Functions (Backend API)
      │
      ▼
Gemini AI / Vertex AI
      │
      ▼
AI Code Review Response
```

---

## Features

- AI-powered code review
- Detects potential bugs
- Identifies security issues
- Suggests performance improvements
- Provides best-practice recommendations
- Simple web interface
- Cloud-native architecture

---

## Technologies Used

- Google Cloud Platform (GCP)
- Firebase Hosting
- Firebase Cloud Functions
- Vertex AI / Gemini API
- JavaScript / Node.js
- HTML / CSS

---

## How It Works

1. User pastes code into the web interface.
2. The frontend sends the code to a Firebase Cloud Function.
3. The Cloud Function sends the code to the **Gemini AI model**.
4. Gemini analyzes the code and generates a review.
5. The review is returned and displayed to the user.

---

## Installation

Clone the repository

```bash
git clone https://github.com/Visvatharsan/GCP_AI_Code_Reviewer.git
```

Navigate to the project folder

```bash
cd GCP_AI_Code_Reviewer
```

Install dependencies

```bash
npm install
```

Login to Firebase

```bash
firebase login
```

Deploy the project

```bash
firebase deploy
```

---

## Project Structure

```
GCP_AI_Code_Reviewer
│
├── functions
│   └── index.js
│
├── public
│   └── index.html
│
├── firebase.json
└── README.md
```

---

## Example Input

```java
for(int i = 0; i <= arr.length; i++){
    System.out.println(arr[i]);
}
```

### Example AI Review

- Possible **ArrayIndexOutOfBoundsException**
- Loop condition should be `i < arr.length`
- Improve error handling
- Follow secure coding practices

---

## Future Improvements

- GitHub Pull Request AI review
- Syntax highlighting for code input
- Multiple programming language support
- AI code quality scoring
- Authentication and user history

---

## Learning Outcomes

Through this project I learned:

- Integrating AI models with cloud services
- Deploying serverless backends with Firebase
- Debugging real-world cloud infrastructure issues
- Building scalable AI-powered applications

---

## Author

**Visvatharsan**

GitHub:  
https://github.com/Visvatharsan
