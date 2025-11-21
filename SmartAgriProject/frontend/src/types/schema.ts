import type { CropType, Season, DayOfWeek, AIModel, IrrigationStatus } from './enums';

// Props types (data passed to components)
export interface DashboardMetrics {
  soilQuality: number;
  soilQualityDelta: number;
  predictedYield: number;
  yieldDelta: number;
  irrigationStatus: string;
  wheatPrice: number;
  wheatPriceDelta: number;
}

export interface MarketUpdate {
  title: string;
  content: string;
}

export interface SoilAnalysis {
  pH: number;
  nitrogen: number;
  phosphorus: number;
  potassium: number;
  organicMatter: number;
  previousCrop: CropType | null;
  season: Season;
}

export interface YieldPrediction {
  crop: CropType;
  area: number;
  rainfall: number;
  temperature: number;
  soilQuality: number;
  nitrogenFert: number;
  phosphorusFert: number;
  potassiumFert: number;
}

export interface MoistureDataPoint {
  date: Date;
  moisture: number;
}

export interface Irrigation {
  soilMoisture: number;
  temperature: number;
  humidity: number;
  rainfallChance: number;
  status: IrrigationStatus;
  duration: number;
  scheduledTime: string;
  scheduledDays: DayOfWeek[];
  moistureHistory: MoistureDataPoint[];
}

export interface PriceDataPoint {
  date: Date;
  price: number;
}

export interface ProfitAnalysis {
  totalRevenue: number;
  totalCost: number;
  totalProfit: number;
  profitPerHectare: number;
}

export interface Seasonality {
  planting: string;
  harvesting: string;
  season: string;
}

export interface MarketAnalysis {
  selectedCrop: CropType;
  plantingDate: Date;
  area: number;
  useTypicalYield: boolean;
  expectedYield: number;
  useTypicalCost: boolean;
  costPerHectare: number;
  predictedPrice: number;
  harvestDate: Date;
  historicalPrices: PriceDataPoint[];
  predictedPrices: PriceDataPoint[];
  profitAnalysis: ProfitAnalysis;
  seasonality: Seasonality;
}

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}

export interface AIAssistant {
  selectedModel: AIModel;
  temperature: number;
  messages: ChatMessage[];
  commonQuestions: string[];
}

export interface PropTypes {
  dashboardMetrics: DashboardMetrics;
  marketUpdates: MarketUpdate[];
  soilAnalysis: SoilAnalysis;
  yieldPrediction: YieldPrediction;
  irrigation: Irrigation;
  marketAnalysis: MarketAnalysis;
  aiAssistant: AIAssistant;
}