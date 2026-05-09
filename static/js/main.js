// --- Helper: Generic Fetch Wrapper ---
async function apiCall(url, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: { 'Content-Type': 'application/json' }
    };
    if (data) options.body = JSON.stringify(data);

    const response = await fetch(url, options);
    const result = await response.json();

    if (!response.ok) {
        alert(result.message || "Something went wrong");
        return null;
    }
    return result;
}

// --- 1. Authentication Logic ---
async function handleLogin(e) {
    e.preventDefault();
    const data = {
        username: document.getElementById('username').value,
        password: document.getElementById('password').value
    };
    const res = await apiCall('/api/login', 'POST', data);
    if (res) window.location.href = '/dashboard';
}

async function handleRegister(e) {
    e.preventDefault();
    const data = {
        username: document.getElementById('reg_username').value,
        password: document.getElementById('reg_password').value
    };
    const res = await apiCall('/api/register', 'POST', data);
    if (res) {
        alert("Registration successful! Please login.");
        window.location.href = '/login';
    }
}

async function handleLogout() {
    await apiCall('/api/logout', 'POST');
    window.location.href = '/';
}

// --- 2. Dashboard & Analytics ---
async function loadDashboard() {
    // Load Analytics (The Pandas/Numpy output)
    const stats = await apiCall('/api/analytics');
    if (stats) {
        document.getElementById('total_tasks').innerText = stats.total_tasks;
        document.getElementById('completed_tasks').innerText = stats.completed_tasks;
        document.getElementById('pending_tasks').innerText = stats.pending_tasks;
        document.getElementById('completion_pct').innerText = stats.completion_percentage + "%";
    }

    // Load Task List
    const tasks = await apiCall('/api/tasks');
    const container = document.getElementById('taskList');
    if (tasks && container) {
        container.innerHTML = tasks.map(t => `
            <div class="card" style="margin-bottom: 1rem; display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <span class="badge ${t.priority.toLowerCase()}">${t.priority}</span>
                    <strong style="margin-left: 10px; font-size: 1.1rem;">${t.title}</strong>
                    <p style="margin: 5px 0 0 0; color: #64748b;">${t.desc}</p>
                </div>
                <div>
                    <button onclick="window.location.href='/edit-task/${t.id}'" class="btn" style="background: #e2e8f0;">Edit</button>
                    <button onclick="deleteTask(${t.id})" class="btn" style="background: #fee2e2; color: #ef4444;">Delete</button>
                </div>
            </div>
        `).join('');
    }
}

// --- 3. Task Operations ---
async function handleAddTask(e) {
    e.preventDefault();
    const data = {
        title: document.getElementById('taskTitle').value,
        desc: document.getElementById('taskDesc').value,
        priority: document.getElementById('taskPriority').value
    };
    const res = await apiCall('/api/tasks', 'POST', data);
    if (res) window.location.href = '/dashboard';
}

async function deleteTask(id) {
    if (confirm("Delete this task?")) {
        const res = await apiCall(`/api/tasks/${id}`, 'DELETE');
        if (res) loadDashboard(); // Refresh UI
    }
}

// --- 4. Initialization Logic ---
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const regForm = document.getElementById('registerForm');
    const taskForm = document.getElementById('taskForm');
    
    if (loginForm) loginForm.addEventListener('submit', handleLogin);
    if (regForm) regForm.addEventListener('submit', handleRegister);
    if (taskForm) taskForm.addEventListener('submit', handleAddTask);
    
    // If we are on the dashboard, load data
    if (document.getElementById('taskList')) {
        loadDashboard();
    }
});

const socket = io();

socket.on('task_updated', (data) => {
    if (document.getElementById('taskList')) {
        console.log("Real-time update received!");
        loadDashboard(); 
    }
});