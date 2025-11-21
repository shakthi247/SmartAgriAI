// Crop types available in the system
export const CropType = {
  WHEAT: "wheat",
  RICE: "rice",
  CORN: "corn",
  SOYBEAN: "soybean",
  COTTON: "cotton",
  SUGARCANE: "sugarcane",
  POTATO: "potato",
  TOMATO: "tomato",
  CHICKPEA: "chickpea",
  LENTIL: "lentil",
  MUSTARD: "mustard",
  GROUNDNUT: "groundnut",
  BARLEY: "barley",
  MAIZE: "maize"
} as const;

export type CropType = typeof CropType[keyof typeof CropType];

// Season types
export const Season = {
  WINTER: "winter",
  SUMMER: "summer",
  MONSOON: "monsoon"
} as const;

export type Season = typeof Season[keyof typeof Season];

// Irrigation status
export const IrrigationStatus = {
  NEEDED: "needed",
  RECOMMENDED: "recommended",
  NOT_NEEDED: "not_needed"
} as const;

export type IrrigationStatus = typeof IrrigationStatus[keyof typeof IrrigationStatus];

// Days of week
export const DayOfWeek = {
  MONDAY: "Monday",
  TUESDAY: "Tuesday",
  WEDNESDAY: "Wednesday",
  THURSDAY: "Thursday",
  FRIDAY: "Friday",
  SATURDAY: "Saturday",
  SUNDAY: "Sunday"
} as const;

export type DayOfWeek = typeof DayOfWeek[keyof typeof DayOfWeek];

// AI Model types
export const AIModel = {
  LLAMA3: "llama3",
  LLAMA2: "llama2",
  MISTRAL: "mistral",
  CODELLAMA: "codellama",
  PHI3: "phi3"
} as const;

export type AIModel = typeof AIModel[keyof typeof AIModel];

// Soil quality levels
export const SoilQualityLevel = {
  EXCELLENT: "excellent",
  GOOD: "good",
  FAIR: "fair",
  POOR: "poor"
} as const;

export type SoilQualityLevel = typeof SoilQualityLevel[keyof typeof SoilQualityLevel];