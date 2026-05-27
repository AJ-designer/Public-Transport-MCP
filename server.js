import express from 'express';
import cors from 'cors';
import { config } from 'dotenv';

config();

const app = express();
app.use(cors());
app.use(express.json());

const HF_TOKEN = process.env.HF_TOKEN;

app.post('/api/chat', async (req, res) => {
  try {
    const { message } = req.body;

    if (!HF_TOKEN) {
      return res.status(500).json({ text: "HF_TOKEN is not set. Add it to your .env file.", stations: [] });
    }

    const response = await fetch(
      "https://router.huggingface.co/hf-inference/v1/chat/completions",
      {
        method: "POST",
        headers: {
          Authorization: `Bearer ${HF_TOKEN}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          model: "meta-llama/Llama-3.2-3B-Instruct",
          messages: [{ role: "user", content: message }],
          max_tokens: 500
        }),
      }
    );

    const result = await response.json();

    if (result.error) {
      return res.json({ text: `HuggingFace error: ${result.error}`, stations: [] });
    }

    const text = result.choices[0].message.content;

    res.json({
      text,
      stations: [
        { name: "Berlin Hauptbahnhof", elevatorStatus: "Operational", notes: "API Connected!" }
      ]
    });
  } catch (error) {
    console.error("Server error:", error);
    res.status(500).json({ text: "The server encountered an error. Check the terminal.", stations: [] });
  }
});

app.listen(3002, () => console.log("GoAccess HuggingFace server running on port 3002"));
