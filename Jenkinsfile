pipeline {
    agent any

    environment {
        VENV = "venv"
        BUILD_BRANCH = "unknown"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
                script {
                    BUILD_BRANCH = sh(
                        script: '''
                        git branch -r --contains HEAD | sed 's|origin/||' | head -n 1
                        ''',
                        returnStdout: true
                    ).trim()

                    if (!BUILD_BRANCH) {
                        BUILD_BRANCH = "unknown"
                    }
                }
                echo "🔹 Building branch: ${BUILD_BRANCH}"
            }
        }

        stage('Install OS Dependencies') {
            steps {
                sh '''
                sudo apt update
                sudo apt install -y python3.10-venv python3-pip
                '''
            }
        }

        stage('Setup Python Environment') {
            steps {
                sh '''
                python3 -m venv ${VENV}
                . ${VENV}/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Branch Specific Validation') {
            steps {
                sh '''
                echo "Running branch-specific checks..."

                if [ "${BUILD_BRANCH}" = "feature_Monitor" ]; then
                    echo "✅ feature_Monitor branch detected"
                else
                    echo "✅ main branch detected – skipping feature checks"
                fi
                '''
            }
        }

        stage('Package & Archive') {
            steps {
                sh '''
                tar -czf monitoring-dashboard-${BUILD_BRANCH}.tar.gz app.py templates requirements.txt
                ls -l monitoring-dashboard-${BUILD_BRANCH}.tar.gz
                '''
                archiveArtifacts artifacts: '*.tar.gz', fingerprint: true
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
