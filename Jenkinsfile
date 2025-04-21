pipeline {
    agent any

    environment {
        IMAGE_NAME = "house-price-app"
        DOCKER_HUB_USER = "10silaspaul" // Replace with your Docker Hub username
    }

    stages {
        stage('Checkout Code') {
            steps {
                git credentialsId: 'github-https', url: 'https://github.com/silaspaul10/house-price.git', branch: 'main'

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

        stage('Run App with Docker Compose') {
            steps {
                script {
                    echo "Running app with Docker Compose..."
                    bat "docker-compose up -d"
                    bat "docker-compose logs --tail=10"
                    bat "docker-compose ps"
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'DOCKER_HUB_USER', passwordVariable: 'DOCKER_HUB_PASS')]) {
                    script {
                        echo "Tagging and pushing to Docker Hub..."
                        bat "docker tag ${IMAGE_NAME} ${DOCKER_HUB_USER}/${IMAGE_NAME}:latest"
                        bat "docker login -u ${DOCKER_HUB_USER} -p ${DOCKER_HUB_PASS}"
                        bat "docker push ${DOCKER_HUB_USER}/${IMAGE_NAME}:latest"
                    }
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
