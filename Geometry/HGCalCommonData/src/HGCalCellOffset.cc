#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "Geometry/HGCalCommonData/interface/HGCalCellOffset.h"
#include <vector>
#include <iostream>

//#define EDM_ML_DEBUG

HGCalCellOffset::HGCalCellOffset(
    double waferSize, int32_t nFine, int32_t nCoarse, double guardRingOffset_, double mouseBiteCut_) {
  ncell_[0] = nFine;
  ncell_[1] = nCoarse;
  hgcalcell = std::make_unique<HGCalCell>(waferSize, nFine, nCoarse);
  for (int k = 0; k < 2; ++k) {
    cellX_[k] = waferSize / (3 * ncell_[k]);
    cellY_[k] = sqrt3By2_ * cellX_[k];
    fullArea[k] = 3 * sqrt3By2_ * cellY_[k];
    std::vector<std::vector<double>> tempOffsetX;
    std::vector<std::vector<double>> tempOffsetY;
    for (int j = 0; j < 3; ++j) {
      if (j == 0) {
        double totalArea = (11.0 * sqrt3_ / 8.0) * std::pow(cellY_[k], 2);
        double cutArea1 = (cellY_[k] * sqrt3_ * guardRingOffset_) - (std::pow(guardRingOffset_, 2) / (2 * sqrt3_));
        double cutArea2 = (cellY_[k] * sqrt3By2_ * guardRingOffset_) - (std::pow(guardRingOffset_, 2) / (2 * sqrt3_));
        double cutArea3 = sqrt3_ * std::pow((mouseBiteCut_ - (guardRingOffset_ / sqrt3By2_)), 2);
        double x1_0 =
            ((1.5 * cellY_[k]) - (cellY_[k] * 0.5 * guardRingOffset_) + (std::pow(guardRingOffset_, 2) / 18)) /
            ((cellY_[k] * sqrt3_) - (guardRingOffset_ / (2 * sqrt3_)));
        double y1_0 = ((cellY_[k] * -sqrt3By2_ * guardRingOffset_) + (std::pow(guardRingOffset_, 2) / (3 * sqrt3_))) /
                      ((cellY_[k] * sqrt3_) - (guardRingOffset_ / (2 * sqrt3_)));
        double x2_0 =
            ((0.375 * cellY_[k]) - (cellY_[k] * 0.25 * guardRingOffset_) + (std::pow(guardRingOffset_, 2) / 18)) /
            ((cellY_[k] * sqrt3By2_) - (guardRingOffset_ / (2 * sqrt3_)));
        double y2_0 =
            ((cellY_[k] * -0.25 * sqrt3_ * guardRingOffset_) + (std::pow(guardRingOffset_, 2) / (3 * sqrt3_))) /
            ((cellY_[k] * sqrt3By2_) - (guardRingOffset_ / (2 * sqrt3_)));
        double x1 = (sqrt3By2_ * x1_0) - (0.5 * y1_0) - cellY_[k];
        double y1 = (sqrt3By2_ * y1_0) + (0.5 * x1_0);
        double x2 = (-sqrt3By2_ * x2_0) - (0.5 * y2_0) + (cellY_[k] * 1.25);
        double y2 = (sqrt3By2_ * y2_0) + (0.5 * x2_0) + (cellY_[k] * 0.25 * sqrt3_);
        double x3 = 0.5 * cellY_[k];
        double y3 = (cellY_[k] * sqrt3By2_) - (2 * mouseBiteCut_ / 3) - (guardRingOffset_ / (3 * sqrt3By2_));
        cellArea[k][j] = totalArea - cutArea1 - cutArea2 - cutArea3;
        double xMag = ((35.0 * cellY_[k] / 132.0) * totalArea - (cutArea1 * x1) - (cutArea2 * x2) - (cutArea3 * x3)) /
                      (cellArea[k][j]);
        double yMag =
            ((5.0 * cellY_[k] / (44.0 * sqrt3_)) * totalArea - (cutArea1 * y1) - (cutArea2 * y2) - (cutArea3 * y3)) /
            (cellArea[k][j]);
        tempOffsetX.emplace_back(std::vector<double>({xMag,
                                                      -1.0 * (0.5 * xMag - sqrt3By2_ * yMag),
                                                      (-0.5 * xMag + sqrt3By2_ * yMag),
                                                      xMag,
                                                      (-0.5 * xMag - sqrt3By2_ * yMag),
                                                      -1.0 * (0.5 * xMag + sqrt3By2_ * yMag)}));
        tempOffsetY.emplace_back(std::vector<double>({yMag,
                                                      (0.5 * yMag + sqrt3By2_ * xMag),
                                                      (-0.5 * yMag - sqrt3By2_ * xMag),
                                                      -yMag,
                                                      (-0.5 * yMag + sqrt3By2_ * xMag),
                                                      (0.5 * yMag - sqrt3By2_ * xMag)}));
      } else if (j == 1) {
        double totalArea = (5.0 * sqrt3_ / 4.0) * std::pow(cellY_[k], 2);
        double cutArea = cellY_[k] * sqrt3_ * guardRingOffset_;
        cellArea[k][j] = totalArea - cutArea;
        double offMag = (((-2.0 / 15.0) * totalArea * cellY_[k]) - ((cellY_[k] - (0.5 * guardRingOffset_)) * cutArea)) /
                        (cellArea[k][j]);
        tempOffsetX.emplace_back(
            std::vector<double>({-0.5 * offMag, -offMag, -0.5 * offMag, 0.5 * offMag, offMag, 0.5 * offMag}));
        tempOffsetY.emplace_back(std::vector<double>(
            {-sqrt3By2_ * offMag, 0.0, sqrt3By2_ * offMag, sqrt3By2_ * offMag, 0.0, -sqrt3By2_ * offMag}));
      } else if (j == 2) {
        double totalArea = (7.0 * sqrt3_ / 4.0) * std::pow(cellY_[k], 2);
        double cutArea = cellY_[k] * sqrt3_ * guardRingOffset_;
        cellArea[k][j] = totalArea - cutArea;
        double offMag =
            (((5.0 / 42.0) * totalArea * cellY_[k]) - ((cellY_[k] - (0.5 * guardRingOffset_))) * (cutArea)) /
            (cellArea[k][j]);
        tempOffsetX.emplace_back(
            std::vector<double>({-0.5 * offMag, -offMag, -0.5 * offMag, 0.5 * offMag, offMag, 0.5 * offMag}));
        tempOffsetY.emplace_back(std::vector<double>(
            {-sqrt3By2_ * offMag, 0.0, sqrt3By2_ * offMag, sqrt3By2_ * offMag, 0.0, -sqrt3By2_ * offMag}));
      }
    }
    offsetX.emplace_back(tempOffsetX);
    offsetY.emplace_back(tempOffsetY);
  }
#ifdef EDM_ML_DEBUG
  edm::LogVerbatim("HGCalGeom") << "HGCalCellOffset initialized with waferSize " << waferSize << " number of cells "
                                << nFine << ":" << nCoarse << " Guardring offset " << guardRingOffset_ << " Mousebite "
                                << mouseBiteCut_;
#endif
}

