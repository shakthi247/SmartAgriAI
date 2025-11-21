import { useState } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { Slider } from '@/components/ui/slider';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Input } from '@/components/ui/input';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { CropType } from '@/types/enums';
import { formatYield } from '@/lib/formatters';

export function YieldPrediction() {
  const [crop, setCrop] = useState<CropType>(CropType.WHEAT);
  const [area, setArea] = useState(1.0);
  const [rainfall, setRainfall] = useState([500]);
  const [temperature, setTemperature] = useState([25]);
  const [soilQuality, setSoilQuality] = useState([7.0]);
  const [nitrogenFert, setNitrogenFert] = useState([100]);
  const [phosphorusFert, setPhosphorusFert] = useState([50]);
  const [potassiumFert, setPotassiumFert] = useState([50]);
  const [prediction, setPrediction] = useState<{ yield: number; total: number } | null>(null);
  const [chartData, setChartData] = useState<any[]>([]);

  const handlePredictYield = () => {
    const baseYield: Record<CropType, number> = {
      [CropType.WHEAT]: 4.5,
      [CropType.RICE]: 3.8,
      [CropType.CORN]: 5.2,
      [CropType.SOYBEAN]: 2.5,
      [CropType.COTTON]: 2.0,
      [CropType.SUGARCANE]: 75.0,
      [CropType.POTATO]: 25.0,
      [CropType.TOMATO]: 30.0,
      [CropType.CHICKPEA]: 1.5,
      [CropType.LENTIL]: 1.2,
      [CropType.MUSTARD]: 1.5,
      [CropType.GROUNDNUT]: 2.0,
      [CropType.BARLEY]: 4.0,
      [CropType.MAIZE]: 4.5
    };

    let yieldFactor = 1.0;
    yieldFactor *= (soilQuality[0] / 7.0);
    yieldFactor *= (rainfall[0] / 500) < 1 ? (rainfall[0] / 500) : (1.0 - (rainfall[0] - 500) / 1000);
    yieldFactor *= (1.0 + (nitrogenFert[0] - 100) / 400);

    const predictedYield = baseYield[crop] * yieldFactor;
    const totalYield = predictedYield * area;

    setPrediction({ yield: predictedYield, total: totalYield });

    // Generate chart data
    const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    const data = months.map((month, i) => ({
      month,
      yield: predictedYield * (0.8 + 0.4 * i / 11)
    }));
    setChartData(data);
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="heading-lg mb-2">📈 Crop Yield Prediction</h2>
        <Alert>
          <AlertDescription>
            Predict crop yield based on historical data and current conditions.
          </AlertDescription>
        </Alert>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card>
          <CardContent className="pt-6 space-y-4">
            <div className="space-y-2">
              <Label>Select Crop</Label>
              <Select value={crop} onValueChange={(value) => setCrop(value as CropType)}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {Object.values(CropType).map((c) => (
                    <SelectItem key={c} value={c}>
                      {c.charAt(0).toUpperCase() + c.slice(1)}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label>Area (hectares)</Label>
              <Input
                type="number"
                value={area}
                onChange={(e) => setArea(parseFloat(e.target.value) || 0)}
                min={0.1}
                step={0.1}
              />
            </div>

            <div className="space-y-2">
              <Label>Expected Rainfall (mm): {rainfall[0]}</Label>
              <Slider value={rainfall} onValueChange={setRainfall} min={0} max={1000} step={10} />
            </div>

            <div className="space-y-2">
              <Label>Expected Average Temperature (°C): {temperature[0]}</Label>
              <Slider value={temperature} onValueChange={setTemperature} min={10} max={40} step={1} />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6 space-y-4">
            <div className="space-y-2">
              <Label>Soil Quality Score: {soilQuality[0].toFixed(1)}</Label>
              <Slider value={soilQuality} onValueChange={setSoilQuality} min={0} max={10} step={0.1} />
            </div>

            <div className="space-y-2">
              <Label>Nitrogen Fertilizer (kg/hectare): {nitrogenFert[0]}</Label>
              <Slider value={nitrogenFert} onValueChange={setNitrogenFert} min={0} max={200} step={1} />
            </div>

            <div className="space-y-2">
              <Label>Phosphorus Fertilizer (kg/hectare): {phosphorusFert[0]}</Label>
              <Slider value={phosphorusFert} onValueChange={setPhosphorusFert} min={0} max={100} step={1} />
            </div>

            <div className="space-y-2">
              <Label>Potassium Fertilizer (kg/hectare): {potassiumFert[0]}</Label>
              <Slider value={potassiumFert} onValueChange={setPotassiumFert} min={0} max={100} step={1} />
            </div>
          </CardContent>
        </Card>
      </div>

      <Button onClick={handlePredictYield} className="w-full bg-primary-green hover:bg-primary-dark">
        Predict Yield
      </Button>

      {prediction && (
        <div className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Alert className="border-success">
              <AlertDescription className="font-semibold">
                Predicted Yield: {formatYield(prediction.yield)}
              </AlertDescription>
            </Alert>
            <Alert className="border-success">
              <AlertDescription className="font-semibold">
                Total Yield: {formatYield(prediction.total, "tons")}
              </AlertDescription>
            </Alert>
          </div>

          <Card>
            <CardContent className="pt-6">
              <h3 className="heading-sm mb-4">Monthly Yield Trend for {crop.charAt(0).toUpperCase() + crop.slice(1)}</h3>
              <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="month" />
                    <YAxis label={{ value: 'Yield (tons/hectare)', angle: -90, position: 'insideLeft' }} />
                    <Tooltip />
                    <Line type="monotone" dataKey="yield" stroke="#22c55e" strokeWidth={2} />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}