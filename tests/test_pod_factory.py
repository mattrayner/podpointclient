from podpointclient.pod import Pod
from podpointclient.factories import PodFactory
from .helpers import Mocks

def test_pod_factory_single_pod_creation():
    mocks = Mocks()
    pods_response = mocks.pods_response()

    factory = PodFactory()
    pods = factory.build_pods(pods_response)
    
    assert 1 == len(pods)
    assert Pod == type(pods[0])