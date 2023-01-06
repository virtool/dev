# Configuration
config.define_string_list("to-edit")

cfg = config.parse()
to_edit = cfg.get('to-edit', [])

# Backing Services and Components
load('ext://helm_resource', 'helm_resource', 'helm_repo')

helm_repo('bitnami', 'https://charts.bitnami.com/bitnami', labels=['helm'])
helm_repo('kedacore', 'https://kedacore.github.io/charts', labels=['helm'])

watch_file("devops/mongo_values.yaml")

helm_resource(
    'mongo',
    'bitnami/mongodb',
    flags=["-f", "devops/mongo_values.yaml"],
    port_forwards=[27017],
    labels=['data']
)

helm_resource(
    'postgresql',
    'bitnami/postgresql',
    flags=["--set", "auth.username=virtool", "--set", "auth.password=virtool", "--set", "auth.database=virtool"],
    labels=['data']
)

helm_resource(
    'redis',
    'bitnami/redis',
    flags=['--set', 'architecture=standalone', '--set', 'auth.password=virtool'],
    labels=['data']
)

helm_resource('keda', 'kedacore/keda', labels=['keda'])

k8s_yaml('devops/ingress.yaml')
k8s_yaml('devops/nfs.yaml')
k8s_resource('nfs-server', labels=['data'], new_name='nfs')

k8s_yaml('devops/openfga.yaml')
k8s_resource('openfga', labels=['data'])

# Actual Virtool stuff.
if 'ui' in to_edit:
    docker_build(
      'ghcr.io/virtool/ui',
      '../virtool-ui/',
      entrypoint='npx webpack-dev-server',
      target='dev',
      live_update=[
        fall_back_on(['../virtool-ui/package.json', '../virtool-ui/package-lock.json']),
        sync('../virtool-ui/src', '/build/src')
      ]
    )

k8s_yaml('devops/ui.yaml')
k8s_resource('virtool-ui', port_forwards=[3000, 9900], labels=['virtool'])

if 'backend' in to_edit:
    docker_build('ghcr.io/virtool/virtool', '../virtool/')

k8s_yaml('devops/api.yaml')
k8s_resource('virtool-api-web', port_forwards=[9950], labels=['virtool'])

k8s_yaml('devops/jobs_api.yaml')
k8s_resource('virtool-api-jobs', port_forwards=[9960], labels=['virtool'])

k8s_yaml('devops/jobs/shared.yaml')
k8s_yaml('devops/jobs/build-index.yaml')
k8s_yaml('devops/jobs/create-sample.yaml')
k8s_yaml('devops/jobs/create-subtraction.yaml')
k8s_yaml('devops/jobs/nuvs.yaml')
k8s_yaml('devops/jobs/pathoscope.yaml')
