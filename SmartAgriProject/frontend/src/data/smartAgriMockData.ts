import { CropType, Season, DayOfWeek, AIModel, IrrigationStatus } from '../types/enums';
import type { PropTypes } from '../types/schema';

// Mock data for dashboard metrics
export const mockRootProps: PropTypes = {
  dashboardMetrics: {
    soilQuality: 7.2,
    soilQualityDelta: 0.3,
    predictedYield: 4.2,
    yieldDelta: -0.1,
    irrigationStatus: "Optimal" as const,
    wheatPrice: 2200,
    wheatPriceDelta: 3.1
  },
  marketUpdates: [
    {
      title: "Wheat prices",
      content: "have increased by 5% due to high export demand. Government announces new minimum support prices for Kharif crops."
    },
    {
      title: "Monsoon forecast",
      content: "looks favorable for most regions. Potato prices expected to rise due to reduced planting area."
    }
  ],
  soilAnalysis: {
    pH: 6.5,
    nitrogen: 50,
    phosphorus: 40,
    potassium: 300,
    organicMatter: 2.5,
    previousCrop: null as CropType | null,
    season: Season.WINTER
  },
  yieldPrediction: {
    crop: CropType.WHEAT,
    area: 1.0,
    rainfall: 500,
    temperature: 25,
    soilQuality: 7.0,
    nitrogenFert: 100,
    phosphorusFert: 50,
    potassiumFert: 50
  },
  irrigation: {
    soilMoisture: 35,
    temperature: 28,
    humidity: 65,
    rainfallChance: 20,
    status: IrrigationStatus.RECOMMENDED,
    duration: 15,
    scheduledTime: "06:00" as const,
    scheduledDays: [DayOfWeek.MONDAY, DayOfWeek.WEDNESDAY, DayOfWeek.FRIDAY],
    moistureHistory: [
      { date: new Date(Date.now() - 6 * 24 * 60 * 60 * 1000), moisture: 35 },
      { date: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000), moisture: 40 },
      { date: new Date(Date.now() - 4 * 24 * 60 * 60 * 1000), moisture: 38 },
      { date: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000), moisture: 32 },
      { date: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000), moisture: 28 },
      { date: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000), moisture: 25 },
      { date: new Date(), moisture: 30 }
    ]
  },
  marketAnalysis: {
    selectedCrop: CropType.WHEAT,
    plantingDate: new Date(),
    area: 1.0,
    useTypicalYield: true,
    expectedYield: 45,
    useTypicalCost: true,
    costPerHectare: 35000,
    predictedPrice: 2350,
    harvestDate: new Date(Date.now() + 120 * 24 * 60 * 60 * 1000),
    historicalPrices: [
      { date: new Date(Date.now() - 150 * 24 * 60 * 60 * 1000), price: 2100 },
      { date: new Date(Date.now() - 120 * 24 * 60 * 60 * 1000), price: 2150 },
      { date: new Date(Date.now() - 90 * 24 * 60 * 60 * 1000), price: 2080 },
      { date: new Date(Date.now() - 60 * 24 * 60 * 60 * 1000), price: 2200 },
      { date: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000), price: 2180 },
      { date: new Date(), price: 2200 }
    ],
    predictedPrices: [
      { date: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000), price: 2250 },
      { date: new Date(Date.now() + 60 * 24 * 60 * 60 * 1000), price: 2280 },
      { date: new Date(Date.now() + 90 * 24 * 60 * 60 * 1000), price: 2320 },
      { date: new Date(Date.now() + 120 * 24 * 60 * 60 * 1000), price: 2350 },
      { date: new Date(Date.now() + 150 * 24 * 60 * 60 * 1000), price: 2380 },
      { date: new Date(Date.now() + 180 * 24 * 60 * 60 * 1000), price: 2400 }
    ],
    profitAnalysis: {
      totalRevenue: 105750,
      totalCost: 35000,
      totalProfit: 70750,
      profitPerHectare: 70750
    },
    seasonality: {
      planting: "Oct-Nov" as const,
      harvesting: "Mar-Apr" as const,
      season: "Rabi" as const
    }
  },
  aiAssistant: {
    selectedModel: AIModel.LLAMA3,
    temperature: 0.7,
    messages: [
      {
        role: "assistant" as const,
        content: "Hello! I'm your agricultural AI assistant. How can I help today?"
      }
    ],
    commonQuestions: [
      "What's the best fertilizer for wheat in Indian soil conditions?",
      "What are the most effective ways to control pests in rice cultivation?",
      "When is the optimal time to harvest cotton for maximum yield and quality?"
    ]
  }
};