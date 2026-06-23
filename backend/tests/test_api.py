import pytest
from app import app, db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_health(client):
    response = client.get('/api/health')
    assert response.status_code == 200
    assert response.json['status'] == 'ok'

def test_create_task(client):
    response = client.post('/api/tasks', json={
        'title': 'Tarea de prueba',
        'description': 'Descripción de prueba'
    })
    assert response.status_code == 201
    assert response.json['title'] == 'Tarea de prueba'
    assert response.json['done'] == False

def test_get_tasks_empty(client):
    response = client.get('/api/tasks')
    assert response.status_code == 200
    assert response.json == []

def test_get_tasks_with_data(client):
    client.post('/api/tasks', json={'title': 'Tarea 1'})
    client.post('/api/tasks', json={'title': 'Tarea 2'})
    
    response = client.get('/api/tasks')
    assert response.status_code == 200
    assert len(response.json) == 2

def test_get_task_by_id(client):
    create_response = client.post('/api/tasks', json={'title': 'Tarea única'})
    task_id = create_response.json['id']
    
    response = client.get(f'/api/tasks/{task_id}')
    assert response.status_code == 200
    assert response.json['title'] == 'Tarea única'

def test_get_task_not_found(client):
    response = client.get('/api/tasks/999')
    assert response.status_code == 404
    assert response.json['error'] == 'Tarea no encontrada'

def test_update_task(client):
    create_response = client.post('/api/tasks', json={'title': 'Original'})
    task_id = create_response.json['id']
    
    response = client.put(f'/api/tasks/{task_id}', json={
        'title': 'Actualizado',
        'done': True
    })
    assert response.status_code == 200
    assert response.json['title'] == 'Actualizado'
    assert response.json['done'] == True

def test_update_task_not_found(client):
    response = client.put('/api/tasks/999', json={'title': 'Nuevo'})
    assert response.status_code == 404

def test_delete_task(client):
    create_response = client.post('/api/tasks', json={'title': 'Eliminar'})
    task_id = create_response.json['id']
    
    response = client.delete(f'/api/tasks/{task_id}')
    assert response.status_code == 200
    assert response.json['message'] == 'Tarea eliminada'
    
    # Verificar que ya no existe
    get_response = client.get(f'/api/tasks/{task_id}')
    assert get_response.status_code == 404

def test_delete_task_not_found(client):
    response = client.delete('/api/tasks/999')
    assert response.status_code == 404

def test_create_task_without_title(client):
    response = client.post('/api/tasks', json={'description': 'Sin título'})
    assert response.status_code == 400
    assert 'error' in response.json