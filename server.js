import express from 'express';
import cors from 'cors';

const app = express();
app.use(cors());
app.use(express.json());

const HF_TOKEN = "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";

app.post('/api/chat', async (req, res) => {
  try {
    const { message } = req.body;

    // We use Llama 3 - one of the best free models available
    const response = await fetch(
      "https://api-inference.huggingface.co/models/meta-llama/Llama-3.2-3B-Instruct",
      {
        headers: { 
          Authorization: `Bearer ${HF_TOKEN}`,
          "Content-Type": "application/json"
        },
        method: "POST",
        body: JSON.stringify({ inputs: message }),
      }
    );

    const result = await response.json();
    
    // Hugging Face returns an array; we grab the generated text
    const text = result[0]?.generated_text || "I'm thinking...";

    res.json({
      text: text,
      stations: [
        { name: "Berlin Hauptbahnhof", elevatorStatus: "Operational", notes: "Free API working!" }
      ]
    });
  } catch (error) {
    console.error("HF Error:", error);
    res.status(500).json({ text: "API limit reached or token invalid." });
  }
});

app.listen(3001, () => console.log("Hugging Face Backend running on 3001"));