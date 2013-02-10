#!/usr/bin/env python

import os
import shlex
import string
import subprocess

samples = {
    'simDYtoMuMu' : {
        'datasetpath' : '/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball/veelken-skimGenZmumuMuPtGt15EtaLt9p9plusMuPtGt5EtaLt9p9-69987cf12dddbc8db709f491408cceae/USER', # (6864801 events)
        'dbs_url'     : 'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_01/servlet/DBSServlet',
        'type'        : 'MC'
    }
}

version = "v1_10_0"

options = {
    # all tau decay modes (for validation that polarization effects for embedded tau lepton pair is simulated correctly by TAUOLA)
    'noEvtSel_embedEqRH_cleanEqDEDX_replaceGenMuons_by_allDecayModes_embedAngleEq0_noVisPtCuts' : {
        'ZmumuCollection'              : 'genMuonsFromZs',
        'mdtau'                        : 0,
        'minVisibleTransverseMomentum' : "",
        'rfRotationAngle'              : 0.,        
        'embeddingMode'                : 'RH',
        'replaceGenOrRecMuonMomenta'   : 'gen',
        'applyMuonRadiationCorrection' : "",
        'cleaningMode'                 : 'DEDX',
        'muonCaloSF'                   : 1.0,
        'applyZmumuSkim'               : False,
        'applyMuonRadiationFilter'     : False,
        'disableCaloNoise'             : True,
        'applyRochesterMuonCorr'       : False
    },
    # e+tau samples
##     'noEvtSel_embedEqPF_replaceGenMuons_by_etau_embedAngleEq90' : {
##         'ZmumuCollection'              : 'genMuonsFromZs',
##         'mdtau'                        : 115,
##         'minVisibleTransverseMomentum' : "elec1_9had1_15",
##         'rfRotationAngle'              : 90.,
##         'embeddingMode'                : 'PF',
##         'replaceGenOrRecMuonMomenta'   : 'gen',
##         'cleaningMode'                 : 'PF',
##         'applyZmumuSkim'               : False,
##         'applyMuonRadiationFilter'     : False
##     },
##     'noEvtSel_embedEqRH_cleanEqPF_replaceGenMuons_by_etau_embedAngleEq90' : {
##         'ZmumuCollection'              : 'genMuonsFromZs',    
##         'mdtau'                        : 115,
##         'minVisibleTransverseMomentum' : "elec1_9had1_15",
##         'rfRotationAngle'              : 90.,
##         'embeddingMode'                : 'RH',
##         'replaceGenOrRecMuonMomenta'   : 'gen',
##         'cleaningMode'                 : 'PF',
##         'applyZmumuSkim'               : False,
##         'applyMuonRadiationFilter'     : False
##     },
##     'noEvtSel_embedEqRH_cleanEqDEDX_replaceGenMuons_by_etau_embedAngleEq90' : {
##         'ZmumuCollection'              : 'genMuonsFromZs',        
##         'mdtau'                        : 115,
##         'minVisibleTransverseMomentum' : "elec1_9had1_15",
##         'rfRotationAngle'              : 90.,    
##         'embeddingMode'                : 'RH',
##         'replaceGenOrRecMuonMomenta'   : 'gen',
##         'cleaningMode'                 : 'DEDX',
##         'applyZmumuSkim'               : False,
##         'applyMuonRadiationFilter'     : False
##     },
##     'noEvtSel_embedEqRH_cleanEqDEDX_replaceGenMuons_by_etau_embedAngleEq90_noVisPtCuts' : {
##         'ZmumuCollection'              : 'genMuonsFromZs',        
##         'mdtau'                        : 115,
##         'minVisibleTransverseMomentum' : "elec1_0had1_0",
##         'rfRotationAngle'              : 90.,    
##         'embeddingMode'                : 'RH',
##         'replaceGenOrRecMuonMomenta'   : 'gen',
##         'cleaningMode'                 : 'DEDX',
##         'applyZmumuSkim'               : False,
##         'applyMuonRadiationFilter'     : False
##     },    
##     'noEvtSel_embedEqRH_cleanEqDEDX_replaceRecMuons_by_etau_embedAngleEq0' : {
##         'ZmumuCollection'              : 'goldenZmumuCandidatesGe2IsoMuons',
##         'mdtau'                        : 115,
##         'minVisibleTransverseMomentum' : "elec1_9had1_15",
##         'rfRotationAngle'              : 0.,    
##         'embeddingMode'                : 'RH',
##         'replaceGenOrRecMuonMomenta'   : 'rec',
##         'cleaningMode'                 : 'DEDX',
##         'applyZmumuSkim'               : True,
##         'applyMuonRadiationFilter'     : False    
##     },
##     'noEvtSel_embedEqRH_cleanEqDEDX_replaceRecMuons_by_etau_embedAngleEq90' : {
##         'ZmumuCollection'              : 'goldenZmumuCandidatesGe2IsoMuons',
##         'mdtau'                        : 115,
##         'minVisibleTransverseMomentum' : "elec1_9had1_15",
##         'rfRotationAngle'              : 90.,    
##         'embeddingMode'                : 'RH',
##         'replaceGenOrRecMuonMomenta'   : 'rec',
##         'cleaningMode'                 : 'DEDX',
##         'applyZmumuSkim'               : True,
##         'applyMuonRadiationFilter'     : False
##     },    
    # mu+tau samples    
##     'noEvtSel_embedEqRH_cleanEqDEDX_replaceGenMuons_by_mutau_embedAngleEq90_muonCaloSF0_5' : {
##         'ZmumuCollection'              : 'genMuonsFromZs',
##         'mdtau'                        : 116,
##         'minVisibleTransverseMomentum' : "mu1_7had1_15",
##         'rfRotationAngle'              : 90.,        
##         'embeddingMode'                : 'RH',
##         'replaceGenOrRecMuonMomenta'   : 'gen',
##         'applyMuonRadiationCorrection' : "photos",
##         'cleaningMode'                 : 'DEDX',
##         'muonCaloCleaningSF'           : 0.5,
##         'muonTrackCleaningMode'        : 2,
##         'applyZmumuSkim'               : False,
##         'applyMuonRadiationFilter'     : False,
##         'disableCaloNoise'             : True,
##         'applyRochesterMuonCorr'       : False
##     },
##     'noEvtSel_embedEqRH_cleanEqDEDX_replaceGenMuons_by_mutau_embedAngleEq90_muonCaloSF1_0' : {
##         'ZmumuCollection'              : 'genMuonsFromZs',
##         'mdtau'                        : 116,
##         'minVisibleTransverseMomentum' : "mu1_7had1_15",
##         'rfRotationAngle'              : 90.,        
##         'embeddingMode'                : 'RH',
##         'replaceGenOrRecMuonMomenta'   : 'gen',
##         'applyMuonRadiationCorrection' : "photos",
##         'cleaningMode'                 : 'DEDX',
##         'muonCaloCleaningSF'           : 1.0,
##         'muonTrackCleaningMode'        : 2,
##         'applyZmumuSkim'               : False,
##         'applyMuonRadiationFilter'     : False,
##         'disableCaloNoise'             : True,
##         'applyRochesterMuonCorr'       : False
##     },
#    'noEvtSel_embedEqRH_cleanEqDEDX_replaceGenMuons_by_mutau_embedAngleEq0_noVisPtCuts' : {
#        'ZmumuCollection'              : 'genMuonsFromZs',
#        'mdtau'                        : 116,
#        'minVisibleTransverseMomentum' : "",
#        'rfRotationAngle'              : 0.,        
#        'embeddingMode'                : 'RH',
#        'replaceGenOrRecMuonMomenta'   : 'gen',
#        'applyMuonRadiationCorrection' : "",
#        'cleaningMode'                 : 'DEDX',
#        'muonCaloCleaningSF'           : 1.0,
#        'muonTrackCleaningMode'        : 2,
#        'applyZmumuSkim'               : False,
#        'applyMuonRadiationFilter'     : False,
#        'disableCaloNoise'             : True,
#        'applyRochesterMuonCorr'       : False
#    },
##     'noEvtSel_embedEqRH_cleanEqDEDX_replaceGenMuons_by_mutau_embedAngleEq90_muonCaloSF2_0' : {
##         'ZmumuCollection'              : 'genMuonsFromZs',
##         'mdtau'                        : 116,
##         'minVisibleTransverseMomentum' : "mu1_7had1_15",
##         'rfRotationAngle'              : 90.,        
##         'embeddingMode'                : 'RH',
##         'replaceGenOrRecMuonMomenta'   : 'gen',
##         'applyMuonRadiationCorrection' : "photos",
##         'cleaningMode'                 : 'DEDX',
##         'muonCaloCleaningSF'           : 2.0,
##         'muonTrackCleaningMode'        : 2,
##         'applyZmumuSkim'               : False,
##         'applyMuonRadiationFilter'     : False,
##         'disableCaloNoise'             : True,
##         'applyRochesterMuonCorr'       : False
##     },
##     'noEvtSel_embedEqRH_cleanEqDEDX_replaceRecMuons_by_mutau_embedAngleEq90_muonCaloSF0_5' : {
##         'ZmumuCollection'              : 'goldenZmumuCandidatesGe2IsoMuons',
##         'mdtau'                        : 116,
##         'minVisibleTransverseMomentum' : "mu1_7had1_15",
##         'rfRotationAngle'              : 90.,        
##         'embeddingMode'                : 'RH',
##         'replaceGenOrRecMuonMomenta'   : 'rec',
##         'applyMuonRadiationCorrection' : "photos",
##         'cleaningMode'                 : 'DEDX',
##         'muonCaloSF'                   : 0.5,
##         'applyZmumuSkim'               : True,
##         'applyMuonRadiationFilter'     : False,
##         'disableCaloNoise'             : True,
##         'applyRochesterMuonCorr'       : True
##     },
##     'noEvtSel_embedEqRH_cleanEqDEDX_replaceRecMuons_by_mutau_embedAngleEq90_muonCaloSF1_0' : {
##         'ZmumuCollection'              : 'goldenZmumuCandidatesGe2IsoMuons',
##         'mdtau'                        : 116,
##         'minVisibleTransverseMomentum' : "mu1_7had1_15",
##         'rfRotationAngle'              : 90.,        
##         'embeddingMode'                : 'RH',
##         'replaceGenOrRecMuonMomenta'   : 'rec',
##         'applyMuonRadiationCorrection' : "photos",
##         'cleaningMode'                 : 'DEDX',
##         'muonCaloSF'                   : 1.0,
##         'applyZmumuSkim'               : True,
##         'applyMuonRadiationFilter'     : False,
##         'disableCaloNoise'             : True,
##         'applyRochesterMuonCorr'       : True
##     },
##     'noEvtSel_embedEqRH_cleanEqDEDX_replaceRecMuons_by_mutau_embedAngleEq90_muonCaloSF2_0' : {
##         'ZmumuCollection'              : 'goldenZmumuCandidatesGe2IsoMuons',
##         'mdtau'                        : 116,
##         'minVisibleTransverseMomentum' : "mu1_7had1_15",
##         'rfRotationAngle'              : 90.,        
##         'embeddingMode'                : 'RH',
##         'replaceGenOrRecMuonMomenta'   : 'rec',
##         'applyMuonRadiationCorrection' : "photos",
##         'cleaningMode'                 : 'DEDX',
##         'muonCaloSF'                   : 2.0,
##         'applyZmumuSkim'               : True,
##         'applyMuonRadiationFilter'     : False,
##         'disableCaloNoise'             : True,
##         'applyRochesterMuonCorr'       : True
##     },     

    # mu+mu samples
##     'noEvtSel_embedEqPF_replaceGenMuons_by_mumu_embedAngleEq90' : {
##         'ZmumuCollection'              : 'genMuonsFromZs',
##         'mdtau'                        : 122,
##         'minVisibleTransverseMomentum' : "mu1_18mu2_8",
##         'rfRotationAngle'              : 90.,    
##         'embeddingMode'                : 'PF',
##         'replaceGenOrRecMuonMomenta'   : 'gen',
##         'cleaningMode'                 : 'PF',
##         'applyZmumuSkim'               : False,
##         'applyMuonRadiationFilter'     : False
##     },
##     'noEvtSel_embedEqRH_cleanEqPF_replaceGenMuons_by_mumu_embedAngleEq90' : {
##         'ZmumuCollection'              : 'genMuonsFromZs',    
##         'mdtau'                        : 122,
##         'minVisibleTransverseMomentum' : "mu1_18mu2_8",
##         'rfRotationAngle'              : 90.,    
##         'embeddingMode'                : 'RH',
##         'replaceGenOrRecMuonMomenta'   : 'gen',
##         'cleaningMode'                 : 'PF',
##         'applyZmumuSkim'               : False,
##         'applyMuonRadiationFilter'     : False
##     },
##     'noEvtSel_embedEqRH_cleanEqDEDX_replaceGenMuons_by_mumu_embedAngleEq90' : {
##         'ZmumuCollection'              : 'genMuonsFromZs',
##         'mdtau'                        : 122,
##         'minVisibleTransverseMomentum' : "mu1_18mu2_8",
##         'rfRotationAngle'              : 90.,    
##         'embeddingMode'                : 'RH',
##         'replaceGenOrRecMuonMomenta'   : 'gen',
##         'cleaningMode'                 : 'DEDX',
##         'applyZmumuSkim'               : False,
##         'applyMuonRadiationFilter'     : False
##     },
##     'noEvtSel_embedEqRH_cleanEqDEDX_replaceGenMuons_by_mumu_embedAngleEq90_noVisPtCuts' : {
##         'ZmumuCollection'              : 'genMuonsFromZs',
##         'mdtau'                        : 122,
##         'minVisibleTransverseMomentum' : "mu1_0mu2_0",
##         'rfRotationAngle'              : 90.,    
##         'embeddingMode'                : 'RH',
##         'replaceGenOrRecMuonMomenta'   : 'gen',
##         'cleaningMode'                 : 'DEDX',
##         'applyZmumuSkim'               : False,
##         'applyMuonRadiationFilter'     : False
##     },    
##     'noEvtSel_embedEqRH_cleanEqDEDX_replaceRecMuons_by_mumu_embedAngleEq0' : {
##         'ZmumuCollection'              : 'goldenZmumuCandidatesGe2IsoMuons',        
##         'mdtau'                        : 122,
##         'minVisibleTransverseMomentum' : "mu1_18mu2_8",
##         'rfRotationAngle'              : 0.,    
##         'embeddingMode'                : 'RH',
##         'replaceGenOrRecMuonMomenta'   : 'rec',
##         'cleaningMode'                 : 'DEDX',
##         'applyZmumuSkim'               : True,
##         'applyMuonRadiationFilter'     : False
##     },
##     'noEvtSel_embedEqRH_cleanEqDEDX_replaceRecMuons_by_mumu_embedAngleEq90' : {
##         'ZmumuCollection'              : 'goldenZmumuCandidatesGe2IsoMuons',        
##         'mdtau'                        : 122,
##         'minVisibleTransverseMomentum' : "mu1_18mu2_8",
##         'rfRotationAngle'              : 90.,    
##         'embeddingMode'                : 'RH',
##         'replaceGenOrRecMuonMomenta'   : 'rec',
##         'cleaningMode'                 : 'DEDX',
##         'applyZmumuSkim'               : True,
##         'applyMuonRadiationFilter'     : False
##     },
    # had+had samples
##     'noEvtSel_embedEqPF_replaceGenMuons_by_tautau_embedAngleEq90' : {
##         'ZmumuCollection'              : 'genMuonsFromZs',    
##         'mdtau'                        : 132,
##         'minVisibleTransverseMomentum' : "had1_17had2_17",
##         'rfRotationAngle'              : 90.,    
##         'embeddingMode'                : 'PF',
##         'replaceGenOrRecMuonMomenta'   : 'gen',
##         'cleaningMode'                 : 'PF',
##         'applyZmumuSkim'               : False,
##         'applyMuonRadiationFilter'     : False
##     },
##     'noEvtSel_embedEqRH_cleanEqPF_replaceGenMuons_by_tautau_embedAngleEq90' : {
##         'ZmumuCollection'              : 'genMuonsFromZs',    
##         'mdtau'                        : 132,
##         'minVisibleTransverseMomentum' : "had1_17had2_17",
##         'rfRotationAngle'              : 90.,    
##         'embeddingMode'                : 'RH',
##         'replaceGenOrRecMuonMomenta'   : 'gen',
##         'cleaningMode'                 : 'PF',
##         'applyZmumuSkim'               : False,
##         'applyMuonRadiationFilter'     : False
##     },
##     'noEvtSel_embedEqRH_cleanEqDEDX_replaceGenMuons_by_tautau_embedAngleEq90' : {
##         'ZmumuCollection'              : 'genMuonsFromZs',        
##         'mdtau'                        : 132,
##         'minVisibleTransverseMomentum' : "had1_17had2_17",
##         'rfRotationAngle'              : 90.,    
##         'embeddingMode'                : 'RH',
##         'replaceGenOrRecMuonMomenta'   : 'gen',
##         'cleaningMode'                 : 'DEDX',
##         'applyZmumuSkim'               : False,
##         'applyMuonRadiationFilter'     : False
##     },
##     'noEvtSel_embedEqRH_cleanEqDEDX_replaceGenMuons_by_tautau_embedAngleEq90_noVisPtCuts' : {
##         'ZmumuCollection'              : 'genMuonsFromZs',        
##         'mdtau'                        : 132,
##         'minVisibleTransverseMomentum' : "had1_0had2_0",
##         'rfRotationAngle'              : 90.,    
##         'embeddingMode'                : 'RH',
##         'replaceGenOrRecMuonMomenta'   : 'gen',
##         'cleaningMode'                 : 'DEDX',
##         'applyZmumuSkim'               : False,
##         'applyMuonRadiationFilter'     : False
##     },    
##     'noEvtSel_embedEqRH_cleanEqDEDX_replaceRecMuons_by_tautau_embedAngleEq0' : {
##         'ZmumuCollection'              : 'goldenZmumuCandidatesGe2IsoMuons',        
##         'mdtau'                        : 132,
##         'minVisibleTransverseMomentum' : "had1_17had2_17",
##         'rfRotationAngle'              : 0.,    
##         'embeddingMode'                : 'RH',
##         'replaceGenOrRecMuonMomenta'   : 'rec',
##         'cleaningMode'                 : 'DEDX',
##         'applyZmumuSkim'               : True,
##         'applyMuonRadiationFilter'     : False
##     },
##     'noEvtSel_embedEqRH_cleanEqDEDX_replaceRecMuons_by_tautau_embedAngleEq90' : {
##         'ZmumuCollection'              : 'goldenZmumuCandidatesGe2IsoMuons',        
##         'mdtau'                        : 132,
##         'minVisibleTransverseMomentum' : "had1_17had2_17",
##         'rfRotationAngle'              : 90.,    
##         'embeddingMode'                : 'RH',
##         'replaceGenOrRecMuonMomenta'   : 'rec',
##         'cleaningMode'                 : 'DEDX',
##         'applyZmumuSkim'               : True,
##         'applyMuonRadiationFilter'     : False
##     }
}

