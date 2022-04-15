#ifndef RecoEcal_EgammaCoreTools_EcalClustersGraph_h
#define RecoEcal_EgammaCoreTools_EcalClustersGraph_h

/**
   \file
   Tools for manipulating ECAL Clusters as graphs
   \author Davide Valsecchi, Badder Marzocchi
   \date 05 October 2020
*/

#include <vector>
#include <cmath>

#include "PhysicsTools/TensorFlow/interface/TensorFlow.h"
#include "FWCore/Utilities/interface/isFinite.h"

#include "DataFormats/CaloRecHit/interface/CaloCluster.h"
#include "DataFormats/CaloRecHit/interface/CaloClusterFwd.h"
#include "DataFormats/EgammaReco/interface/SuperCluster.h"
#include "DataFormats/ParticleFlowReco/interface/PFCluster.h"
#include "DataFormats/ParticleFlowReco/interface/PFLayer.h"
#include "DataFormats/Math/interface/deltaPhi.h"

#include "RecoEcal/EgammaCoreTools/interface/EcalClusterTools.h"
#include "DataFormats/EcalDetId/interface/EBDetId.h"
#include "DataFormats/EcalDetId/interface/EEDetId.h"

#include "Geometry/CaloTopology/interface/CaloTopology.h"
#include "Geometry/CaloGeometry/interface/CaloGeometry.h"
#include "Geometry/CaloGeometry/interface/CaloSubdetectorGeometry.h"
#include "Geometry/Records/interface/CaloTopologyRecord.h"
#include "Geometry/CaloTopology/interface/CaloSubdetectorTopology.h"
#include "DataFormats/GeometryVector/interface/GlobalPoint.h"
#include "Geometry/EcalAlgo/interface/EcalBarrelGeometry.h"
#include "Geometry/EcalAlgo/interface/EcalEndcapGeometry.h"

#include "RecoEcal/EgammaCoreTools/interface/CalibratedPFCluster.h"
#include "RecoEcal/EgammaCoreTools/interface/GraphMap.h"
#include "RecoEcal/EgammaCoreTools/interface/SCProducerCache.h"

/*
 * class:  EcalClustersGraph 
 * Authors:  D.Valsecchi, B.Marzocchi
 * Date:  January 2022
 * 
 * Utility class to handle all the PFClusters in ECAL as a graph.
 * The DeepSC algorithm is applied on sub-graphs of clusters to form SuperCluster.
 */

namespace reco {

  class EcalClustersGraph {
  public:
    typedef std::shared_ptr<CalibratedPFCluster> CalibratedClusterPtr;
    typedef std::vector<CalibratedClusterPtr> CalibratedClusterPtrVector;
    typedef std::vector<std::pair<CalibratedClusterPtr, CalibratedClusterPtrVector>> EcalGraphOutput;

    EcalClustersGraph(CalibratedClusterPtrVector clusters,
                      int nSeeds,
                      const CaloTopology* topology,
                      const CaloSubdetectorGeometry* ebGeom,
                      const CaloSubdetectorGeometry* eeGeom,
                      const EcalRecHitCollection* recHitsEB,
                      const EcalRecHitCollection* recHitsEE,
                      const reco::SCProducerCache* cache);

    std::vector<int> clusterPosition(const CaloCluster* cluster);

    // Sign flip deltaEta as in the Mustache
    double deltaEta(double seed_eta, double cluster_eta) { return (1 - 2 * (seed_eta < 0)) * (cluster_eta - seed_eta); }

    // The dEta-dPhi detector window dimension is chosen to that the algorithm is always larger than
    // the Mustache dimension
    std::vector<double> dynamicWindow(double seedEta);

    std::vector<double> computeVariables(const CaloCluster* seed, const CaloCluster* cluster);
    std::vector<std::vector<double>> fillHits(const CaloCluster* cluster);
    std::vector<double> computeWindowVariables(const std::vector<std::vector<double>>& clusters);

    std::pair<double, double> computeCovariances(const CaloCluster* cluster);
    std::vector<double> computeShowerShapes(const CaloCluster* cluster, bool full5x5);

    void fillVariables();

    double scoreThreshold(const CaloCluster* cluster);
    void initWindows();

    void setThresholds();
    void evaluateScores();
    void selectClusters();

    EcalGraphOutput getGraphOutput();

  private:
    CalibratedClusterPtrVector clusters_;
    uint nSeeds_;
    uint nCls_;

    std::array<float, 3> locCov_;
    std::pair<double, double> widths_;

    //To compute the input variables
    const CaloTopology* topology_;
    const CaloSubdetectorGeometry* ebGeom_;
    const CaloSubdetectorGeometry* eeGeom_;
    const EcalRecHitCollection* recHitsEB_;
    const EcalRecHitCollection* recHitsEE_;
    const reco::SCProducerCache* SCProducerCache_;

    // GraphMap for handling all the windows and scores
    reco::GraphMap graphMap_;
    reco::GraphMap::CollectionStrategy strategy_;
    float threshold_;
    reco::DeepSCInputs inputs_;
  };

}  // namespace reco
#endif
