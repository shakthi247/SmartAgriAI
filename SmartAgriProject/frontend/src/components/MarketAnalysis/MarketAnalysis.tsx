import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Input } from '@/components/ui/input';
import { Checkbox } from '@/components/ui/checkbox';
import { Calendar } from '@/components/ui/calendar';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts';
import { CropType } from '@/types/enums';
import { formatCurrency, formatDate } from '@/lib/formatters';
import type { MarketAnalysis as MarketAnalysisType } from '@/types/schema';
import { MetricCard } from '../MetricCard';

interface MarketAnalysisProps {
  initialData: MarketAnalysisType;
}

export function MarketAnalysis({ initialData }: MarketAnalysisProps) {
  const [selectedCrop, setSelectedCrop] = useState<CropType>(initialData.selectedCrop);
  const [plantingDate, setPlantingDate] = useState<Date>(initialData.plantingDate);
  const [area, setArea] = useState(initialData.area);
  const [useTypicalYield, setUseTypicalYield] = useState(initialData.useTypicalYield);
  const [expectedYield, setExpectedYield] = useState(initialData.expectedYield);
  const [useTypicalCost, setUseTypicalCost] = useState(initialData.useTypicalCost);
  const [costPerHectare, setCostPerHectare] = useState(initialData.costPerHectare);
  const [analysisResult, setAnalysisResult] = useState<MarketAnalysisType | null>(null);

  const handleAnalyze = () => {
    // Mock analysis - in real app this would call an API
    setAnalysisResult(initialData);
  };

  const chartData = analysisResult ? [
    ...analysisResult.historicalPrices.map(p => ({
      date: p.date.getTime(),
      price: p.price,
      type: 'historical'
    })),
    ...analysisResult.predictedPrices.map(p => ({
      date: p.date.getTime(),
      price: p.price,
      type: 'predicted'
    }))
  ] : [];

  return (
    <div className="space-y-6">
      <div>
        <h2 className="heading-lg mb-2">📊 Crop Market Analysis & Price Prediction (₹)</h2>
        <Alert>
          <AlertDescription>
            Analyze market trends and predict future prices for your crops.
          </AlertDescription>
        </Alert>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card>
          <CardContent className="pt-6 space-y-4">
            <div className="space-y-2">
              <Label>Select crop to analyze:</Label>
              <Select value={selectedCrop} onValueChange={(value) => setSelectedCrop(value as CropType)}>
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
              <Label>Expected planting date:</Label>
              <Calendar
                mode="single"
                selected={plantingDate}
                onSelect={(date) => date && setPlantingDate(date)}
                className="rounded-md border"
              />
            </div>

            <div className="space-y-2">
              <Label>Area (hectares):</Label>
              <Input
                type="number"
                value={area}
                onChange={(e) => setArea(parseFloat(e.target.value) || 0)}
                min={0.1}
                max={1000}
                step={0.1}
              />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6 space-y-4">
            <div className="flex items-center space-x-2">
              <Checkbox
                id="typicalYield"
                checked={useTypicalYield}
                onCheckedChange={(checked) => setUseTypicalYield(checked as boolean)}
              />
              <label htmlFor="typicalYield" className="body-sm cursor-pointer">
                Use typical yield for this crop
              </label>
            </div>

            {!useTypicalYield && (
              <div className="space-y-2">
                <Label>Expected yield (quintals/hectare):</Label>
                <Input
                  type="number"
                  value={expectedYield}
                  onChange={(e) => setExpectedYield(parseFloat(e.target.value) || 0)}
                  min={1}
                  max={1000}
                  step={1}
                />
              </div>
            )}

            <div className="flex items-center space-x-2">
              <Checkbox
                id="typicalCost"
                checked={useTypicalCost}
                onCheckedChange={(checked) => setUseTypicalCost(checked as boolean)}
              />
              <label htmlFor="typicalCost" className="body-sm cursor-pointer">
                Use typical cultivation cost
              </label>
            </div>

            {!useTypicalCost && (
              <div className="space-y-2">
                <Label>Cost per hectare (₹):</Label>
                <Input
                  type="number"
                  value={costPerHectare}
                  onChange={(e) => setCostPerHectare(parseFloat(e.target.value) || 0)}
                  min={1000}
                  max={200000}
                  step={1000}
                />
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      <Button onClick={handleAnalyze} className="w-full bg-primary-green hover:bg-primary-dark">
        📈 Analyze Market & Predict Prices
      </Button>

      {analysisResult && (
        <div className="space-y-6">
          <Alert className="border-success">
            <AlertDescription>
              Analysis complete for {selectedCrop.charAt(0).toUpperCase() + selectedCrop.slice(1)}!
            </AlertDescription>
          </Alert>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <MetricCard
              title="Predicted Harvest Price"
              value={formatCurrency(analysisResult.predictedPrice) + '/quintal'}
            />
            <MetricCard
              title="Expected Harvest Date"
              value={formatDate(analysisResult.harvestDate)}
            />
            <MetricCard
              title="Expected Yield"
              value={`${analysisResult.expectedYield} quintals/hectare`}
            />
            <MetricCard
              title="Cultivation Cost"
              value={formatCurrency(analysisResult.costPerHectare) + '/hectare'}
            />
          </div>

          <Card>
            <CardHeader>
              <CardTitle>{selectedCrop.charAt(0).toUpperCase() + selectedCrop.slice(1)} Price Prediction (₹/quintal)</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="h-96">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis
                      dataKey="date"
                      type="number"
                      domain={['dataMin', 'dataMax']}
                      tickFormatter={(value) => new Date(value).toLocaleDateString('en-IN', { month: 'short', day: 'numeric' })}
                    />
                    <YAxis label={{ value: 'Price (₹ per quintal)', angle: -90, position: 'insideLeft' }} />
                    <Tooltip
                      labelFormatter={(value) => new Date(value).toLocaleDateString('en-IN')}
                      formatter={(value: number) => [formatCurrency(value), 'Price']}
                    />
                    <ReferenceLine
                      x={analysisResult.harvestDate.getTime()}
                      stroke="#22c55e"
                      strokeDasharray="3 3"
                      label="Harvest Date"
                    />
                    <ReferenceLine
                      x={new Date().getTime()}
                      stroke="#f97316"
                      label="Today"
                    />
                    <Line
                      data={analysisResult.historicalPrices.map(p => ({ date: p.date.getTime(), price: p.price }))}
                      type="monotone"
                      dataKey="price"
                      stroke="#3b82f6"
                      strokeWidth={2}
                      name="Historical"
                      dot={false}
                    />
                    <Line
                      data={analysisResult.predictedPrices.map(p => ({ date: p.date.getTime(), price: p.price }))}
                      type="monotone"
                      dataKey="price"
                      stroke="#ef4444"
                      strokeWidth={2}
                      strokeDasharray="5 5"
                      name="Predicted"
                      dot={false}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>

          <div>
            <h3 className="heading-md mb-4">💰 Expected Profit Analysis</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <MetricCard
                title="Total Revenue"
                value={formatCurrency(analysisResult.profitAnalysis.totalRevenue)}
              />
              <MetricCard
                title="Total Cost"
                value={formatCurrency(analysisResult.profitAnalysis.totalCost)}
              />
              <MetricCard
                title="Total Profit"
                value={formatCurrency(analysisResult.profitAnalysis.totalProfit)}
              />
              <MetricCard
                title="Profit per Hectare"
                value={formatCurrency(analysisResult.profitAnalysis.profitPerHectare)}
              />
            </div>
          </div>

          <div>
            <h3 className="heading-md mb-4">🌾 Crop Seasonality Information</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <Alert>
                <AlertDescription>
                  <strong>Planting Season:</strong> {analysisResult.seasonality.planting}
                </AlertDescription>
              </Alert>
              <Alert>
                <AlertDescription>
                  <strong>Harvesting Season:</strong> {analysisResult.seasonality.harvesting}
                </AlertDescription>
              </Alert>
              <Alert>
                <AlertDescription>
                  <strong>Crop Season:</strong> {analysisResult.seasonality.season}
                </AlertDescription>
              </Alert>
            </div>
          </div>

          <div>
            <h3 className="heading-md mb-4">💡 Planting Recommendations</h3>
            {analysisResult.profitAnalysis.totalProfit > 0 ? (
              <Alert className="border-success">
                <AlertDescription>
                  <strong>Good choice!</strong> {selectedCrop.charAt(0).toUpperCase() + selectedCrop.slice(1)} shows positive profit potential.
                </AlertDescription>
              </Alert>
            ) : (
              <Alert className="border-warning">
                <AlertDescription>
                  <strong>Consider alternatives!</strong> {selectedCrop.charAt(0).toUpperCase() + selectedCrop.slice(1)} may not be profitable.
                </AlertDescription>
              </Alert>
            )}
          </div>
        </div>
      )}
    </div>
  );
}