import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { Slider } from '@/components/ui/slider';
import { Input } from '@/components/ui/input';
import { Checkbox } from '@/components/ui/checkbox';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceArea } from 'recharts';
import { DayOfWeek, IrrigationStatus } from '@/types/enums';
import { getIrrigationStatusMessage } from '@/lib/formatters';
import type { MoistureDataPoint } from '@/types/schema';

interface IrrigationProps {
  moistureHistory: MoistureDataPoint[];
}

export function Irrigation({ moistureHistory }: IrrigationProps) {
  const [soilMoisture, setSoilMoisture] = useState([35]);
  const [temperature, setTemperature] = useState(28);
  const [humidity, setHumidity] = useState([65]);
  const [rainfallChance, setRainfallChance] = useState([20]);
  const [duration, setDuration] = useState([15]);
  const [irrigationTime, setIrrigationTime] = useState("06:00");
  const [selectedDays, setSelectedDays] = useState<DayOfWeek[]>([
    DayOfWeek.MONDAY,
    DayOfWeek.WEDNESDAY,
    DayOfWeek.FRIDAY
  ]);

  const getIrrigationStatus = (): IrrigationStatus => {
    if (soilMoisture[0] < 30) return IrrigationStatus.NEEDED;
    if (soilMoisture[0] < 50) return IrrigationStatus.RECOMMENDED;
    return IrrigationStatus.NOT_NEEDED;
  };

  const status = getIrrigationStatus();
  const statusColor = status === IrrigationStatus.NEEDED ? 'text-error' :
                      status === IrrigationStatus.RECOMMENDED ? 'text-warning' : 'text-success';

  const handleStartIrrigation = () => {
    alert(`Irrigation started for ${duration[0]} minutes`);
  };

  const handleSetSchedule = () => {
    alert(`Irrigation scheduled for ${irrigationTime} on ${selectedDays.join(', ')}`);
  };

  const toggleDay = (day: DayOfWeek) => {
    setSelectedDays(prev =>
      prev.includes(day) ? prev.filter(d => d !== day) : [...prev, day]
    );
  };

  const chartData = moistureHistory.map(point => ({
    date: point.date.toLocaleDateString('en-IN', { month: 'short', day: 'numeric' }),
    moisture: point.moisture
  }));

  return (
    <div className="space-y-6">
      <div>
        <h2 className="heading-lg mb-2">💧 Smart Irrigation System</h2>
        <Alert>
          <AlertDescription>
            Monitor and control your irrigation system based on soil moisture and weather conditions.
          </AlertDescription>
        </Alert>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Current Conditions</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label>Soil Moisture (%): {soilMoisture[0]}</Label>
              <Slider value={soilMoisture} onValueChange={setSoilMoisture} min={0} max={100} step={1} />
            </div>

            <div className="space-y-2">
              <Label>Temperature (°C)</Label>
              <Input
                type="number"
                value={temperature}
                onChange={(e) => setTemperature(parseFloat(e.target.value) || 0)}
              />
            </div>

            <div className="space-y-2">
              <Label>Humidity (%): {humidity[0]}</Label>
              <Slider value={humidity} onValueChange={setHumidity} min={0} max={100} step={1} />
            </div>

            <div className="space-y-2">
              <Label>Chance of Rain (%): {rainfallChance[0]}</Label>
              <Slider value={rainfallChance} onValueChange={setRainfallChance} min={0} max={100} step={1} />
            </div>

            <div className="pt-4">
              <p className="body-sm text-muted-foreground mb-2">Status:</p>
              <p className={`heading-sm ${statusColor}`}>
                {getIrrigationStatusMessage(status)}
              </p>
            </div>
          </CardContent>
        </Card>

        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Irrigation Control</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label>Irrigation Duration (minutes): {duration[0]}</Label>
                <Slider value={duration} onValueChange={setDuration} min={0} max={60} step={1} />
              </div>

              <Button onClick={handleStartIrrigation} className="w-full bg-primary-green hover:bg-primary-dark">
                Start Irrigation
              </Button>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Schedule Irrigation</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label>Preferred Time</Label>
                <Input
                  type="time"
                  value={irrigationTime}
                  onChange={(e) => setIrrigationTime(e.target.value)}
                />
              </div>

              <div className="space-y-2">
                <Label>Days</Label>
                <div className="grid grid-cols-2 gap-2">
                  {Object.values(DayOfWeek).map((day) => (
                    <div key={day} className="flex items-center space-x-2">
                      <Checkbox
                        id={day}
                        checked={selectedDays.includes(day)}
                        onCheckedChange={() => toggleDay(day)}
                      />
                      <label htmlFor={day} className="body-sm cursor-pointer">
                        {day}
                      </label>
                    </div>
                  ))}
                </div>
              </div>

              <Button onClick={handleSetSchedule} className="w-full bg-primary-green hover:bg-primary-dark">
                Set Schedule
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Soil Moisture History</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis label={{ value: 'Moisture (%)', angle: -90, position: 'insideLeft' }} />
                <Tooltip />
                <ReferenceArea y1={30} y2={50} fill="#22c55e" fillOpacity={0.2} label="Optimal Range" />
                <Line type="monotone" dataKey="moisture" stroke="#3b82f6" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}