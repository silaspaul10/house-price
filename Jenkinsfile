pipeline {
    agent any

    environment {
        IMAGE_NAME = "house-price-app"
        CONTAINER_NAME = "house-price-container"
    }

    stages {
        stage('Checkout Code') {
    steps {
        git credentialsId: 'github-ssh', url: 'git@github.com:silaspaul10/house-price.git', branch: 'main'
    }
}

        stage('Prepare Environment') {
            steps {
                // Disable SSL certificate verification for Git (temporary/testing fix)
                bat 'git config --global http.sslVerify false'
            }
        }

        stage('Checkout Code') {
            steps {
                git url: 'git@github.com:silaspaul10/house-price.git', branch: 'main'
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
                    docker stop ${CONTAINER_NAME} || echo "Container not running"
                    docker rm ${CONTAINER_NAME} || echo "No container to remove"
                    """
                }
            }
        }

        stage('Run App with Docker Compose') {
            steps {
                script {
                    echo "Running app with Docker Compose..."
                    bat "docker-compose up -d"

                    echo "Docker Compose Logs:"
                    bat "docker-compose logs --tail=10"

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
