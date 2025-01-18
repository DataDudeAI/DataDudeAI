## 🚀 **Overview**
DataDude is a cutting-edge web-based analytics and campaign tracking platform designed to:
- Track visits in real-time.
- Manage and monitor campaigns effortlessly.
- Enable deep linking with precision.

Powered by **Flask** (Python) for backend and **vanilla JavaScript** for frontend, DataDude delivers a seamless user experience with actionable insights.

---

## 🗂️ **Project Structure**
```
📁 datadude
├── app.py              # Main Flask application
├── database.py         # Database operations and schema
├── geo_service.py      # User agent and device detection
├── check_db.py         # Database testing utility
├── services/
│   └── tracking_service.py # Visit tracking logic
├── models/
│   ├── campaign.py     # Campaign data model
│   └── deeplink.py     # Deep link data model
├── static/
│   ├── css/
│   │   └── style.css   # Global styles
│   └── js/
│       ├── analytics.js
│       ├── campaign.js
│       ├── dashboard.js
│       ├── deeplink.js
│       └── track.js
├── templates/
│   ├── analytics.html
│   ├── campaigns.html
│   ├── index.html
│   └── deeplink.html
└── visits.db           # SQLite database
```
---

## 🔑 **Core Components**

### 1. **Backend (Python/Flask)**

#### 🛠️ Database
- SQLite with tables for campaigns and visits.
- Campaign tracking and visit data storage.
- Schema highlights:

```sql
CREATE TABLE campaigns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    short_code TEXT UNIQUE NOT NULL,
    original_url TEXT NOT NULL,
    type TEXT NOT NULL,
    status TEXT DEFAULT 'active',
    utm_source TEXT,
    utm_medium TEXT,
    utm_campaign TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```
```sql
CREATE TABLE visits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    campaign_code TEXT,
    session_id TEXT,
    ip_address TEXT,
    user_agent TEXT,
    referrer TEXT,
    visit_data TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(campaign_code) REFERENCES campaigns(short_code)
);
```

#### 🛠️ Tracking Service
- Handles real-time tracking.
- Processes user agent, browser, and device detection.

#### 🛠️ Geo Service
- Extracts geographic and device-specific data from user agents.

---

### 2. **Frontend (JavaScript)**

#### 📊 Dashboard (dashboard.js)
- Real-time statistics and mini charts.
- Displays recent activity feed.

#### 📈 Analytics (analytics.js)
- Advanced data visualizations.
- Includes timeline views and filtering.

#### 📋 Campaign Management (campaign.js)
- CRUD operations for campaigns.
- URL shortening and campaign performance stats.

---

## 🌟 **Key Features**

### 1. 📑 **Campaign Tracking**
- URL shortening.
- Campaign attribution.
- Real-time updates and statistics.

### 2. 🧩 **Analytics**
- Device and browser detection.
- Geographic insights.
- Time-based analysis.

### 3. 💻 **User Interface**
- Interactive and responsive.
- Error-handling for smoother user experience.

---

## 🛠️ **Development Setup**

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/datadude.git
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Initialize the database:
   ```bash
   python check_db.py
   ```

4. Run the development server:
   ```bash
   python app.py
   ```

---

## 🌍 **API Endpoints**

### 🟢 Campaign Endpoints
- **GET /api/campaigns** - List all campaigns.
- **POST /api/campaigns** - Create a new campaign.
- **GET /api/campaigns/<short_code>** - Fetch campaign details.
- **PUT /api/campaigns/<short_code>** - Update a campaign.
- **DELETE /api/campaigns/<short_code>** - Delete a campaign.

### 🟢 Analytics Endpoints
- **GET /api/stats** - Fetch analytics overview.
- **GET /api/visits** - Retrieve visit details.
- **POST /track** - Record a new visit.

---

## 💡 **Best Practices**

### 1. **Code Organization**
- Group related functionality in services.
- Maintain a clear separation of concerns.

### 2. **Error Handling**
- Implement robust try-catch blocks.
- Log errors for troubleshooting.

### 3. **Frontend Development**
- Use descriptive naming conventions.
- Ensure responsive and accessible designs.

---

## 🧪 **Testing**

1. **Database Testing:**
   ```bash
   python check_db.py
   ```

2. **API Testing:**
   - Use tools like Postman.
   - Test CRUD operations and validate error handling.

---

## 🚀 **Deployment**

1. **Update Configuration:**
   - Set `DEBUG = False` in production.
   - Configure logging and secret keys.

2. **Database:**
   - Initialize and regularly back up.

3. **Server Setup:**
   - Use a reverse proxy (e.g., Nginx).
   - Enable SSL for secure communication.

---

## 📅 **Maintenance**

### Regular Tasks
- Database backups.
- Performance monitoring.
- Log rotation.

### Updates
- Regularly update dependencies.
- Monitor security advisories.

---

## 📩 **Support**
For technical queries or support:
- Review the documentation.
- Report issues on the issue tracker.
- Contact the development team.

---

### 🎉 **Animation Suggestion**
For a better user experience, consider integrating animations using libraries like **Lottie** or **CSS Animations** for:
1. Page loading transitions.
2. Button hover effects.
3. Real-time chart updates.

---

**DataDude** – Your all-in-one AI-powered campaign tracking and analytics platform. Harness the power of data with ease!


- 👯 I’m looking to collaborate on ...
- 🤔 I’m looking for help with ...
- 💬 Ask me about ...
- 📫 How to reach me: ...
- 😄 Pronouns: ...
- ⚡ Fun fact: ...
-->
