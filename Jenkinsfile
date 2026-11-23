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