import { CropType, SoilQualityLevel, IrrigationStatus } from '../types/enums';

export const formatCurrency = (amount: number): string => {
  return `₹${amount.toLocaleString('en-IN')}`;
};

export const formatCurrencyPerUnit = (amount: number, unit: string): string => {
  return `₹${amount.toLocaleString('en-IN')}/${unit}`;
};

export const formatYield = (value: number, unit: string = "tons/hectare"): string => {
  return `${value.toFixed(2)} ${unit}`;
};

export const formatPercentage = (value: number): string => {
  return `${value.toFixed(1)}%`;
};

export const formatDate = (date: Date): string => {
  return date.toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' });
};

export const formatSoilQualityScore = (score: number): string => {
  return `${score.toFixed(1)}/10`;
};

export const getSoilQualityLevel = (score: number): SoilQualityLevel => {
  if (score >= 8) return SoilQualityLevel.EXCELLENT;
  if (score >= 6) return SoilQualityLevel.GOOD;
  if (score >= 4) return SoilQualityLevel.FAIR;
  return SoilQualityLevel.POOR;
};

export const getSoilQualityMessage = (level: SoilQualityLevel): string => {
  const messages = {
    [SoilQualityLevel.EXCELLENT]: "Excellent soil quality! Most crops will thrive.",
    [SoilQualityLevel.GOOD]: "Good soil quality. Some amendments may be needed.",
    [SoilQualityLevel.FAIR]: "Fair soil quality. Consider soil amendments.",
    [SoilQualityLevel.POOR]: "Poor soil quality. Significant amendments needed."
  };
  return messages[level];
};

export const getIrrigationStatusMessage = (status: IrrigationStatus): string => {
  const messages = {
    [IrrigationStatus.NEEDED]: "⚠️ Irrigation Needed",
    [IrrigationStatus.RECOMMENDED]: "ℹ️ Irrigation Recommended",
    [IrrigationStatus.NOT_NEEDED]: "✅ Irrigation Not Needed"
  };
  return messages[status];
};

export const formatCropName = (crop: CropType): string => {
  return crop.charAt(0).toUpperCase() + crop.slice(1);
};