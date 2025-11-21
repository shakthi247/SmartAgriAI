# Smart Agriculture AI System - Frontend

A modern React + TypeScript web application for agricultural management with AI-powered assistance.

## Features

- **Dashboard**: Overview of farm metrics, market updates, and quick profit estimates
- **Soil Quality Analysis**: Interactive soil parameter analysis with recommendations
- **Yield Prediction**: Crop yield forecasting with visual trends
- **Smart Irrigation**: Moisture monitoring, scheduling, and control
- **Market Analysis**: Price prediction and profit analysis with interactive charts
- **AI Assistant**: Chat with Ollama-powered AI for agricultural advice

## Prerequisites

- Node.js 20.19+ or 22.12+ (currently running on 20.15.1 with warnings)
- Ollama installed and running locally

## Setup

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run dev
```

3. Ensure Ollama is running:
```bash
ollama serve
```

4. (Optional) Pull AI models if not already available:
```bash
ollama pull llama3
ollama pull mistral
```

## Using the AI Chatbot

The AI Assistant tab connects to your local Ollama instance to provide agricultural advice.

### Connection Status
- Green indicator: Connected to Ollama
- Red indicator: Cannot connect (make sure Ollama is running)

### Available Models
The chatbot automatically detects models installed on your system. Common models:
- `llama3:latest` - General purpose, good for agricultural advice
- `deepseek-r1:8b` - Reasoning model
- `mistral` - Fast and efficient

### Tips for Best Results
1. Ask specific questions about farming, crops, pests, or fertilizers
2. Adjust temperature (0-1) for response creativity:
   - Lower (0.3-0.5): More focused, factual responses
   - Higher (0.7-1.0): More creative, varied responses
3. Use the common question buttons for quick queries

### Example Questions
- "What's the best fertilizer for wheat in Indian soil conditions?"
- "How do I control pests in rice cultivation?"
- "When should I harvest cotton for maximum yield?"
- "What are the signs of nitrogen deficiency in crops?"
- "How much water does sugarcane need during different growth stages?"

## Tech Stack

- React 19 + TypeScript
- Vite
- Tailwind CSS v4
- shadcn/ui components
- Recharts for data visualization
- Ollama API for AI chat

## Project Structure

```
src/
├── components/          # React components
│   ├── Dashboard/
│   ├── SoilQuality/
│   ├── YieldPrediction/
│   ├── Irrigation/
│   ├── MarketAnalysis/
│   └── AIAssistant/
├── types/              # TypeScript type definitions
├── lib/                # Utility functions and API clients
├── data/               # Mock data
└── App.tsx             # Main application component
```

## Troubleshooting

### Ollama Connection Issues
- Ensure Ollama is running: `ollama serve`
- Check if Ollama is accessible: `curl http://127.0.0.1:11434/api/tags`
- Verify models are installed: `ollama list`

### Model Not Found
If you get "model not found" errors:
```bash
ollama pull llama3
```

### CORS Issues
Ollama allows localhost connections by default. If you encounter CORS issues, check Ollama's OLLAMA_ORIGINS environment variable.

## Development

Run type checking:
```bash
npm run build
```

---

## React + TypeScript + Vite Template Info

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) (or [oxc](https://oxc.rs) when used in [rolldown-vite](https://vite.dev/guide/rolldown)) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

### React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

### Expanding the ESLint configuration

If you are developing a production application, we recommend updating the configuration to enable type-aware lint rules:

```js
export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Other configs...

      // Remove tseslint.configs.recommended and replace with this
      tseslint.configs.recommendedTypeChecked,
      // Alternatively, use this for stricter rules
      tseslint.configs.strictTypeChecked,
      // Optionally, add this for stylistic rules
      tseslint.configs.stylisticTypeChecked,

      // Other configs...
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])
```

You can also install [eslint-plugin-react-x](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-x) and [eslint-plugin-react-dom](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-dom) for React-specific lint rules:

```js
// eslint.config.js
import reactX from 'eslint-plugin-react-x'
import reactDom from 'eslint-plugin-react-dom'

export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Other configs...
      // Enable lint rules for React
      reactX.configs['recommended-typescript'],
      // Enable lint rules for React DOM
      reactDom.configs.recommended,
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])
```