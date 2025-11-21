import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Dashboard } from '@/components/Dashboard/Dashboard';
import { SoilQuality } from '@/components/SoilQuality/SoilQuality';
import { YieldPrediction } from '@/components/YieldPrediction/YieldPrediction';
import { Irrigation } from '@/components/Irrigation/Irrigation';
import { MarketAnalysis } from '@/components/MarketAnalysis/MarketAnalysis';
import { AIAssistant } from '@/components/AIAssistant/AIAssistant';
import { mockRootProps } from '@/data/smartAgriMockData';
import { Sprout } from 'lucide-react';

function App() {
  return (
    <div className="min-h-screen bg-background">
      <header className="border-b bg-white sticky top-0 z-10">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center gap-3">
            <Sprout size={32} className="text-primary-green" />
            <h1 className="heading-xl text-primary-green">Smart Agriculture AI System</h1>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-6">
        <Tabs defaultValue="dashboard" className="w-full">
          <TabsList className="grid w-full grid-cols-2 md:grid-cols-3 lg:grid-cols-6 mb-6">
            <TabsTrigger value="dashboard">🏠 Dashboard</TabsTrigger>
            <TabsTrigger value="soil">🧪 Soil Quality</TabsTrigger>
            <TabsTrigger value="yield">📈 Yield Prediction</TabsTrigger>
            <TabsTrigger value="irrigation">💧 Irrigation</TabsTrigger>
            <TabsTrigger value="market">📊 Market Analysis</TabsTrigger>
            <TabsTrigger value="ai">🤖 AI Assistant</TabsTrigger>
          </TabsList>

          <TabsContent value="dashboard">
            <Dashboard
              metrics={mockRootProps.dashboardMetrics}
              marketUpdates={mockRootProps.marketUpdates}
            />
          </TabsContent>

          <TabsContent value="soil">
            <SoilQuality />
          </TabsContent>

          <TabsContent value="yield">
            <YieldPrediction />
          </TabsContent>

          <TabsContent value="irrigation">
            <Irrigation moistureHistory={mockRootProps.irrigation.moistureHistory} />
          </TabsContent>

          <TabsContent value="market">
            <MarketAnalysis initialData={mockRootProps.marketAnalysis} />
          </TabsContent>

          <TabsContent value="ai">
            <AIAssistant />
          </TabsContent>
        </Tabs>
      </main>
    </div>
  );
}

export default App;