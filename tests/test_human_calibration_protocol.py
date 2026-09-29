from sorelia.analysis.calibration import build_matching_annotation_packet, cohen_kappa, calibrate_matcher


def test_annotation_packet_and_agreement_scoring():
    report = {'mechanisms': [
        {'stable_id':'m0','before_cluster':0,'after_cluster':1,'similarity':.9,'match_margin':.1,'family':'browser','failure_type':'grounding'},
        {'stable_id':'m1','before_cluster':2,'after_cluster':3,'similarity':.8,'match_margin':.01,'family':'browser','failure_type':'planning'},
    ]}
    packet = build_matching_annotation_packet(report)
    assert len(packet) == 2
    a=[dict(packet[0],label='same'),dict(packet[1],label='different')]
    b=[dict(packet[0],label='same'),dict(packet[1],label='different')]
    k=cohen_kappa(a,b)
    assert k['kappa'] == 1.0
    c=calibrate_matcher(a)
    assert c['n'] == 2
