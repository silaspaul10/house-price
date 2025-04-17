pipeline {
    agent any

    environment {
        IMAGE_NAME = "house-price-app"
        CONTAINER_NAME = "house-price-container"
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/nithin282004/House-Price-Prediction'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building Docker Image..."
                    bat "docker build -t ${IMAGE_NAME} ."
                }
            }
        }

        stage('Stop and Remove Old Container') {
    steps {
        script {
            echo "Stopping and removing old container..."
            bat """
            docker ps -q -f name=${CONTAINER_NAME}
            docker ps -a -q -f name=${CONTAINER_NAME}
            """
        }
    }
}

        stage('Run App with Docker Compose') {
            steps {
                script {
                    echo "Running app with Docker Compose..."
                    bat "docker-compose up -d"
                    
                    // Capture Docker Compose logs
                    echo "Docker Compose Logs:"
                    bat "docker-compose logs --tail=10"
                    
                    // Show the status of containers
                    bat "docker-compose ps"
                }
            }
        }
    }

    post {
        failure {
            echo '❌ Build or deployment failed!'
        }
        success {
            echo '✅ App deployed successfully.'
        }
    }
}
