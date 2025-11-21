import { useState } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { Slider } from '@/components/ui/slider';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { CropType, Season } from '@/types/enums';
import { getSoilQualityLevel, getSoilQualityMessage, formatSoilQualityScore } from '@/lib/formatters';

export function SoilQuality() {
  const [pH, setpH] = useState([6.5]);
  const [nitrogen, setNitrogen] = useState([50]);
  const [phosphorus, setPhosphorus] = useState([40]);
  const [potassium, setPotassium] = useState([300]);
  const [organicMatter, setOrganicMatter] = useState([2.5]);
  const [previousCrop, setPreviousCrop] = useState<string>("None");
  const [season, setSeason] = useState<Season>(Season.WINTER);
  const [soilScore, setSoilScore] = useState<number | null>(null);
  const [recommendedCrop, setRecommendedCrop] = useState<string | null>(null);

  const calculateSoilQuality = () => {
    // Mock calculation
    const pHScore = 10 * (1 - Math.abs(6.5 - pH[0]) / 3.5);
    const nitrogenScore = Math.min(nitrogen[0] / 50 * 10, 10);
    const phosphorusScore = Math.min(phosphorus[0] / 40 * 10, 10);
    const potassiumScore = Math.min(potassium[0] / 300 * 10, 10);
    const organicMatterScore = Math.min(organicMatter[0] * 2, 10);

    const totalScore = (
      pHScore * 0.2 +
      nitrogenScore * 0.25 +
      phosphorusScore * 0.25 +
      potassiumScore * 0.2 +
      organicMatterScore * 0.1
    );

    setSoilScore(totalScore);

    // Mock crop recommendation
    const crops = {
      [Season.WINTER]: ['wheat', 'chickpea', 'potato'],
      [Season.SUMMER]: ['corn', 'soybean', 'tomato'],
      [Season.MONSOON]: ['rice', 'cotton', 'sugarcane']
    };
    setRecommendedCrop(crops[season][0]);
  };

  const soilLevel = soilScore !== null ? getSoilQualityLevel(soilScore) : null;

  return (
    <div className="space-y-6">
      <div>
        <h2 className="heading-lg mb-2">🧪 Soil Quality Analysis</h2>
        <Alert>
          <AlertDescription>
            Enter your soil parameters to get a quality score and recommendations.
          </AlertDescription>
        </Alert>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card>
          <CardContent className="pt-6 space-y-6">
            <div className="space-y-2">
              <Label>pH Level: {pH[0].toFixed(1)}</Label>
              <Slider value={pH} onValueChange={setpH} min={3} max={10} step={0.1} />
            </div>

            <div className="space-y-2">
              <Label>Nitrogen (mg/kg): {nitrogen[0]}</Label>
              <Slider value={nitrogen} onValueChange={setNitrogen} min={0} max={100} step={1} />
            </div>

            <div className="space-y-2">
              <Label>Phosphorus (mg/kg): {phosphorus[0]}</Label>
              <Slider value={phosphorus} onValueChange={setPhosphorus} min={0} max={100} step={1} />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6 space-y-6">
            <div className="space-y-2">
              <Label>Potassium (mg/kg): {potassium[0]}</Label>
              <Slider value={potassium} onValueChange={setPotassium} min={0} max={500} step={1} />
            </div>

            <div className="space-y-2">
              <Label>Organic Matter (%): {organicMatter[0].toFixed(1)}</Label>
              <Slider value={organicMatter} onValueChange={setOrganicMatter} min={0} max={10} step={0.1} />
            </div>

            <div className="space-y-2">
              <Label>Previous Crop</Label>
              <Select value={previousCrop} onValueChange={setPreviousCrop}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="None">None</SelectItem>
                  <SelectItem value={CropType.WHEAT}>Wheat</SelectItem>
                  <SelectItem value={CropType.RICE}>Rice</SelectItem>
                  <SelectItem value={CropType.CORN}>Corn</SelectItem>
                  <SelectItem value={CropType.SOYBEAN}>Soybean</SelectItem>
                  <SelectItem value={CropType.COTTON}>Cotton</SelectItem>
                  <SelectItem value={CropType.SUGARCANE}>Sugarcane</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </CardContent>
        </Card>
      </div>

      <Button onClick={calculateSoilQuality} className="w-full bg-primary-green hover:bg-primary-dark">
        Analyze Soil Quality
      </Button>

      {soilScore !== null && (
        <div className="space-y-4">
          <Alert className="border-primary-green">
            <AlertDescription className="text-lg font-semibold">
              Soil Quality Score: {formatSoilQualityScore(soilScore)}
            </AlertDescription>
          </Alert>

          {soilLevel && (
            <Alert className={
              soilLevel === 'excellent' ? 'border-success' :
              soilLevel === 'good' ? 'border-info' :
              soilLevel === 'fair' ? 'border-warning' : 'border-error'
            }>
              <AlertDescription>
                {getSoilQualityMessage(soilLevel)}
              </AlertDescription>
            </Alert>
          )}

          <div className="space-y-2">
            <Label>Current Season</Label>
            <div className="flex gap-2">
              {[Season.WINTER, Season.SUMMER, Season.MONSOON].map((s) => (
                <Button
                  key={s}
                  variant={season === s ? "default" : "outline"}
                  onClick={() => setSeason(s)}
                  className={season === s ? "bg-primary-green hover:bg-primary-dark" : ""}
                >
                  {s.charAt(0).toUpperCase() + s.slice(1)}
                </Button>
              ))}
            </div>
          </div>

          {recommendedCrop && (
            <Alert>
              <AlertDescription>
                <strong>Recommended crop:</strong> {recommendedCrop.charAt(0).toUpperCase() + recommendedCrop.slice(1)}
              </AlertDescription>
            </Alert>
          )}
        </div>
      )}
    </div>
  );
}