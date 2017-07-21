common = new com.mirantis.mk.Common()

/**
 * Creates env according to input params by DevOps tool
 * 
 * @param path Path to dos.py 
 * @param type Path to template having been created
 */
def createDevOpsEnv(path, tpl){
    echo "${path} ${tpl}"
    return sh(script:"""
    export ENV_NAME=${params.ENV_NAME} &&
    ${path} create-env ${tpl}
    """, returnStdout: true)
}   

node {
    stage ('creating environmet') {
        if ("${params.ENV_NAME}" == '') {
            error("ENV_NAME have to be defined")
        }
        echo "${params.ENV_NAME} ${params.TEMPLATE}"
        if ("${params.TEMPLATE}" == 'Single') {
            echo "Single"
            tpl = '/var/fuel-devops-venv/tpl/clound-init-single.yaml'
//          createDevOpsEnv('Create')
        } else if ("${params.TEMPLATE}" == 'Multi') {
            echo "Multi"
        }
        createDevOpsEnv('/var/fuel-devops-venv/fuel-devops-venv/bin/dos.py',"${tpl}")
    }
}

