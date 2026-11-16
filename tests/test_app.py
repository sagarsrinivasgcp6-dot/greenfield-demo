import unittest
from fastapi.testclient import TestClient
import app

class TestTaskManager(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app.app)
        app.tasks_db.clear()
        app.next_task_id = 1

    def tearDown(self):
        app.tasks_db.clear()
        app.next_task_id = 1

    def test_health_check(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "healthy"})

    def test_list_tasks_empty(self):
        response = self.client.get("/tasks")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_create_and_get_task(self):
        payload = {"title": "Test Task", "description": "A test description", "priority": "high"}
        create_resp = self.client.post("/tasks", json=payload)
        self.assertEqual(create_resp.status_code, 201)
        data = create_resp.json()
        self.assertEqual(data["id"], 1)
        self.assertEqual(data["title"], "Test Task")
        self.assertEqual(data["description"], "A test description")
        self.assertEqual(data["status"], "pending")
        self.assertEqual(data["priority"], "high")

        get_resp = self.client.get("/tasks/1")
        self.assertEqual(get_resp.status_code, 200)
        self.assertEqual(get_resp.json()["title"], "Test Task")

    def test_get_nonexistent_task(self):
        response = self.client.get("/tasks/999")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Task not found")

    def test_update_task(self):
        create_resp = self.client.post("/tasks", json={"title": "Original Title"})
        self.assertEqual(create_resp.status_code, 201)
        task_id = create_resp.json()["id"]

        update_resp = self.client.put(f"/tasks/{task_id}", json={"title": "Updated Title", "status": "completed"})
        self.assertEqual(update_resp.status_code, 200)
        data = update_resp.json()
        self.assertEqual(data["title"], "Updated Title")
        self.assertEqual(data["status"], "completed")

    def test_delete_task(self):
        create_resp = self.client.post("/tasks", json={"title": "To Delete"})
        task_id = create_resp.json()["id"]

        delete_resp = self.client.delete(f"/tasks/{task_id}")
        self.assertEqual(delete_resp.status_code, 204)

        get_resp = self.client.get(f"/tasks/{task_id}")
        self.assertEqual(get_resp.status_code, 404)

    def test_validation_empty_title(self):
        response = self.client.post("/tasks", json={"title": ""})
        self.assertEqual(response.status_code, 422)

if __name__ == "__main__":
    unittest.main()
