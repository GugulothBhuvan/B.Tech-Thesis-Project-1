<<<<<<< HEAD
# KGP GPT - Multi-Agent RAG Chatbot

A sophisticated multi-agent Retrieval-Augmented Generation (RAG) chatbot prototype powered by **Gemini LLM**. This system combines local knowledge retrieval with real-time web search to provide comprehensive, accurate responses.

## 🚀 Features

- **Multi-Agent Architecture**: Specialized agents for query understanding, retrieval, web search, reasoning, and response generation
- **Hybrid RAG**: Combines local vector database (Qdrant) with real-time internet search (Serper API)
- **Intelligent Query Routing**: Automatically determines whether to use local knowledge, web search, or both
- **Real-time System Monitoring**: Health checks and performance metrics for all system components
- **Modern UI**: Clean, responsive React frontend with Tailwind CSS
- **API-First Design**: RESTful API endpoints for easy integration

## 🏗️ Architecture

### Multi-Agent Framework

1. **Query Understanding Agent (Q-UA)**: Analyzes user intent and routes queries appropriately
2. **Retriever Agent (R-A)**: Searches local knowledge base using Qdrant vector database
3. **Web Search Agent (WS-A)**: Performs real-time internet searches using Serper API
4. **Reasoning Agent (RS-A)**: Synthesizes and analyzes information from multiple sources
5. **Summarizer Agent (SM-A)**: Generates final responses using Gemini LLM
6. **Orchestrator Agent**: Coordinates all agents and manages the pipeline

### Data Flow

```
User Query → Query Understanding → Local Retrieval + Web Search → Reasoning → Response Generation → User
```

## 🛠️ Technology Stack

- **Frontend**: Next.js 14, React 18, TypeScript, Tailwind CSS
- **AI/ML**: Google Gemini LLM API, Gemini-compatible embeddings
- **Vector Database**: Qdrant (local)
- **Web Search**: Serper API
- **Backend**: Next.js API routes (serverless)
- **Styling**: Tailwind CSS with custom animations

## 📋 Prerequisites

- Node.js 18+ and npm/yarn
- Qdrant vector database (local or cloud)
- Gemini API key from Google AI Studio
- Serper API key for web search functionality

## 🚀 Quick Start

### 1. Clone and Install

```bash
git clone <repository-url>
cd kgpgpt
npm install
```

### 2. Environment Setup

Copy the example environment file and configure your API keys:

```bash
cp env.example .env.local
```

Edit `.env.local` with your actual API keys:

```env
GEMINI_API_KEY=your_actual_gemini_api_key
SERPER_API_KEY=your_actual_serper_api_key
QDRANT_URL=http://localhost:6333
```

### 3. Start Qdrant Database

#### Option A: Docker (Recommended)

```bash
docker run -p 6333:6333 qdrant/qdrant
```

#### Option B: Local Installation

Follow the [Qdrant installation guide](https://qdrant.tech/documentation/guides/installation/)

### 4. Run the Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GEMINI_API_KEY` | Google Gemini API key | Required |
| `SERPER_API_KEY` | Serper API key for web search | Required |
| `QDRANT_URL` | Qdrant database URL | `http://localhost:6333` |

### System Settings

The system can be configured through the `lib/config.ts` file:

- Vector size: 768 dimensions
- Max retrieval results: 5 documents
- Max web search results: 5 results
- Request timeout: 30 seconds

## 📚 Knowledge Base Setup

### 1. Prepare Your Documents

The system expects JSON documents with the following structure:

```json
{
  "id": "unique_document_id",
  "content": "document text content",
  "metadata": {
    "title": "Document Title",
    "source": "source_url_or_name",
    "category": "document_category"
  }
}
```

### 2. Index Documents

Use the provided utilities to index your documents:

```typescript
import { QdrantClient } from 'qdrant-client';
import { indexDocuments } from '@/lib/utils/qdrant-setup';

const client = new QdrantClient({ url: 'http://localhost:6333' });
const success = await indexDocuments(client, documents, config);
```

## 🧪 Testing

### Health Check

Check system status:

```bash
curl http://localhost:3000/api/health
```

### Test Query

Send a test query:

```bash
curl -X POST http://localhost:3000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is artificial intelligence?", "enableWebSearch": false}'
```

## 📊 Performance Metrics

The system tracks various performance metrics:

- **Query Processing Time**: Total time from query to response
- **Agent Timeline**: Individual agent processing times
- **Confidence Scores**: Response confidence based on available information
- **System Health**: Real-time status of all services

## 🔍 API Endpoints

### POST `/api/query`

Main endpoint for processing chat queries.

**Request:**
```json
{
  "query": "Your question here",
  "enableWebSearch": true
}
```

**Response:**
```json
{
  "response": "AI generated response",
  "confidence": 0.85,
  "sources": ["Local Knowledge Base", "Web Search Results"],
  "metadata": {
    "totalProcessingTime": 2450,
    "agentTimeline": {
      "queryUnderstanding": 15,
      "retrieval": 1200,
      "webSearch": 800,
      "reasoning": 200,
      "summarization": 1235
    }
  }
}
```

### GET `/api/health`

System health check endpoint.

## 🚧 Development

### Project Structure

```
kgpgpt/
├── app/                    # Next.js app directory
│   ├── api/               # API routes
│   ├── globals.css        # Global styles
│   ├── layout.tsx         # Root layout
│   └── page.tsx           # Main page
├── components/             # React components
├── lib/                   # Core library
│   ├── agents/            # Multi-agent framework
│   ├── config.ts          # Configuration
│   └── utils/             # Utility functions
├── scraper.py             # Web scraper for data collection
└── package.json           # Dependencies
```

### Adding New Agents

1. Extend the `BaseAgent` class
2. Implement the `process()` method
3. Add the agent to the `OrchestratorAgent`
4. Update the pipeline flow

### Customizing Embeddings

Replace the placeholder embedding generation in `RetrieverAgent` with your preferred embedding model:

```typescript
private async generateQueryEmbedding(query: string): Promise<number[]> {
  // Replace with your embedding model
  const response = await fetch('your-embedding-api', {
    method: 'POST',
    body: JSON.stringify({ text: query })
  });
  return await response.json();
}
```

## 🐛 Troubleshooting

### Common Issues

1. **Qdrant Connection Failed**
   - Ensure Qdrant is running on the specified port
   - Check firewall settings
   - Verify the URL in environment variables

2. **API Key Errors**
   - Verify API keys are correctly set in `.env.local`
   - Check API key permissions and quotas
   - Ensure keys are not expired

3. **Collection Not Ready**
   - Wait for Qdrant to fully initialize
   - Check collection status in Qdrant dashboard
   - Verify vector dimensions match configuration

### Debug Mode

Enable detailed logging by setting the log level in your environment:

```env
DEBUG=true
LOG_LEVEL=debug
```

## 🔮 Future Enhancements

- [ ] Backend scaling with distributed Qdrant
- [ ] Redis caching layer for high-frequency queries
- [ ] Multi-turn conversation memory
- [ ] Advanced ranking algorithms
- [ ] Multi-modal support (images, PDFs)
- [ ] Fine-tuned domain-specific embeddings
- [ ] Agent memory and personalization

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For questions and support:

- Create an issue in the repository
- Check the troubleshooting section
- Review the API documentation

## 🙏 Acknowledgments

- Google Gemini team for the LLM API
- Qdrant team for the vector database
- Serper team for the web search API
- Next.js and React communities

---

**Built with ❤️ for the KGP community**
=======
# kgpgpt
>>>>>>> d955e4cdb2cc8dfffaf7fccbfc3436dd4649fc0e
