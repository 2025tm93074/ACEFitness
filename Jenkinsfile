pipeline {

    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    environment {
        IMAGE_NAME = 'aceest-fitness'
        IMAGE_TAG = "build-${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
                echo 'Source code checked out successfully.'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    echo "Building ACEest Fitness Docker image..."

                    docker build \
                        -t ${IMAGE_NAME}:${IMAGE_TAG} \
                        .
                '''
            }
        }

        stage('Run Pytest') {
            steps {
                script {
                    def containerName = "aceest-test-${env.BUILD_NUMBER}"

                    sh """
                        docker rm -f ${containerName} 2>/dev/null || true
                    """

                    def testStatus = sh(
                        returnStatus: true,
                        script: """
                            docker run \
                                --name ${containerName} \
                                ${IMAGE_NAME}:${IMAGE_TAG} \
                                python -m pytest -v \
                                --junitxml=/tmp/pytest-results.xml
                        """
                    )

                    sh """
                        docker cp \
                            ${containerName}:/tmp/pytest-results.xml \
                            "\${WORKSPACE}/pytest-results.xml" \
                            2>/dev/null || true

                        docker rm -f ${containerName} \
                            2>/dev/null || true
                    """

                    if (testStatus != 0) {
                        error('Pytest failed. Docker image will not be published.')
                    }
                }
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    def scannerHome = tool 'SonarScanner'

                    withSonarQubeEnv('SonarQube') {
                        sh "${scannerHome}/bin/sonar-scanner"
                    }
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                        set -e

                        docker tag aceest-fitness:build-${BUILD_NUMBER} \
                            ${DOCKER_USER}/aceest-fitness:build-${BUILD_NUMBER}

                        docker tag aceest-fitness:build-${BUILD_NUMBER} \
                            ${DOCKER_USER}/aceest-fitness:latest

                        echo "$DOCKER_PASS" | docker login \
                            -u "$DOCKER_USER" --password-stdin

                        docker push ${DOCKER_USER}/aceest-fitness:build-${BUILD_NUMBER}
                        docker push ${DOCKER_USER}/aceest-fitness:latest

                        docker logout
                    '''
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
    }

    post {

        always {
            junit(
                testResults: 'pytest-results.xml',
                allowEmptyResults: true
            )
        }

        success {
            echo 'ACEest Fitness CI pipeline completed successfully.'
        }

        failure {
            echo 'ACEest Fitness CI pipeline failed.'
        }
    }
}