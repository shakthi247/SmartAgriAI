import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Slider } from '@/components/ui/slider';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from '@/components/ui/collapsible';
import { ChevronDown, Loader2, AlertCircle, CheckCircle } from 'lucide-react';
import { AIModel } from '@/types/enums';
import type { ChatMessage } from '@/types/schema';
import { chatWithOllama, checkOllamaConnection, getAvailableModels, type OllamaMessage } from '@/lib/ollamaApi';

export function AIAssistant() {
  const [model, setModel] = useState<string>('llama3:latest');
  const [temperature, setTemperature] = useState([0.7]);
  const [messages, setMessages] = useState<ChatMessage[]>([
    { role: 'assistant', content: "Hello! I'm your agricultural AI assistant. How can I help today?" }
  ]);
  const [input, setInput] = useState('');
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isConnected, setIsConnected] = useState(false);
  const [availableModels, setAvailableModels] = useState<string[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    checkConnection();
    fetchAvailableModels();
  }, []);

  const checkConnection = async () => {
    const connected = await checkOllamaConnection();
    setIsConnected(connected);
    if (!connected) {
      setError('Cannot connect to Ollama. Please make sure Ollama is running.');
    } else {
      setError(null);
    }
  };

  const fetchAvailableModels = async () => {
    const models = await getAvailableModels();
    setAvailableModels(models);
  };

  const commonQuestions = [
    "What's the best fertilizer for wheat in Indian soil conditions?",
    "What are the most effective ways to control pests in rice cultivation?",
    "When is the optimal time to harvest cotton for maximum yield and quality?"
  ];

  const handleSendMessage = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage = input.trim();
    setInput('');
    setError(null);

    const newMessages: ChatMessage[] = [
      ...messages,
      { role: 'user', content: userMessage }
    ];
    setMessages(newMessages);
    setIsLoading(true);

    try {
      // Convert to Ollama message format
      const ollamaMessages: OllamaMessage[] = newMessages.map(msg => ({
        role: msg.role,
        content: msg.content
      }));

      const response = await chatWithOllama(model as AIModel, ollamaMessages, temperature[0]);

      setMessages([
        ...newMessages,
        { role: 'assistant', content: response }
      ]);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to get response from AI');
      // Remove the user message if there was an error
      setMessages(messages);
      setInput(userMessage); // Restore the input
    } finally {
      setIsLoading(false);
    }
  };

  const handleQuickQuestion = (question: string) => {
    setInput(question);
  };

  const handleClearConversation = () => {
    setMessages([
      { role: 'assistant', content: "Hello! I'm your agricultural AI assistant. How can I help today?" }
    ]);
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="heading-lg mb-2">🤖 AI Agriculture Assistant</h2>
        <Alert>
          <AlertDescription>
            Ask questions about crop management, pest control, fertilizers, or any other farming-related topic.
          </AlertDescription>
        </Alert>
      </div>

      <Alert className={isConnected ? 'border-success' : 'border-error'}>
        <div className="flex items-center gap-2">
          {isConnected ? (
            <>
              <CheckCircle size={16} className="text-success" />
              <AlertDescription>Connected to Ollama</AlertDescription>
            </>
          ) : (
            <>
              <AlertCircle size={16} className="text-error" />
              <AlertDescription>
                Not connected to Ollama. Please start Ollama service.
              </AlertDescription>
            </>
          )}
          <Button
            variant="outline"
            size="sm"
            onClick={checkConnection}
            className="ml-auto"
          >
            Retry
          </Button>
        </div>
      </Alert>

      <Collapsible open={isSettingsOpen} onOpenChange={setIsSettingsOpen}>
        <Card>
          <CardHeader>
            <CollapsibleTrigger className="flex items-center justify-between w-full">
              <CardTitle>Ollama Settings</CardTitle>
              <ChevronDown className={`transition-transform ${isSettingsOpen ? 'rotate-180' : ''}`} />
            </CollapsibleTrigger>
          </CardHeader>
          <CollapsibleContent>
            <CardContent className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label>Select AI Model</Label>
                <Select value={model} onValueChange={setModel}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {availableModels.length > 0 ? (
                      availableModels.map((m) => (
                        <SelectItem key={m} value={m}>{m}</SelectItem>
                      ))
                    ) : (
                      Object.values(AIModel).map((m) => (
                        <SelectItem key={m} value={m}>{m}</SelectItem>
                      ))
                    )}
                  </SelectContent>
                </Select>
                {availableModels.length > 0 && (
                  <p className="body-sm text-muted-foreground">
                    {availableModels.length} model(s) available
                  </p>
                )}
              </div>

              <div className="space-y-2">
                <Label>Response Creativity: {temperature[0].toFixed(1)}</Label>
                <Slider
                  value={temperature}
                  onValueChange={setTemperature}
                  min={0}
                  max={1}
                  step={0.1}
                />
              </div>
            </CardContent>
          </CollapsibleContent>
        </Card>
      </Collapsible>

      {error && (
        <Alert className="border-error">
          <AlertCircle size={16} className="text-error" />
          <AlertDescription className="text-error">{error}</AlertDescription>
        </Alert>
      )}

      <Card>
        <CardContent className="p-0">
          <ScrollArea className="h-96 p-4">
            <div className="space-y-4">
              {messages.map((message, index) => (
                <div
                  key={index}
                  className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-[80%] rounded-lg p-3 ${
                      message.role === 'user'
                        ? 'bg-primary-green text-white'
                        : 'bg-muted'
                    }`}
                  >
                    <p className="body-md">{message.content}</p>
                  </div>
                </div>
              ))}
            </div>
          </ScrollArea>
        </CardContent>
      </Card>

      <div className="flex gap-2">
        <Input
          placeholder="Ask a question about farming..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && !isLoading && handleSendMessage()}
          disabled={isLoading || !isConnected}
        />
        <Button
          onClick={handleSendMessage}
          disabled={isLoading || !isConnected || !input.trim()}
          className="bg-primary-green hover:bg-primary-dark"
        >
          {isLoading ? (
            <>
              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
              Sending...
            </>
          ) : (
            'Send'
          )}
        </Button>
      </div>

      <div>
        <h3 className="heading-sm mb-4">Common Questions</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {commonQuestions.map((question, index) => (
            <Button
              key={index}
              variant="outline"
              onClick={() => handleQuickQuestion(question)}
              disabled={isLoading || !isConnected}
              className="h-auto text-left whitespace-normal"
            >
              {question}
            </Button>
          ))}
        </div>
      </div>

      <Button
        variant="outline"
        onClick={handleClearConversation}
        className="w-full"
      >
        Clear Conversation
      </Button>
    </div>
  );
}