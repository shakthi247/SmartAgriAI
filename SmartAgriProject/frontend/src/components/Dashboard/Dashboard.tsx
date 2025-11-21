import { useState } from 'react';
import { MetricCard } from '../MetricCard';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Button } from '@/components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Slider } from '@/components/ui/slider';
import { Label } from '@/components/ui/label';
import { Droplets, Sprout, CloudRain, TrendingUp } from 'lucide-react';
import type { DashboardMetrics, MarketUpdate } from '@/types/schema';
import { CropType } from '@/types/enums';
import { formatCurrency } from '@/lib/formatters';

interface DashboardProps {
  metrics: DashboardMetrics;
  marketUpdates: MarketUpdate[];
}

export function Dashboard({ metrics, marketUpdates }: DashboardProps) {
  const [quickCrop, setQuickCrop] = useState<CropType>(CropType.WHEAT);
  const [quickArea, setQuickArea] = useState([5]);
  const [profitEstimate, setProfitEstimate] = useState<number | null>(null);

  const handleEstimateProfit = () => {
    // Mock profit calculation
    const baseProfit: Record<string, number> = { 
      [CropType.WHEAT]: 70000, 
      [CropType.RICE]: 65000, 
      [CropType.COTTON]: 85000 
    };
    const profit = (baseProfit[quickCrop] || 70000) * quickArea[0];
    setProfitEstimate(profit);
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="heading-lg mb-6">Farm Management Dashboard</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <MetricCard
            title="Soil Quality"
            value={`${metrics.soilQuality}/10`}
            delta={metrics.soilQualityDelta}
            icon={<Sprout size={24} />}
          />
          <MetricCard
            title="Predicted Yield"
            value={`${metrics.predictedYield} t/ha`}
            delta={metrics.yieldDelta}
            icon={<TrendingUp size={24} />}
          />
          <MetricCard
            title="Irrigation"
            value={metrics.irrigationStatus}
            icon={<Droplets size={24} />}
          />
          <MetricCard
            title="Wheat Market"
            value={formatCurrency(metrics.wheatPrice) + '/quintal'}
            delta={`+${metrics.wheatPriceDelta}%`}
            icon={<CloudRain size={24} />}
          />
        </div>
      </div>

      <div>
        <h3 className="heading-md mb-4">📰 Market Updates</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {marketUpdates.map((update, index) => (
            <Alert key={index}>
              <AlertDescription>
                <strong>{update.title}</strong> {update.content}
              </AlertDescription>
            </Alert>
          ))}
        </div>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>💰 Quick Profit Estimate</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label>Select crop:</Label>
            <Select value={quickCrop} onValueChange={(value) => setQuickCrop(value as CropType)}>
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value={CropType.WHEAT}>Wheat</SelectItem>
                <SelectItem value={CropType.RICE}>Rice</SelectItem>
                <SelectItem value={CropType.COTTON}>Cotton</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <Label>Area (hectares): {quickArea[0]}</Label>
            <Slider
              value={quickArea}
              onValueChange={setQuickArea}
              min={1}
              max={100}
              step={1}
            />
          </div>

          <Button onClick={handleEstimateProfit} className="w-full bg-primary-green hover:bg-primary-dark">
            Estimate Profit
          </Button>

          {profitEstimate !== null && (
            <Alert className={profitEstimate > 0 ? 'border-success' : 'border-error'}>
              <AlertDescription className={profitEstimate > 0 ? 'text-success' : 'text-error'}>
                {profitEstimate > 0 ? 'Expected profit: ' : 'Expected loss: '}
                {formatCurrency(Math.abs(profitEstimate))}
              </AlertDescription>
            </Alert>
          )}
        </CardContent>
      </Card>
    </div>
  );
}