crab_template = string.Template('''
[CRAB]
jobtype = cmssw
scheduler = glite
use_server = 1

[CMSSW]
datasetpath = $datasetpath
dbs_url = $dbs_url
pset = $pset
output_file = embed_AOD.root
# CV: use for MC
total_number_of_events = -1
events_per_job = 2500
# CV: use for Data
#lumi_mask = /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions12/8TeV/DCSOnly/json_DCSONLY.txt
#total_number_of_lumis = 2
#number_of_jobs = 1
#runselection = 190450-190790

[USER]
ui_working_dir = $ui_working_dir
return_data = 0
copy_data = 1
email = christian.veelken@cern.ch 
storage_element = T2_FR_GRIF_LLR
user_remote_dir = $user_remote_dir
publish_data = 1
publish_data_name = $publish_data_name
dbs_url_for_publication = https://cmsdbsprod.cern.ch:8443/cms_dbs_ph_analysis_01_writer/servlet/DBSServlet
''')

cfg_template = "embed_cfg.py"

currentDirectory    = os.getcwd()
submissionDirectory = os.path.join(currentDirectory, "crab")

def getStringRep_bool(flag):
    retVal = None
    if flag:
        retVal = "True"
    else:
        retVal = "False"
    return retVal

def runCommand(commandLine):
    print(commandLine)
    subprocess.call(commandLine, shell = True)

