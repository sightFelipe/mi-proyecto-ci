pipeline {
    agent any

    environment {
        COMPOSE_PROJECT_NAME = 'mi-proyecto-ci'
    }

    stages {
        stage('Checkout') {
            steps {
                echo '==> Descargando codigo desde GitHub...'
                checkout scm
            }
        }

        stage('Build') {
            steps {
                echo '==> Construyendo imagenes Docker...'
                sh 'docker compose build'
            }
        }

        stage('Test') {
            steps {
                echo '==> Ejecutando pruebas pytest...'
                sh 'docker compose run --rm backend pytest -v --tb=short'
            }
        }

        stage('Deploy') {
            steps {
                echo '==> Desplegando contenedores...'
                sh 'docker compose up -d'
            }
        }

        stage('Health Check') {
            steps {
                echo '==> Verificando API...'
                sh '''
                    for i in 1 2 3 4 5; do
                        if curl -sf http://mi-backend:5000/api/health > /dev/null; then
                            echo "Backend respondiendo correctamente."
                            curl -s http://mi-backend:5000/api/health
                            exit 0
                        fi
                        echo "Intento $i: backend no responde, esperando..."
                        sleep 3
                    done
                    echo "Backend no respondio despues de 5 intentos."
                    exit 1
                '''
            }
        }
    }

    post {
        success {
            echo '==> Pipeline ejecutado exitosamente.'
            echo 'API disponible en: http://localhost:5000'
        }
        failure {
            echo '==> Pipeline fallo. Revisar console output.'
        }
        always {
            echo "Build #${env.BUILD_NUMBER} finalizado."
        }
    }
}