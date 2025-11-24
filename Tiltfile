load('ext://restart_process', 'docker_build_with_restart')

# Configuration
config.define_string_list("to-edit")
config.define_bool("persistence")

cfg = config.parse()
to_edit = cfg.get('to-edit', [])
persistence = cfg.get('persistence', True)

load('ext://helm_resource', 'helm_resource', 'helm_repo')
load('ext://uibutton', 'cmd_button', 'location')

cmd_button('pull',
    argv=['bash', 'scripts/pull.sh'],
    icon_name="cloud_download",
    location=location.NAV,
    text='Pull',
)

helm_repo('bitnami', 'https://charts.bitnami.com/bitnami', labels=['helm'])
helm_repo('kedacore', 'https://kedacore.github.io/charts', labels=['helm'])



helm_resource(
    'keda',
    'kedacore/keda',
    labels=['keda'],
    resource_deps=['kedacore']
)

k8s_yaml('manifests/db/mongo.yaml')
k8s_resource(
    "mongo",
    labels=['data'],
)


k8s_yaml('manifests/db/postgres.yaml')
k8s_resource(
    "postgres",
    labels=['data'],
    objects=['pv-postgres', 'pvc-postgres']
)

k8s_yaml('manifests/openfga.yaml')
k8s_resource(
    'openfga',
    labels=['data'],
    port_forwards=[8080, 3000],
    resource_deps=["postgres"]
)

k8s_yaml('manifests/db/redis.yaml')
k8s_resource(
    'redis',
    labels=['data'],
    objects=['pv-redis', 'pvc-redis']
)



k8s_yaml('manifests/storage.yaml')
k8s_resource(
    labels=['data'],
    new_name='storage',
    objects=['pv-virtool', 'pvc-virtool']
)

if 'migration' in to_edit:
    docker_build('ghcr.io/virtool/migration', '../virtool-migration/')

k8s_yaml('manifests/ingress.yaml')
k8s_yaml('manifests/migration.yaml')

docker_prune_settings(max_age_mins=1)

# Actual Virtool stuff.
if 'ui' in to_edit:
    docker_build(
      'ghcr.io/virtool/ui',
      '../virtool-ui/',
      entrypoint='npx vite serve --host 0.0.0.0 --port 9900',
      target='dev',
      live_update=[
        fall_back_on(['../virtool-ui/package.json', '../virtool-ui/package-lock.json']),
        sync('../virtool-ui/src', '/build/src')
      ]
    )

if 'backend' in to_edit:
    custom_build(
      'ghcr.io/virtool/virtool',
      'docker build -t $EXPECTED_REF ../virtool',
      ['../virtool'],
    )

k8s_yaml(kustomize('manifests/ui'))
k8s_yaml(kustomize('manifests/virtool'))

k8s_resource(
    'virtool-api-jobs',
    labels=['virtool'],
    port_forwards=["9960:9950"],
    new_name="api-jobs",
    resource_deps=["migration"],
    trigger_mode=TRIGGER_MODE_MANUAL
)

k8s_resource(
    'virtool-api-web',
    labels=['virtool'],
    new_name="api-web",
    port_forwards=[9950],
    resource_deps=["migration"],
    trigger_mode=TRIGGER_MODE_MANUAL
)

k8s_resource(
    labels=['virtool'],
    new_name='ingress',
    objects=['ingress'],
    resource_deps=["api-web", "ui"]
)

k8s_resource(
    'virtool-migration',
    labels=['virtool'],
    new_name="migration",
    resource_deps=["mongo", "openfga", "postgresql", "redis", "storage"],
    trigger_mode=TRIGGER_MODE_MANUAL
)

k8s_resource(
    'virtool-task-runner',
    labels=['virtool'],
    new_name="task-runner",
    port_forwards=["9970:9950"],
    resource_deps=["migration"],
    trigger_mode=TRIGGER_MODE_MANUAL
)

k8s_resource(
    'virtool-ui',
    labels=['virtool'],
    new_name="ui",
    port_forwards=[9900],
    resource_deps=["api-web"]
)

"""Workflows"""
if "build-index" in to_edit:
    docker_build(
        'ghcr.io/virtool/build-index',
        '../workflow-build-index/',
        target='base'
    )

if "create-sample" in to_edit:
    docker_build(
        'ghcr.io/virtool/create-sample',
        '../workflow-create-sample/',
        target='base'
    )

if "create-subtraction" in to_edit:
    docker_build(
        'ghcr.io/virtool/create-subtraction',
        '../workflow-create-subtraction/',
        target='base'
    )

if "iimi" in to_edit:
    docker_build(
        'ghcr.io/virtool/iimi',
        '../workflow-iimi/',
        target='base'
    )

if "nuvs" in to_edit:
    docker_build(
        'ghcr.io/virtool/nuvs',
        '../workflow-nuvs/',
        target='base'
    )

if "pathoscope" in to_edit:
    docker_build(
        'ghcr.io/virtool/pathoscope',
        '../workflow-pathoscope/',
        target='base'
    )

k8s_kind(
    'ScaledJob',
    image_json_path='{.spec.jobTargetRef.template.spec.containers[0].image}'
)

k8s_yaml(kustomize('manifests/workflows'))

scaled_job_deps = ['keda', 'redis']

k8s_resource(
    "virtool-workflow-build-index",
    labels=["workflows"],
    new_name="build-index",
    resource_deps=scaled_job_deps
)

k8s_resource(
    'virtool-workflow-create-sample',
    labels=["workflows"],
    new_name="create-sample",
    resource_deps=scaled_job_deps
)


k8s_resource(
    'virtool-workflow-create-subtraction',
    labels=["workflows"],
    new_name="create-subraction",
    resource_deps=scaled_job_deps
)


k8s_resource(
    'virtool-workflow-iimi',
    labels=["workflows"],
    new_name="iimi",
    resource_deps=scaled_job_deps
)


k8s_resource(
    'virtool-workflow-nuvs',
    labels=["workflows"],
    new_name="nuvs",
    resource_deps=scaled_job_deps
)

k8s_resource(
    'virtool-workflow-pathoscope',
    labels=["workflows"],
    new_name="pathoscope",
    resource_deps=scaled_job_deps,
    trigger_mode=TRIGGER_MODE_MANUAL
)
