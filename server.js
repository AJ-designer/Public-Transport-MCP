app.post('/api/chat', async (req, res) => {
  try {
    const { message } = req.body;

    const response = await fetch(
      "https://router.huggingface.co/hf-inference/v1/chat/completions",
      {
        headers: { 
          Authorization: `Bearer ${HF_TOKEN}`,
          "Content-Type": "application/json"
        },
        method: "POST",
        body: JSON.stringify({ 
            model: "meta-llama/Llama-3.2-3B-Instruct", // Put model name INSIDE the body
            messages: [{ role: "user", content: message }],
            max_tokens: 500
        }),
      }
    );

    const result = await response.json();
    
    // Check if the API returned an error message inside the JSON
    if (result.error) {
        return res.json({ text: `HF Error: ${result.error}`, stations: [] });
    }

    // New format for the Router API
    const text = result.choices[0].message.content;

    res.json({
      text: text,
      stations: [
        { name: "Berlin Hauptbahnhof", elevatorStatus: "Operational", notes: "API Connected!" }
      ]
    });
  } catch (error) {
    console.error("HF Error:", error);
    res.status(500).json({ text: "The server encountered an error. Check terminal." });
  }
});