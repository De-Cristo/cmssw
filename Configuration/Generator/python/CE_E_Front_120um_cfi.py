import FWCore.ParameterSet.Config as cms

generator = cms.EDProducer("CloseByParticleGunProducer",
    PGunParameters = cms.PSet(PartID = cms.vint32(22),
        ControlledByEta = cms.bool(False),
        EnMin = cms.double(25.),
        EnMax = cms.double(200.),
        MaxEnSpread = cms.bool(False),
        RMin = cms.double(54.99),
        RMax = cms.double(55.01),
        ZMin = cms.double(320.99),
        ZMax = cms.double(321.01),
        Delta = cms.double(10),
        Pointing = cms.bool(True),
        Overlapping = cms.bool(False),
        RandomShoot = cms.bool(False),
        NParticles = cms.int32(1),
        EtaMax = cms.double(2.7),
        EtaMin = cms.double(1.7),
        PhiMax = cms.double(3.14159265359),
        PhiMin = cms.double(-3.14159265359),

    ),
    Verbosity = cms.untracked.int32(0),

    psethack = cms.string('random particles in phi and r windows'),
    AddAntiParticle = cms.bool(False),
    firstRun = cms.untracked.uint32(1)
)