crabCommands_create_and_submit = []
crabCommands_publish           = []

for sampleName, sampleOption in samples.items():
    for embeddingName, embeddingOption in options.items():
        # create config file for cmsRun
        cfgFileName = "embed_%s_%s_cfg.py" % (sampleName, embeddingName)
        cfgFileName_full = os.path.join(submissionDirectory, cfgFileName)
        runCommand('rm -f %s' % cfgFileName_full)
        sedCommand  = "sed 's/#__//g"
        isMC = None
        if sampleOption['type'] == "Data":
            isMC = False
        elif sampleOption['type'] == "MC":
            isMC = True
        else:
            raise ValueError ("Sample = %s is of invalid type = %s !!" % (sampleName, sampleOption['type']))
        sedCommand += ";s/$isMC/%s/g" % getStringRep_bool(isMC)
        sedCommand += ";s/$ZmumuCollection/%s/g" % embeddingOption['ZmumuCollection']
        sedCommand += ";s/$mdtau/%i/g" % embeddingOption['mdtau']
        sedCommand += ";s/$minVisibleTransverseMomentum/%s/g" % embeddingOption['minVisibleTransverseMomentum'].replace(";", "\;")
        sedCommand += ";s/$rfRotationAngle/%1.0f/g" % embeddingOption['rfRotationAngle']   
        sedCommand += ";s/$embeddingMode/%s/g" % embeddingOption['embeddingMode']        
        sedCommand += ";s/$replaceGenOrRecMuonMomenta/%s/g" % embeddingOption['replaceGenOrRecMuonMomenta']
        sedCommand += ";s/$applyMuonRadiationCorrection/%s/g" % embeddingOption['applyMuonRadiationCorrection']
        sedCommand += ";s/$cleaningMode/%s/g" % embeddingOption['cleaningMode']
        sedCommand += ";s/$muonCaloCleaningSF/%f/g" % embeddingOption['muonCaloCleaningSF']
        sedCommand += ";s/$muonTrackCleaningMode/%i/g" % embeddingOption['muonTrackCleaningMode']
        sedCommand += ";s/$applyZmumuSkim/%s/g" % getStringRep_bool(embeddingOption['applyZmumuSkim'])    
        sedCommand += ";s/$applyMuonRadiationFilter/%s/g" % embeddingOption['applyMuonRadiationFilter']
        sedCommand += ";s/$disableCaloNoise/%s/g" % getStringRep_bool(embeddingOption['disableCaloNoise'])
        sedCommand += ";s/$applyRochesterMuonCorr/%s/g" % getStringRep_bool(embeddingOption['applyRochesterMuonCorr'])
        sedCommand += "'"
        sedCommand += " %s > %s" % (cfg_template, cfgFileName_full)
        runCommand(sedCommand)
        
        # create crab config file
        crabOptions = {
            'datasetpath'       : sampleOption['datasetpath'],
            'dbs_url'           : sampleOption['dbs_url'],
            'pset'              : cfgFileName_full,
            'ui_working_dir'    : os.path.join(submissionDirectory, "crabdir_%s_%s" % (sampleName, embeddingName)),
            'user_remote_dir'   : "CMSSW_5_3_x_embed_%s_%s_%s" % (sampleName, embeddingName, version),
            'publish_data_name' : "embed_%s_%s_%s" % (sampleName, embeddingName, version)
        }
        crabFileName = "crab_embed_%s_%s.cfg" % (sampleName, embeddingName)
        crabFileName_full = os.path.join(submissionDirectory, crabFileName)
        crabFile = open(crabFileName_full, 'w')
        crabConfig = crab_template.substitute(crabOptions)
        crabFile.write(crabConfig)
        crabFile.close()

        # keep track of commands necessary to create, submit and publish crab jobs
        crabCommands_create_and_submit.append('crab -create -cfg %s' % crabFileName_full)
        crabCommands_create_and_submit.append('crab -submit -c %s' % crabOptions['ui_working_dir'])
        
        crabCommands_publish.append('crab -publish -c %s' % crabOptions['ui_working_dir'])

shellFileName_create_and_submit = "embed_crab_create_and_submit.sh"
shellFile_create_and_submit = open(shellFileName_create_and_submit, "w")
for crabCommand in crabCommands_create_and_submit:
    shellFile_create_and_submit.write("%s\n" % crabCommand)
shellFile_create_and_submit.close()

shellFileName_publish = "embed_crab_publish.sh"
shellFile_publish = open(shellFileName_publish, "w")
for crabCommand in crabCommands_publish:
    shellFile_publish.write("%s\n" % crabCommand)
    shellFile_publish.write("sleep 10\n") # CV: wait for 10s to prevent overloading crab with too many commands in too short a time
shellFile_publish.close()

print("Finished building config files. Now execute 'source %s' to create & submit crab jobs." % shellFileName_create_and_submit)
print("Once all crab jobs have finished processing, execute 'source %s' to publish the samples produced." % shellFileName_publish)
