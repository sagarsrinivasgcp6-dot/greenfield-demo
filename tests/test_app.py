import unittest
from fastapi.testclient import TestClient
from app import app, tasks_db

class TestTaskManagerApp(unittest.TestCase):
    def setUp(self):
        tasks_db.clear()
        self.client = TestClient(app)

    def test_health_check(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_create_task(self):
        payload = {"title": "Test Task", "description": "Description for test", "completed": False}
        response = self.client.post("/tasks", json=payload)
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["title"], "Test Task")
        self.assertEqual(data["description"], "Description for test")
        self.assertFalse(data["completed"])
        self.assertIn("id", data)

    def test_create_task_validation_error(self):
        payload = {"title": ""}
        response = self.client.post("/tasks", json=payload)
        self.assertEqual(response.status_code, 422)

    def test_list_tasks(self):
        self.client.post("/tasks", json={"title": "Task 1"})
        self.client.post("/tasks", json={"title": "Task 2"})
        response = self.client.get("/tasks")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 2)

    def test_get_task(self):
        create_res = self.client.post("/tasks", json={"title": "Task 1", "description": "Details"})
        task_id = create_res.json()["id"]
        response = self.client.get(f"/tasks/{task_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], "Task 1")

    def test_get_task_not_found(self):
        response = self.client.get("/tasks/99999")
        self.assertEqual(response.status_code, 404)

    def test_update_task(self):
        create_res = self.client.post("/tasks", json={"title": "Task 1", "completed": False})
        task_id = create_res.json()["id"]
        update_res = self.client.put(f"/tasks/{task_id}", json={"completed": True})
        self.assertEqual(update_res.status_code, 200)
        self.assertTrue(update_res.json()["completed"])
        self.assertEqual(update_res.json()["title"], "Task 1")

    def test_update_task_not_found(self):
        response = self.client.put("/tasks/99999", json={"title": "Updated"})
        self.assertEqual(response.status_code, 404)

    def test_delete_task(self):
        create_res = self.client.post("/tasks", json={"title": "Task 1"})
        task_id = create_res.json()["id"]
        del_res = self.client.delete(f"/tasks/{task_id}")
        self.assertEqual(del_res.status_code, 204)
        get_res = self.client.get(f"/tasks/{task_id}")
        self.assertEqual(get_res.status_code, 404)

    def test_delete_task_not_found(self):
        response = self.client.delete("/tasks/99999")
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main()
