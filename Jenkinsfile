pipeline {
    agent none
    stages {
        stage('Tests') {
            matrix {
                agent { label "${NODENAME}" }
                axes {
                    axis {
                        name 'NODENAME'
                        values 'tsa', 'daint', 'dom', 'manali', 'balfrin'
                    }
                }
                post {
                    always {
                        archiveArtifacts artifacts: '*.log', allowEmptyArchive: true
                        echo 'Cleaning up workspace'
                        deleteDir()
                    }
                }
                stages {
                    stage('Clone') {
                        steps {
                            sh """
                            if [ ${NODENAME} == 'tsa' ]; then
                                module load git
                            fi
                            git clone --depth 1 --recurse-submodules --shallow-submodules -b dev_v0.18.1 https://github.com/C2SM/spack-c2sm.git ${NODENAME}
                            """
                        }
                    }
                    stage('Unit Tests') {
                        steps {
                            sh "${NODENAME}/test/unit/test_env_setup_machine.sh ${NODENAME} >> ${NODENAME}_test_env_setup_machine.log 2>&1"
                        }
                    }
<<<<<<< HEAD
                    post {
                        always {
                            withCredentials([string(credentialsId: 'd976fe24-cabf-479e-854f-587c152644bc', variable: 'GITHUB_AUTH_TOKEN')]) {
                                sh"""
                                module load cray-python
                                python send_summary_as_comment_to_PR.py
                                """
                            }
                            archiveArtifacts artifacts: '*.log', allowEmptyArchive: true
                            echo 'Cleaning up workspace'
                            deleteDir() 
=======
                    stage('Integration Tests') {
                        steps {
                            sh """
                            . ${NODENAME}/setup-env.sh
                            python3 ${NODENAME}/test/integration/test_spack_info.py >> ${NODENAME}_test_spack_info.log 2>&1
                            python3 ${NODENAME}/test/integration/test_spack_spec.py >> ${NODENAME}_test_spack_spec.log 2>&1
                            """
>>>>>>> origin/dev_v0.18.1
                        }
                    }
                }
            }
        }
    }
}
