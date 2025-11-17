# AI-Powered Calling, Blogging & Automation System

## Overview
This project integrates **AI agents**, **Twilio calling**, **LinkedIn scraping**, and **automatic blog posting** into a single automation workflow.

It provides a unified interface to:

- Scrape LinkedIn data  
- Make automated phone calls using Twilio  
- Generate & publish blog posts  
- Use an AI agent capable of calling, posting, and responding to user prompts  

The frontend communicates with a backend built using **FastAPI**, **Twilio**, **Google Gemini**, and **MCP tools**.

---

## Features

### **1. LinkedIn Scraping**
You can extract LinkedIn profile data by uploading:

- **A CSV file** containing LinkedIn profile links  
- **An XPath file** defining what data to scrape  

After uploading both files, the system automatically scrapes LinkedIn and displays structured results.

---

### **2. Automated Calling (Twilio)**

Two calling options are supported:

#### **a. Bulk Calling**
- Upload a **.txt file**
- The file must contain **one phone number per line**, registered with Twilio  
  Example:
+19876543210

The system will automatically start calling each number and show summaries in the dashboard.

#### **b. Dial Pad Calling**
Call a single customer by entering:

- Customer phone number  
- Your **Twilio** registered phone number  
- A message  

The backend initiates a call and also sends an SMS automatically.

---

### **3. Blogging System**

Two ways to create blog posts:

#### **a. Manual Blog Posting**
Write your own blog content in the editor and publish instantly.

#### **b. AI-Generated Blogging**
Give the AI a prompt and it will generate a complete blog post automatically.

All posts appear immediately in the **Generated Posts** section.

---

### **4. AI Agent (Gemini + MCP Tools)**

Chat with the AI to perform special tasks:

- Make calls  
- Create blog posts  
- Answer questions  
- Execute MCP tools  

> **Note:**  
> The AI agent processes **only the current request**.  
> It does **not** maintain long-term memory.

---

## Installation

### **1. Clone the Repository**
git clone <repository-url>
cd <project-folder>
**2. Install Frontend Dependencies**
npm install

**3. Install Backend Dependencies**
pip install -r requirements.txt

**4. Run the Backend Server**
Start FastAPI using Uvicorn:
uvicorn test_server:app --reload

**5. Required Environment Variables**
Create a .env file:
GEMINI_API_KEY=your_gemini_key
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_DEFAULT_PHONE=your_twilio_phone_number


### **Usage**
**1. Start the Frontend**
Open your project in VS Code → Run Live Server to open the UI.

From the UI you can:

Upload CSV + XPath for LinkedIn scraping

Upload .txt for bulk calling

Use the dial pad

Generate blogs (manual or AI)

Chat with the AI agent

**2. Backend Endpoints**
The backend exposes:

Endpoint |	Purpose
-------- | ---------
/ask-gemini   |	AI agent tasks (calling, blogging, responses)
/calltool	Direct  | calling through Twilio (no AI)
/call-status  |	Twilio webhook listener
/	  |  Health check

**Contributing**
Contributions, issues, and feature requests are welcome.
Feel free to open a pull request or submit an issue.
