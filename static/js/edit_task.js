document.addEventListener('DOMContentLoaded', async () => {
    const taskId = document.getElementById('edit_task_id').value;
    
    // Fetch current data (We use our existing GET endpoint or create a single task getter)
    const tasks = await apiCall('/api/tasks'); 
    const task = tasks.find(t => t.id == taskId);
    
    if (task) {
        document.getElementById('edit_title').value = task.title;
        document.getElementById('edit_desc').value = task.desc;
        document.getElementById('edit_priority').value = task.priority;
        document.getElementById('edit_status').value = task.status;
    }

    document.getElementById('editTaskForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const updatedData = {
            title: document.getElementById('edit_title').value,
            desc: document.getElementById('edit_desc').value,
            priority: document.getElementById('edit_priority').value,
            status: document.getElementById('edit_status').value
        };
        await apiCall(`/api/tasks/${taskId}`, 'PUT', updatedData);
        window.location.href = '/dashboard';
    });
});