AI SOC Assistant
============================

AI-powered SOC Assistant 
_A smart security tool that allows analysts to query SIEM logs using natural language, auto-generate queries, and visualize results for faster investigations._

---

Description
---------------
The **AI SOC Assistant** is an open-source project designed to simplify Security Operations Center (SOC) workflows.  
Instead of writing complex SIEM queries manually, analysts can type **natural language questions**, and the assistant will automatically generate queries, run them, and visualize the results.

This project is aimed at:
- Security analysts looking to save time during investigations  
- SOC teams wanting to standardize query building  
- Students and researchers exploring AI-assisted cybersecurity  

---

 Features
-----------
* **Natural Language Queries** – ask in plain English, get SIEM queries automatically.  
* **Log Visualization** – interactive charts and tables for faster analysis.  
* **Investigation Chat** – chat-based interface for guided triage.  
* **Authentication** – Single Sign-On (SSO) support.  
* **Scalable Design** – modular architecture that can connect to different SIEM backends.  

---

🧰 Tech Stack
--------------------
| Category   | Technology |
|------------|------------|
| Backend    | Python (Flask/FastAPI) |
| Frontend   | JavaScript |
| AI/NLP     | NLP models for natural language understanding |
| SIEM       | Connectors to Splunk, ELK, or other SIEMs |
| Tools      | UXaccelerate, Pandas, Matplotlib |

---

📁 Project Structure
---------------------
* **`src/`** – Core backend code (query engine, NLP modules).  
* **`ui/`** – Frontend UI for chat and visualization.  
* **`assets/`** – Screenshots and static files (e.g., `interface.png`).  
* **`tests/`** – Unit and integration tests.  
* **`docs/`** – Documentation and setup guides.  

---

⚙️ How to Run
----------------
### Setup
```bash
git clone https://github.com/SadashivPole/sadashivpole-AI-SOC-Assistant.git
cd sadashivpole-AI-SOC-Assistant
pip install -r requirements.txt