std::pair<double, double> HGCalCellOffset::cellOffsetUV2XY1(int32_t u, int32_t v, int32_t placementIndex, int32_t type) {
  if (type != 0)
    type = 1;
  double x_off(0), y_off(0);
  std::pair<int, int> cell = hgcalcell->cellType(u, v, ncell_[type], placementIndex);
  int cellPos = cell.first;
  int cellType = cell.second;
  if (cellType == HGCalCell::truncatedCell || cellType == HGCalCell::extendedCell) {
    x_off = offsetX[type][cellType - 1][cellPos - 1];
    y_off = offsetY[type][cellType - 1][cellPos - 1];
  } else if (cellType == HGCalCell::cornerCell) {
    if (((placementIndex >= HGCalCell::cellPlacementExtra) && (placementIndex % 2 == 0)) ||
        ((placementIndex < HGCalCell::cellPlacementExtra) && (placementIndex % 2 == 1))) {
      cellPos = 11 + (17 - cellPos) % 6;
    }
    x_off = offsetX[type][cellType - 1][cellPos - 11];
    y_off = offsetY[type][cellType - 1][cellPos - 11];
    if (((placementIndex >= HGCalCell::cellPlacementExtra) && (placementIndex % 2 == 0)) ||
        ((placementIndex < HGCalCell::cellPlacementExtra) && (placementIndex % 2 == 1))) {
      x_off = -1 * x_off;
    }
  }
#ifdef EDM_ML_DEBUG
  edm::LogVerbatim("HGCalGeom") << "HGCalCellOffset in wafer with placement index " << placementIndex << " type "
                                << type << " for cell u " << u << " v " << v << " Offset x:y " << x_off << ":" << y_off;
#endif
  return std::make_pair(x_off, y_off);
}

double HGCalCellOffset::cellAreaUV(int32_t u, int32_t v, int32_t placementIndex, int32_t type) {
  if (type != 0)
    type = 1;
  double area(0);
  std::pair<int, int> cell = hgcalcell->cellType(u, v, ncell_[type], placementIndex);
  int cellType = cell.second;
  if (cellType == HGCalCell::fullCell) {
    area = fullArea[type];
  } else {
    area = cellArea[type][cellType - 1];
  }
#ifdef EDM_ML_DEBUG
  edm::LogVerbatim("HGCalGeom") << "HGCalCellOffset in wafer with placement index " << placementIndex << " type "
                                << type << " for cell u " << u << " v " << v << " Area " << area;
#endif
  return area;
}
